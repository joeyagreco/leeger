from typing import Any

from leeger.enum.MatchupType import MatchupType
from leeger.exception.InvalidFilterException import InvalidFilterException
from leeger.model.filter.YearFilters import YearFilters
from leeger.model.league.Matchup import Matchup
from leeger.model.league.Year import Year
from leeger.util.GeneralUtil import GeneralUtil
from leeger.util.navigator.YearNavigator import YearNavigator


class YearCalculator:
    """
    Should be inherited by all Year calculators
    """

    @classmethod
    def _getYearFilters(cls, year: Year, **kwargs) -> YearFilters:
        onlyChampionship = kwargs.pop("onlyChampionship", False)
        onlyPostSeason = kwargs.pop("onlyPostSeason", False)
        onlyRegularSeason = kwargs.pop("onlyRegularSeason", False)
        weekNumberStart = kwargs.pop("weekNumberStart", year.weeks[0].weekNumber)
        weekNumberEnd = kwargs.pop("weekNumberEnd", year.weeks[-1].weekNumber)

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

    @classmethod
    def _getAllFilteredMatchups(cls, year: Year, yearFilters: YearFilters, **kwargs) -> list[Matchup]:
        """
        Returns all Matchups in the given Year that are remaining after the given filters are applied.
        """
        allFilteredMatchups: list[Matchup] = list()
        for i in range(yearFilters.weekNumberStart - 1, yearFilters.weekNumberEnd):
            week = year.weeks[i]
            for matchup in week.matchups:
                if matchup.matchupType in yearFilters.includeMatchupTypes:
                    allFilteredMatchups.append(matchup)

        return allFilteredMatchups

    @classmethod
    def _setToNoneIfNoGamesPlayed(cls, responseDict: dict[str, Any], year: Year, yearFilters: YearFilters = None,
                                  **kwargs) -> None:
        """
        Takes a response dict and sets any value to None where the Team ID has no games played in the given range.
        """
        yearFilters = yearFilters if yearFilters is not None else cls._getYearFilters(year, **kwargs)
        teamIdAndNumberOfGamesPlayed = YearNavigator.getNumberOfGamesPlayed(year, yearFilters)

        for teamId in responseDict:
            if teamIdAndNumberOfGamesPlayed[teamId] == 0:
                responseDict[teamId] = None
