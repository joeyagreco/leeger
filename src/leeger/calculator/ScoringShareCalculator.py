from src.leeger.calculator.PointsScoredCalculator import PointsScoredCalculator
from src.leeger.calculator.parent.YearCalculator import YearCalculator
from src.leeger.decorator.validate.validators import validateYear
from src.leeger.model.Year import Year
from src.leeger.util.Deci import Deci
from src.leeger.util.YearNavigator import YearNavigator


class ScoringShareCalculator(YearCalculator):
    """
    Used to calculate all scoring shares.
    """

    @classmethod
    @validateYear
    def getScoringShare(cls, year: Year, **kwargs) -> dict[str, Deci]:
        """
        Scoring Share is used to show what percentage of league scoring a team was responsible for.
        Scoring Share = ((ΣA) / (ΣB)) * 100
        WHERE:
        A = All scores by a Team in a Year
        B = All scores by all Teams in a Year

        Returns the Scoring Share for each team in the given Year.

        Example response:
            {
            "someTeamId": Deci("10.7"),
            "someOtherTeamId": Deci("14.2"),
            "yetAnotherTeamId": Deci("12.1"),
            ...
            }
        """
        cls.loadFilters(year, validateYear=False, **kwargs)

        teamIdAndPointsScored = PointsScoredCalculator.getPointsScored(year, **kwargs)
        totalPointsScoredInYear = sum(teamIdAndPointsScored.values())
        teamIdAndScoringShare = dict()
        for teamId in YearNavigator.getAllTeamIds(year):
            teamIdAndScoringShare[teamId] = (teamIdAndPointsScored[teamId] / totalPointsScoredInYear) * Deci(100)

        return teamIdAndScoringShare

    @classmethod
    @validateYear
    def getOpponentScoringShare(cls, year: Year, **kwargs) -> dict[str, Deci]:
        """
        Opponent Scoring Share is used to show what percentage of league scoring a team's opponent was responsible for.
        Opponent Scoring Share = ((ΣA) / (ΣB)) * 100
        WHERE:
        A = All scores by a Team's opponent in a Year
        B = All scores by all Teams in a Year

        Returns the Opponent Scoring Share for each team in the given Year.

        Example response:
            {
            "someTeamId": Deci("10.7"),
            "someOtherTeamId": Deci("14.2"),
            "yetAnotherTeamId": Deci("12.1"),
            ...
            }
        """
        cls.loadFilters(year, validateYear=False, **kwargs)

        teamIdAndOpponentPointsScored = PointsScoredCalculator.getOpponentPointsScored(year, **kwargs)
        totalPointsScoredInYear = sum(teamIdAndOpponentPointsScored.values())
        teamIdAndOpponentScoringShare = dict()
        for teamId in YearNavigator.getAllTeamIds(year):
            teamIdAndOpponentScoringShare[teamId] = (teamIdAndOpponentPointsScored[
                                                         teamId] / totalPointsScoredInYear) * Deci(100)

        return teamIdAndOpponentScoringShare
