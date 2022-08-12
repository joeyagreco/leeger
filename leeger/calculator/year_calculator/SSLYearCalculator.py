from typing import Optional

from leeger.calculator.parent.YearCalculator import YearCalculator
from leeger.calculator.year_calculator.AWALYearCalculator import AWALYearCalculator
from leeger.calculator.year_calculator.GameOutcomeYearCalculator import GameOutcomeYearCalculator
from leeger.calculator.year_calculator.ScoringShareYearCalculator import ScoringShareYearCalculator
from leeger.calculator.year_calculator.SingleScoreYearCalculator import SingleScoreYearCalculator
from leeger.decorator.validators import validateYear
from leeger.model.league.Year import Year
from leeger.util.Deci import Deci
from leeger.util.navigator.YearNavigator import YearNavigator


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
    def getTeamScore(cls, year: Year, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Team Score is a score given to a team that is representative of how good that team is.

        Formula:
        Team Score = ((AWAL Per Game) * aMultiplier) + (Scoring Share * bMultiplier) + ((Max Score + Min Score) * cMultiplier)

        Returns the Team Score for each team in the given Year.
        Returns None if any stat used to calculate this is not found in the given range.

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

            # check if all stats could be found
            if None in (awalPerGame, scoringShare, maxScore, minScore):
                teamIdAndTeamScore[teamId] = None
            else:
                teamIdAndTeamScore[teamId] = (awalPerGame * Deci(cls.__AWAL_AND_WAL_PER_GAME_MULTIPLIER)) + \
                                             (scoringShare * Deci(cls.__SCORING_SHARE_MULTIPLIER)) + \
                                             ((Deci(maxScore) + Deci(minScore)) * Deci(
                                                 cls.__MAX_AND_MIN_SCORE_MULTIPLIER))
        return teamIdAndTeamScore

    @classmethod
    @validateYear
    def getTeamSuccess(cls, year: Year, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Team Success is a score given to a team that is representative of how successful that team is.

        Formula:
        Team Success = ((WAL Per Game) * aMultiplier) + (Scoring Share * bMultiplier) + ((Max Score + Min Score) * cMultiplier)

        Returns the Team Success for each team in the given Year.
        Returns None if any stat used to calculate this is not found in the given range.

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

            # check if all stats could be found
            if None in (walPerGame, scoringShare, maxScore, minScore):
                teamIdAndTeamSuccess[teamId] = None
            else:
                teamIdAndTeamSuccess[teamId] = (walPerGame * Deci(cls.__AWAL_AND_WAL_PER_GAME_MULTIPLIER)) + \
                                               (scoringShare * Deci(cls.__SCORING_SHARE_MULTIPLIER)) + \
                                               ((Deci(maxScore) + Deci(minScore)) * Deci(
                                                   cls.__MAX_AND_MIN_SCORE_MULTIPLIER))

        return teamIdAndTeamSuccess

    @classmethod
    @validateYear
    def getTeamLuck(cls, year: Year, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Team Luck is a score given to a team that is representative of how lucky that team is.

        Formula:
        Team Luck = Team Success - Team Score

        Returns the Team Luck for each team in the given Year.
        Returns None if any stat used to calculate this is not found in the given range.

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
            teamScore = cls.getTeamScore(year, **kwargs)[teamId]
            teamSuccess = cls.getTeamSuccess(year, **kwargs)[teamId]

            if None in (teamScore, teamSuccess):
                teamIdAndTeamLuck[teamId] = None
            else:
                teamIdAndTeamLuck[teamId] = teamSuccess - teamScore

        return teamIdAndTeamLuck
