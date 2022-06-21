from src.leeger.calculator.parent.YearCalculator import YearCalculator
from src.leeger.decorator.validate.validators import validateYear
from src.leeger.model.Year import Year
from src.leeger.util.Deci import Deci
from src.leeger.util.MatchupNavigator import MatchupNavigator
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
        filters = cls.getYearFilters(year, validateYear=False, **kwargs)

        teamIdAndWins = dict()
        for teamId in YearNavigator.getAllTeamIds(year):
            teamIdAndWins[teamId] = 0

        for i in range(filters.weekNumberStart - 1, filters.weekNumberEnd):
            week = year.weeks[i]
            for matchup in week.matchups:
                if matchup.matchupType in filters.includeMatchupTypes:
                    # get winner team ID (if this wasn't a tie)
                    winnerTeamId = MatchupNavigator.getTeamIdOfMatchupWinner(matchup)
                    if winnerTeamId is not None:
                        teamIdAndWins[winnerTeamId] += 1
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
        filters = cls.getYearFilters(year, validateYear=False, **kwargs)

        teamIdAndLosses = dict()
        for teamId in YearNavigator.getAllTeamIds(year):
            teamIdAndLosses[teamId] = 0

        for i in range(filters.weekNumberStart - 1, filters.weekNumberEnd):
            week = year.weeks[i]
            for matchup in week.matchups:
                if matchup.matchupType in filters.includeMatchupTypes:
                    # get loser team ID (if this wasn't a tie)
                    winnerTeamId = MatchupNavigator.getTeamIdOfMatchupWinner(matchup)
                    if winnerTeamId is not None:
                        # return the OTHER team's ID
                        loserTeamId = matchup.teamAId if winnerTeamId != matchup.teamAId else matchup.teamBId
                        teamIdAndLosses[loserTeamId] += 1
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
        filters = cls.getYearFilters(year, validateYear=False, **kwargs)

        teamIdAndTies = dict()
        for teamId in YearNavigator.getAllTeamIds(year):
            teamIdAndTies[teamId] = 0

        for i in range(filters.weekNumberStart - 1, filters.weekNumberEnd):
            week = year.weeks[i]
            for matchup in week.matchups:
                if matchup.matchupType in filters.includeMatchupTypes:
                    if MatchupNavigator.getTeamIdOfMatchupWinner(matchup) is None:
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

        teamIdAndWAL = dict()
        teamIdAndWins = GameOutcomeCalculator.getWins(year, **kwargs)
        teamIdAndTies = GameOutcomeCalculator.getTies(year, **kwargs)

        for teamId in YearNavigator.getAllTeamIds(year):
            teamIdAndWAL[teamId] = teamIdAndWins[teamId] + (Deci(0.5) * Deci(teamIdAndTies[teamId]))

        return teamIdAndWAL

    @classmethod
    @validateYear
    def getWALPerGame(cls, year: Year, **kwargs) -> dict[str, Deci]:
        """
        Returns the number of Wins Against the League per game for each team in the given Year.

        Example response:
            {
            "someTeamId": Deci("0.7"),
            "someOtherTeamId": Deci("0.29"),
            "yetAnotherTeamId": Deci("0.48"),
            ...
            }
        """
        teamIdAndWAL = cls.getWAL(year, **kwargs)
        teamIdAndNumberOfGamesPlayed = YearNavigator.getNumberOfGamesPlayed(year, cls.getYearFilters(year, **kwargs))

        teamIdAndWALPerGame = dict()
        allTeamIds = YearNavigator.getAllTeamIds(year)
        for teamId in allTeamIds:
            # to avoid division by zero, we'll just set the WAL per game to 0 if the team has no games played
            if teamIdAndNumberOfGamesPlayed[teamId] == 0:
                teamIdAndWALPerGame[teamId] = Deci(0)
            else:
                teamIdAndWALPerGame[teamId] = teamIdAndWAL[teamId] / teamIdAndNumberOfGamesPlayed[teamId]

        return teamIdAndWALPerGame
