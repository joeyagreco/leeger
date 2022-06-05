from src.leeger.calculator.parent.filter.YearFilters import YearFilters
from src.leeger.decorator.validate.validators import validateYear
from src.leeger.exception.InvalidFilterException import InvalidFilterException
from src.leeger.model.Year import Year


class YearCalculator:

    @staticmethod
    @validateYear
    def getFilters(year: Year, **kwargs) -> YearFilters:
        onlyPostSeason = kwargs.pop("onlyPostSeason", False)  # only include post season wins
        onlyRegularSeason = kwargs.pop("onlyRegularSeason", False)  # only include regular season wins
        weekNumberStart = kwargs.pop("weekNumberStart",
                                     year.weeks[0].weekNumber)  # week to start the calculations at (inclusive)
        weekNumberEnd = kwargs.pop("weekNumberEnd",
                                   year.weeks[-1].weekNumber)  # week to end the calculations at (inclusive)

        # validate filters

        # type checks
        if type(onlyPostSeason) != bool:
            raise InvalidFilterException("'onlyPostSeason' must be type 'bool'")
        if type(onlyRegularSeason) != bool:
            raise InvalidFilterException("'onlyRegularSeason' must be type 'bool'")
        if type(weekNumberStart) != int:
            raise InvalidFilterException("'weekNumberStart' must be type 'int'")
        if type(weekNumberEnd) != int:
            raise InvalidFilterException("'weekNumberEnd' must be type 'int'")

        # logic checks
        if onlyPostSeason and onlyRegularSeason:
            raise InvalidFilterException("'onlyPostSeason' and 'onlyRegularSeason' cannot both be True.")
        if weekNumberStart < 1:
            raise InvalidFilterException("'weekNumberStart' cannot be less than 1.")
        if weekNumberEnd > len(year.weeks):
            raise InvalidFilterException("'weekNumberEnd' cannot be greater than the number of weeks in the year.")

        return YearFilters(onlyPostSeason=onlyPostSeason, onlyRegularSeason=onlyRegularSeason,
                           weekNumberStart=weekNumberStart, weekNumberEnd=weekNumberEnd)
