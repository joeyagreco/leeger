from typing import Optional

import numpy

from src.leeger.calculator.parent.YearCalculator import YearCalculator
from src.leeger.decorator.validate.validators import validateYear
from src.leeger.model.league.Year import Year
from src.leeger.util.Deci import Deci
from src.leeger.util.YearNavigator import YearNavigator


class ScoringStandardDeviationYearCalculator(YearCalculator):
    """
    Used to calculate all scoring standard deviations.
    """

    @classmethod
    @validateYear
    def getScoringStandardDeviation(cls, year: Year, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Scoring STDEV (Standard Deviation) is used to show how volatile a team's scoring was.
        This stat measures a team's scores relative to the mean (or PPG) of all of their scores.

        Scoring STDEV = sqrt((Σ|x-u|²)/N)
        WHERE:
        x = A score
        u = PPG
        N = Number of scores (typically weeks played)

        Returns the Scoring Standard Deviation for each team in the given Year.
        Returns None for a Team if they have no games played in the range.


        Example response:
            {
            "someTeamId": Deci("10.7"),
            "someOtherTeamId": Deci("11.2"),
            "yetAnotherTeamId": Deci("34.1"),
            ...
            }
        """
        filters = cls._getYearFilters(year, validateYear=False, **kwargs)

        teamIdAndScores = dict()
        allTeamIds = YearNavigator.getAllTeamIds(year)
        for teamId in allTeamIds:
            teamIdAndScores[teamId] = list()

        for i in range(filters.weekNumberStart - 1, filters.weekNumberEnd):
            week = year.weeks[i]
            for matchup in week.matchups:
                if matchup.matchupType in filters.includeMatchupTypes:
                    teamIdAndScores[matchup.teamAId].append(Deci(matchup.teamAScore))
                    teamIdAndScores[matchup.teamBId].append(Deci(matchup.teamBScore))

        teamIdAndScoringStandardDeviation = dict()
        for teamId in allTeamIds:
            if len(teamIdAndScores[teamId]) > 0:
                # the Team has scores in this range
                teamIdAndScoringStandardDeviation[teamId] = Deci(numpy.std(teamIdAndScores[teamId]))
            else:
                # no scores for this Team in this range, return None for them
                teamIdAndScoringStandardDeviation[teamId] = None

        return teamIdAndScoringStandardDeviation
