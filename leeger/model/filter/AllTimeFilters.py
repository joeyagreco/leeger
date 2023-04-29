from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Any

from leeger.enum.MatchupType import MatchupType
from leeger.model.league import League


@dataclass(kw_only=True)
class AllTimeFilters:
    """
    Used to house filters that will be used to calculate All-Time stats.
    """

    yearNumberStart: int  # year to start at (inclusive)
    weekNumberStart: int  # week to start at (inclusive)
    yearNumberEnd: int  # year to end at (inclusive)
    weekNumberEnd: int  # week to end at (inclusive)
    onlyChampionship: bool  # only include championship weeks
    onlyPostSeason: bool  # only include playoff weeks
    onlyRegularSeason: bool  # only include regular season weeks

    @property
    def includeMatchupTypes(self) -> list[MatchupType]:
        if self.onlyChampionship:
            return [MatchupType.CHAMPIONSHIP]
        elif self.onlyPostSeason:
            return [MatchupType.PLAYOFF, MatchupType.CHAMPIONSHIP]
        elif self.onlyRegularSeason:
            return [MatchupType.REGULAR_SEASON]
        else:
            return [MatchupType.REGULAR_SEASON, MatchupType.PLAYOFF, MatchupType.CHAMPIONSHIP]

    @classmethod
    def preferredOrderWithTitle(cls, league: League, **kwargs) -> list[tuple[str, Any]]:
        allTimeFilters = AllTimeFilters.getForLeague(league, **kwargs)
        return [
            ("Week Number Start", allTimeFilters.weekNumberStart),
            ("Year Number Start", allTimeFilters.yearNumberStart),
            ("Week Number End", allTimeFilters.weekNumberEnd),
            ("Year Number End", allTimeFilters.yearNumberEnd),
            ("Only Regular Season", allTimeFilters.onlyRegularSeason),
            ("Only Post Season", allTimeFilters.onlyPostSeason),
            ("Only Championship", allTimeFilters.onlyChampionship),
        ]

    @classmethod
    def getForLeague(cls, league: League, **kwargs) -> AllTimeFilters:
        from leeger.exception import InvalidFilterException
        from leeger.util.GeneralUtil import GeneralUtil
        from leeger.util.navigator import LeagueNavigator

        kwargsCopy = copy.deepcopy(kwargs)
        onlyChampionship = kwargsCopy.pop("onlyChampionship", False)
        onlyPostSeason = kwargsCopy.pop("onlyPostSeason", False)
        onlyRegularSeason = kwargsCopy.pop("onlyRegularSeason", False)
        yearNumberStart = kwargsCopy.pop("yearNumberStart", league.years[0].yearNumber)
        weekNumberStart = kwargsCopy.pop(
            "weekNumberStart",
            LeagueNavigator.getYearByYearNumber(league, yearNumberStart).weeks[0].weekNumber,
        )
        yearNumberEnd = kwargsCopy.pop("yearNumberEnd", league.years[-1].yearNumber)
        weekNumberEnd = kwargsCopy.pop(
            "weekNumberEnd",
            LeagueNavigator.getYearByYearNumber(league, yearNumberEnd).weeks[-1].weekNumber,
        )

        GeneralUtil.warnForUnusedKwargs(kwargsCopy)

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
        if not isinstance(yearNumberStart, int):
            raise InvalidFilterException("'yearNumberStart' must be type 'int'")
        if not isinstance(weekNumberStart, int):
            raise InvalidFilterException("'weekNumberStart' must be type 'int'")
        if not isinstance(yearNumberEnd, int):
            raise InvalidFilterException("'yearNumberEnd' must be type 'int'")
        if not isinstance(weekNumberEnd, int):
            raise InvalidFilterException("'weekNumberEnd' must be type 'int'")

        # logic checks
        if [onlyChampionship, onlyPostSeason, onlyRegularSeason].count(True) > 1:
            raise InvalidFilterException(
                "Only one of 'onlyChampionship', 'onlyPostSeason', 'onlyRegularSeason' can be True"
            )
        if yearNumberStart > yearNumberEnd:
            raise InvalidFilterException(
                "'yearNumberStart' cannot be greater than 'yearNumberEnd'."
            )
        if weekNumberStart < 1:
            raise InvalidFilterException("'weekNumberStart' cannot be less than 1.")
        if weekNumberEnd > len(LeagueNavigator.getYearByYearNumber(league, yearNumberEnd).weeks):
            raise InvalidFilterException(
                "'weekNumberEnd' cannot be greater than the number of weeks in the year."
            )
        if weekNumberStart > weekNumberEnd and yearNumberStart == yearNumberEnd:
            raise InvalidFilterException(
                "'weekNumberStart' cannot be greater than 'weekNumberEnd' within the same year."
            )

        return AllTimeFilters(
            yearNumberStart=yearNumberStart,
            weekNumberStart=weekNumberStart,
            yearNumberEnd=yearNumberEnd,
            weekNumberEnd=weekNumberEnd,
            onlyChampionship=onlyChampionship,
            onlyPostSeason=onlyPostSeason,
            onlyRegularSeason=onlyRegularSeason,
        )
