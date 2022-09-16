from __future__ import annotations

from dataclasses import dataclass

from leeger.enum.MatchupType import MatchupType
from leeger.model.league import Year


@dataclass(kw_only=True)
class YearFilters:
    """
    Used to house filters that will be applied to a Year when navigating through it.
    """
    weekNumberStart: int  # week to start at (inclusive)
    weekNumberEnd: int  # week to end at (inclusive)
    includeMatchupTypes: list[MatchupType]  # include matchups of these types
    includeMultiWeekMatchups: bool = True

    @classmethod
    def getForYear(cls, year: Year, **kwargs) -> YearFilters:
        from leeger.exception import InvalidFilterException
        from leeger.util.GeneralUtil import GeneralUtil
        onlyChampionship = kwargs.pop("onlyChampionship", False)
        onlyPostSeason = kwargs.pop("onlyPostSeason", False)
        onlyRegularSeason = kwargs.pop("onlyRegularSeason", False)
        weekNumberStart = kwargs.pop("weekNumberStart", year.weeks[0].weekNumber)
        weekNumberEnd = kwargs.pop("weekNumberEnd", year.weeks[-1].weekNumber)
        includeMultiWeekMatchups = kwargs.pop("includeMultiWeekMatchups", True)

        GeneralUtil.warnForUnusedKwargs(kwargs)

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
        if not isinstance(onlyChampionship, bool):
            raise InvalidFilterException("'onlyChampionship' must be type 'bool'")
        if not isinstance(onlyPostSeason, bool):
            raise InvalidFilterException("'onlyPostSeason' must be type 'bool'")
        if not isinstance(onlyRegularSeason, bool):
            raise InvalidFilterException("'onlyRegularSeason' must be type 'bool'")
        if not isinstance(weekNumberStart, int):
            raise InvalidFilterException("'weekNumberStart' must be type 'int'")
        if not isinstance(weekNumberEnd, int):
            raise InvalidFilterException("'weekNumberEnd' must be type 'int'")
        if not isinstance(includeMultiWeekMatchups, bool):
            raise InvalidFilterException("'includeMultiWeekMatchups' must be type 'bool'")

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
                           includeMatchupTypes=includeMatchupTypes, includeMultiWeekMatchups=includeMultiWeekMatchups)
