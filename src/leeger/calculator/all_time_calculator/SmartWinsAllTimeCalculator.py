from src.leeger.calculator.parent.AllTimeCalculator import AllTimeCalculator
from src.leeger.decorator.validate.validators import validateLeague
from src.leeger.model.league.League import League
from src.leeger.util.Deci import Deci
from src.leeger.util.LeagueNavigator import LeagueNavigator


class SmartWinsAllTimeCalculator(AllTimeCalculator):
    """
    Used to calculate all Smart Wins stats.
    """

    @classmethod
    @validateLeague
    def getSmartWins(cls, league: League, **kwargs) -> dict[str, Deci]:
        """
        Smart Wins show how many wins a team would have if it played against every score in a given collection.
        In this case, the collection is every score in the given League.
        Smart Wins = Σ((W + (T/2)) / S)
        WHERE:
        W = Total scores in the League beat
        T = Total scores in the League tied
        S = Number of scores in the League - 1

        Returns the number of Smart Wins for each Owner in the given League.

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
            ownerIdAndSmartWins[ownerId] = Deci(0)

        for ownerIdAndScore in ownerIdsAndScores:
            scoresBeat, scoresTied = getNumberOfScoresBeatAndTied(ownerIdAndScore[1], allScores)
            smartWins = (scoresBeat + (scoresTied / Deci(2))) / (len(allScores) - Deci(1))
            ownerIdAndSmartWins[ownerIdAndScore[0]] += smartWins

        return ownerIdAndSmartWins

    @classmethod
    @validateLeague
    def getSmartWinsPerGame(cls, league: League, **kwargs) -> dict[str, Deci]:
        """
        Returns the number of Smart Wins per game for each Owner in the given League.

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
            # to avoid division by zero, we'll just set the AWAL per game to 0 if the team has no games played
            if ownerIdAndNumberOfGamesPlayed[ownerId] == 0:
                ownerIdAndSmartWinsPerGame[ownerId] = Deci(0)
            else:
                ownerIdAndSmartWinsPerGame[ownerId] = ownerIdAndSmartWins[ownerId] / ownerIdAndNumberOfGamesPlayed[
                    ownerId]

        return ownerIdAndSmartWinsPerGame
