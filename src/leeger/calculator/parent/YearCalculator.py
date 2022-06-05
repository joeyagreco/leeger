from src.leeger.calculator.parent.filter.YearFilters import YearFilters
from src.leeger.model.Year import Year


class YearCalculator:

    @staticmethod
    def getFilters(year: Year, **kwargs) -> YearFilters:
        onlyPostSeason = kwargs.pop("onlyPostSeason", False)  # only include post season wins
        onlyRegularSeason = kwargs.pop("onlyRegularSeason", False)  # only include regular season wins
        weekNumberStart = kwargs.pop("weekNumberStart",
                                     year.weeks[0].weekNumber)  # week to start the calculations at (inclusive)
        weekNumberEnd = kwargs.pop("weekNumberEnd",
                                   year.weeks[-1].weekNumber)  # week to end the calculations at (inclusive)

        return YearFilters(onlyPostSeason=onlyPostSeason, onlyRegularSeason=onlyRegularSeason,
                           weekNumberStart=weekNumberStart, weekNumberEnd=weekNumberEnd)
