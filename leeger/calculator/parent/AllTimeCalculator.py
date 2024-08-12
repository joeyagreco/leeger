from typing import Optional

from leeger.model.filter import YearFilters
from leeger.model.filter.AllTimeFilters import AllTimeFilters
from leeger.model.league.League import League
from leeger.model.league.Matchup import Matchup
from leeger.util.Deci import Deci
from leeger.util.navigator import MatchupNavigator
from leeger.util.navigator.LeagueNavigator import LeagueNavigator


class AllTimeCalculator:
    """
    Should be inherited by all All-Time calculators
    """

    @classmethod
    def _addAndCombineResults(
        cls, league: League, function: callable, **kwargs
    ) -> dict[str, Optional[int | float | Deci]]:
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
            result[ownerId] = (
                0  # TODO: this may have a Deci/int/float so test for bugs there
            )
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
    def __getAllResultDicts(
        cls, league: League, function: callable, **kwargs
    ) -> list[dict[str, int | float | Deci]]:
        """
        Returns the results for each given callable function in order from least -> most recent year.
        TODO: Replace this with the getAllResultDictsByYear() function.
        """

        allTimeFilters = AllTimeFilters.getForLeague(league, **kwargs)

        # parse filters
        yearWeekNumberStartWeekNumberEnd: list[tuple] = list()
        if allTimeFilters.yearNumberStart == allTimeFilters.yearNumberEnd:
            yearWeekNumberStartWeekNumberEnd.append(
                (
                    LeagueNavigator.getYearByYearNumber(
                        league, allTimeFilters.yearNumberStart
                    ),
                    allTimeFilters.weekNumberStart,
                    allTimeFilters.weekNumberEnd,
                )
            )
        else:
            for year in league.years:
                if year.yearNumber == allTimeFilters.yearNumberStart:
                    # first year we want, make sure week number start matches what was requested
                    # givenWeekStart and every week greater
                    yearWeekNumberStartWeekNumberEnd.append(
                        (year, allTimeFilters.weekNumberStart, len(year.weeks))
                    )
                elif year.yearNumber == allTimeFilters.yearNumberEnd:
                    # last year we want, make sure week number end matches what was requested
                    # first week and every week til givenWeekEnd
                    yearWeekNumberStartWeekNumberEnd.append(
                        (year, 1, allTimeFilters.weekNumberEnd)
                    )
                elif (
                    allTimeFilters.yearNumberStart
                    < year.yearNumber
                    < allTimeFilters.yearNumberEnd
                ):
                    # this year is in our year range, include every week in this year
                    yearWeekNumberStartWeekNumberEnd.append((year, 1, len(year.weeks)))

        allResultDicts: list[dict] = list()

        for yse in yearWeekNumberStartWeekNumberEnd:
            currentYear = yse[0]
            currentWeekNumberStart = yse[1]
            currentWeekNumberEnd = yse[2]
            allResultDicts.append(
                function(
                    currentYear,
                    onlyChampionship=allTimeFilters.onlyChampionship,
                    onlyPostSeason=allTimeFilters.onlyPostSeason,
                    onlyRegularSeason=allTimeFilters.onlyRegularSeason,
                    weekNumberStart=currentWeekNumberStart,
                    weekNumberEnd=currentWeekNumberEnd,
                    validate=kwargs.get("validate", True),
                )
            )
        return allResultDicts

    @classmethod
    def _getAllResultDictsByYear(
        cls, league: League, function: callable, **kwargs
    ) -> dict[str, dict]:
        """
        Returns the results for each given callable function by year.
        """

        allTimeFilters = AllTimeFilters.getForLeague(league, **kwargs)

        # parse filters
        yearWeekNumberStartWeekNumberEnd: list[tuple] = list()
        if allTimeFilters.yearNumberStart == allTimeFilters.yearNumberEnd:
            yearWeekNumberStartWeekNumberEnd.append(
                (
                    LeagueNavigator.getYearByYearNumber(
                        league, allTimeFilters.yearNumberStart
                    ),
                    allTimeFilters.weekNumberStart,
                    allTimeFilters.weekNumberEnd,
                )
            )
        else:
            for year in league.years:
                if year.yearNumber == allTimeFilters.yearNumberStart:
                    # first year we want, make sure week number start matches what was requested
                    # givenWeekStart and every week greater
                    yearWeekNumberStartWeekNumberEnd.append(
                        (year, allTimeFilters.weekNumberStart, len(year.weeks))
                    )
                elif year.yearNumber == allTimeFilters.yearNumberEnd:
                    # last year we want, make sure week number end matches what was requested
                    # first week and every week til givenWeekEnd
                    yearWeekNumberStartWeekNumberEnd.append(
                        (year, 1, allTimeFilters.weekNumberEnd)
                    )
                elif (
                    allTimeFilters.yearNumberStart
                    < year.yearNumber
                    < allTimeFilters.yearNumberEnd
                ):
                    # this year is in our year range, include every week in this year
                    yearWeekNumberStartWeekNumberEnd.append((year, 1, len(year.weeks)))

        allResultDicts: dict[str, dict] = dict()

        for yse in yearWeekNumberStartWeekNumberEnd:
            currentYear = yse[0]
            currentWeekNumberStart = yse[1]
            currentWeekNumberEnd = yse[2]
            allResultDicts[currentYear.yearNumber] = function(
                currentYear,
                onlyChampionship=allTimeFilters.onlyChampionship,
                onlyPostSeason=allTimeFilters.onlyPostSeason,
                onlyRegularSeason=allTimeFilters.onlyRegularSeason,
                weekNumberStart=currentWeekNumberStart,
                weekNumberEnd=currentWeekNumberEnd,
                validate=kwargs.get("validate", True),
            )
        return allResultDicts

    @classmethod
    def _getAllFilteredMatchups(
        cls,
        league: League,
        allTimeFilters: AllTimeFilters,
        simplifyMultiWeekMatchups=False,
    ) -> list[Matchup]:
        """
        Returns all Matchups in the given League that are remaining after the given filters are applied.
        """

        # parse filters
        yearWeekNumberStartWeekNumberEnd: list[tuple] = list()
        if allTimeFilters.yearNumberStart == allTimeFilters.yearNumberEnd:
            yearWeekNumberStartWeekNumberEnd.append(
                (
                    LeagueNavigator.getYearByYearNumber(
                        league, allTimeFilters.yearNumberStart
                    ),
                    allTimeFilters.weekNumberStart,
                    allTimeFilters.weekNumberEnd,
                )
            )
        else:
            for year in league.years:
                if year.yearNumber == allTimeFilters.yearNumberStart:
                    # first year we want, make sure week number start matches what was requested
                    # givenWeekStart and every week greater
                    yearWeekNumberStartWeekNumberEnd.append(
                        (year, allTimeFilters.weekNumberStart, len(year.weeks))
                    )
                elif year.yearNumber == allTimeFilters.yearNumberEnd:
                    # last year we want, make sure week number end matches what was requested
                    # first week and every week til givenWeekEnd
                    yearWeekNumberStartWeekNumberEnd.append(
                        (year, 1, allTimeFilters.weekNumberEnd)
                    )
                elif (
                    allTimeFilters.yearNumberStart
                    < year.yearNumber
                    < allTimeFilters.yearNumberEnd
                ):
                    # this year is in our year range, include every week in this year
                    yearWeekNumberStartWeekNumberEnd.append((year, 1, len(year.weeks)))

        allFilteredMatchups: list[Matchup] = list()
        multiWeekMatchupIdToMatchupsMap: dict[str, list[Matchup]] = dict()

        for yse in yearWeekNumberStartWeekNumberEnd:
            currentYear = yse[0]
            currentWeekNumberStart = yse[1]
            currentWeekNumberEnd = yse[2]

            for week in currentYear.weeks:
                if (
                    week.weekNumber >= currentWeekNumberStart
                    and week.weekNumber <= currentWeekNumberEnd
                ):
                    for matchup in week.matchups:
                        if matchup.matchupType in allTimeFilters.includeMatchupTypes:
                            mwmid = matchup.multiWeekMatchupId
                            if simplifyMultiWeekMatchups and mwmid is not None:
                                if mwmid in multiWeekMatchupIdToMatchupsMap:
                                    multiWeekMatchupIdToMatchupsMap[
                                        matchup.multiWeekMatchupId
                                    ].append(matchup)
                                else:
                                    multiWeekMatchupIdToMatchupsMap[
                                        matchup.multiWeekMatchupId
                                    ] = [matchup]
                            else:
                                allFilteredMatchups.append(matchup)

        if simplifyMultiWeekMatchups:
            # simplify any multi-week matchups and add them to the returning list
            for _, matchupList in multiWeekMatchupIdToMatchupsMap.items():
                allFilteredMatchups.append(
                    MatchupNavigator.simplifyMultiWeekMatchups(matchupList)
                )

        return allFilteredMatchups

    @classmethod
    def _allTimeFiltersToYearFilters(
        cls, league: League, allTimeFilters: AllTimeFilters
    ) -> dict[str, YearFilters]:
        """
        Returns the given AllTimeFilters as a dict of YearFilters by year.

        {
            "2020": YearFilters(...),
            "2021": YearFilters(...),
            etc...
        }
        """
        # TODO: look into how we are handling multiWeekMatchups in this filter transfer
        yearFiltersByYear: dict[str, YearFilters] = dict()
        # parse filters
        yearWeekNumberStartWeekNumberEnd: list[tuple] = list()
        if allTimeFilters.yearNumberStart == allTimeFilters.yearNumberEnd:
            yearNumber = str(
                LeagueNavigator.getYearByYearNumber(
                    league, allTimeFilters.yearNumberStart
                ).yearNumber
            )
            yearFiltersByYear[yearNumber] = YearFilters(
                weekNumberStart=allTimeFilters.weekNumberStart,
                weekNumberEnd=allTimeFilters.weekNumberEnd,
                includeMultiWeekMatchups=True,
                onlyPostSeason=allTimeFilters.onlyPostSeason,
                onlyChampionship=allTimeFilters.onlyChampionship,
                onlyRegularSeason=allTimeFilters.onlyRegularSeason,
            )
        else:
            for year in league.years:
                if year.yearNumber == allTimeFilters.yearNumberStart:
                    # first year we want, make sure week number start matches what was requested
                    # givenWeekStart and every week greater
                    yearFiltersByYear[str(year.yearNumber)] = YearFilters(
                        weekNumberStart=allTimeFilters.weekNumberStart,
                        weekNumberEnd=len(year.weeks),
                        includeMultiWeekMatchups=True,
                        onlyPostSeason=allTimeFilters.onlyPostSeason,
                        onlyChampionship=allTimeFilters.onlyChampionship,
                        onlyRegularSeason=allTimeFilters.onlyRegularSeason,
                    )
                elif year.yearNumber == allTimeFilters.yearNumberEnd:
                    # last year we want, make sure week number end matches what was requested
                    # first week and every week til givenWeekEnd
                    yearFiltersByYear[str(year.yearNumber)] = YearFilters(
                        weekNumberStart=1,
                        weekNumberEnd=allTimeFilters.weekNumberEnd,
                        includeMultiWeekMatchups=True,
                        onlyPostSeason=allTimeFilters.onlyPostSeason,
                        onlyChampionship=allTimeFilters.onlyChampionship,
                        onlyRegularSeason=allTimeFilters.onlyRegularSeason,
                    )
                elif (
                    allTimeFilters.yearNumberStart
                    < year.yearNumber
                    < allTimeFilters.yearNumberEnd
                ):
                    # this year is in our year range, include every week in this year
                    yearFiltersByYear[str(year.yearNumber)] = YearFilters(
                        weekNumberStart=1,
                        weekNumberEnd=len(year.weeks),
                        includeMultiWeekMatchups=True,
                        onlyPostSeason=allTimeFilters.onlyPostSeason,
                        onlyChampionship=allTimeFilters.onlyChampionship,
                        onlyRegularSeason=allTimeFilters.onlyRegularSeason,
                    )

        return yearFiltersByYear
