from typing import Optional

from leeger.calculator.parent.AllTimeCalculator import AllTimeCalculator
from leeger.calculator.year_calculator import TeamSummaryYearCalculator
from leeger.decorator.validators import validateLeague
from leeger.model.league.League import League


class TeamSummaryAllTimeCalculator(AllTimeCalculator):

    @classmethod
    @validateLeague
    def getGamesPlayed(cls, league: League, **kwargs) -> dict[str, Optional[int]]:
        """
        Returns the number of wins for each team in the given League.

        Example response:
            {
            "someOwnerId": 18,
            "someOtherOwnerId": 21,
            "yetAnotherOwnerId": 17,
            ...
            }
        """
        return cls._addAndCombineResults(league, TeamSummaryYearCalculator.getGamesPlayed, **kwargs)
