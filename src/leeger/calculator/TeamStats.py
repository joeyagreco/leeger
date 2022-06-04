from src.leeger.decorator.validate.validators import validateYear
from src.leeger.model.Year import Year


class TeamStats:
    @classmethod
    @validateYear
    def getWins(cls, year: Year, **kwargs) -> dict[str, int]:
        """
        Returns the number of wins for each team in the given Year.

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
        weekNumberStart = kwargs.pop("weekNumberStart", year.weeks[0])  # week to start the calculations at (inclusive)
        weekNumberEnd = kwargs.pop("weekNumberEnd", year.weeks[-1])  # week to end the calculations at (inclusive)
