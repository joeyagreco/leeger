from src.leeger.decorator.validate.validators import validateYear
from src.leeger.exception.InvalidFilterException import InvalidFilterException
from src.leeger.model.Year import Year


class YearCalculator:
    """
    Should be inherited by all stat calculators that calculate stats for a Year.
    """
    _onlyPostSeason: bool  # only include post season wins
    _onlyRegularSeason: bool  # only include regular season wins
    _weekNumberStart: int  # week to start the calculations at (inclusive)
    _weekNumberEnd: int  # week to end the calculations at (inclusive)

    @classmethod
    @validateYear
    def loadFilters(cls, year: Year, **kwargs) -> None:
        cls._onlyPostSeason = kwargs.pop("onlyPostSeason", False)
        cls._onlyRegularSeason = kwargs.pop("onlyRegularSeason", False)
        cls._weekNumberStart = kwargs.pop("weekNumberStart", year.weeks[0].weekNumber)
        cls._weekNumberEnd = kwargs.pop("weekNumberEnd", year.weeks[-1].weekNumber)

        ####################
        # validate filters #
        ####################
        # type checks
        if type(cls._onlyPostSeason) != bool:
            raise InvalidFilterException("'onlyPostSeason' must be type 'bool'")
        if type(cls._onlyRegularSeason) != bool:
            raise InvalidFilterException("'onlyRegularSeason' must be type 'bool'")
        if type(cls._weekNumberStart) != int:
            raise InvalidFilterException("'weekNumberStart' must be type 'int'")
        if type(cls._weekNumberEnd) != int:
            raise InvalidFilterException("'weekNumberEnd' must be type 'int'")

        # logic checks
        if cls._onlyPostSeason and cls._onlyRegularSeason:
            raise InvalidFilterException("'onlyPostSeason' and 'onlyRegularSeason' cannot both be True.")
        if cls._weekNumberStart < 1:
            raise InvalidFilterException("'weekNumberStart' cannot be less than 1.")
        if cls._weekNumberEnd > len(year.weeks):
            raise InvalidFilterException("'weekNumberEnd' cannot be greater than the number of weeks in the year.")
        if cls._weekNumberStart > cls._weekNumberEnd:
            raise InvalidFilterException("'weekNumberEnd' cannot be greater than 'weekNumberStart'.")
