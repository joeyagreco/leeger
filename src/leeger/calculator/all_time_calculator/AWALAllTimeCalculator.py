from src.leeger.calculator.parent.AllTimeCalculator import AllTimeCalculator
from src.leeger.calculator.year_calculator.AWALYearCalculator import AWALYearCalculator
from src.leeger.decorator.validate.validators import validateLeague
from src.leeger.model.league.League import League
from src.leeger.util.Deci import Deci
from src.leeger.util.LeagueNavigator import LeagueNavigator


class AWALAllTimeCalculator(AllTimeCalculator):
    """
    Used to calculate all AWAL stats.
    """

    @classmethod
    @validateLeague
    def getAWAL(cls, league: League, **kwargs) -> dict[str, Deci]:
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
    def getAWALPerGame(cls, league: League, **kwargs) -> dict[str, Deci]:
        """
        Returns the number of Adjusted Wins Against the League per game for each team in the given League.

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
                                                                               cls._getAllTimeFilters(league, **kwargs))

        ownerIdAndAWALPerGame = dict()
        allOwnerIds = LeagueNavigator.getAllOwnerIds(league)
        for ownerId in allOwnerIds:
            # to avoid division by zero, we'll just set the AWAL per game to 0 if the team has no games played
            if ownerIdAndNumberOfGamesPlayed[ownerId] == 0:
                ownerIdAndAWALPerGame[ownerId] = Deci(0)
            else:
                ownerIdAndAWALPerGame[ownerId] = ownerIdAndAWAL[ownerId] / ownerIdAndNumberOfGamesPlayed[ownerId]

        return ownerIdAndAWALPerGame

    @classmethod
    @validateLeague
    def getOpponentAWAL(cls, league: League, **kwargs) -> dict[str, Deci]:
        """
        Returns the number of Adjusted Wins Against the League for each Owner's opponents in the given League.

        Example response:
            {
            "someOwnerId": Deci("18.7"),
            "someOtherOwnerId": Deci("21.2"),
            "yetAnotherOwnerId": Deci("17.1"),
            ...
            }
        """
        return cls._addAndCombineResults(league, AWALYearCalculator.getOpponentAWAL, **kwargs)
