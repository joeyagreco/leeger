from src.leeger.decorator.validate.validators import validateLeague
from src.leeger.exception.InvalidFilterException import InvalidFilterException
from src.leeger.model.filter.AllTimeFilters import AllTimeFilters
from src.leeger.model.league.League import League
from src.leeger.util.Deci import Deci
from src.leeger.util.LeagueNavigator import LeagueNavigator


class AllTimeCalculator:
    """
    Should be inherited by all All-Time calculators
    """

    @classmethod
    def __getAllTimeFilters(cls, league: League, **kwargs) -> AllTimeFilters:
        onlyChampionship = kwargs.pop("onlyChampionship", False)
        onlyPostSeason = kwargs.pop("onlyPostSeason", False)
        onlyRegularSeason = kwargs.pop("onlyRegularSeason", False)
        yearNumberStart = kwargs.pop("yearNumberStart", league.years[0].yearNumber)
        weekNumberStart = kwargs.pop("weekNumberStart",
                                     LeagueNavigator.getYearByYearNumber(league, yearNumberStart).weeks[0].weekNumber)
        yearNumberEnd = kwargs.pop("yearNumberEnd", league.years[-1].yearNumber)
        weekNumberEnd = kwargs.pop("weekNumberEnd",
                                   LeagueNavigator.getYearByYearNumber(league, yearNumberEnd).weeks[-1].weekNumber)

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

        return AllTimeFilters(yearNumberStart=yearNumberStart,
                              weekNumberStart=weekNumberStart,
                              yearNumberEnd=yearNumberEnd,
                              weekNumberEnd=weekNumberEnd,
                              onlyChampionship=onlyChampionship,
                              onlyPostSeason=onlyPostSeason,
                              onlyRegularSeason=onlyRegularSeason)

    @classmethod
    @validateLeague
    def _addAndCombineResults(cls, league: League, function: callable, **kwargs) -> dict[str, int | float | Deci]:
        allResultDicts = cls.__getAllResultDicts(league, function, **kwargs)

        # sum all results
        result: dict[str, int | float | Deci] = dict()
        for ownerId in LeagueNavigator.getAllOwnerIds(league):
            result[ownerId] = 0  # TODO: this may have a Deci/int/float so test for bugs there

        for resultDict in allResultDicts:
            # go through each team ID and value to get the owner ID and add to result
            for teamId in resultDict.keys():
                team = LeagueNavigator.getTeamById(league, teamId)
                result[team.ownerId] += resultDict[teamId]
        return result

    @classmethod
    @validateLeague
    def _averageAndCombineResults(cls, league: League, function: callable, **kwargs) -> dict[str, int | float | Deci]:
        allResultDicts = cls.__getAllResultDicts(league, function, **kwargs)

        # average all results
        result: dict[str, int | float | Deci] = dict()
        for ownerId in LeagueNavigator.getAllOwnerIds(league):
            result[ownerId] = 0  # TODO: this may have a Deci/int/float so test for bugs there

        for resultDict in allResultDicts:
            # go through each team ID and value to get the owner ID and add to result
            for teamId in resultDict.keys():
                team = LeagueNavigator.getTeamById(league, teamId)
                result[team.ownerId] += resultDict[teamId]
        # divide by number of result dicts to get average
        for teamId in result.keys():
            result[teamId] = result[teamId] / Deci(len(allResultDicts))
        return result

    @classmethod
    @validateLeague
    def __getAllResultDicts(cls, league: League, function: callable, **kwargs) -> list[dict]:

        allTimeFilters = cls.__getAllTimeFilters(league, **kwargs)

        # parse filters
        yearWeekNumberStartWeekNumberEnd: list[tuple] = list()
        if allTimeFilters.yearNumberStart == allTimeFilters.yearNumberEnd:
            yearWeekNumberStartWeekNumberEnd.append(
                (LeagueNavigator.getYearByYearNumber(league, allTimeFilters.yearNumberStart),
                 allTimeFilters.weekNumberStart,
                 allTimeFilters.weekNumberEnd))
        else:
            for year in league.years:
                if year.yearNumber == allTimeFilters.yearNumberStart:
                    # first year we want, make sure week number start matches what was requested
                    # givenWeekStart and every week greater
                    yearWeekNumberStartWeekNumberEnd.append((year, allTimeFilters.weekNumberStart, len(year.weeks)))
                elif year.yearNumber == allTimeFilters.yearNumberEnd:
                    # last year we want, make sure week number end matches what was requested
                    # first week and every week til givenWeekEnd
                    yearWeekNumberStartWeekNumberEnd.append((year, 1, allTimeFilters.weekNumberEnd))
                elif allTimeFilters.yearNumberStart < year.yearNumber < allTimeFilters.yearNumberEnd:
                    # this year is in our year range, include every week in this year
                    yearWeekNumberStartWeekNumberEnd.append((year, 1, len(year.weeks)))

        allResultDicts: list[dict] = list()

        for yse in yearWeekNumberStartWeekNumberEnd:
            currentYear = yse[0]
            currentWeekNumberStart = yse[1]
            currentWeekNumberEnd = yse[2]
            allResultDicts.append(function(currentYear,
                                           onlyChampionship=allTimeFilters.onlyChampionship,
                                           onlyPostSeason=allTimeFilters.onlyPostSeason,
                                           onlyRegularSeason=allTimeFilters.onlyRegularSeason,
                                           weekNumberStart=currentWeekNumberStart,
                                           weekNumberEnd=currentWeekNumberEnd))
        return allResultDicts
