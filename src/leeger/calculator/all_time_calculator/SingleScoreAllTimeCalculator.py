from typing import Optional

from src.leeger.calculator.parent.AllTimeCalculator import AllTimeCalculator
from src.leeger.decorator.validate.validators import validateLeague
from src.leeger.model.league.League import League
from src.leeger.util.LeagueNavigator import LeagueNavigator


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
        filters = cls._getAllTimeFilters(league, validateLeague=False, **kwargs)

        ownerIdAndMaxScore = dict()

        allMatchups = cls._getAllFilteredMatchups(league, filters, validateLeague=False)

        for ownerId in LeagueNavigator.getAllOwnerIds(league, validateLeague=False):
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
