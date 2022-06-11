from decimal import Decimal

from src.leeger.calculator.parent.YearCalculator import YearCalculator
from src.leeger.decorator.validate.validators import validateYear
from src.leeger.model.Year import Year
from src.leeger.util.YearNavigator import YearNavigator


class Scoring(YearCalculator):
    """
    Used to calculate all scoring outcomes.
    """

    @classmethod
    @validateYear
    def getPointsScored(cls, year: Year, **kwargs) -> dict[str, Decimal]:
        """
        Returns the number of Points Scored for each team in the given Year.

        Example response:
            {
            "someTeamId": Decimal("1009.7"),
            "someOtherTeamId": Decimal("1412.2"),
            "yetAnotherTeamId": Decimal("1227.1"),
            ...
            }
        """
        cls.loadFilters(year, validateYear=False, **kwargs)

        teamIdAndPointsScored = dict()
        for teamId in YearNavigator.getAllTeamIds(year):
            teamIdAndPointsScored[teamId] = Decimal(0)

        for i in range(cls._weekNumberStart - 1, cls._weekNumberEnd):
            week = year.weeks[i]
            if (week.isPlayoffWeek and not cls._onlyRegularSeason) or (
                    not week.isPlayoffWeek and not cls._onlyPostSeason):
                for matchup in week.matchups:
                    teamIdAndPointsScored[matchup.teamAId] += Decimal(str(matchup.teamAScore))
                    teamIdAndPointsScored[matchup.teamBId] += Decimal(str(matchup.teamBScore))

        return teamIdAndPointsScored
