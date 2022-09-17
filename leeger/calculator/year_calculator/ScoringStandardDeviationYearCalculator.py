from typing import Optional

import numpy

from leeger.calculator.parent.YearCalculator import YearCalculator
from leeger.decorator.validators import validateYear
from leeger.model.filter import YearFilters
from leeger.model.league.Year import Year
from leeger.util.Deci import Deci
from leeger.util.navigator.YearNavigator import YearNavigator


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
        filters = YearFilters.getForYear(year, **kwargs)

        teamIdAndScores = dict()
        allTeamIds = YearNavigator.getAllTeamIds(year)
        for teamId in allTeamIds:
            teamIdAndScores[teamId] = list()

        allMatchups = YearNavigator.getAllSimplifiedMatchupsInYear(year, filters)
        for matchup in allMatchups:
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
