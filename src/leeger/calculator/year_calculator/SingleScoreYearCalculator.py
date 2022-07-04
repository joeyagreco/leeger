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
        If a Team has no scores in the range, None is returned for them.

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
    def getMinScore(cls, year: Year, **kwargs) -> dict[str, float | int]:
        """
        Returns the Min Score for each team in the given Year.

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

        for i in range(filters.weekNumberStart - 1, filters.weekNumberEnd):
            week = year.weeks[i]
            for matchup in week.matchups:
                if matchup.matchupType in filters.includeMatchupTypes:
                    if matchup.teamAId in teamIdAndMinScore:
                        teamIdAndMinScore[matchup.teamAId] = min(teamIdAndMinScore[matchup.teamAId], matchup.teamAScore)
                    else:
                        teamIdAndMinScore[matchup.teamAId] = matchup.teamAScore
                    if matchup.teamBId in teamIdAndMinScore:
                        teamIdAndMinScore[matchup.teamBId] = min(teamIdAndMinScore[matchup.teamBId], matchup.teamBScore)
                    else:
                        teamIdAndMinScore[matchup.teamBId] = matchup.teamBScore

        return teamIdAndMinScore
