from src.leeger.calculator.parent.AllTimeCalculator import AllTimeCalculator
from src.leeger.calculator.year_calculator.PlusMinusYearCalculator import PlusMinusYearCalculator
from src.leeger.decorator.validate.validators import validateLeague
from src.leeger.model.league.League import League
from src.leeger.util.Deci import Deci


class PlusMinusAllTimeCalculator(AllTimeCalculator):
    """
    Used to calculate all plus/minuses.
    """

    @classmethod
    @validateLeague
    def getPlusMinus(cls, league: League, **kwargs) -> dict[str, Deci]:
        """
        Plus/Minus (+/-) is used to show the net score differential for an Owner in a League.
        Plus/Minus = ΣA - ΣB
        WHERE:
        A = All scores by an Owner in a League
        B = All scores against an Owner in a League
        Returns the Plus/Minus for each Owner in the given League.

        Example response:
            {
            "someTeamId": Deci("10.7"),
            "someOtherTeamId": Deci("-11.2"),
            "yetAnotherTeamId": Deci("34.1"),
            ...
            }
        """

        return cls._addAndCombineResults(league, PlusMinusYearCalculator.getPlusMinus, **kwargs)