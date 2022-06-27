from src.leeger.calculator.parent.AllTimeCalculator import AllTimeCalculator
from src.leeger.calculator.year_calculator.GameOutcomeCalculator import GameOutcomeCalculator
from src.leeger.decorator.validate.validators import validateLeague
from src.leeger.model.league.League import League


class GameOutcomeAllTime(AllTimeCalculator):

    @classmethod
    @validateLeague
    def getWins(cls, league: League, **kwargs) -> dict[str, int]:
        """
        Returns the number of wins for each team in the given League.

        Example response:
            {
            "someTeamId": 18,
            "someOtherTeamId": 21,
            "yetAnotherTeamId": 17,
            ...
            }
        """
        return cls._sumAndCombineResults(league, GameOutcomeCalculator.getWins, **kwargs)
