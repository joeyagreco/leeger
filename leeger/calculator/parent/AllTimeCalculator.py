from typing import Optional

from leeger.exception.InvalidFilterException import InvalidFilterException
from leeger.model.filter.AllTimeFilters import AllTimeFilters
from leeger.model.league.League import League
from leeger.model.league.Matchup import Matchup
from leeger.util.Deci import Deci
from leeger.util.GeneralUtil import GeneralUtil
from leeger.util.navigator.LeagueNavigator import LeagueNavigator


class AllTimeCalculator:
    """
    Should be inherited by all All-Time calculators
    """

    @classmethod
    def _getAllTimeFilters(cls, league: League, **kwargs) -> AllTimeFilters:
        onlyChampionship = kwargs.pop("onlyChampionship", False)
        onlyPostSeason = kwargs.pop("onlyPostSeason", False)
        onlyRegularSeason = kwargs.pop("onlyRegularSeason", False)
        yearNumberStart = kwargs.pop("yearNumberStart", league.years[0].yearNumber)
        weekNumberStart = kwargs.pop("weekNumberStart",
                                     LeagueNavigator.getYearByYearNumber(league, yearNumberStart).weeks[0].weekNumber)
        yearNumberEnd = kwargs.pop("yearNumberEnd", league.years[-1].yearNumber)
        weekNumberEnd = kwargs.pop("weekNumberEnd",
                                   LeagueNavigator.getYearByYearNumber(league, yearNumberEnd).weeks[-1].weekNumber)

        GeneralUtil.warnForUnusedKwargs(kwargs)

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
    def _addAndCombineResults(cls, league: League, function: callable, **kwargs) -> dict[
        str, Optional[int | float | Deci]]:
        """
        Sums all results retrieved from passing each Year in the given League into the given callable.
        The given callable should be a YearCalculator method.

        Example response:
            {
            "someOwnerId": Deci("18.7"),
            "someOtherOwnerId": Deci("21.2"),
            "yetAnotherOwnerId": Deci("17.1"),
            ...
            }
        NOTE: The type in the return dictionary values will match whatever the type the callable returns in its values for each Year.
        NOTE2: If ALL results for an Owner are None, the response will have None for that Owner. If only SOME results are None, then the None results will be ignored.
        """

        allResultDicts = cls.__getAllResultDicts(league, function, **kwargs)

        # this will keep track of whether an Owner has had a non-None result
        ownerIdAndWhetherOwnerHasHadAValidResult: dict[str, bool] = dict()

        # sum all results
        result: dict[str, int | float | Deci] = dict()
        for ownerId in LeagueNavigator.getAllOwnerIds(league):
            result[ownerId] = 0  # TODO: this may have a Deci/int/float so test for bugs there
            ownerIdAndWhetherOwnerHasHadAValidResult[ownerId] = False

        for resultDict in allResultDicts:
            # go through each team ID and value to get the owner ID and add to result
            for teamId in resultDict.keys():
                # check if this is a valid result
                if resultDict[teamId] is None:
                    continue
                team = LeagueNavigator.getTeamById(league, teamId)
                result[team.ownerId] += resultDict[teamId]
                ownerIdAndWhetherOwnerHasHadAValidResult[team.ownerId] = True

        # set None for each Owner that did not have a single valid result
        for ownerId in ownerIdAndWhetherOwnerHasHadAValidResult:
            if not ownerIdAndWhetherOwnerHasHadAValidResult[ownerId]:
                result[ownerId] = None
        return result

    @classmethod
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
    def __getAllResultDicts(cls, league: League, function: callable, **kwargs) -> list[dict]:

        allTimeFilters = cls._getAllTimeFilters(league, **kwargs)

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
                                           weekNumberEnd=currentWeekNumberEnd,
                                           validate=kwargs.get("validate", True)))
        return allResultDicts

    @classmethod
    def _getAllFilteredMatchups(cls, league: League, allTimeFilters: AllTimeFilters, **kwargs) -> list[Matchup]:
        """
        Returns all Matchups in the given League that are remaining after the given filters are applied.
        """

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

        allFilteredMatchups: list[Matchup] = list()

        for yse in yearWeekNumberStartWeekNumberEnd:
            currentYear = yse[0]
            currentWeekNumberStart = yse[1]
            currentWeekNumberEnd = yse[2]

            for week in currentYear.weeks:
                if week.weekNumber >= currentWeekNumberStart and week.weekNumber <= currentWeekNumberEnd:
                    for matchup in week.matchups:
                        if matchup.matchupType in allTimeFilters.includeMatchupTypes:
                            allFilteredMatchups.append(matchup)

        return allFilteredMatchups
