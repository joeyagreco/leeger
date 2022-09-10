from typing import Optional

from leeger.calculator.parent.YearCalculator import YearCalculator
from leeger.decorator.validators import validateYear
from leeger.model.league import Matchup
from leeger.model.league.Year import Year
from leeger.util.Deci import Deci
from leeger.util.navigator.MatchupNavigator import MatchupNavigator
from leeger.util.navigator.YearNavigator import YearNavigator


class GameOutcomeYearCalculator(YearCalculator):
    """
    Used to calculate all game outcomes.
    """

    @classmethod
    @validateYear
    def getWins(cls, year: Year, **kwargs) -> dict[str, Optional[int]]:
        """
        Returns the number of wins for each team in the given Year.
        Returns None for a Team if they have no games played in the range.

        Example response:
            {
            "someTeamId": 8,
            "someOtherTeamId": 11,
            "yetAnotherTeamId": 7,
            ...
            }
        """
        filters = cls._getYearFilters(year, **kwargs)

        teamIdAndWins = dict()
        for teamId in YearNavigator.getAllTeamIds(year):
            teamIdAndWins[teamId] = 0

        # keep track of all matchups to count towards this calculation
        allMatchups = list()
        # keep track of scores and tiebreakers for multi-week matchups
        multiWeekMatchupIdToMatchupListMap: dict[str, list[Matchup]] = dict()

        for i in range(filters.weekNumberStart - 1, filters.weekNumberEnd):
            week = year.weeks[i]
            for matchup in week.matchups:
                if matchup.matchupType in filters.includeMatchupTypes:
                    mwmid = matchup.multiWeekMatchupId
                    if mwmid is not None:
                        # multi-week matchup
                        if mwmid in multiWeekMatchupIdToMatchupListMap:
                            multiWeekMatchupIdToMatchupListMap[mwmid].append(matchup)
                        else:
                            multiWeekMatchupIdToMatchupListMap[mwmid] = [matchup]
                    else:
                        # non multi-week matchup
                        allMatchups.append(matchup)

        # simplify multi-week matchups into single Matchups
        for matchupList in multiWeekMatchupIdToMatchupListMap.values():
            allMatchups.append(MatchupNavigator.simplifyMultiWeekMatchups(matchupList))
        for matchup in allMatchups:
            # get winner team ID (if this wasn't a tie)
            winnerTeamId = MatchupNavigator.getTeamIdOfMatchupWinner(matchup)
            if winnerTeamId is not None:
                teamIdAndWins[winnerTeamId] += 1
        cls._setToNoneIfNoGamesPlayed(teamIdAndWins, year, filters, **kwargs)
        return teamIdAndWins

    @classmethod
    @validateYear
    def getLosses(cls, year: Year, **kwargs) -> dict[str, Optional[int]]:
        """
        Returns the number of losses for each team in the given Year.
        Returns None for a Team if they have no games played in the range.

        Example response:
            {
            "someTeamId": 8,
            "someOtherTeamId": 11,
            "yetAnotherTeamId": 7,
            ...
            }
        """
        filters = cls._getYearFilters(year, **kwargs)

        teamIdAndLosses = dict()
        for teamId in YearNavigator.getAllTeamIds(year):
            teamIdAndLosses[teamId] = 0

        # keep track of all matchups to count towards this calculation
        allMatchups = list()
        # keep track of scores and tiebreakers for multi-week matchups
        multiWeekMatchupIdToMatchupListMap: dict[str, list[Matchup]] = dict()

        for i in range(filters.weekNumberStart - 1, filters.weekNumberEnd):
            week = year.weeks[i]
            for matchup in week.matchups:
                if matchup.matchupType in filters.includeMatchupTypes:
                    mwmid = matchup.multiWeekMatchupId
                    if mwmid is not None:
                        # multi-week matchup
                        if mwmid in multiWeekMatchupIdToMatchupListMap:
                            multiWeekMatchupIdToMatchupListMap[mwmid].append(matchup)
                        else:
                            multiWeekMatchupIdToMatchupListMap[mwmid] = [matchup]
                    else:
                        # non multi-week matchup
                        allMatchups.append(matchup)

        # simplify multi-week matchups into single Matchups
        for matchupList in multiWeekMatchupIdToMatchupListMap.values():
            allMatchups.append(MatchupNavigator.simplifyMultiWeekMatchups(matchupList))
        for matchup in allMatchups:
            # get loser team ID (if this wasn't a tie)
            winnerTeamId = MatchupNavigator.getTeamIdOfMatchupWinner(matchup)
            if winnerTeamId is not None:
                loserTeamId = matchup.teamAId if winnerTeamId == matchup.teamBId else matchup.teamBId
                teamIdAndLosses[loserTeamId] += 1
        cls._setToNoneIfNoGamesPlayed(teamIdAndLosses, year, filters, **kwargs)
        return teamIdAndLosses

    @classmethod
    @validateYear
    def getTies(cls, year: Year, **kwargs) -> dict[str, Optional[int]]:
        """
        Returns the number of ties for each team in the given Year.
        Returns None for a Team if they have no games played in the range.

        Example response:
            {
            "someTeamId": 8,
            "someOtherTeamId": 11,
            "yetAnotherTeamId": 7,
            ...
            }
        """
        filters = cls._getYearFilters(year, **kwargs)

        teamIdAndTies = dict()
        for teamId in YearNavigator.getAllTeamIds(year):
            teamIdAndTies[teamId] = 0

        for i in range(filters.weekNumberStart - 1, filters.weekNumberEnd):
            week = year.weeks[i]
            for matchup in week.matchups:
                if matchup.matchupType in filters.includeMatchupTypes:
                    if MatchupNavigator.getTeamIdOfMatchupWinner(matchup) is None:
                        teamIdAndTies[matchup.teamAId] += 1
                        teamIdAndTies[matchup.teamBId] += 1
        cls._setToNoneIfNoGamesPlayed(teamIdAndTies, year, filters, **kwargs)
        return teamIdAndTies

    @classmethod
    @validateYear
    def getWinPercentage(cls, year: Year, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Returns the win percentage for each team in the given Year.
        Returns None for a Team if they have no games played in the range.
        Win percentage will be represented as a non-rounded decimal.
        Example:
            33% win percentage -> Deci("0.3333333333333333333333333333")
            100% win percentage -> Deci("1.0")

        Example response:
            {
            "someTeamId": Deci("0.85"),
            "someOtherTeamId": Deci("0.1156"),
            "yetAnotherTeamId": Deci("0.72"),
            ...
            }
        """

        teamIdAndWinPercentage = dict()
        teamIdAndWins = GameOutcomeYearCalculator.getWins(year, **kwargs)
        teamIdAndLosses = GameOutcomeYearCalculator.getLosses(year, **kwargs)
        teamIdAndTies = GameOutcomeYearCalculator.getTies(year, **kwargs)

        for teamId in YearNavigator.getAllTeamIds(year):
            numberOfWins = teamIdAndWins[teamId]
            numberOfLosses = teamIdAndLosses[teamId]
            numberOfTies = teamIdAndTies[teamId]
            if None in (numberOfWins, numberOfLosses, numberOfTies):
                teamIdAndWinPercentage[teamId] = None
            else:
                numberOfGamesPlayed = numberOfWins + numberOfLosses + numberOfTies
                teamIdAndWinPercentage[teamId] = (Deci(numberOfWins) + (Deci("0.5") * Deci(numberOfTies))) / Deci(
                    numberOfGamesPlayed)

        return teamIdAndWinPercentage

    @classmethod
    @validateYear
    def getWAL(cls, year: Year, **kwargs) -> dict[str, Optional[Deci]]:
        """
        WAL is "Wins Against the League"
        Formula: (Number of Wins * 1) + (Number of Ties * 0.5)
        Returns the number of Wins Against the League for each team in the given Year.
        Returns None for a Team if they have no games played in the range.

        Example response:
            {
            "someTeamId": Deci("8.7"),
            "someOtherTeamId": Deci("11.2"),
            "yetAnotherTeamId": Deci("7.1"),
            ...
            }
        """

        teamIdAndWAL = dict()
        teamIdAndWins = GameOutcomeYearCalculator.getWins(year, **kwargs)
        teamIdAndTies = GameOutcomeYearCalculator.getTies(year, **kwargs)

        for teamId in YearNavigator.getAllTeamIds(year):
            wins = teamIdAndWins[teamId]
            ties = teamIdAndTies[teamId]
            if None in (wins, ties):
                teamIdAndWAL[teamId] = None
            else:
                teamIdAndWAL[teamId] = Deci(wins) + (Deci("0.5") * Deci(ties))

        return teamIdAndWAL

    @classmethod
    @validateYear
    def getWALPerGame(cls, year: Year, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Returns the number of Wins Against the League per game for each team in the given Year.
        Returns None for a Team if they have no games played in the range.

        Example response:
            {
            "someTeamId": Deci("0.7"),
            "someOtherTeamId": Deci("0.29"),
            "yetAnotherTeamId": Deci("0.48"),
            ...
            }
        """
        teamIdAndWAL = cls.getWAL(year, **kwargs)
        teamIdAndNumberOfGamesPlayed = YearNavigator.getNumberOfGamesPlayed(year,
                                                                            cls._getYearFilters(year,
                                                                                                **kwargs))

        teamIdAndWALPerGame = dict()
        allTeamIds = YearNavigator.getAllTeamIds(year)
        for teamId in allTeamIds:
            # to avoid division by zero, we'll just set the WAL per game to 0 if the team has no games played
            if teamIdAndNumberOfGamesPlayed[teamId] == 0:
                teamIdAndWALPerGame[teamId] = Deci("0")
            else:
                teamIdAndWALPerGame[teamId] = teamIdAndWAL[teamId] / teamIdAndNumberOfGamesPlayed[teamId]

        cls._setToNoneIfNoGamesPlayed(teamIdAndWALPerGame, year, **kwargs)
        return teamIdAndWALPerGame
