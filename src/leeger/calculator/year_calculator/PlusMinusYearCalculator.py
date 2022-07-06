from typing import Optional

from src.leeger.calculator.parent.YearCalculator import YearCalculator
from src.leeger.calculator.year_calculator.PointsScoredYearCalculator import PointsScoredYearCalculator
from src.leeger.decorator.validate.validators import validateYear
from src.leeger.model.league.Year import Year
from src.leeger.util.Deci import Deci
from src.leeger.util.YearNavigator import YearNavigator


class PlusMinusYearCalculator(YearCalculator):
    """
    Used to calculate all plus/minuses.
    """

    @classmethod
    @validateYear
    def getPlusMinus(cls, year: Year, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Plus/Minus (+/-) is used to show the net score differential for a team in a Year.
        
        Plus/Minus = ΣA - ΣB
        WHERE:
        A = All scores by a team in a Year
        B = All scores against a team in a Year

        Returns the Plus/Minus for each team in the given Year.
        Returns None for a Team if they have no games played in the range.

        Example response:
            {
            "someTeamId": Deci("10.7"),
            "someOtherTeamId": Deci("-11.2"),
            "yetAnotherTeamId": Deci("34.1"),
            ...
            }
        """

        teamIdAndPlusMinus = dict()
        teamIdAndPointsScored = PointsScoredYearCalculator.getPointsScored(year, **kwargs)
        teamIdAndOpponentPointsScored = PointsScoredYearCalculator.getOpponentPointsScored(year, **kwargs)
        for teamId in YearNavigator.getAllTeamIds(year):
            pointsScored = teamIdAndPointsScored[teamId]
            opponentPointsScored = teamIdAndOpponentPointsScored[teamId]
            if None in (pointsScored, opponentPointsScored):
                teamIdAndPlusMinus[teamId] = None
            else:
                teamIdAndPlusMinus[teamId] = teamIdAndPointsScored[teamId] - teamIdAndOpponentPointsScored[teamId]

        return teamIdAndPlusMinus
