from typing import Optional

from src.leeger.calculator.parent.YearCalculator import YearCalculator
from src.leeger.decorator.validate.validators import validateYear
from src.leeger.model.league.Year import Year
from src.leeger.util.YearNavigator import YearNavigator


class SingleScoreYearCalculator(YearCalculator):
    """
    Used to calculate all single score stats.
    """

    @classmethod
    @validateYear
    def getMaxScore(cls, year: Year, **kwargs) -> dict[str, Optional[float | int]]:
        """
        Returns the Max Score for each Team in the given Year.
        Returns None for a Team if they have no games played in the range.

        Example response:
            {
            "someTeamId": 100.7,
            "someOtherTeamId": 111,
            "yetAnotherTeamId": 112.2,
            ...
            }
        """
        filters = cls._getYearFilters(year, validateYear=False, **kwargs)

        teamIdAndMaxScore = dict()

        allMatchups = cls._getAllFilteredMatchups(year, filters, validateYear=False)

        for teamId in YearNavigator.getAllTeamIds(year, validateYear=False):
            teamIdAndMaxScore[teamId] = None

        for matchup in allMatchups:
            aPreviousMaxScore = teamIdAndMaxScore[matchup.teamAId]
            if aPreviousMaxScore is None or matchup.teamAScore > aPreviousMaxScore:
                teamIdAndMaxScore[matchup.teamAId] = matchup.teamAScore

            bPreviousMaxScore = teamIdAndMaxScore[matchup.teamBId]
            if bPreviousMaxScore is None or matchup.teamBScore > bPreviousMaxScore:
                teamIdAndMaxScore[matchup.teamBId] = matchup.teamBScore

        return teamIdAndMaxScore

    @classmethod
    @validateYear
    def getMinScore(cls, year: Year, **kwargs) -> dict[str, Optional[float | int]]:
        """
        Returns the Min Score for each Team in the given Year.
        Returns None for a Team if they have no games played in the range.

        Example response:
            {
            "someTeamId": 78.6,
            "someOtherTeamId": 102,
            "yetAnotherTeamId": 57.3,
            ...
            }
        """
        filters = cls._getYearFilters(year, validateYear=False, **kwargs)

        teamIdAndMinScore = dict()

        allMatchups = cls._getAllFilteredMatchups(year, filters, validateYear=False)

        for teamId in YearNavigator.getAllTeamIds(year, validateYear=False):
            teamIdAndMinScore[teamId] = None

        for matchup in allMatchups:
            aPreviousMinScore = teamIdAndMinScore[matchup.teamAId]
            if aPreviousMinScore is None or matchup.teamAScore < aPreviousMinScore:
                teamIdAndMinScore[matchup.teamAId] = matchup.teamAScore

            bPreviousMinScore = teamIdAndMinScore[matchup.teamBId]
            if bPreviousMinScore is None or matchup.teamBScore < bPreviousMinScore:
                teamIdAndMinScore[matchup.teamBId] = matchup.teamBScore

        return teamIdAndMinScore
