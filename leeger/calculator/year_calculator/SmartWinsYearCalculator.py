from typing import Optional

from leeger.calculator.parent.YearCalculator import YearCalculator
from leeger.decorator.validators import validateYear
from leeger.model.filter import YearFilters
from leeger.model.league.Year import Year
from leeger.util.Deci import Deci
from leeger.util.navigator.YearNavigator import YearNavigator


class SmartWinsYearCalculator(YearCalculator):
    """
    Used to calculate all Smart Wins stats.
    """

    @classmethod
    @validateYear
    def getSmartWins(cls, year: Year, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Smart Wins show how many wins a team would have if it played against every score in a given collection.
        In this case, the collection is every score in the given Year.
        Smart Wins = Σ((W + (T/2)) / S)
        WHERE:
        W = Total scores in the Year beat
        T = Total scores in the Year tied
        S = Number of scores in the Year - 1

        Returns the number of Smart Wins for each team in the given Year.
        Returns None for a Team if they have no games played in the range.

        Example response:
            {
            "someTeamId": Deci("8.7"),
            "someOtherTeamId": Deci("11.2"),
            "yetAnotherTeamId": Deci("7.1"),
            ...
            }
        """

        ####################
        # Helper functions #
        ####################
        def getNumberOfScoresBeatAndTied(score: float | int, scores: list[float | int]) -> list[int, int]:
            scoresBeatAndTied = [0, 0]
            for s in scores:
                if score > s:
                    scoresBeatAndTied[0] += 1
                elif score == s:
                    scoresBeatAndTied[1] += 1
            # remove 1 from the scores tied tracker since we will always find a tie for this teams score in the list of all scores
            scoresBeatAndTied[1] -= 1
            return scoresBeatAndTied

        ####################
        ####################
        ####################

        filters = YearFilters.getForYear(year, **kwargs)

        # get all scores we want to include in our smart wins calculation
        teamIdsAndScores = list()

        allMatchups = YearNavigator.getAllSimplifiedMatchupsInYear(year, filters)

        for matchup in allMatchups:
            teamIdsAndScores.append((matchup.teamAId, matchup.teamAScore))
            teamIdsAndScores.append((matchup.teamBId, matchup.teamBScore))

        teamIdAndSmartWins = dict()
        allTeamIds = YearNavigator.getAllTeamIds(year)
        for teamId in allTeamIds:
            teamIdAndSmartWins[teamId] = Deci(0)

        allScores = YearNavigator.getAllScoresInYear(year, simplifyMultiWeekMatchups=True)
        for teamId, score in teamIdsAndScores:
            scoresBeat, scoresTied = getNumberOfScoresBeatAndTied(score, allScores)
            smartWins = (scoresBeat + (scoresTied / Deci("2"))) / (len(allScores) - Deci("1"))
            teamIdAndSmartWins[teamId] += smartWins

        cls._setToNoneIfNoGamesPlayed(teamIdAndSmartWins, year, filters, **kwargs)
        return teamIdAndSmartWins

    @classmethod
    @validateYear
    def getSmartWinsPerGame(cls, year: Year, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Returns the number of Smart Wins per game for each team in the given Year.
        Returns None for a Team if they have no games played in the range.

        Example response:
            {
            "someTeamId": Deci("8.7"),
            "someOtherTeamId": Deci("11.2"),
            "yetAnotherTeamId": Deci("7.1"),
            ...
            }
        """

        teamIdAndSmartWins = SmartWinsYearCalculator.getSmartWins(year, **kwargs)
        teamIdAndNumberOfGamesPlayed = YearNavigator.getNumberOfGamesPlayed(year,
                                                                            YearFilters.getForYear(year, **kwargs),
                                                                            countMultiWeekMatchupsAsOneGame=True)

        teamIdAndSmartWinsPerGame = dict()
        allTeamIds = YearNavigator.getAllTeamIds(year)
        for teamId in allTeamIds:
            if teamIdAndNumberOfGamesPlayed[teamId] == 0:
                teamIdAndSmartWinsPerGame[teamId] = None
            else:
                teamIdAndSmartWinsPerGame[teamId] = teamIdAndSmartWins[teamId] / teamIdAndNumberOfGamesPlayed[teamId]

        return teamIdAndSmartWinsPerGame

    @classmethod
    @validateYear
    def getOpponentSmartWins(cls, year: Year, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Returns the number of Smart Wins for each team's opponents in the given Year.
        Returns None for a Team if they have no games played in the range.

        Example response:
            {
            "someTeamId": Deci("8.7"),
            "someOtherTeamId": Deci("11.2"),
            "yetAnotherTeamId": Deci("7.1"),
            ...
            }
        """

        ####################
        # Helper functions #
        ####################
        def getNumberOfScoresBeatAndTied(score: float | int, scores: list[float | int]) -> list[int, int]:
            scoresBeatAndTied = [0, 0]
            for s in scores:
                if score > s:
                    scoresBeatAndTied[0] += 1
                elif score == s:
                    scoresBeatAndTied[1] += 1
            # remove 1 from the scores tied tracker since we will always find a tie for this teams score in the list of all scores
            scoresBeatAndTied[1] -= 1
            return scoresBeatAndTied

        ####################
        ####################
        ####################

        filters = YearFilters.getForYear(year, **kwargs)

        # get all scores we want to include in our smart wins calculation
        teamIdsAndScores = list()

        allMatchups = YearNavigator.getAllSimplifiedMatchupsInYear(year, filters)

        for matchup in allMatchups:
            teamIdsAndScores.append((matchup.teamAId, matchup.teamBScore))
            teamIdsAndScores.append((matchup.teamBId, matchup.teamAScore))

        teamIdAndOpponentSmartWins = dict()
        allTeamIds = YearNavigator.getAllTeamIds(year)
        for teamId in allTeamIds:
            teamIdAndOpponentSmartWins[teamId] = Deci(0)

        allScores = YearNavigator.getAllScoresInYear(year, simplifyMultiWeekMatchups=True)
        for teamId, score in teamIdsAndScores:
            scoresBeat, scoresTied = getNumberOfScoresBeatAndTied(score, allScores)
            smartWins = (scoresBeat + (scoresTied / Deci("2"))) / (len(allScores) - Deci("1"))
            teamIdAndOpponentSmartWins[teamId] += smartWins

        cls._setToNoneIfNoGamesPlayed(teamIdAndOpponentSmartWins, year, filters, **kwargs)
        return teamIdAndOpponentSmartWins

    @classmethod
    @validateYear
    def getOpponentSmartWinsPerGame(cls, year: Year, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Returns the number of Smart Wins per game for each team's opponents in the given Year.
        Returns None for a Team if they have no games played in the range.

        Example response:
            {
            "someTeamId": Deci("8.7"),
            "someOtherTeamId": Deci("11.2"),
            "yetAnotherTeamId": Deci("7.1"),
            ...
            }
        """

        teamIdAndOpponentSmartWins = SmartWinsYearCalculator.getOpponentSmartWins(year, **kwargs)
        teamIdAndNumberOfGamesPlayed = YearNavigator.getNumberOfGamesPlayed(year, YearFilters.getForYear(year,
                                                                                                         **kwargs))

        teamIdAndOpponentSmartWinsPerGame = dict()
        allTeamIds = YearNavigator.getAllTeamIds(year)
        for teamId in allTeamIds:
            # to avoid division by zero, we'll just set the opponent Smart Wins per game to 0 if the team has no games played
            if teamIdAndNumberOfGamesPlayed[teamId] == 0:
                teamIdAndOpponentSmartWinsPerGame[teamId] = None
            else:
                teamIdAndOpponentSmartWinsPerGame[teamId] = teamIdAndOpponentSmartWins[teamId] / \
                                                            teamIdAndNumberOfGamesPlayed[teamId]

        return teamIdAndOpponentSmartWinsPerGame
