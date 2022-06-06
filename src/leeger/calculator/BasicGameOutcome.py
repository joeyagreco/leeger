from decimal import Decimal

from src.leeger.calculator.parent.YearCalculator import YearCalculator
from src.leeger.decorator.validate.validators import validateYear
from src.leeger.model.Year import Year
from src.leeger.util.YearNavigator import YearNavigator


class BasicGameOutcome(YearCalculator):
    """
    Used to calculate all basic game outcomes.
    """

    @classmethod
    @validateYear
    def getWins(cls, year: Year, **kwargs) -> dict[str, int]:
        """
        Returns the number of wins for each team in the given Year.

        Example response:
            {
            "someTeamId": 8,
            "someOtherTeamId": 11,
            "yetAnotherTeamId": 7,
            ...
            }
        """
        cls.loadFilters(year, validateYear=False, **kwargs)

        teamIdAndWins = dict()
        for teamId in YearNavigator.getAllTeamIds(year):
            teamIdAndWins[teamId] = 0

        for i in range(cls._weekNumberStart - 1, cls._weekNumberEnd):
            week = year.weeks[i]
            if (week.isPlayoffWeek and not cls._onlyRegularSeason) or (
                    not week.isPlayoffWeek and not cls._onlyPostSeason):
                for matchup in week.matchups:
                    # team A won
                    if (matchup.teamAScore > matchup.teamBScore) or (
                            matchup.teamAScore == matchup.teamBScore and matchup.teamAHasTiebreaker):
                        teamIdAndWins[matchup.teamAId] += 1
                    # team B won
                    elif (matchup.teamBScore > matchup.teamAScore) or (
                            matchup.teamAScore == matchup.teamBScore and matchup.teamBHasTiebreaker):
                        teamIdAndWins[matchup.teamBId] += 1
        return teamIdAndWins

    @classmethod
    @validateYear
    def getLosses(cls, year: Year, **kwargs) -> dict[str, int]:
        """
        Returns the number of losses for each team in the given Year.

        Example response:
            {
            "someTeamId": 8,
            "someOtherTeamId": 11,
            "yetAnotherTeamId": 7,
            ...
            }
        """
        cls.loadFilters(year, validateYear=False, **kwargs)

        teamIdAndLosses = dict()
        for teamId in YearNavigator.getAllTeamIds(year):
            teamIdAndLosses[teamId] = 0

        for i in range(cls._weekNumberStart - 1, cls._weekNumberEnd):
            week = year.weeks[i]
            if (week.isPlayoffWeek and not cls._onlyRegularSeason) or (
                    not week.isPlayoffWeek and not cls._onlyPostSeason):
                for matchup in week.matchups:
                    # team A lost
                    if (matchup.teamAScore < matchup.teamBScore) or (
                            matchup.teamAScore == matchup.teamBScore and matchup.teamBHasTiebreaker):
                        teamIdAndLosses[matchup.teamAId] += 1
                    # team B lost
                    elif (matchup.teamBScore < matchup.teamAScore) or (
                            matchup.teamAScore == matchup.teamBScore and matchup.teamAHasTiebreaker):
                        teamIdAndLosses[matchup.teamBId] += 1
        return teamIdAndLosses

    @classmethod
    @validateYear
    def getTies(cls, year: Year, **kwargs) -> dict[str, int]:
        """
        Returns the number of ties for each team in the given Year.

        Example response:
            {
            "someTeamId": 8,
            "someOtherTeamId": 11,
            "yetAnotherTeamId": 7,
            ...
            }
        """
        cls.loadFilters(year, validateYear=False, **kwargs)

        teamIdAndTies = dict()
        for teamId in YearNavigator.getAllTeamIds(year):
            teamIdAndTies[teamId] = 0

        for i in range(cls._weekNumberStart - 1, cls._weekNumberEnd):
            week = year.weeks[i]
            if (week.isPlayoffWeek and not cls._onlyRegularSeason) or (
                    not week.isPlayoffWeek and not cls._onlyPostSeason):
                for matchup in week.matchups:
                    if matchup.teamAScore == matchup.teamBScore and not matchup.teamAHasTiebreaker and not matchup.teamBHasTiebreaker:
                        teamIdAndTies[matchup.teamAId] += 1
                        teamIdAndTies[matchup.teamBId] += 1
        return teamIdAndTies

    @classmethod
    @validateYear
    def getWinPercentage(cls, year: Year, **kwargs) -> dict[str, Decimal]:
        """
        Returns the win percentage for each team in the given Year.
        Win percentage will be represented as a non-rounded decimal.
        Example:
            33% win percentage -> Decimal("0.3333333333333333333333333333")
            100% win percentage -> Decimal("1.0")

        Example response:
            {
            "someTeamId": Decimal("0.85"),
            "someOtherTeamId": Decimal("0.1156"),
            "yetAnotherTeamId": Decimal("0.72"),
            ...
            }
        """
        cls.loadFilters(year, validateYear=False, **kwargs)

        teamIdAndWinPercentage = dict()
        teamIdAndWins = BasicGameOutcome.getWins(year, **kwargs)
        teamIdAndLosses = BasicGameOutcome.getLosses(year, **kwargs)
        teamIdAndTies = BasicGameOutcome.getTies(year, **kwargs)

        for teamId in YearNavigator.getAllTeamIds(year):
            numberOfWins = teamIdAndWins[teamId]
            numberOfLosses = teamIdAndLosses[teamId]
            numberOfTies = teamIdAndTies[teamId]
            numberOfGamesPlayed = numberOfWins + numberOfLosses + numberOfTies
            teamIdAndWinPercentage[teamId] = (Decimal(numberOfWins) + (Decimal(0.5) * Decimal(numberOfTies))) / Decimal(
                numberOfGamesPlayed)

        return teamIdAndWinPercentage
