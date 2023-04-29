from typing import Optional

from leeger.calculator.parent.YearCalculator import YearCalculator
from leeger.decorator.validators import validateYear
from leeger.model.filter import YearFilters
from leeger.model.league.Year import Year
from leeger.util.navigator import YearNavigator


class TeamSummaryYearCalculator(YearCalculator):
    """
    Used to calculate general stats for a team.
    """

    @classmethod
    @validateYear
    def getGamesPlayed(cls, year: Year, **kwargs) -> dict[str, Optional[int]]:
        """
        Returns the number of games played for each team in the given year.
        """
        filters = YearFilters.getForYear(year, **kwargs)
        simplifiedMatchups = YearNavigator.getAllSimplifiedMatchupsInYear(year, filters)

        teamIdAndGamesPlayed = dict()

        for teamId in YearNavigator.getAllTeamIds(year):
            teamIdAndGamesPlayed[teamId] = 0

        for matchup in simplifiedMatchups:
            teamIdAndGamesPlayed[matchup.teamAId] += 1
            teamIdAndGamesPlayed[matchup.teamBId] += 1

        return teamIdAndGamesPlayed

    @classmethod
    @validateYear
    def getTotalGames(cls, year: Year, **kwargs) -> dict[str, Optional[int]]:
        """
        Returns the total number of games for each team in the given year.
        Notes:
            - Multi-week matchups will count 1 game per matchup
            - League Median Games will count 1 extra game per applicable matchup
        """
        filters = YearFilters.getForYear(year, **kwargs)

        return YearNavigator.getNumberOfGamesPlayed(
            year, filters, countLeagueMedianGamesAsTwoGames=True
        )
