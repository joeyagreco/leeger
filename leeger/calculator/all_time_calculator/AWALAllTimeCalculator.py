from typing import Optional

from leeger.calculator.parent.AllTimeCalculator import AllTimeCalculator
from leeger.calculator.year_calculator.AWALYearCalculator import AWALYearCalculator
from leeger.decorator.validators import validateLeague
from leeger.model.filter import AllTimeFilters
from leeger.model.league.League import League
from leeger.util.Deci import Deci
from leeger.util.navigator.LeagueNavigator import LeagueNavigator


class AWALAllTimeCalculator(AllTimeCalculator):
    """
    Used to calculate all AWAL stats.
    """

    @classmethod
    @validateLeague
    def getAWAL(cls, league: League, **kwargs) -> dict[str, Optional[Deci]]:
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

        Returns the number of Adjusted Wins Against the League for each Owner in the given League.
        Returns None for an Owner if they have no games played in the range.

        Example response:
            {
            "someOwnerId": Deci("18.7"),
            "someOtherOwnerId": Deci("21.2"),
            "yetAnotherOwnerId": Deci("17.1"),
            ...
            }
        """
        return cls._addAndCombineResults(league, AWALYearCalculator.getAWAL, **kwargs)

    @classmethod
    @validateLeague
    def getAWALPerGame(cls, league: League, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Returns the number of Adjusted Wins Against the League per game for each Owner in the given League.
        Returns None for an Owner if they have no games played in the range.

        Example response:
            {
            "someOwnerId": Deci("0.7"),
            "someOtherOwnerId": Deci("0.2"),
            "yetAnotherOwnerId": Deci("0.1"),
            ...
            }
        """

        ownerIdAndAWAL = cls.getAWAL(league, **kwargs)
        ownerIdAndNumberOfGamesPlayed = LeagueNavigator.getNumberOfGamesPlayed(league,
                                                                               AllTimeFilters.getForLeague(league,
                                                                                                           **kwargs),
                                                                               countLeagueMedianGamesAsTwoGames=True)

        ownerIdAndAWALPerGame = dict()
        allOwnerIds = LeagueNavigator.getAllOwnerIds(league)
        for ownerId in allOwnerIds:
            if ownerIdAndNumberOfGamesPlayed[ownerId] == 0:
                ownerIdAndAWALPerGame[ownerId] = None
            else:
                ownerIdAndAWALPerGame[ownerId] = ownerIdAndAWAL[ownerId] / ownerIdAndNumberOfGamesPlayed[ownerId]

        return ownerIdAndAWALPerGame

    @classmethod
    @validateLeague
    def getOpponentAWAL(cls, league: League, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Returns the number of Adjusted Wins Against the League for each Owner's opponents in the given League.
        Returns None for an Owner if they have no games played in the range.

        Example response:
            {
            "someOwnerId": Deci("18.7"),
            "someOtherOwnerId": Deci("21.2"),
            "yetAnotherOwnerId": Deci("17.1"),
            ...
            }
        """
        return cls._addAndCombineResults(league, AWALYearCalculator.getOpponentAWAL, **kwargs)

    @classmethod
    @validateLeague
    def getOpponentAWALPerGame(cls, league: League, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Returns the number of Adjusted Wins Against the League per game for each Owner's opponent in the given League.
        Returns None for an Owner if they have no games played in the range.

        Example response:
            {
            "someOwnerId": Deci("0.7"),
            "someOtherOwnerId": Deci("0.2"),
            "yetAnotherOwnerId": Deci("0.1"),
            ...
            }
        """

        ownerIdAndOpponentAWAL = cls.getOpponentAWAL(league, **kwargs)
        ownerIdAndNumberOfGamesPlayed = LeagueNavigator.getNumberOfGamesPlayed(league,
                                                                               AllTimeFilters.getForLeague(league,
                                                                                                           **kwargs),
                                                                               countLeagueMedianGamesAsTwoGames=True)

        ownerIdAndOpponentAWALPerGame = dict()
        allOwnerIds = LeagueNavigator.getAllOwnerIds(league)
        for ownerId in allOwnerIds:
            if ownerIdAndNumberOfGamesPlayed[ownerId] == 0:
                ownerIdAndOpponentAWALPerGame[ownerId] = None
            else:
                ownerIdAndOpponentAWALPerGame[ownerId] = ownerIdAndOpponentAWAL[ownerId] / \
                                                         ownerIdAndNumberOfGamesPlayed[ownerId]

        return ownerIdAndOpponentAWALPerGame
