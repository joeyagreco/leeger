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
            "someTeamId": Deci("10.7"),
            "someOtherTeamId": Deci("14.2"),
            "yetAnotherTeamId": Deci("12.1"),
            ...
            }
        """

        ownerIdAndPointsScored = PointsScoredAllTimeCalculator.getPointsScored(league, **kwargs)
        totalPointsScoredInLeague = sum(ownerIdAndPointsScored.values())
        ownerIdAndScoringShare = dict()
        for ownerId in LeagueNavigator.getAllOwnerIds(league):
            ownerIdAndScoringShare[ownerId] = (ownerIdAndPointsScored[ownerId] / totalPointsScoredInLeague) * Deci(
                "100")

        return ownerIdAndScoringShare
