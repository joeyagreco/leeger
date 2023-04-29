from typing import Optional

from leeger.calculator.all_time_calculator.PointsScoredAllTimeCalculator import (
    PointsScoredAllTimeCalculator,
)
from leeger.calculator.parent.AllTimeCalculator import AllTimeCalculator
from leeger.calculator.year_calculator import ScoringShareYearCalculator
from leeger.decorator.validators import validateLeague
from leeger.model.league.League import League
from leeger.util.Deci import Deci
from leeger.util.GeneralUtil import GeneralUtil
from leeger.util.navigator.LeagueNavigator import LeagueNavigator


class ScoringShareAllTimeCalculator(AllTimeCalculator):
    """
    Used to calculate all scoring shares.
    """

    @classmethod
    @validateLeague
    def getScoringShare(cls, league: League, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Scoring Share is used to show what percentage of league scoring a team was responsible for.

        Scoring Share = ((ΣA) / (ΣB)) * 100
        WHERE:
        A = All scores by an Owner in a League
        B = All scores by all Owners in a League

        Returns the Scoring Share for each Owner in the given League.
        Returns None for an Owner if they have no games played in the range.

        Example response:
            {
            "someOwnerId": Deci("10.7"),
            "someOtherOwnerId": Deci("14.2"),
            "yetAnotherOwnerId": Deci("12.1"),
            ...
            }
        """

        ownerIdAndPointsScored = PointsScoredAllTimeCalculator.getPointsScored(league, **kwargs)
        allScores = GeneralUtil.filter(value=None, list_=ownerIdAndPointsScored.values())
        totalPointsScoredInLeague = sum(allScores)
        ownerIdAndScoringShare = dict()
        for ownerId in LeagueNavigator.getAllOwnerIds(league):
            if len(allScores) == 0 or ownerIdAndPointsScored[ownerId] is None:
                ownerIdAndScoringShare[ownerId] = None
            else:
                # avoid division by 0
                if totalPointsScoredInLeague == 0:
                    ownerIdAndScoringShare[ownerId] = Deci("0")
                else:
                    ownerIdAndScoringShare[ownerId] = (
                        ownerIdAndPointsScored[ownerId] / totalPointsScoredInLeague
                    ) * Deci("100")

        return ownerIdAndScoringShare

    @classmethod
    @validateLeague
    def getOpponentScoringShare(cls, league: League, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Returns the Scoring Share for each Owner's opponent in the given League.
        Returns None for an Owner if they have no games played in the range.

        Example response:
            {
            "someOwnerId": Deci("10.7"),
            "someOtherOwnerId": Deci("14.2"),
            "yetAnotherOwnerId": Deci("12.1"),
            ...
            }
        """

        ownerIdAndOpponentPointsScored = PointsScoredAllTimeCalculator.getOpponentPointsScored(
            league, **kwargs
        )
        allScores = GeneralUtil.filter(value=None, list_=ownerIdAndOpponentPointsScored.values())
        totalPointsScoredInLeague = sum(allScores)
        ownerIdAndOpponentScoringShare = dict()
        for ownerId in LeagueNavigator.getAllOwnerIds(league):
            if len(allScores) == 0 or ownerIdAndOpponentPointsScored[ownerId] is None:
                ownerIdAndOpponentScoringShare[ownerId] = None
            else:
                # avoid division by 0
                if totalPointsScoredInLeague == 0:
                    ownerIdAndOpponentScoringShare[ownerId] = Deci("0")
                else:
                    ownerIdAndOpponentScoringShare[ownerId] = (
                        ownerIdAndOpponentPointsScored[ownerId] / totalPointsScoredInLeague
                    ) * Deci("100")

        return ownerIdAndOpponentScoringShare

    @classmethod
    @validateLeague
    def getMaxScoringShare(cls, league: League, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Returns the Max Scoring Share for each Owner in the given League.
        Returns None for an Owner if they have no games played in the range.

        Example response:
            {
            "someOwnerId": Deci("10.7"),
            "someOtherOwnerId": Deci("14.2"),
            "yetAnotherOwnerId": Deci("12.1"),
            ...
            }
        """

        ownerIdAndMaxScoringShare = dict()

        allOwnerIds = LeagueNavigator.getAllOwnerIds(league)

        for ownerId in allOwnerIds:
            ownerIdAndMaxScoringShare[ownerId] = None

        maxScoringSharesByYearTeamIds = cls._getAllResultDictsByYear(
            league, ScoringShareYearCalculator.getMaxScoringShare, **kwargs
        )
        # swap out team IDs for owner IDs
        maxScoringSharesByYear = dict()
        for (yearNumber, maxScoringSharesByTeamId) in maxScoringSharesByYearTeamIds.items():
            maxScoringSharesByYear[yearNumber] = dict()
            for teamId, maxScoringShare in maxScoringSharesByTeamId.items():
                ownerId = LeagueNavigator.getTeamById(league, teamId).ownerId
                maxScoringSharesByYear[yearNumber][ownerId] = maxScoringShare

        ownerIdAndMaxScoringShares: dict[str, list] = dict()
        for yearNumber in maxScoringSharesByYear.keys():
            for ownerId in allOwnerIds:
                if (
                    ownerId in ownerIdAndMaxScoringShares.keys()
                    and ownerIdAndMaxScoringShares[ownerId] is not None
                ):
                    ownerIdAndMaxScoringShares[ownerId].append(
                        maxScoringSharesByYear[yearNumber][ownerId]
                    )
                else:
                    ownerIdAndMaxScoringShares[ownerId] = [
                        maxScoringSharesByYear[yearNumber][ownerId]
                    ]

        for ownerId in allOwnerIds:
            # remove all None values from list
            ownerIdAndMaxScoringShares[ownerId] = [
                i for i in ownerIdAndMaxScoringShares[ownerId] if i is not None
            ]
            if len(ownerIdAndMaxScoringShares[ownerId]) > 0:
                ownerIdAndMaxScoringShare[ownerId] = max(ownerIdAndMaxScoringShares[ownerId])
            else:
                ownerIdAndMaxScoringShare[ownerId] = None

        return ownerIdAndMaxScoringShare

    @classmethod
    @validateLeague
    def getMinScoringShare(cls, league: League, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Returns the Min Scoring Share for each Owner in the given League.
        Returns None for an Owner if they have no games played in the range.

        Example response:
            {
            "someOwnerId": Deci("10.7"),
            "someOtherOwnerId": Deci("14.2"),
            "yetAnotherOwnerId": Deci("12.1"),
            ...
            }
        """

        ownerIdAndMinScoringShare = dict()

        allOwnerIds = LeagueNavigator.getAllOwnerIds(league)

        for ownerId in allOwnerIds:
            ownerIdAndMinScoringShare[ownerId] = None

        minScoringSharesByYearTeamIds = cls._getAllResultDictsByYear(
            league, ScoringShareYearCalculator.getMinScoringShare, **kwargs
        )
        # swap out team IDs for owner IDs
        minScoringSharesByYear = dict()
        for (yearNumber, minScoringSharesByTeamId) in minScoringSharesByYearTeamIds.items():
            minScoringSharesByYear[yearNumber] = dict()
            for teamId, maxScoringShare in minScoringSharesByTeamId.items():
                ownerId = LeagueNavigator.getTeamById(league, teamId).ownerId
                minScoringSharesByYear[yearNumber][ownerId] = maxScoringShare

        ownerIdAndMinScoringShares: dict[str, list] = dict()
        for yearNumber in minScoringSharesByYear.keys():
            for ownerId in allOwnerIds:
                if (
                    ownerId in ownerIdAndMinScoringShares.keys()
                    and ownerIdAndMinScoringShares[ownerId] is not None
                ):
                    ownerIdAndMinScoringShares[ownerId].append(
                        minScoringSharesByYear[yearNumber][ownerId]
                    )
                else:
                    ownerIdAndMinScoringShares[ownerId] = [
                        minScoringSharesByYear[yearNumber][ownerId]
                    ]

        for ownerId in allOwnerIds:
            # remove all None values from list
            ownerIdAndMinScoringShares[ownerId] = [
                i for i in ownerIdAndMinScoringShares[ownerId] if i is not None
            ]
            if len(ownerIdAndMinScoringShares[ownerId]) > 0:
                ownerIdAndMinScoringShare[ownerId] = min(ownerIdAndMinScoringShares[ownerId])
            else:
                ownerIdAndMinScoringShare[ownerId] = None

        return ownerIdAndMinScoringShare
