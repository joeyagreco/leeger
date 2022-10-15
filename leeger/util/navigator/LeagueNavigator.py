from leeger.enum.MatchupType import MatchupType
from leeger.exception.DoesNotExistException import DoesNotExistException
from leeger.model.filter.AllTimeFilters import AllTimeFilters
from leeger.model.filter.YearFilters import YearFilters
from leeger.model.league.League import League
from leeger.model.league.Team import Team
from leeger.model.league.Year import Year
from leeger.util.navigator.YearNavigator import YearNavigator


class LeagueNavigator:
    """
    Used to navigate the League model.
    """

    @staticmethod
    def getYearByYearNumber(league: League, yearNumber: int) -> Year:
        for year in league.years:
            if year.yearNumber == yearNumber:
                return year
        raise DoesNotExistException(f"Year {yearNumber} does not exist in the given League.")

    @staticmethod
    def getTeamById(league: League, teamId: str) -> Team:
        for year in league.years:
            for team in year.teams:
                if team.id == teamId:
                    return team
        raise DoesNotExistException(f"Team with ID {teamId} does not exist in the given League.")

    @staticmethod
    def getAllOwnerIds(league: League) -> list[str]:
        return [owner.id for owner in league.owners]

    @classmethod
    def getNumberOfGamesPlayed(cls,
                               league: League,
                               allTimeFilters: AllTimeFilters,
                               countMultiWeekMatchupsAsOneGame=False,
                               countLeagueMedianGamesAsTwoGames=False) -> dict[str, int]:
        """
        Returns the number of games played for each owner in the given League all time.

        Example response:
            {
            "someTeamId": 14,
            "someOtherTeamId": 16,
            "yetAnotherTeamId": 21,
            ...
            }
        """

        # parse filters
        yearWeekNumberStartWeekNumberEnd: list[tuple] = list()
        if allTimeFilters.yearNumberStart == allTimeFilters.yearNumberEnd:
            yearWeekNumberStartWeekNumberEnd.append(
                (LeagueNavigator.getYearByYearNumber(league, allTimeFilters.yearNumberStart),
                 allTimeFilters.weekNumberStart,
                 allTimeFilters.weekNumberEnd))
        else:
            for year in league.years:
                if year.yearNumber == allTimeFilters.yearNumberStart:
                    # first year we want, make sure week number start matches what was requested
                    # givenWeekStart and every week greater
                    yearWeekNumberStartWeekNumberEnd.append((year, allTimeFilters.weekNumberStart, len(year.weeks)))
                elif year.yearNumber == allTimeFilters.yearNumberEnd:
                    # last year we want, make sure week number end matches what was requested
                    # first week and every week til givenWeekEnd
                    yearWeekNumberStartWeekNumberEnd.append((year, 1, allTimeFilters.weekNumberEnd))
                elif allTimeFilters.yearNumberStart < year.yearNumber < allTimeFilters.yearNumberEnd:
                    # this year is in our year range, include every week in this year
                    yearWeekNumberStartWeekNumberEnd.append((year, 1, len(year.weeks)))

        allResultDicts: list[dict] = list()

        for yse in yearWeekNumberStartWeekNumberEnd:
            currentYear = yse[0]
            currentWeekNumberStart = yse[1]
            currentWeekNumberEnd = yse[2]
            # build year filters
            if allTimeFilters.onlyChampionship:
                includeMatchupTypes = [MatchupType.CHAMPIONSHIP]
            elif allTimeFilters.onlyPostSeason:
                includeMatchupTypes = [MatchupType.PLAYOFF, MatchupType.CHAMPIONSHIP]
            elif allTimeFilters.onlyRegularSeason:
                includeMatchupTypes = [MatchupType.REGULAR_SEASON]
            else:
                includeMatchupTypes = [MatchupType.REGULAR_SEASON, MatchupType.PLAYOFF, MatchupType.CHAMPIONSHIP]
            yearFilters = YearFilters(weekNumberStart=currentWeekNumberStart, weekNumberEnd=currentWeekNumberEnd,
                                      includeMatchupTypes=includeMatchupTypes)

            allResultDicts.append(YearNavigator.getNumberOfGamesPlayed(currentYear,
                                                                       yearFilters,
                                                                       countMultiWeekMatchupsAsOneGame=countMultiWeekMatchupsAsOneGame,
                                                                       countLeagueMedianGamesAsTwoGames=countLeagueMedianGamesAsTwoGames))

        # combine results
        ownerIdAndNumberOfGamesPlayed = dict()
        allOwnerIds = LeagueNavigator.getAllOwnerIds(league)
        for ownerId in allOwnerIds:
            ownerIdAndNumberOfGamesPlayed[ownerId] = 0

        for resultDict in allResultDicts:
            for teamId in resultDict.keys():
                ownerIdAndNumberOfGamesPlayed[LeagueNavigator.getTeamById(league, teamId).ownerId] += resultDict[teamId]

        return ownerIdAndNumberOfGamesPlayed

    @staticmethod
    def getAllScoresInLeague(league: League, simplifyMultiWeekMatchups=False) -> list[float | int]:
        """
        Returns a list of all scores for the given League.
        Will count all scores EXCEPT for IGNORE Matchups.
        """
        allScores = list()
        for year in league.years:
            allScores += YearNavigator.getAllScoresInYear(year, simplifyMultiWeekMatchups=simplifyMultiWeekMatchups)
        return allScores
