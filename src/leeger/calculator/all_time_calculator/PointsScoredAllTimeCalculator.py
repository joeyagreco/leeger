from src.leeger.calculator.parent.AllTimeCalculator import AllTimeCalculator
from src.leeger.calculator.year_calculator.PointsScoredYearCalculator import PointsScoredYearCalculator
from src.leeger.decorator.validate.validators import validateLeague
from src.leeger.model.league.League import League
from src.leeger.util.Deci import Deci
from src.leeger.util.LeagueNavigator import LeagueNavigator


class PointsScoredAllTimeCalculator(AllTimeCalculator):
    """
    Used to calculate all points scored.
    """

    @classmethod
    @validateLeague
    def getPointsScored(cls, league: League, **kwargs) -> dict[str, Deci]:
        """
        Returns the number of Points Scored for each Owner in the given League.

        Example response:
            {
            "someTeamId": Deci("1009.7"),
            "someOtherTeamId": Deci("1412.2"),
            "yetAnotherTeamId": Deci("1227.1"),
            ...
            }
        """
        return cls._addAndCombineResults(league, PointsScoredYearCalculator.getPointsScored, **kwargs)

    @classmethod
    @validateLeague
    def getPointsScoredPerGame(cls, league: League, **kwargs) -> dict[str, Deci]:
        """
        Returns the number of Points Scored per game for each Owner in the given League.

        Example response:
            {
            "someTeamId": Deci("100.7"),
            "someOtherTeamId": Deci("141.2"),
            "yetAnotherTeamId": Deci("122.1"),
            ...
            }
        """

        ownerIdAndPointsScored = cls.getPointsScored(league, **kwargs)
        ownerIdAndNumberOfGamesPlayed = LeagueNavigator.getNumberOfGamesPlayed(league,
                                                                               cls._getAllTimeFilters(league, **kwargs))

        ownerIdAndPointsScoredPerGame = dict()
        allOwnerIds = LeagueNavigator.getAllOwnerIds(league)
        for ownerId in allOwnerIds:
            # to avoid division by zero, we'll just set the Points Scored per game to 0 if the team has no games played
            if ownerIdAndNumberOfGamesPlayed[ownerId] == 0:
                ownerIdAndPointsScoredPerGame[ownerId] = Deci(0)
            else:
                ownerIdAndPointsScoredPerGame[ownerId] = ownerIdAndPointsScored[ownerId] / \
                                                         ownerIdAndNumberOfGamesPlayed[ownerId]

        return ownerIdAndPointsScoredPerGame
