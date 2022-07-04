from src.leeger.calculator.all_time_calculator.PointsScoredAllTimeCalculator import PointsScoredAllTimeCalculator
from src.leeger.calculator.parent.AllTimeCalculator import AllTimeCalculator
from src.leeger.decorator.validate.validators import validateLeague
from src.leeger.model.league.League import League
from src.leeger.util.Deci import Deci
from src.leeger.util.LeagueNavigator import LeagueNavigator


class ScoringShareAllTimeCalculator(AllTimeCalculator):
    """
    Used to calculate all scoring shares.
    """

    @classmethod
    @validateLeague
    def getScoringShare(cls, league: League, **kwargs) -> dict[str, Deci]:
        """
        Scoring Share is used to show what percentage of league scoring a team was responsible for.
        Scoring Share = ((ΣA) / (ΣB)) * 100
        WHERE:
        A = All scores by an Owner in a League
        B = All scores by all Owners in a League

        Returns the Scoring Share for each Owner in the given League.

        Example response:
            {
            "someOwnerId": Deci("10.7"),
            "someOtherOwnerId": Deci("14.2"),
            "yetAnotherOwnerId": Deci("12.1"),
            ...
            }
        """

        ownerIdAndPointsScored = PointsScoredAllTimeCalculator.getPointsScored(league, **kwargs)
        totalPointsScoredInLeague = sum(ownerIdAndPointsScored.values())
        ownerIdAndScoringShare = dict()
        for ownerId in LeagueNavigator.getAllOwnerIds(league):
            if totalPointsScoredInLeague == 0:
                # avoid division by 0
                ownerIdAndScoringShare[ownerId] = 0
            else:
                ownerIdAndScoringShare[ownerId] = (ownerIdAndPointsScored[ownerId] / totalPointsScoredInLeague) * Deci(
                    "100")

        return ownerIdAndScoringShare

    @classmethod
    @validateLeague
    def getOpponentScoringShare(cls, league: League, **kwargs) -> dict[str, Deci]:
        """
        Returns the Scoring Share for each Owner's opponent in the given League.

        Example response:
            {
            "someOwnerId": Deci("10.7"),
            "someOtherOwnerId": Deci("14.2"),
            "yetAnotherOwnerId": Deci("12.1"),
            ...
            }
        """

        ownerIdAndOpponentPointsScored = PointsScoredAllTimeCalculator.getOpponentPointsScored(league, **kwargs)
        totalPointsScoredInLeague = sum(ownerIdAndOpponentPointsScored.values())
        ownerIdAndOpponentScoringShare = dict()
        for ownerId in LeagueNavigator.getAllOwnerIds(league):
            if totalPointsScoredInLeague == 0:
                # avoid division by 0
                ownerIdAndOpponentScoringShare[ownerId] = 0
            else:
                ownerIdAndOpponentScoringShare[ownerId] = (ownerIdAndOpponentPointsScored[
                                                               ownerId] / totalPointsScoredInLeague) * Deci("100")

        return ownerIdAndOpponentScoringShare
