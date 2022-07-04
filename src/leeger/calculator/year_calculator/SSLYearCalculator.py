from src.leeger.calculator.parent.YearCalculator import YearCalculator
from src.leeger.calculator.year_calculator.AWALYearCalculator import AWALYearCalculator
from src.leeger.calculator.year_calculator.GameOutcomeYearCalculator import GameOutcomeYearCalculator
from src.leeger.calculator.year_calculator.ScoringShareYearCalculator import ScoringShareYearCalculator
from src.leeger.calculator.year_calculator.SingleScoreYearCalculator import SingleScoreYearCalculator
from src.leeger.decorator.validate.validators import validateYear
from src.leeger.model.league.Year import Year
from src.leeger.util.Deci import Deci
from src.leeger.util.YearNavigator import YearNavigator


class SSLYearCalculator(YearCalculator):
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

    __AWAL_AND_WAL_PER_GAME_MULTIPLIER: float = 100.0
    __SCORING_SHARE_MULTIPLIER: float = 2.0
    __MAX_AND_MIN_SCORE_MULTIPLIER: float = 0.05

    @classmethod
    @validateYear
    def getTeamScore(cls, year: Year, **kwargs) -> dict[str, Deci]:
        """
        Team Score is a score given to a team that is representative of how good that team is.

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
            awalPerGame = AWALYearCalculator.getAWALPerGame(year, **kwargs)[teamId]
            scoringShare = ScoringShareYearCalculator.getScoringShare(year, **kwargs)[teamId]
            maxScore = SingleScoreYearCalculator.getMaxScore(year, **kwargs)[teamId]
            minScore = SingleScoreYearCalculator.getMinScore(year, **kwargs)[teamId]

            teamIdAndTeamScore[teamId] = (awalPerGame * Deci(cls.__AWAL_AND_WAL_PER_GAME_MULTIPLIER)) + \
                                         (scoringShare * Deci(cls.__SCORING_SHARE_MULTIPLIER)) + \
                                         ((Deci(maxScore) + Deci(minScore)) * Deci(cls.__MAX_AND_MIN_SCORE_MULTIPLIER))
        return teamIdAndTeamScore

    @classmethod
    @validateYear
    def getTeamSuccess(cls, year: Year, **kwargs) -> dict[str, Deci]:
        """
        Team Success is a score given to a team that is representative of how successful that team is.

        Formula:
        Team Success = ((WAL Per Game) * aMultiplier) + (Scoring Share * bMultiplier) + ((Max Score + Min Score) * cMultiplier)

        Returns the Team Success for each team in the given Year.

        Example response:
            {
            "someTeamId": Deci("118.7"),
            "someOtherTeamId": Deci("112.2"),
            "yetAnotherTeamId": Deci("79.1"),
            ...
            }
        """

        teamIdAndTeamSuccess = dict()
        for teamId in YearNavigator.getAllTeamIds(year):
            walPerGame = GameOutcomeYearCalculator.getWALPerGame(year, **kwargs)[teamId]
            scoringShare = ScoringShareYearCalculator.getScoringShare(year, **kwargs)[teamId]
            maxScore = SingleScoreYearCalculator.getMaxScore(year, **kwargs)[teamId]
            minScore = SingleScoreYearCalculator.getMinScore(year, **kwargs)[teamId]

            teamIdAndTeamSuccess[teamId] = (walPerGame * Deci(cls.__AWAL_AND_WAL_PER_GAME_MULTIPLIER)) + \
                                           (scoringShare * Deci(cls.__SCORING_SHARE_MULTIPLIER)) + \
                                           ((Deci(maxScore) + Deci(minScore)) * Deci(
                                               cls.__MAX_AND_MIN_SCORE_MULTIPLIER))
        return teamIdAndTeamSuccess

    @classmethod
    @validateYear
    def getTeamLuck(cls, year: Year, **kwargs) -> dict[str, Deci]:
        """
        Team Luck is a score given to a team that is representative of how lucky that team is.

        Formula:
        Team Luck = Team Success - Team Score

        Returns the Team Luck for each team in the given Year.

        Example response:
            {
            "someTeamId": Deci("18.7"),
            "someOtherTeamId": Deci("12.2"),
            "yetAnotherTeamId": Deci("-9.1"),
            ...
            }
        """

        teamIdAndTeamLuck = dict()
        for teamId in YearNavigator.getAllTeamIds(year):
            teamIdAndTeamLuck[teamId] = cls.getTeamSuccess(year, **kwargs)[teamId] \
                                        - cls.getTeamScore(year, **kwargs)[teamId]
        return teamIdAndTeamLuck
