from src.leeger.calculator.parent.AllTimeCalculator import AllTimeCalculator
from src.leeger.calculator.year_calculator.GameOutcomeYearCalculator import GameOutcomeYearCalculator
from src.leeger.decorator.validate.validators import validateLeague
from src.leeger.model.league.League import League


class GameOutcomeAllTimeCalculator(AllTimeCalculator):

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
        return cls._addAndCombineResults(league, GameOutcomeYearCalculator.getWins, **kwargs)

    @classmethod
    @validateLeague
    def getLosses(cls, league: League, **kwargs) -> dict[str, int]:
        """
        Returns the number of losses for each team in the given League.

        Example response:
            {
            "someTeamId": 18,
            "someOtherTeamId": 21,
            "yetAnotherTeamId": 17,
            ...
            }
        """
        return cls._addAndCombineResults(league, GameOutcomeYearCalculator.getLosses, **kwargs)

    @classmethod
    @validateLeague
    def getTies(cls, league: League, **kwargs) -> dict[str, int]:
        """
        Returns the number of ties for each team in the given League.

        Example response:
            {
            "someTeamId": 1,
            "someOtherTeamId": 0,
            "yetAnotherTeamId": 2,
            ...
            }
        """
        return cls._addAndCombineResults(league, GameOutcomeYearCalculator.getTies, **kwargs)
