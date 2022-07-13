from typing import Optional

from leeger.calculator.parent.YearCalculator import YearCalculator
from leeger.decorator.validate.validators import validateYear
from leeger.model.league.Year import Year
from leeger.util.Deci import Deci
from leeger.util.YearNavigator import YearNavigator


class PointsScoredYearCalculator(YearCalculator):
    """
    Used to calculate all points scored.
    """

    @classmethod
    @validateYear
    def getPointsScored(cls, year: Year, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Returns the number of Points Scored for each team in the given Year.
        Returns None for a Team if they have no games played in the range.

        Example response:
            {
            "someTeamId": Deci("1009.7"),
            "someOtherTeamId": Deci("1412.2"),
            "yetAnotherTeamId": Deci("1227.1"),
            ...
            }
        """
        filters = cls._getYearFilters(year, validateYear=False, **kwargs)

        teamIdAndPointsScored = dict()
        for teamId in YearNavigator.getAllTeamIds(year):
            teamIdAndPointsScored[teamId] = Deci(0)

        for i in range(filters.weekNumberStart - 1, filters.weekNumberEnd):
            week = year.weeks[i]
            for matchup in week.matchups:
                if matchup.matchupType in filters.includeMatchupTypes:
                    teamIdAndPointsScored[matchup.teamAId] += Deci(matchup.teamAScore)
                    teamIdAndPointsScored[matchup.teamBId] += Deci(matchup.teamBScore)

        cls._setToNoneIfNoGamesPlayed(teamIdAndPointsScored, year, filters, **kwargs)
        return teamIdAndPointsScored

    @classmethod
    @validateYear
    def getPointsScoredPerGame(cls, year: Year, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Returns the number of Points Scored per game for each team in the given Year.
        Returns None for a Team if they have no games played in the range.

        Example response:
            {
            "someTeamId": Deci("100.7"),
            "someOtherTeamId": Deci("141.2"),
            "yetAnotherTeamId": Deci("122.1"),
            ...
            }
        """

        teamIdAndPointsScored = cls.getPointsScored(year, **kwargs)
        teamIdAndNumberOfGamesPlayed = YearNavigator.getNumberOfGamesPlayed(year,
                                                                            cls._getYearFilters(year,
                                                                                                **kwargs))

        teamIdAndPointsScoredPerGame = dict()
        allTeamIds = YearNavigator.getAllTeamIds(year)
        for teamId in allTeamIds:
            # to avoid division by zero, we'll just set the points scored per game to 0 if the team has no games played
            if teamIdAndNumberOfGamesPlayed[teamId] == 0:
                teamIdAndPointsScoredPerGame[teamId] = None
            else:
                teamIdAndPointsScoredPerGame[teamId] = teamIdAndPointsScored[teamId] / teamIdAndNumberOfGamesPlayed[
                    teamId]

        return teamIdAndPointsScoredPerGame

    @classmethod
    @validateYear
    def getOpponentPointsScored(cls, year: Year, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Returns the number of opponent Points Scored for each team in the given Year.
        Returns None for a Team if they have no games played in the range.

        Example response:
            {
            "someTeamId": Deci("1009.7"),
            "someOtherTeamId": Deci("1412.2"),
            "yetAnotherTeamId": Deci("1227.1"),
            ...
            }
        """
        filters = cls._getYearFilters(year, validateYear=False, **kwargs)

        teamIdAndOpponentPointsScored = dict()
        for teamId in YearNavigator.getAllTeamIds(year):
            teamIdAndOpponentPointsScored[teamId] = Deci(0)

        for i in range(filters.weekNumberStart - 1, filters.weekNumberEnd):
            week = year.weeks[i]
            for matchup in week.matchups:
                if matchup.matchupType in filters.includeMatchupTypes:
                    teamIdAndOpponentPointsScored[matchup.teamAId] += Deci(matchup.teamBScore)
                    teamIdAndOpponentPointsScored[matchup.teamBId] += Deci(matchup.teamAScore)

        cls._setToNoneIfNoGamesPlayed(teamIdAndOpponentPointsScored, year, filters, **kwargs)
        return teamIdAndOpponentPointsScored

    @classmethod
    @validateYear
    def getOpponentPointsScoredPerGame(cls, year: Year, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Returns the number of opponent Points Scored per game for each team in the given Year.
        Returns None for a Team if they have no games played in the range.

        Example response:
            {
            "someTeamId": Deci("100.7"),
            "someOtherTeamId": Deci("141.2"),
            "yetAnotherTeamId": Deci("122.1"),
            ...
            }
        """

        teamIdAndOpponentPointsScored = cls.getOpponentPointsScored(year, **kwargs)
        teamIdAndNumberOfGamesPlayed = YearNavigator.getNumberOfGamesPlayed(year,
                                                                            cls._getYearFilters(year,
                                                                                                **kwargs))

        teamIdAndOpponentPointsScoredPerGame = dict()
        allTeamIds = YearNavigator.getAllTeamIds(year)
        for teamId in allTeamIds:
            # to avoid division by zero, we'll just set the opponent points scored per game to 0 if the team has no games played
            if teamIdAndNumberOfGamesPlayed[teamId] == 0:
                teamIdAndOpponentPointsScoredPerGame[teamId] = None
            else:
                teamIdAndOpponentPointsScoredPerGame[teamId] = teamIdAndOpponentPointsScored[teamId] / \
                                                               teamIdAndNumberOfGamesPlayed[teamId]

        return teamIdAndOpponentPointsScoredPerGame
