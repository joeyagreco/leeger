from typing import Optional

from leeger.calculator.all_time_calculator.PointsScoredAllTimeCalculator import PointsScoredAllTimeCalculator
from leeger.calculator.parent.AllTimeCalculator import AllTimeCalculator
from leeger.decorator.validate.validators import validateLeague
from leeger.model.league.League import League
from leeger.util.Deci import Deci
from leeger.util.GeneralUtil import GeneralUtil
from leeger.util.LeagueNavigator import LeagueNavigator


class ScoringShareAllTimeCalculator(AllTimeCalculator):
    """
    Used to calculate all scoring shares.
    """

    @classmethod
    @validateLeague
    def getScoringShare(cls, league: League, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Scoring Share is used to show what percentage of league scoring a team was responsible for.

        Scoring Share = ((ΣA) / (ΣB)) * 100
        WHERE:
        A = All scores by an Owner in a League
        B = All scores by all Owners in a League

        Returns the Scoring Share for each Owner in the given League.
        Returns None for an Owner if they have no games played in the range.

        Example response:
            {
            "someOwnerId": Deci("10.7"),
            "someOtherOwnerId": Deci("14.2"),
            "yetAnotherOwnerId": Deci("12.1"),
            ...
            }
        """

        ownerIdAndPointsScored = PointsScoredAllTimeCalculator.getPointsScored(league, **kwargs)
        allScores = GeneralUtil.filter(value=None, list_=ownerIdAndPointsScored.values())
        totalPointsScoredInLeague = sum(allScores)
        ownerIdAndScoringShare = dict()
        for ownerId in LeagueNavigator.getAllOwnerIds(league):
            if len(allScores) == 0 or ownerIdAndPointsScored[ownerId] is None:
                ownerIdAndScoringShare[ownerId] = None
            else:
                # avoid division by 0
                if totalPointsScoredInLeague == 0:
                    ownerIdAndScoringShare[ownerId] = Deci("0")
                else:
                    ownerIdAndScoringShare[ownerId] = (ownerIdAndPointsScored[
                                                           ownerId] / totalPointsScoredInLeague) * Deci("100")

        return ownerIdAndScoringShare

    @classmethod
    @validateLeague
    def getOpponentScoringShare(cls, league: League, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Returns the Scoring Share for each Owner's opponent in the given League.
        Returns None for an Owner if they have no games played in the range.

        Example response:
            {
            "someOwnerId": Deci("10.7"),
            "someOtherOwnerId": Deci("14.2"),
            "yetAnotherOwnerId": Deci("12.1"),
            ...
            }
        """

        ownerIdAndOpponentPointsScored = PointsScoredAllTimeCalculator.getOpponentPointsScored(league, **kwargs)
        allScores = GeneralUtil.filter(value=None, list_=ownerIdAndOpponentPointsScored.values())
        totalPointsScoredInLeague = sum(allScores)
        ownerIdAndOpponentScoringShare = dict()
        for ownerId in LeagueNavigator.getAllOwnerIds(league):
            if len(allScores) == 0 or ownerIdAndOpponentPointsScored[ownerId] is None:
                ownerIdAndOpponentScoringShare[ownerId] = None
            else:
                # avoid division by 0
                if totalPointsScoredInLeague == 0:
                    ownerIdAndOpponentScoringShare[ownerId] = Deci("0")
                else:
                    ownerIdAndOpponentScoringShare[ownerId] = (ownerIdAndOpponentPointsScored[
                                                                   ownerId] / totalPointsScoredInLeague) * Deci("100")

        return ownerIdAndOpponentScoringShare
