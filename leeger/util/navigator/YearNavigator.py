import copy

from leeger.enum import MatchupType
from leeger.exception import DoesNotExistException
from leeger.model.filter.YearFilters import YearFilters
from leeger.model.league import Matchup, Team
from leeger.model.league.Year import Year


class YearNavigator:
    """
    Used to navigate the Year model.
    """

    @staticmethod
    def getAllTeamIds(year: Year) -> list[str]:
        return [team.id for team in year.teams]

    @staticmethod
    def getTeamById(year: Year, teamId: str) -> Team:
        for team in year.teams:
            if team.id == teamId:
                return team
        raise DoesNotExistException(f"Team with ID {teamId} does not exist in the given Year.")

    @classmethod
    def getNumberOfGamesPlayed(cls,
                               year: Year,
                               yearFilters: YearFilters,
                               countMultiWeekMatchupsAsOneGame=False,
                               countLeagueMedianGamesAsTwoGames=False) -> dict[str, int]:
        """
        Returns the number of games played for each team in the given Year.

        Example response:
            {
            "someTeamId": 4,
            "someOtherTeamId": 6,
            "yetAnotherTeamId": 11,
            ...
            }
        """

        teamIdAndNumberOfGamesPlayed = dict()
        allTeamIds = YearNavigator.getAllTeamIds(year)
        for teamId in allTeamIds:
            teamIdAndNumberOfGamesPlayed[teamId] = 0

        # keep track of multi-week matchups that have been counted
        multiWeekMatchupIdsCounted: list[str] = list()

        for i in range(yearFilters.weekNumberStart - 1, yearFilters.weekNumberEnd):
            week = year.weeks[i]
            for matchup in week.matchups:
                if matchup.matchupType in yearFilters.includeMatchupTypes:
                    mwmid = matchup.multiWeekMatchupId
                    if mwmid is not None and countMultiWeekMatchupsAsOneGame is True:
                        # these matchups will only count as 1 game
                        if mwmid in multiWeekMatchupIdsCounted:
                            # don't count this matchup as another game
                            continue
                        multiWeekMatchupIdsCounted.append(mwmid)
                    numberOfGamesToAdd = 1
                    # count regular season games in league median years as 2 games
                    if year.yearSettings.leagueMedianGames and matchup.matchupType == MatchupType.REGULAR_SEASON and countLeagueMedianGamesAsTwoGames:
                        numberOfGamesToAdd = 2
                    teamIdAndNumberOfGamesPlayed[matchup.teamAId] += numberOfGamesToAdd
                    teamIdAndNumberOfGamesPlayed[matchup.teamBId] += numberOfGamesToAdd
        return teamIdAndNumberOfGamesPlayed

    @staticmethod
    def getAllScoresInYear(year: Year, simplifyMultiWeekMatchups=False) -> list[float | int]:
        """
        Returns a list of all scores for the given Year.
        Will count all scores EXCEPT for IGNORE Matchups.
        """
        # add simplified multi-week matchup scores if requested
        if simplifyMultiWeekMatchups:
            allMatchups = YearNavigator.getAllSimplifiedMatchupsInYear(year)
        else:
            allMatchups = YearNavigator.getAllMatchupsInYear(year)

        allScores = [matchup.teamAScore for matchup in allMatchups]
        allScores += [matchup.teamBScore for matchup in allMatchups]

        return allScores

    @staticmethod
    def getAllMultiWeekMatchups(year: Year, filters: YearFilters = None) -> dict[str, list[Matchup]]:
        """
        Returns a dictionary that has the multi-week matchup ID as the key and a list of matchups as the value.
        """
        filters = filters if filters is not None else YearFilters.getForYear(year)
        if not filters.includeMultiWeekMatchups:
            raise ValueError("Multi-Week matchups must be included in this calculation.")
        multiWeekMatchupIdToMatchupListMap: dict[str, list[Matchup]] = dict()

        for i in range(filters.weekNumberStart - 1, filters.weekNumberEnd):
            week = year.weeks[i]
            for matchup in week.matchups:
                if matchup.matchupType in filters.includeMatchupTypes:
                    mwmid = matchup.multiWeekMatchupId
                    if mwmid is not None:
                        if mwmid in multiWeekMatchupIdToMatchupListMap.keys():
                            multiWeekMatchupIdToMatchupListMap[mwmid].append(matchup)
                        else:
                            multiWeekMatchupIdToMatchupListMap[mwmid] = [matchup]
        return multiWeekMatchupIdToMatchupListMap

    @staticmethod
    def getAllMatchupsInYear(year: Year, filters: YearFilters = None) -> list[Matchup]:
        filters = filters if filters is not None else YearFilters.getForYear(year)
        allMatchups = list()
        for i in range(filters.weekNumberStart - 1, filters.weekNumberEnd):
            week = year.weeks[i]
            for matchup in week.matchups:
                if matchup.matchupType in filters.includeMatchupTypes and (
                        filters.includeMultiWeekMatchups or matchup.multiWeekMatchupId is None):
                    allMatchups.append(matchup)
        return allMatchups

    @staticmethod
    def getAllSimplifiedMatchupsInYear(year: Year, filters: YearFilters = None) -> list[Matchup]:
        """
        Returns a list of matchups for the given year with multi-week matchups simplified.
        """
        from leeger.util.navigator import MatchupNavigator
        filters = filters if filters is not None else YearFilters.getForYear(year)
        if not filters.includeMultiWeekMatchups:
            raise ValueError("Multi-Week matchups must be included in this calculation.")

        # get all non multi-week matchups
        modifiedFilters = copy.deepcopy(filters)
        modifiedFilters.includeMultiWeekMatchups = False
        allMatchups: list[Matchup] = YearNavigator.getAllMatchupsInYear(year, modifiedFilters)
        # get all multi-week matchups
        allMultiWeekMatchups: dict[str, list[Matchup]] = YearNavigator.getAllMultiWeekMatchups(year, filters)

        # simplify multi-week matchups
        for _, matchupList in allMultiWeekMatchups.items():
            allMatchups.append(MatchupNavigator.simplifyMultiWeekMatchups(matchupList))
        return allMatchups
