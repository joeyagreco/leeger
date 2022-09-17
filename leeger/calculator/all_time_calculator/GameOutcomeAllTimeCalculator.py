from typing import Optional

from leeger.calculator.parent.AllTimeCalculator import AllTimeCalculator
from leeger.calculator.year_calculator.GameOutcomeYearCalculator import GameOutcomeYearCalculator
from leeger.decorator.validators import validateLeague
from leeger.model.filter import AllTimeFilters
from leeger.model.league.League import League
from leeger.util.Deci import Deci
from leeger.util.navigator.LeagueNavigator import LeagueNavigator


class GameOutcomeAllTimeCalculator(AllTimeCalculator):

    @classmethod
    @validateLeague
    def getWins(cls, league: League, **kwargs) -> dict[str, Optional[int]]:
        """
        Returns the number of wins for each team in the given League.
        Returns None for an Owner if they have no games played in the range.

        Example response:
            {
            "someOwnerId": 18,
            "someOtherOwnerId": 21,
            "yetAnotherOwnerId": 17,
            ...
            }
        """
        return cls._addAndCombineResults(league, GameOutcomeYearCalculator.getWins, **kwargs)

    @classmethod
    @validateLeague
    def getLosses(cls, league: League, **kwargs) -> dict[str, Optional[int]]:
        """
        Returns the number of losses for each team in the given League.
        Returns None for an Owner if they have no games played in the range.

        Example response:
            {
            "someOwnerId": 18,
            "someOtherOwnerId": 21,
            "yetAnotherOwnerId": 17,
            ...
            }
        """
        return cls._addAndCombineResults(league, GameOutcomeYearCalculator.getLosses, **kwargs)

    @classmethod
    @validateLeague
    def getTies(cls, league: League, **kwargs) -> dict[str, Optional[int]]:
        """
        Returns the number of ties for each team in the given League.
        Returns None for an Owner if they have no games played in the range.

        Example response:
            {
            "someOwnerId": 1,
            "someOtherOwnerId": 0,
            "yetAnotherOwnerId": 2,
            ...
            }
        """
        return cls._addAndCombineResults(league, GameOutcomeYearCalculator.getTies, **kwargs)

    @classmethod
    @validateLeague
    def getWinPercentage(cls, league: League, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Returns the win percentage for each team in the given League.
        Returns None for an Owner if they have no games played in the range.
        Win percentage will be represented as a non-rounded decimal.

        Example:
            33% win percentage -> Deci("0.3333333333333333333333333333")
            100% win percentage -> Deci("1.0")

        Example response:
            {
            "someOwnerId": Deci("0.85"),
            "someOtherOwnerId": Deci("0.1156"),
            "yetAnotherOwnerId": Deci("0.72"),
            ...
            }
        """
        ownerIdAndWinPercentage = dict()
        ownerIdAndWins = GameOutcomeAllTimeCalculator.getWins(league, **kwargs)
        ownerIdAndLosses = GameOutcomeAllTimeCalculator.getLosses(league, **kwargs)
        ownerIdAndTies = GameOutcomeAllTimeCalculator.getTies(league, **kwargs)

        for ownerId in [owner.id for owner in league.owners]:
            numberOfWins = ownerIdAndWins[ownerId]
            numberOfLosses = ownerIdAndLosses[ownerId]
            numberOfTies = ownerIdAndTies[ownerId]

            if None in (numberOfWins, numberOfLosses, numberOfTies):
                ownerIdAndWinPercentage[ownerId] = None
            else:
                numberOfGamesPlayed = numberOfWins + numberOfLosses + numberOfTies
                ownerIdAndWinPercentage[ownerId] = (Deci(numberOfWins) + (Deci("0.5") * Deci(numberOfTies))) / Deci(
                    numberOfGamesPlayed)

        return ownerIdAndWinPercentage

    @classmethod
    @validateLeague
    def getWAL(cls, league: League, **kwargs) -> dict[str, Optional[Deci]]:
        """
        WAL is "Wins Against the League"
        Formula: (Number of Wins * 1) + (Number of Ties * 0.5)

        Returns the number of Wins Against the League for each team in the given League.
        Returns None for an Owner if they have no games played in the range.

        Example response:
            {
            "someOwnerId": Deci("18.5"),
            "someOtherOwnerId": Deci("21.0"),
            "yetAnotherOwnerId": Deci("27.5"),
            ...
            }
        """

        ownerIdAndWAL = dict()
        ownerIdAndWins = GameOutcomeAllTimeCalculator.getWins(league, **kwargs)
        ownerIdAndTies = GameOutcomeAllTimeCalculator.getTies(league, **kwargs)

        for ownerId in [owner.id for owner in league.owners]:
            wins = ownerIdAndWins[ownerId]
            ties = ownerIdAndTies[ownerId]
            if None in (wins, ties):
                ownerIdAndWAL[ownerId] = None
            else:
                ownerIdAndWAL[ownerId] = Deci(wins) + (Deci("0.5") * Deci(ties))

        return ownerIdAndWAL

    @classmethod
    @validateLeague
    def getWALPerGame(cls, league: League, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Returns the number of Wins Against the League per game for each owner in the given League.
        Returns None for an Owner if they have no games played in the range.

        Example response:
            {
            "someOwnerId": Deci("0.7"),
            "someOtherOwnerId": Deci("0.29"),
            "yetAnotherOwnerId": Deci("0.48"),
            ...
            }
        """
        ownerIdAndWAL = cls.getWAL(league, **kwargs)
        ownerIdAndNumberOfGamesPlayed = LeagueNavigator.getNumberOfGamesPlayed(league,
                                                                               AllTimeFilters.getForLeague(league,
                                                                                                           **kwargs),
                                                                               countMultiWeekMatchupsAsOneGame=True)

        ownerIdAndWALPerGame = dict()
        allOwnerIds = LeagueNavigator.getAllOwnerIds(league)
        for ownerId in allOwnerIds:
            if ownerIdAndNumberOfGamesPlayed[ownerId] == 0:
                ownerIdAndWALPerGame[ownerId] = None
            else:
                ownerIdAndWALPerGame[ownerId] = ownerIdAndWAL[ownerId] / ownerIdAndNumberOfGamesPlayed[ownerId]

        return ownerIdAndWALPerGame
