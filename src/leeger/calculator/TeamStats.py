from src.leeger.decorator.validateLeague import validateLeague
from src.leeger.model.League import League


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
        onlyPostSeason = kwargs.pop("onlyPostSeason", False)  # only include post season wins
        onlyRegularSeason = kwargs.pop("onlyRegularSeason", False)  # only include regular season wins
        weekNumberStart = kwargs.pop("weekNumberStart", None)  # week to start the calculations at (inclusive)
        weekNumberEnd = kwargs.pop("weekNumberEnd", None)  # week to end the calculations at (inclusive)
