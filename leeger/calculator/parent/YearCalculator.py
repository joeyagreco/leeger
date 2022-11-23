from typing import Any

from leeger.model.filter.YearFilters import YearFilters
from leeger.model.league.Matchup import Matchup
from leeger.model.league.Year import Year
from leeger.util.navigator.YearNavigator import YearNavigator


class YearCalculator:
    """
    Should be inherited by all Year calculators
    """

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
        yearFilters = yearFilters if yearFilters is not None else YearFilters.getForYear(year, **kwargs)
        teamIdAndNumberOfGamesPlayed = YearNavigator.getNumberOfGamesPlayed(year, yearFilters)

        for teamId in responseDict:
            if teamIdAndNumberOfGamesPlayed[teamId] == 0:
                responseDict[teamId] = None

    @classmethod
    def _rank(cls, responseDict: dict[str, Any]) -> dict[str, int]:
        """
        Ranks the values of the given dict 1 -> n
        WHERE:
            - 1 is the largest value
            - n is the smallest value

        This will rank None values last.
        """

        # remove all None values before ranking
        teamIdsWithNoneValues = [teamId for teamId, value in responseDict.items() if value is None]

        # rank non-None values
        teamIdsAndValues = [(teamId, value) for teamId, value in responseDict.items() if value is not None]
        teamIdsAndValues.sort(key=lambda x: x[1], reverse=True)

        rankedDict = dict()
        currentRank = 1
        lastValue = None
        for teamId, value in teamIdsAndValues:
            rankedDict[teamId] = currentRank
            if lastValue is None or lastValue != value:
                currentRank += 1
            lastValue = value

        # add None values back
        for teamId in teamIdsWithNoneValues:
            rankedDict[teamId] = None
        return rankedDict
