from typing import Optional

from src.leeger.calculator.parent.AllTimeCalculator import AllTimeCalculator
from src.leeger.calculator.year_calculator.SSLYearCalculator import SSLYearCalculator
from src.leeger.decorator.validate.validators import validateLeague
from src.leeger.model.league.League import League
from src.leeger.util.Deci import Deci


class SSLAllTimeCalculator(AllTimeCalculator):
    """
    Used to calculate all SSL stats.

    SSL stands for "Score Success Luck", which are 3 stats calculated here that go hand in hand.

    Team Score = How good a team is
    Team Success = How successful a team is
    Team Luck = How lucky a team is

    So Team Luck = Team Success = Team Score

    NOTE:
    These formulas uses several "magic" numbers as multipliers, which typically should be avoided.
    However, these numbers can be tweaked and the Team SSL relative to the test_league will remain roughly the same.
    This stat is more accurate with larger sample sizes (the more games played, the better).
    """

    @classmethod
    @validateLeague
    def getTeamScore(cls, league: League, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Team Score is a score given to a team that is representative of how good that team is.

        Formula:
        Team Score = ((AWAL Per Game) * aMultiplier) + (Scoring Share * bMultiplier) + ((Max Score + Min Score) * cMultiplier)

        Returns the combined Team Score for each Owner in the given League.
        Returns None for an Owner if all Years for that Owner are None

        Example response:
            {
            "someOwnerId": Deci("1118.7"),
            "someOtherOwnerId": Deci("1112.2"),
            "yetAnotherOwnerId": Deci("779.1"),
            ...
            }
        """

        return cls._addAndCombineResults(league, SSLYearCalculator.getTeamScore, validateLeague=False, **kwargs)

    @classmethod
    @validateLeague
    def getTeamSuccess(cls, league: League, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Team Success is a score given to a team that is representative of how successful that team is.

        Formula:
        Team Success = ((WAL Per Game) * aMultiplier) + (Scoring Share * bMultiplier) + ((Max Score + Min Score) * cMultiplier)

        Returns the combined Team Success for each Owner in the given League.
        Returns None for an Owner if all Years for that Owner are None

        Example response:
            {
            "someTeamId": Deci("1118.7"),
            "someOtherTeamId": Deci("1112.2"),
            "yetAnotherTeamId": Deci("779.1"),
            ...
            }
        """
        return cls._addAndCombineResults(league, SSLYearCalculator.getTeamSuccess, validateLeague=False, **kwargs)

    @classmethod
    @validateLeague
    def getTeamLuck(cls, league: League, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Team Luck is a score given to a team that is representative of how lucky that team is.

        Formula:
        Team Luck = Team Success - Team Score

        Returns the combined Team Luck for each Owner in the given League.
        Returns None for an Owner if all Years for that Owner are None

        Example response:
            {
            "someTeamId": Deci("118.7"),
            "someOtherTeamId": Deci("112.2"),
            "yetAnotherTeamId": Deci("-19.1"),
            ...
            }
        """
        return cls._addAndCombineResults(league, SSLYearCalculator.getTeamLuck, validateLeague=False, **kwargs)
