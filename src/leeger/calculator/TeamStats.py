from src.leeger.decorator.validate.validateLeague import validateLeague
from src.leeger.model.League import League
from src.leeger.util.LeagueNavigator import LeagueNavigator


class TeamStats:
    @classmethod
    @validateLeague
    def getWins(cls, league: League, yearNumber: int, **kwargs) -> dict[str, int]:
        """
        Returns the number of wins for each team in the given League in the given year.

        Example response:
            {
            "someTeamId": 8,
            "someOtherTeamId": 11,
            "yetAnotherTeamId": 7,
            ...
            }
        """
        year = LeagueNavigator.getYearByYearNumber(league, yearNumber, validateLeague=False)
        onlyPostSeason = kwargs.pop("onlyPostSeason", False)  # only include post season wins
        onlyRegularSeason = kwargs.pop("onlyRegularSeason", False)  # only include regular season wins
        weekNumberStart = kwargs.pop("weekNumberStart", year.weeks[0])  # week to start the calculations at (inclusive)
        weekNumberEnd = kwargs.pop("weekNumberEnd", year.weeks[-1])  # week to end the calculations at (inclusive)
