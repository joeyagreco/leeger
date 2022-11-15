from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Any

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
    onlyChampionship: bool = False
    onlyPostSeason: bool = False
    onlyRegularSeason: bool = False
    calculateAgainstTeamIds: list[str] = None

    @classmethod
    def getForYear(cls, year: Year, **kwargs) -> YearFilters:
        from leeger.util.navigator import YearNavigator
        kwargsCopy = copy.deepcopy(kwargs)
        from leeger.exception import InvalidFilterException
        from leeger.util.GeneralUtil import GeneralUtil
        onlyChampionship = kwargsCopy.pop("onlyChampionship", False)
        onlyPostSeason = kwargsCopy.pop("onlyPostSeason", False)
        onlyRegularSeason = kwargsCopy.pop("onlyRegularSeason", False)
        weekNumberStart = kwargsCopy.pop("weekNumberStart", year.weeks[0].weekNumber)
        weekNumberEnd = kwargsCopy.pop("weekNumberEnd", year.weeks[-1].weekNumber)
        includeMultiWeekMatchups = kwargsCopy.pop("includeMultiWeekMatchups", True)
        calculateAgainstTeamIds = kwargsCopy.pop("calculateAgainstTeamIds", YearNavigator.getAllTeamIds(year))
        kwargsCopy.pop("includeMatchupTypes", None)  # so we don't get an unused kwarg warning

        GeneralUtil.warnForUnusedKwargs(kwargsCopy)

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
        if not isinstance(calculateAgainstTeamIds, list) or not all(
                isinstance(x, str) for x in calculateAgainstTeamIds):
            raise InvalidFilterException("'calculateAgainstTeamIds' must be type 'list[str]'")

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
                           includeMatchupTypes=includeMatchupTypes, includeMultiWeekMatchups=includeMultiWeekMatchups,
                           onlyPostSeason=onlyPostSeason, onlyChampionship=onlyChampionship,
                           onlyRegularSeason=onlyRegularSeason, calculateAgainstTeamIds=calculateAgainstTeamIds)

    def asKwargs(self) -> dict[str, Any]:
        return {
            "weekNumberStart": self.weekNumberStart,
            "weekNumberEnd": self.weekNumberEnd,
            "includeMatchupTypes": self.includeMatchupTypes,
            "includeMultiWeekMatchups": self.includeMultiWeekMatchups,
            "onlyPostSeason": self.onlyPostSeason,
            "onlyChampionship": self.onlyChampionship,
            "onlyRegularSeason": self.onlyRegularSeason,
            "calculateAgainstTeamIds": self.calculateAgainstTeamIds
        }
