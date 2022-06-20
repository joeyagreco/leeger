from src.leeger.calculator.AWALCalculator import AWALCalculator
from src.leeger.calculator.ScoringShareCalculator import ScoringShareCalculator
from src.leeger.calculator.SingleScoreCalculator import SingleScoreCalculator
from src.leeger.calculator.parent.YearCalculator import YearCalculator
from src.leeger.decorator.validate.validators import validateYear
from src.leeger.model.Year import Year
from src.leeger.util.Deci import Deci
from src.leeger.util.YearNavigator import YearNavigator


class SSLCalculator(YearCalculator):
    """
    Used to calculate all SSL stats.

    SSL stands for "Score Success Luck", which are 3 stats calculated here that go hand in hand.

    Team Score = How good a team is
    Team Success = How successful a team is
    Team Luck = How lucky a team is

    So Team Luck = Team Success = Team Score

    NOTE:
    These formulas uses several "magic" numbers as multipliers, which typically should be avoided.
    However, these numbers can be tweaked and the Team SSL relative to the league will remain roughly the same.
    This stat is more accurate with larger sample sizes (the more games played, the better).
    """

    __AWALAndWALPerGameMultiplier: Deci = 100
    __ScoringShareMultiplier: Deci = 2
    __MaxAndMinScoreMultiplier: Deci = 0.05

    @classmethod
    @validateYear
    def getTeamScore(cls, year: Year, **kwargs) -> dict[str, Deci]:
        """
        Team Score is a score given to a team that is representative of how "good" that team is.

        Formula:
        Team Score = ((AWAL Per Game) * aMultiplier) + (Scoring Share * bMultiplier) + ((Max Score + Min Score) * cMultiplier)

        Returns the Team Score for each team in the given Year.

        Example response:
            {
            "someTeamId": Deci("118.7"),
            "someOtherTeamId": Deci("112.2"),
            "yetAnotherTeamId": Deci("79.1"),
            ...
            }
        """

        teamIdAndTeamScore = dict()
        for teamId in YearNavigator.getAllTeamIds(year):
            awalPerGame = AWALCalculator.getAWALPerGame(year, **kwargs)[teamId]
            scoringShare = ScoringShareCalculator.getScoringShare(year, **kwargs)[teamId]
            maxScore = SingleScoreCalculator.getMaxScore(year, **kwargs)[teamId]
            minScore = SingleScoreCalculator.getMinScore(year, **kwargs)[teamId]

            teamIdAndTeamScore[teamId] = (awalPerGame * Deci(cls.__AWALAndWALPerGameMultiplier)) + \
                                         (scoringShare * Deci(cls.__ScoringShareMultiplier)) + \
                                         ((Deci(maxScore) + Deci(minScore)) * Deci(cls.__MaxAndMinScoreMultiplier))
        return teamIdAndTeamScore
