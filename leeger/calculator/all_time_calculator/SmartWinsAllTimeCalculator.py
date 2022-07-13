from typing import Optional

from leeger.calculator.parent.AllTimeCalculator import AllTimeCalculator
from leeger.decorator.validate.validators import validateLeague
from leeger.model.league.League import League
from leeger.util.Deci import Deci
from leeger.util.LeagueNavigator import LeagueNavigator


class SmartWinsAllTimeCalculator(AllTimeCalculator):
    """
    Used to calculate all Smart Wins stats.
    """

    @classmethod
    @validateLeague
    def getSmartWins(cls, league: League, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Smart Wins show how many wins a team would have if it played against every score in a given collection.
        In this case, the collection is every score in the given League.

        Smart Wins = Σ((W + (T/2)) / S)
        WHERE:
        W = Total scores in the League beat
        T = Total scores in the League tied
        S = Number of scores in the League - 1

        Returns the number of Smart Wins for each Owner in the given League.
        Returns None for an Owner if they have no games played in the range.

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

        filters = cls._getAllTimeFilters(league, validateLeague=False, **kwargs)

        # get all scores we want to include in our smart wins calculation
        ownerIdsAndScores: list[tuple] = list()

        for matchup in cls._getAllFilteredMatchups(league, filters):
            teamA = LeagueNavigator.getTeamById(league, matchup.teamAId)
            teamB = LeagueNavigator.getTeamById(league, matchup.teamBId)
            ownerIdsAndScores.append((teamA.ownerId, matchup.teamAScore))
            ownerIdsAndScores.append((teamB.ownerId, matchup.teamBScore))

        allScores = LeagueNavigator.getAllScoresInLeague(league)
        ownerIdAndSmartWins = dict()
        allOwnerIds = LeagueNavigator.getAllOwnerIds(league)
        for ownerId in allOwnerIds:
            ownerIdAndSmartWins[ownerId] = None

        for ownerIdAndScore in ownerIdsAndScores:
            scoresBeat, scoresTied = getNumberOfScoresBeatAndTied(ownerIdAndScore[1], allScores)
            smartWins = (scoresBeat + (scoresTied / Deci(2))) / (len(allScores) - Deci(1))
            if ownerIdAndSmartWins[ownerIdAndScore[0]] is None:
                ownerIdAndSmartWins[ownerIdAndScore[0]] = smartWins
            else:
                ownerIdAndSmartWins[ownerIdAndScore[0]] += smartWins

        return ownerIdAndSmartWins

    @classmethod
    @validateLeague
    def getSmartWinsPerGame(cls, league: League, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Returns the number of Smart Wins per game for each Owner in the given League.
        Returns None for an Owner if they have no games played in the range.

        Example response:
            {
            "someTeamId": Deci("0.7"),
            "someOtherTeamId": Deci("0.2"),
            "yetAnotherTeamId": Deci("0.1"),
            ...
            }
        """

        ownerIdAndSmartWins = cls.getSmartWins(league, **kwargs)
        ownerIdAndNumberOfGamesPlayed = LeagueNavigator.getNumberOfGamesPlayed(league,
                                                                               cls._getAllTimeFilters(league, **kwargs))

        ownerIdAndSmartWinsPerGame = dict()
        allOwnerIds = LeagueNavigator.getAllOwnerIds(league)
        for ownerId in allOwnerIds:
            if ownerIdAndNumberOfGamesPlayed[ownerId] == 0:
                ownerIdAndSmartWinsPerGame[ownerId] = None
            else:
                ownerIdAndSmartWinsPerGame[ownerId] = ownerIdAndSmartWins[ownerId] / ownerIdAndNumberOfGamesPlayed[
                    ownerId]

        return ownerIdAndSmartWinsPerGame

    @classmethod
    @validateLeague
    def getOpponentSmartWins(cls, league: League, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Returns the number of Smart Wins for each Owner's opponent in the given League.
        Returns None for an Owner if they have no games played in the range.

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

        filters = cls._getAllTimeFilters(league, validateLeague=False, **kwargs)

        # get all scores we want to include in our smart wins calculation
        ownerIdsAndOpponentScores: list[tuple] = list()

        for matchup in cls._getAllFilteredMatchups(league, filters):
            teamA = LeagueNavigator.getTeamById(league, matchup.teamAId)
            teamB = LeagueNavigator.getTeamById(league, matchup.teamBId)
            ownerIdsAndOpponentScores.append((teamA.ownerId, matchup.teamBScore))
            ownerIdsAndOpponentScores.append((teamB.ownerId, matchup.teamAScore))

        allScores = LeagueNavigator.getAllScoresInLeague(league)
        ownerIdAndOpponentSmartWins = dict()
        allOwnerIds = LeagueNavigator.getAllOwnerIds(league)
        for ownerId in allOwnerIds:
            ownerIdAndOpponentSmartWins[ownerId] = None

        for ownerIdAndOpponentScore in ownerIdsAndOpponentScores:
            scoresBeat, scoresTied = getNumberOfScoresBeatAndTied(ownerIdAndOpponentScore[1], allScores)
            smartWins = (scoresBeat + (scoresTied / Deci(2))) / (len(allScores) - Deci(1))
            if ownerIdAndOpponentSmartWins[ownerIdAndOpponentScore[0]] is None:
                ownerIdAndOpponentSmartWins[ownerIdAndOpponentScore[0]] = smartWins
            else:
                ownerIdAndOpponentSmartWins[ownerIdAndOpponentScore[0]] += smartWins

        return ownerIdAndOpponentSmartWins

    @classmethod
    @validateLeague
    def getOpponentSmartWinsPerGame(cls, league: League, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Returns the number of Smart Wins per game for each Owner's opponent in the given League.
        Returns None for an Owner if they have no games played in the range.

        Example response:
            {
            "someTeamId": Deci("0.7"),
            "someOtherTeamId": Deci("0.2"),
            "yetAnotherTeamId": Deci("0.1"),
            ...
            }
        """

        ownerIdAndOpponentSmartWins = cls.getOpponentSmartWins(league, **kwargs)
        ownerIdAndNumberOfGamesPlayed = LeagueNavigator.getNumberOfGamesPlayed(league,
                                                                               cls._getAllTimeFilters(league, **kwargs))

        ownerIdAndOpponentSmartWinsPerGame = dict()
        allOwnerIds = LeagueNavigator.getAllOwnerIds(league)
        for ownerId in allOwnerIds:
            if ownerIdAndNumberOfGamesPlayed[ownerId] == 0:
                ownerIdAndOpponentSmartWinsPerGame[ownerId] = None
            else:
                ownerIdAndOpponentSmartWinsPerGame[ownerId] = ownerIdAndOpponentSmartWins[ownerId] / \
                                                              ownerIdAndNumberOfGamesPlayed[
                                                                  ownerId]

        return ownerIdAndOpponentSmartWinsPerGame
