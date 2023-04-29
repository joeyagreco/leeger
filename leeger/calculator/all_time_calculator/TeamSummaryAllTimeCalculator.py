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

    @classmethod
    @validateLeague
    def getTotalGames(cls, league: League, **kwargs) -> dict[str, Optional[int]]:
        """
        Returns the total number of games for each team in the given year.
        Notes:
            - Multi-week matchups will count 1 game per matchup
            - League Median Games will count 1 extra game per applicable matchup

        Example response:
            {
            "someOwnerId": 18,
            "someOtherOwnerId": 21,
            "yetAnotherOwnerId": 17,
            ...
            }
        """
        return cls._addAndCombineResults(league, TeamSummaryYearCalculator.getTotalGames, **kwargs)
