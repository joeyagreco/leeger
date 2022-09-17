from typing import Optional

import numpy

from leeger.calculator.parent.AllTimeCalculator import AllTimeCalculator
from leeger.decorator.validators import validateLeague
from leeger.model.filter import AllTimeFilters
from leeger.model.league.League import League
from leeger.util.Deci import Deci
from leeger.util.navigator.LeagueNavigator import LeagueNavigator


class ScoringStandardDeviationAllTimeCalculator(AllTimeCalculator):
    """
    Used to calculate all scoring standard deviations.
    """

    @classmethod
    @validateLeague
    def getScoringStandardDeviation(cls, league: League, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Scoring STDEV (Standard Deviation) is used to show how volatile a team's scoring was.
        This stat measures an Owner's scores relative to the mean (or PPG) of all of their scores.

        Scoring STDEV = sqrt((Σ|x-u|²)/N)
        WHERE:
        x = A score
        u = PPG
        N = Number of scores (typically weeks played)

        Returns the Scoring Standard Deviation for each Owner in the given League.
        Returns None for an Owner if they have no games played in the range.

        Example response:
            {
            "someTeamId": Deci("10.7"),
            "someOtherTeamId": Deci("11.2"),
            "yetAnotherTeamId": Deci("34.1"),
            ...
            }
        """
        filters = AllTimeFilters.getForLeague(league, **kwargs)

        ownerIdAndScores = dict()
        allOwnerIds = LeagueNavigator.getAllOwnerIds(league)
        for ownerId in allOwnerIds:
            ownerIdAndScores[ownerId] = list()

        for matchup in cls._getAllFilteredMatchups(league, filters, simplifyMultiWeekMatchups=True):
            ownerAId = LeagueNavigator.getTeamById(league, matchup.teamAId).ownerId
            ownerBId = LeagueNavigator.getTeamById(league, matchup.teamBId).ownerId
            ownerIdAndScores[ownerAId].append(Deci(matchup.teamAScore))
            ownerIdAndScores[ownerBId].append(Deci(matchup.teamBScore))

        ownerIdAndScoringStandardDeviation = dict()
        for ownerId in allOwnerIds:
            if len(ownerIdAndScores[ownerId]) > 0:
                # the Owner has scores in this range
                ownerIdAndScoringStandardDeviation[ownerId] = Deci(numpy.std(ownerIdAndScores[ownerId]))
            else:
                # no scores for this Owner in this range, return None for them
                ownerIdAndScoringStandardDeviation[ownerId] = None

        return ownerIdAndScoringStandardDeviation
