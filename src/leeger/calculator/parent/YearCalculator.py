from src.leeger.decorator.validate.validators import validateYear
from src.leeger.enum.MatchupType import MatchupType
from src.leeger.exception.InvalidFilterException import InvalidFilterException
from src.leeger.model.Year import Year
from src.leeger.util.Deci import Deci
from src.leeger.util.YearNavigator import YearNavigator


class YearCalculator:
    """
    Should be inherited by all stat calculators that calculate stats for a Year.
    """
    _weekNumberStart: int  # week to start the calculations at (inclusive)
    _weekNumberEnd: int  # week to end the calculations at (inclusive)
    _includeMatchupTypes: list[MatchupType]  # include matchups of these types

    @classmethod
    @validateYear
    def loadFilters(cls, year: Year, **kwargs) -> None:
        onlyPostSeason = kwargs.pop("onlyPostSeason", False)
        onlyRegularSeason = kwargs.pop("onlyRegularSeason", False)
        cls._weekNumberStart = kwargs.pop("weekNumberStart", year.weeks[0].weekNumber)
        cls._weekNumberEnd = kwargs.pop("weekNumberEnd", year.weeks[-1].weekNumber)

        if onlyPostSeason:
            cls._includeMatchupTypes = [
                MatchupType.PLAYOFF,
                MatchupType.CHAMPIONSHIP
            ]
        elif onlyRegularSeason:
            cls._includeMatchupTypes = [
                MatchupType.REGULAR_SEASON
            ]
        else:
            cls._includeMatchupTypes = [
                MatchupType.REGULAR_SEASON,
                MatchupType.PLAYOFF,
                MatchupType.CHAMPIONSHIP
            ]

        ####################
        # validate filters #
        ####################
        # type checks
        if type(onlyPostSeason) != bool:
            raise InvalidFilterException("'onlyPostSeason' must be type 'bool'")
        if type(onlyRegularSeason) != bool:
            raise InvalidFilterException("'onlyRegularSeason' must be type 'bool'")
        if type(cls._weekNumberStart) != int:
            raise InvalidFilterException("'weekNumberStart' must be type 'int'")
        if type(cls._weekNumberEnd) != int:
            raise InvalidFilterException("'weekNumberEnd' must be type 'int'")

        # logic checks
        if onlyPostSeason and onlyRegularSeason:
            raise InvalidFilterException("'onlyPostSeason' and 'onlyRegularSeason' cannot both be True.")
        if cls._weekNumberStart < 1:
            raise InvalidFilterException("'weekNumberStart' cannot be less than 1.")
        if cls._weekNumberEnd > len(year.weeks):
            raise InvalidFilterException("'weekNumberEnd' cannot be greater than the number of weeks in the year.")
        if cls._weekNumberStart > cls._weekNumberEnd:
            raise InvalidFilterException("'weekNumberEnd' cannot be greater than 'weekNumberStart'.")

    @classmethod
    @validateYear
    def getNumberOfGamesPlayed(cls, year: Year, **kwargs) -> dict[str, Deci]:
        """
        Returns the number of games played for each team in the given Year.

        Example response:
            {
            "someTeamId": Deci("4"),
            "someOtherTeamId": Deci("4"),
            "yetAnotherTeamId": Deci("5"),
            ...
            }
        """
        cls.loadFilters(year, **kwargs)

        teamIdAndNumberOfGamesPlayed = dict()
        allTeamIds = YearNavigator.getAllTeamIds(year)
        for teamId in allTeamIds:
            teamIdAndNumberOfGamesPlayed[teamId] = Deci(0)

        for i in range(cls._weekNumberStart - 1, cls._weekNumberEnd):
            week = year.weeks[i]
            for matchup in week.matchups:
                if matchup.matchupType in cls._includeMatchupTypes:
                    teamIdAndNumberOfGamesPlayed[matchup.teamAId] += Deci(1)
                    teamIdAndNumberOfGamesPlayed[matchup.teamBId] += Deci(1)
        return teamIdAndNumberOfGamesPlayed
