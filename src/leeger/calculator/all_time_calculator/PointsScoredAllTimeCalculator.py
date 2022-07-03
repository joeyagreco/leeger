from src.leeger.calculator.parent.AllTimeCalculator import AllTimeCalculator
from src.leeger.calculator.year_calculator.PointsScoredYearCalculator import PointsScoredYearCalculator
from src.leeger.decorator.validate.validators import validateLeague
from src.leeger.model.league.League import League
from src.leeger.util.Deci import Deci


class PointsScoredAllTimeCalculator(AllTimeCalculator):
    """
    Used to calculate all points scored.
    """

    @classmethod
    @validateLeague
    def getPointsScored(cls, league: League, **kwargs) -> dict[str, Deci]:
        """
        Returns the number of Points Scored for each Owner in the given League.

        Example response:
            {
            "someTeamId": Deci("1009.7"),
            "someOtherTeamId": Deci("1412.2"),
            "yetAnotherTeamId": Deci("1227.1"),
            ...
            }
        """
        return cls._addAndCombineResults(league, PointsScoredYearCalculator.getPointsScored, **kwargs)
