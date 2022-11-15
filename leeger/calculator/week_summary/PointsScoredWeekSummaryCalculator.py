from typing import Optional

from leeger.calculator.parent.WeekSummaryCalculator import WeekSummaryCalculator
from leeger.decorator.validators import validateWeek
from leeger.model.league import Week
from leeger.util.Deci import Deci


class PointsScoredWeekSummaryCalculator(WeekSummaryCalculator):
    """
    Used to calculate all points scored.
    """

    @classmethod
    @validateWeek
    def getPointsScored(cls, week: Week, **kwargs) -> Optional[Deci]:
        """
        Returns the number of Points Scored in the given week.
        Returns None if there are no valid matchups.
        """
        ...
