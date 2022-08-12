from leeger.decorator.validators import validateLeague
from leeger.exception.InvalidFilterException import InvalidFilterException
from leeger.model.filter.StreakFilters import StreakFilters
from leeger.model.league.League import League
from leeger.model.league.Matchup import Matchup
from leeger.util.GeneralUtil import GeneralUtil
from leeger.util.navigator.LeagueNavigator import LeagueNavigator


class StreakCalculator:
    """
    Should be inherited by all Streak calculators
    """
    MINIMUM_GAMES_FOR_STREAK = 2  # minimum number of games to be considered a streak

    @classmethod
    def _getStreakFilters(cls, league: League, **kwargs) -> StreakFilters:
        onlyChampionship = kwargs.pop("onlyChampionship", False)
        onlyPostSeason = kwargs.pop("onlyPostSeason", False)
        onlyRegularSeason = kwargs.pop("onlyRegularSeason", False)
        yearNumberStart = kwargs.pop("yearNumberStart", league.years[0].yearNumber)
        weekNumberStart = kwargs.pop("weekNumberStart",
                                     LeagueNavigator.getYearByYearNumber(league, yearNumberStart).weeks[0].weekNumber)
        yearNumberEnd = kwargs.pop("yearNumberEnd", league.years[-1].yearNumber)
        weekNumberEnd = kwargs.pop("weekNumberEnd",
                                   LeagueNavigator.getYearByYearNumber(league, yearNumberEnd).weeks[-1].weekNumber)
        onlyOngoing = kwargs.pop("onlyOngoing", False)

        GeneralUtil.warnForUnusedKwargs(kwargs)

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
        if type(yearNumberStart) != int:
            raise InvalidFilterException("'yearNumberStart' must be type 'int'")
        if type(weekNumberStart) != int:
            raise InvalidFilterException("'weekNumberStart' must be type 'int'")
        if type(yearNumberEnd) != int:
            raise InvalidFilterException("'yearNumberEnd' must be type 'int'")
        if type(weekNumberEnd) != int:
            raise InvalidFilterException("'weekNumberEnd' must be type 'int'")
        if type(onlyOngoing) != bool:
            raise InvalidFilterException("'onlyOngoing' must be type 'bool'")

        # logic checks
        if [onlyChampionship, onlyPostSeason, onlyRegularSeason].count(True) > 1:
            raise InvalidFilterException(
                "Only one of 'onlyChampionship', 'onlyPostSeason', 'onlyRegularSeason' can be True")
        if yearNumberStart > yearNumberEnd:
            raise InvalidFilterException("'yearNumberStart' cannot be greater than 'yearNumberEnd'.")
        if weekNumberStart < 1:
            raise InvalidFilterException("'weekNumberStart' cannot be less than 1.")
        if weekNumberEnd > len(LeagueNavigator.getYearByYearNumber(league, yearNumberEnd).weeks):
            raise InvalidFilterException("'weekNumberEnd' cannot be greater than the number of weeks in the year.")
        if weekNumberStart > weekNumberEnd and yearNumberStart == yearNumberEnd:
            raise InvalidFilterException(
                "'weekNumberStart' cannot be greater than 'weekNumberEnd' within the same year.")

        return StreakFilters(yearNumberStart=yearNumberStart,
                             weekNumberStart=weekNumberStart,
                             yearNumberEnd=yearNumberEnd,
                             weekNumberEnd=weekNumberEnd,
                             onlyChampionship=onlyChampionship,
                             onlyPostSeason=onlyPostSeason,
                             onlyRegularSeason=onlyRegularSeason,
                             onlyOngoing=onlyOngoing)

    @classmethod
    @validateLeague
    def _getAllFilteredMatchupsByWeek(cls, league: League, streakFilters: StreakFilters, **kwargs) -> dict[
        int, list[Matchup]]:
        """
        Returns all Matchups in the given League that are remaining after the given filters are applied.
        Key: Week Number
        Value: List of Matchups
        """

        # parse filters
        yearWeekNumberStartWeekNumberEnd: list[tuple] = list()
        if streakFilters.yearNumberStart == streakFilters.yearNumberEnd:
            yearWeekNumberStartWeekNumberEnd.append(
                (LeagueNavigator.getYearByYearNumber(league, streakFilters.yearNumberStart),
                 streakFilters.weekNumberStart,
                 streakFilters.weekNumberEnd))
        else:
            for year in league.years:
                if year.yearNumber == streakFilters.yearNumberStart:
                    # first year we want, make sure week number start matches what was requested
                    # givenWeekStart and every week greater
                    yearWeekNumberStartWeekNumberEnd.append((year, streakFilters.weekNumberStart, len(year.weeks)))
                elif year.yearNumber == streakFilters.yearNumberEnd:
                    # last year we want, make sure week number end matches what was requested
                    # first week and every week til givenWeekEnd
                    yearWeekNumberStartWeekNumberEnd.append((year, 1, streakFilters.weekNumberEnd))
                elif streakFilters.yearNumberStart < year.yearNumber < streakFilters.yearNumberEnd:
                    # this year is in our year range, include every week in this year
                    yearWeekNumberStartWeekNumberEnd.append((year, 1, len(year.weeks)))

        allFilteredMatchupsByWeek: dict[int, list[Matchup]] = dict()

        for yse in yearWeekNumberStartWeekNumberEnd:
            currentYear = yse[0]
            currentWeekNumberStart = yse[1]
            currentWeekNumberEnd = yse[2]

            for week in currentYear.weeks:
                allFilteredMatchupsByWeek[week.weekNumber] = list()
                if week.weekNumber >= currentWeekNumberStart and week.weekNumber <= currentWeekNumberEnd:
                    for matchup in week.matchups:
                        if matchup.matchupType in streakFilters.includeMatchupTypes:
                            allFilteredMatchupsByWeek[week.weekNumber].append(matchup)

        return allFilteredMatchupsByWeek
