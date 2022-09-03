from typing import Optional

from leeger.calculator.parent.AllTimeCalculator import AllTimeCalculator
from leeger.calculator.year_calculator.PointsScoredYearCalculator import PointsScoredYearCalculator
from leeger.decorator.validators import validateLeague
from leeger.model.league.League import League
from leeger.util.Deci import Deci
from leeger.util.navigator.LeagueNavigator import LeagueNavigator


class PointsScoredAllTimeCalculator(AllTimeCalculator):
    """
    Used to calculate all points scored.
    """

    @classmethod
    @validateLeague
    def getPointsScored(cls, league: League, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Returns the number of Points Scored for each Owner in the given League.
        Returns None for an Owner if they have no games played in the range.

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
    def getPointsScoredPerGame(cls, league: League, **kwargs) -> dict[str, Optional[Deci]]:
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
            if ownerIdAndNumberOfGamesPlayed[ownerId] == 0:
                ownerIdAndPointsScoredPerGame[ownerId] = None
            else:
                ownerIdAndPointsScoredPerGame[ownerId] = ownerIdAndPointsScored[ownerId] / \
                                                         ownerIdAndNumberOfGamesPlayed[ownerId]

        return ownerIdAndPointsScoredPerGame

    @classmethod
    @validateLeague
    def getOpponentPointsScored(cls, league: League, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Returns the number of Points Scored for each Owner's opponent in the given League.
        Returns None for an Owner if they have no games played in the range.

        Example response:
            {
            "someTeamId": Deci("1009.7"),
            "someOtherTeamId": Deci("1412.2"),
            "yetAnotherTeamId": Deci("1227.1"),
            ...
            }
        """
        return cls._addAndCombineResults(league, PointsScoredYearCalculator.getOpponentPointsScored, **kwargs)

    @classmethod
    @validateLeague
    def getOpponentPointsScoredPerGame(cls, league: League, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Returns the number of Points Scored per game for each Owner's opponent in the given League.
        Returns None for an Owner if they have no games played in the range.

        Example response:
            {
            "someTeamId": Deci("100.7"),
            "someOtherTeamId": Deci("141.2"),
            "yetAnotherTeamId": Deci("122.1"),
            ...
            }
        """

        ownerIdAndOpponentPointsScored = cls.getOpponentPointsScored(league, **kwargs)
        ownerIdAndNumberOfGamesPlayed = LeagueNavigator.getNumberOfGamesPlayed(league,
                                                                               cls._getAllTimeFilters(league, **kwargs))

        ownerIdAndOpponentPointsScoredPerGame = dict()
        allOwnerIds = LeagueNavigator.getAllOwnerIds(league)
        for ownerId in allOwnerIds:
            if ownerIdAndNumberOfGamesPlayed[ownerId] == 0:
                ownerIdAndOpponentPointsScoredPerGame[ownerId] = None
            else:
                ownerIdAndOpponentPointsScoredPerGame[ownerId] = ownerIdAndOpponentPointsScored[ownerId] / \
                                                                 ownerIdAndNumberOfGamesPlayed[ownerId]

        return ownerIdAndOpponentPointsScoredPerGame
