from src.leeger.calculator.all_time_calculator.parent.YearCalculator import YearCalculator
from src.leeger.decorator.validate.validators import validateYear
from src.leeger.model.league.Year import Year
from src.leeger.util.Deci import Deci
from src.leeger.util.YearNavigator import YearNavigator


class SmartWinsCalculator(YearCalculator):
    """
    Used to calculate all Smart Wins stats.
    """

    @classmethod
    @validateYear
    def getSmartWins(cls, year: Year, **kwargs) -> dict[str, Deci]:
        """
        Smart Wins show how many wins a team would have if it played against every score in a given collection.
        In this case, the collection is every score in the given Year.
        Smart Wins = Σ((W + (T/2)) / S)
        WHERE:
        W = Total scores in the Year beat
        T = Total scores in the Year tied
        S = Number of scores in the Year - 1

        Returns the number of Smart Wins for each team in the given Year.

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

        filters = cls._getYearFilters(year, validateYear=False, **kwargs)

        teamIdsAndScores = list()

        for i in range(filters.weekNumberStart - 1, filters.weekNumberEnd):
            week = year.weeks[i]
            for matchup in week.matchups:
                if matchup.matchupType in filters.includeMatchupTypes:
                    teamIdsAndScores.append((matchup.teamAId, matchup.teamAScore))
                    teamIdsAndScores.append((matchup.teamBId, matchup.teamBScore))

        teamIdAndSmartWins = dict()
        allTeamIds = YearNavigator.getAllTeamIds(year)
        for teamId in allTeamIds:
            teamIdAndSmartWins[teamId] = Deci(0)

        allScores = [teamIdAndScore[1] for teamIdAndScore in teamIdsAndScores]
        for teamIdAndScore in teamIdsAndScores:
            scoresBeat, scoresTied = getNumberOfScoresBeatAndTied(teamIdAndScore[1], allScores)
            smartWins = (scoresBeat + (scoresTied / Deci(2))) / (len(allScores) - Deci(1))
            teamIdAndSmartWins[teamIdAndScore[0]] += smartWins

        return teamIdAndSmartWins

    @classmethod
    @validateYear
    def getSmartWinsPerGame(cls, year: Year, **kwargs) -> dict[str, Deci]:
        """
        Returns the number of Smart Wins per game for each team in the given Year.

        Example response:
            {
            "someTeamId": Deci("8.7"),
            "someOtherTeamId": Deci("11.2"),
            "yetAnotherTeamId": Deci("7.1"),
            ...
            }
        """

        teamIdAndSmartWins = SmartWinsCalculator.getSmartWins(year, **kwargs)
        teamIdAndNumberOfGamesPlayed = YearNavigator.getNumberOfGamesPlayed(year,
                                                                            cls._getYearFilters(year,
                                                                                                **kwargs))

        teamIdAndSmartWinsPerGame = dict()
        allTeamIds = YearNavigator.getAllTeamIds(year)
        for teamId in allTeamIds:
            # to avoid division by zero, we'll just set the Smart Wins per game to 0 if the team has no games played
            if teamIdAndNumberOfGamesPlayed[teamId] == 0:
                teamIdAndSmartWinsPerGame[teamId] = Deci(0)
            else:
                teamIdAndSmartWinsPerGame[teamId] = teamIdAndSmartWins[teamId] / teamIdAndNumberOfGamesPlayed[teamId]

        return teamIdAndSmartWinsPerGame

    @classmethod
    @validateYear
    def getOpponentSmartWins(cls, year: Year, **kwargs) -> dict[str, Deci]:
        """
        Returns the number of Smart Wins for each team's opponents in the given Year.

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

        filters = cls._getYearFilters(year, validateYear=False, **kwargs)

        teamIdsAndOpponentScores = list()

        for i in range(filters.weekNumberStart - 1, filters.weekNumberEnd):
            week = year.weeks[i]
            for matchup in week.matchups:
                if matchup.matchupType in filters.includeMatchupTypes:
                    teamIdsAndOpponentScores.append((matchup.teamAId, matchup.teamBScore))
                    teamIdsAndOpponentScores.append((matchup.teamBId, matchup.teamAScore))

        teamIdAndOpponentSmartWins = dict()
        allTeamIds = YearNavigator.getAllTeamIds(year)
        for teamId in allTeamIds:
            teamIdAndOpponentSmartWins[teamId] = Deci(0)

        allScores = [teamIdAndScore[1] for teamIdAndScore in teamIdsAndOpponentScores]
        for teamIdAndScore in teamIdsAndOpponentScores:
            scoresBeat, scoresTied = getNumberOfScoresBeatAndTied(teamIdAndScore[1], allScores)
            smartWins = (scoresBeat + (scoresTied / Deci(2))) / (len(allScores) - Deci(1))
            teamIdAndOpponentSmartWins[teamIdAndScore[0]] += smartWins

        return teamIdAndOpponentSmartWins

    @classmethod
    @validateYear
    def getOpponentSmartWinsPerGame(cls, year: Year, **kwargs) -> dict[str, Deci]:
        """
        Returns the number of Smart Wins per game for each team's opponents in the given Year.

        Example response:
            {
            "someTeamId": Deci("8.7"),
            "someOtherTeamId": Deci("11.2"),
            "yetAnotherTeamId": Deci("7.1"),
            ...
            }
        """

        teamIdAndOpponentSmartWins = SmartWinsCalculator.getOpponentSmartWins(year, **kwargs)
        teamIdAndNumberOfGamesPlayed = YearNavigator.getNumberOfGamesPlayed(year,
                                                                            cls._getYearFilters(year,
                                                                                                **kwargs))

        teamIdAndOpponentSmartWinsPerGame = dict()
        allTeamIds = YearNavigator.getAllTeamIds(year)
        for teamId in allTeamIds:
            # to avoid division by zero, we'll just set the opponent Smart Wins per game to 0 if the team has no games played
            if teamIdAndNumberOfGamesPlayed[teamId] == 0:
                teamIdAndOpponentSmartWinsPerGame[teamId] = Deci(0)
            else:
                teamIdAndOpponentSmartWinsPerGame[teamId] = teamIdAndOpponentSmartWins[teamId] / \
                                                            teamIdAndNumberOfGamesPlayed[teamId]

        return teamIdAndOpponentSmartWinsPerGame
