from decimal import Decimal

from src.leeger.calculator.BasicGameOutcome import BasicGameOutcome
from src.leeger.calculator.parent.YearCalculator import YearCalculator
from src.leeger.decorator.validate.validators import validateYear
from src.leeger.model.Year import Year
from src.leeger.util.YearNavigator import YearNavigator


class AdvancedGameOutcome(YearCalculator):
    """
    Used to calculate all advanced game outcomes.
    """

    @classmethod
    @validateYear
    def getWAL(cls, year: Year, **kwargs) -> dict[str, Decimal]:
        """
        WAL is "Wins Against the League"
        Formula: (Number of Wins * 1) + (Number of Ties * 0.5)
        Returns the number of Wins Against the League for each team in the given Year.

        Example response:
            {
            "someTeamId": 8.7,
            "someOtherTeamId": 11.2,
            "yetAnotherTeamId": 7.1,
            ...
            }
        """
        cls.loadFilters(year, validateYear=False, **kwargs)

        teamIdAndWAL = dict()
        teamIdAndWins = BasicGameOutcome.getWins(year, **kwargs)
        teamIdAndTies = BasicGameOutcome.getTies(year, **kwargs)

        for teamId in YearNavigator.getAllTeamIds(year):
            teamIdAndWAL[teamId] = teamIdAndWins[teamId] + (Decimal(0.5) * Decimal(teamIdAndTies[teamId]))

        return teamIdAndWAL
