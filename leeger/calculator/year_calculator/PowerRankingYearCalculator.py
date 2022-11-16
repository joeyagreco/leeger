import copy
from typing import Optional

from leeger.calculator.parent.YearCalculator import YearCalculator
from leeger.calculator.year_calculator import SSLYearCalculator
from leeger.decorator.validators import validateYear
from leeger.model.filter import YearFilters
from leeger.model.league.Year import Year
from leeger.util.Deci import Deci
from leeger.util.navigator.YearNavigator import YearNavigator


class PowerRankingYearCalculator(YearCalculator):
    """
    Used to calculate all power ranking stats.
    """

    @classmethod
    @validateYear
    def getRealPowerRanking(cls, year: Year, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Returns the Real Power Ranking for each team in the given Year.
        Returns None for a Team if they have no games played in the range.

        Example response:
            {
            "someTeamId": Deci("100.7"),
            "someOtherTeamId": Deci("120.2"),
            "yetAnotherTeamId": Deci("99.1"),
            ...
            }
        """
        filters = YearFilters.getForYear(year, **kwargs)

        teamIdAndRealPowerRanking = dict()
        for teamId in YearNavigator.getAllTeamIds(year):
            teamIdAndRealPowerRanking[teamId] = Deci(0)

        teamIdAndTeamScores: dict[str, list[Deci]] = dict()
        teamIdAndTeamSuccesses: dict[str, list[Deci]] = dict()
        for weekNumber in range(filters.weekNumberStart, filters.weekNumberEnd + 1):
            # get the Team Score and Team Success for each team each week
            kwargsCopy = copy.deepcopy(kwargs)
            kwargsCopy["weekNumberStart"] = weekNumber
            kwargsCopy["weekNumberEnd"] = weekNumber

            # get team score / success for this week only
            teamScoresForWeek = SSLYearCalculator.getTeamScore(year, **kwargsCopy)
            teamSuccessesForWeek = SSLYearCalculator.getTeamSuccess(year, **kwargsCopy)

            # add team scores to tracking dict
            for teamId, teamScore in teamScoresForWeek.items():
                if teamScore is not None:
                    if teamId in teamIdAndTeamScores:
                        teamIdAndTeamScores[teamId].append(teamScore)
                    else:
                        teamIdAndTeamScores[teamId] = [teamScore]

            # add team successes to tracking dict
            for teamId, teamSuccess in teamSuccessesForWeek.items():
                if teamSuccess is not None:
                    if teamId in teamIdAndTeamSuccesses:
                        teamIdAndTeamSuccesses[teamId].append(teamSuccess)
                    else:
                        teamIdAndTeamSuccesses[teamId] = [teamSuccess]

        for teamId in teamIdAndRealPowerRanking.keys():
            teamScores = teamIdAndTeamScores[teamId]
            teamSuccesses = teamIdAndTeamSuccesses[teamId]
            for i, (teamScore, teamSuccess) in enumerate(zip(teamScores, teamSuccesses)):
                weekMultiplier = i + 1
                powerRankingForWeek = weekMultiplier * ((teamScore * Deci(0.5)) + (teamSuccess * Deci(0.5)))
                teamIdAndRealPowerRanking[teamId] += powerRankingForWeek

            teamIdAndRealPowerRanking[teamId] = teamIdAndRealPowerRanking[teamId] / len(teamScores)

        cls._setToNoneIfNoGamesPlayed(teamIdAndRealPowerRanking, year, filters, **kwargs)
        return teamIdAndRealPowerRanking
