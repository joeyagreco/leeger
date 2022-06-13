from src.leeger.calculator.parent.YearCalculator import YearCalculator
from src.leeger.decorator.validate.validators import validateYear
from src.leeger.model.Year import Year
from src.leeger.util.Deci import Deci
from src.leeger.util.YearNavigator import YearNavigator


class GameOutcomeCalculator(YearCalculator):
    """
    Used to calculate all game outcomes.
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
    def getWinPercentage(cls, year: Year, **kwargs) -> dict[str, Deci]:
        """
        Returns the win percentage for each team in the given Year.
        Win percentage will be represented as a non-rounded decimal.
        Example:
            33% win percentage -> Deci("0.3333333333333333333333333333")
            100% win percentage -> Deci("1.0")

        Example response:
            {
            "someTeamId": Deci("0.85"),
            "someOtherTeamId": Deci("0.1156"),
            "yetAnotherTeamId": Deci("0.72"),
            ...
            }
        """
        cls.loadFilters(year, validateYear=False, **kwargs)

        teamIdAndWinPercentage = dict()
        teamIdAndWins = GameOutcomeCalculator.getWins(year, **kwargs)
        teamIdAndLosses = GameOutcomeCalculator.getLosses(year, **kwargs)
        teamIdAndTies = GameOutcomeCalculator.getTies(year, **kwargs)

        for teamId in YearNavigator.getAllTeamIds(year):
            numberOfWins = teamIdAndWins[teamId]
            numberOfLosses = teamIdAndLosses[teamId]
            numberOfTies = teamIdAndTies[teamId]
            numberOfGamesPlayed = numberOfWins + numberOfLosses + numberOfTies
            teamIdAndWinPercentage[teamId] = (Deci(numberOfWins) + (Deci(0.5) * Deci(numberOfTies))) / Deci(
                numberOfGamesPlayed)

        return teamIdAndWinPercentage

    @classmethod
    @validateYear
    def getWAL(cls, year: Year, **kwargs) -> dict[str, Deci]:
        """
        WAL is "Wins Against the League"
        Formula: (Number of Wins * 1) + (Number of Ties * 0.5)
        Returns the number of Wins Against the League for each team in the given Year.

        Example response:
            {
            "someTeamId": Deci("8.7"),
            "someOtherTeamId": Deci("11.2"),
            "yetAnotherTeamId": Deci("7.1"),
            ...
            }
        """
        cls.loadFilters(year, validateYear=False, **kwargs)

        teamIdAndWAL = dict()
        teamIdAndWins = GameOutcomeCalculator.getWins(year, **kwargs)
        teamIdAndTies = GameOutcomeCalculator.getTies(year, **kwargs)

        for teamId in YearNavigator.getAllTeamIds(year):
            teamIdAndWAL[teamId] = teamIdAndWins[teamId] + (Deci(0.5) * Deci(teamIdAndTies[teamId]))

        return teamIdAndWAL
