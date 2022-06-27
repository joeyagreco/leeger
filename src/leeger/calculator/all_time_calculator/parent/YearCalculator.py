from src.leeger.decorator.validate.validators import validateYear
from src.leeger.enum.MatchupType import MatchupType
from src.leeger.exception.InvalidFilterException import InvalidFilterException
from src.leeger.model.filter.YearFilters import YearFilters
from src.leeger.model.league.Year import Year


class YearCalculator:
    """
    Should be inherited by all Year calculators
    """

    @classmethod
    @validateYear
    def _getYearFilters(cls, year: Year, **kwargs) -> YearFilters:
        onlyChampionship = kwargs.pop("onlyChampionship", False)
        onlyPostSeason = kwargs.pop("onlyPostSeason", False)
        onlyRegularSeason = kwargs.pop("onlyRegularSeason", False)
        weekNumberStart = kwargs.pop("weekNumberStart", year.weeks[0].weekNumber)
        weekNumberEnd = kwargs.pop("weekNumberEnd", year.weeks[-1].weekNumber)

        if onlyChampionship:
            includeMatchupTypes = [
                MatchupType.CHAMPIONSHIP
            ]
        elif onlyPostSeason:
            includeMatchupTypes = [
                MatchupType.PLAYOFF,
                MatchupType.CHAMPIONSHIP
            ]
        elif onlyRegularSeason:
            includeMatchupTypes = [
                MatchupType.REGULAR_SEASON
            ]
        else:
            includeMatchupTypes = [
                MatchupType.REGULAR_SEASON,
                MatchupType.PLAYOFF,
                MatchupType.CHAMPIONSHIP
            ]

        ####################
        # validate filters #
        ####################
        # type checks
        if type(onlyChampionship) != bool:
            raise InvalidFilterException("'onlyChampionship' must be type 'bool'")
        if type(onlyPostSeason) != bool:
            raise InvalidFilterException("'onlyPostSeason' must be type 'bool'")
        if type(onlyRegularSeason) != bool:
            raise InvalidFilterException("'onlyRegularSeason' must be type 'bool'")
        if type(weekNumberStart) != int:
            raise InvalidFilterException("'weekNumberStart' must be type 'int'")
        if type(weekNumberEnd) != int:
            raise InvalidFilterException("'weekNumberEnd' must be type 'int'")

        # logic checks
        if [onlyChampionship, onlyPostSeason, onlyRegularSeason].count(True) > 1:
            raise InvalidFilterException(
                "Only one of 'onlyChampionship', 'onlyPostSeason', 'onlyRegularSeason' can be True")
        if weekNumberStart < 1:
            raise InvalidFilterException("'weekNumberStart' cannot be less than 1.")
        if weekNumberEnd > len(year.weeks):
            raise InvalidFilterException("'weekNumberEnd' cannot be greater than the number of weeks in the year.")
        if weekNumberStart > weekNumberEnd:
            raise InvalidFilterException("'weekNumberStart' cannot be greater than 'weekNumberEnd'.")

        return YearFilters(weekNumberStart=weekNumberStart, weekNumberEnd=weekNumberEnd,
                           includeMatchupTypes=includeMatchupTypes)
