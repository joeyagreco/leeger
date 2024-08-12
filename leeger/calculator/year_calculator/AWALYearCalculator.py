from typing import Optional

from leeger.calculator.parent.YearCalculator import YearCalculator
from leeger.calculator.year_calculator.GameOutcomeYearCalculator import (
    GameOutcomeYearCalculator,
)
from leeger.decorator.validators import validateYear
from leeger.model.filter import YearFilters
from leeger.model.filter.WeekFilters import WeekFilters
from leeger.model.league.Year import Year
from leeger.util.Deci import Deci
from leeger.util.GeneralUtil import GeneralUtil
from leeger.util.navigator.WeekNavigator import WeekNavigator
from leeger.util.navigator.YearNavigator import YearNavigator


class AWALYearCalculator(YearCalculator):
    """
    Used to calculate all AWAL stats.
    """

    @classmethod
    @validateYear
    def getAWAL(cls, year: Year, **kwargs) -> dict[str, Optional[Deci]]:
        """
        AWAL stands for Adjusted Wins Against the League.
        It is exactly that, an adjustment added to the Wins Against the League (or WAL) of a team.
        In simple terms, this stat more accurately represents how many WAL any given team should have.
        i.e. A team with 6.3 AWAL "deserves" 6.3 WAL.

        AWAL = W * (1/L) + T * (0.5/L)
        Where:
        W = Teams outscored in a week
        T = Teams tied in a week
        L = Opponents in a week (usually test_league size - 1)

        Returns the number of Adjusted Wins Against the League for each team in the given Year.
        Returns None for a Team if they have no games played in the range.

        Example response:
            {
            "someTeamId": Deci("8.7"),
            "someOtherTeamId": Deci("11.2"),
            "yetAnotherTeamId": Deci("7.1"),
            ...
            }
        """
        filters = YearFilters.getForYear(year, **kwargs)

        teamIdAndAWAL = dict()
        allTeamIds = YearNavigator.getAllTeamIds(year)
        for teamId in allTeamIds:
            teamIdAndAWAL[teamId] = Deci(0)

        for i in range(filters.weekNumberStart - 1, filters.weekNumberEnd):
            week = year.weeks[i]
            opponentsInWeek = (
                WeekNavigator.getNumberOfValidTeamsInWeek(
                    week, WeekFilters(includeMatchupTypes=filters.includeMatchupTypes)
                )
                - 1
            )
            teamsOutscored = dict()
            teamsTied = dict()
            for teamId in allTeamIds:
                teamsOutscored[teamId] = 0
                teamsTied[teamId] = 0
            allTeamIdsAndScoresForWeek = WeekNavigator.getTeamIdsAndScores(
                week, WeekFilters(includeMatchupTypes=filters.includeMatchupTypes)
            )
            allScores = allTeamIdsAndScoresForWeek.values()

            for teamId in allTeamIdsAndScoresForWeek.keys():
                teamsOutscored[teamId] = 0
                teamsTied[teamId] = 0
                score = allTeamIdsAndScoresForWeek[teamId]
                for s in allScores:
                    if score > s:
                        teamsOutscored[teamId] += 1
                    if score == s:
                        teamsTied[teamId] += 1
                # remove 1 from the teamsTied tracker since we will always find a tie for this team's score in the list of all scores in the week
                teamsTied[teamId] -= 1
                # calculate the AWAL for each team for this week
                teamIdAndAWAL[teamId] += (
                    Deci(teamsOutscored[teamId]) * (Deci(1) / Deci(opponentsInWeek))
                ) + (Deci(teamsTied[teamId]) * (Deci(0.5) / Deci(opponentsInWeek)))

        # add league median wins if applicable
        if year.yearSettings.leagueMedianGames:
            teamIdAndLeagueMedianWins = GameOutcomeYearCalculator.getLeagueMedianWins(
                year, **kwargs
            )
            for teamId in allTeamIds:
                leagueMedianWins = teamIdAndLeagueMedianWins[teamId]
                teamIdAndAWAL[teamId] = GeneralUtil.safeSum(
                    teamIdAndAWAL[teamId], leagueMedianWins
                )

        cls._setToNoneIfNoGamesPlayed(teamIdAndAWAL, year, filters, **kwargs)
        return teamIdAndAWAL

    @classmethod
    @validateYear
    def getAWALPerGame(cls, year: Year, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Returns the number of Adjusted Wins Against the League per game for each team in the given Year.
        Returns None for a Team if they have no games played in the range.

        Example response:
            {
            "someTeamId": Deci("0.7"),
            "someOtherTeamId": Deci("0.2"),
            "yetAnotherTeamId": Deci("0.1"),
            ...
            }
        """

        teamIdAndAWAL = AWALYearCalculator.getAWAL(year, **kwargs)
        teamIdAndNumberOfGamesPlayed = YearNavigator.getNumberOfGamesPlayed(
            year,
            YearFilters.getForYear(year, **kwargs),
            countLeagueMedianGamesAsTwoGames=True,
        )

        teamIdAndAWALPerGame = dict()
        allTeamIds = YearNavigator.getAllTeamIds(year)
        for teamId in allTeamIds:
            if teamIdAndNumberOfGamesPlayed[teamId] == 0:
                teamIdAndAWALPerGame[teamId] = None
            else:
                teamIdAndAWALPerGame[teamId] = (
                    teamIdAndAWAL[teamId] / teamIdAndNumberOfGamesPlayed[teamId]
                )

        return teamIdAndAWALPerGame

    @classmethod
    @validateYear
    def getOpponentAWAL(cls, year: Year, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Returns the number of Adjusted Wins Against the League for each team's opponents in the given Year.
        Returns None for a Team if they have no games played in the range.

        Example response:
            {
            "someTeamId": Deci("8.7"),
            "someOtherTeamId": Deci("11.2"),
            "yetAnotherTeamId": Deci("7.1"),
            ...
            }
        """
        filters = YearFilters.getForYear(year, **kwargs)

        teamIdAndOpponentAWAL = dict()
        allTeamIds = YearNavigator.getAllTeamIds(year)
        for teamId in allTeamIds:
            teamIdAndOpponentAWAL[teamId] = Deci(0)

        for i in range(filters.weekNumberStart - 1, filters.weekNumberEnd):
            week = year.weeks[i]
            opponentsInWeek = (
                WeekNavigator.getNumberOfValidTeamsInWeek(
                    week, WeekFilters(includeMatchupTypes=filters.includeMatchupTypes)
                )
                - 1
            )
            teamsOutscored = dict()
            teamsTied = dict()
            for teamId in allTeamIds:
                teamsOutscored[teamId] = 0
                teamsTied[teamId] = 0
            allTeamIdsAndOpponentScoresForWeek = (
                WeekNavigator.getTeamIdsAndOpponentScores(
                    week, WeekFilters(includeMatchupTypes=filters.includeMatchupTypes)
                )
            )
            allScores = allTeamIdsAndOpponentScoresForWeek.values()

            for teamId in allTeamIdsAndOpponentScoresForWeek.keys():
                teamsOutscored[teamId] = 0
                teamsTied[teamId] = 0
                score = allTeamIdsAndOpponentScoresForWeek[teamId]
                for s in allScores:
                    if score > s:
                        teamsOutscored[teamId] += 1
                    if score == s:
                        teamsTied[teamId] += 1
                # remove 1 from the teamsTied tracker since we will always find a tie for this team's score in the list of all scores in the week
                teamsTied[teamId] -= 1
                # calculate the AWAL for each team's opponent for this week
                teamIdAndOpponentAWAL[teamId] += (
                    Deci(teamsOutscored[teamId]) * (Deci(1) / Deci(opponentsInWeek))
                ) + (Deci(teamsTied[teamId]) * (Deci(0.5) / Deci(opponentsInWeek)))

        # add league median wins if applicable
        if year.yearSettings.leagueMedianGames:
            teamIdAndLeagueMedianWins = (
                GameOutcomeYearCalculator.getOpponentLeagueMedianWins(year, **kwargs)
            )
            for teamId in allTeamIds:
                leagueMedianWins = teamIdAndLeagueMedianWins[teamId]
                teamIdAndOpponentAWAL[teamId] = GeneralUtil.safeSum(
                    teamIdAndOpponentAWAL[teamId], leagueMedianWins
                )

        cls._setToNoneIfNoGamesPlayed(teamIdAndOpponentAWAL, year, filters, **kwargs)
        return teamIdAndOpponentAWAL

    @classmethod
    @validateYear
    def getOpponentAWALPerGame(cls, year: Year, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Returns the number of Adjusted Wins Against the League per game for each team's opponents in the given Year.
        Returns None for a Team if they have no games played in the range.

        Example response:
            {
            "someTeamId": Deci("8.7"),
            "someOtherTeamId": Deci("11.2"),
            "yetAnotherTeamId": Deci("7.1"),
            ...
            }
        """

        teamIdAndOpponentAWAL = AWALYearCalculator.getOpponentAWAL(year, **kwargs)
        teamIdAndNumberOfGamesPlayed = YearNavigator.getNumberOfGamesPlayed(
            year,
            YearFilters.getForYear(year, **kwargs),
            countLeagueMedianGamesAsTwoGames=True,
        )

        teamIdAndOpponentAWALPerGame = dict()
        allTeamIds = YearNavigator.getAllTeamIds(year)
        for teamId in allTeamIds:
            if teamIdAndNumberOfGamesPlayed[teamId] == 0:
                teamIdAndOpponentAWALPerGame[teamId] = None
            else:
                teamIdAndOpponentAWALPerGame[teamId] = (
                    teamIdAndOpponentAWAL[teamId] / teamIdAndNumberOfGamesPlayed[teamId]
                )

        return teamIdAndOpponentAWALPerGame
