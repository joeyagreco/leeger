from typing import Optional

from leeger.calculator.parent.AllTimeCalculator import AllTimeCalculator
from leeger.decorator.validators import validateLeague
from leeger.model.league.League import League
from leeger.util.navigator.LeagueNavigator import LeagueNavigator


class SingleScoreAllTimeCalculator(AllTimeCalculator):
    """
    Used to calculate all single score stats.
    """

    @classmethod
    @validateLeague
    def getMaxScore(cls, league: League, **kwargs) -> dict[str, Optional[float | int]]:
        """
        Returns the Max Score for each Owner in the given League.
        If an Owner has no scores in the range, None is returned for them.

        Example response:
            {
            "someOwnerId": 100.7,
            "someOtherOwnerId": 111,
            "yetAnotherOwnerId": 112.2,
            ...
            }
        """
        filters = cls._getAllTimeFilters(league, **kwargs)

        ownerIdAndMaxScore = dict()

        allMatchups = cls._getAllFilteredMatchups(league, filters)

        for ownerId in LeagueNavigator.getAllOwnerIds(league):
            ownerIdAndMaxScore[ownerId] = None

        for matchup in allMatchups:
            aOwnerId = LeagueNavigator.getTeamById(league, matchup.teamAId).ownerId
            aPreviousMaxScore = ownerIdAndMaxScore[aOwnerId]
            if aPreviousMaxScore is None or matchup.teamAScore > aPreviousMaxScore:
                ownerIdAndMaxScore[aOwnerId] = matchup.teamAScore

            bOwnerId = LeagueNavigator.getTeamById(league, matchup.teamBId).ownerId
            bPreviousMaxScore = ownerIdAndMaxScore[bOwnerId]
            if bPreviousMaxScore is None or matchup.teamBScore > bPreviousMaxScore:
                ownerIdAndMaxScore[bOwnerId] = matchup.teamBScore

        return ownerIdAndMaxScore

    @classmethod
    @validateLeague
    def getMinScore(cls, league: League, **kwargs) -> dict[str, Optional[float | int]]:
        """
        Returns the Min Score for each Owner in the given League.
        If an Owner has no scores in the range, None is returned for them.

        Example response:
            {
            "someOwnerId": 90.7,
            "someOtherOwnerId": 71,
            "yetAnotherOwnerId": 82.2,
            ...
            }
        """
        filters = cls._getAllTimeFilters(league, **kwargs)

        ownerIdAndMinScore = dict()

        allMatchups = cls._getAllFilteredMatchups(league, filters)

        for ownerId in LeagueNavigator.getAllOwnerIds(league):
            ownerIdAndMinScore[ownerId] = None

        for matchup in allMatchups:
            aOwnerId = LeagueNavigator.getTeamById(league, matchup.teamAId).ownerId
            aPreviousMinScore = ownerIdAndMinScore[aOwnerId]
            if aPreviousMinScore is None or matchup.teamAScore < aPreviousMinScore:
                ownerIdAndMinScore[aOwnerId] = matchup.teamAScore

            bOwnerId = LeagueNavigator.getTeamById(league, matchup.teamBId).ownerId
            bPreviousMinScore = ownerIdAndMinScore[bOwnerId]
            if bPreviousMinScore is None or matchup.teamBScore < bPreviousMinScore:
                ownerIdAndMinScore[bOwnerId] = matchup.teamBScore

        return ownerIdAndMinScore
