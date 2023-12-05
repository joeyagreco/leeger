from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from leeger.enum.MatchupType import MatchupType
from leeger.exception import InvalidMatchupFormatException
from leeger.model.abstract.EqualityCheck import EqualityCheck
from leeger.model.abstract.UniqueId import UniqueId
from leeger.util.CustomLogger import CustomLogger
from leeger.util.equality import modelEquals
from leeger.util.JSONSerializable import JSONSerializable


@dataclass(kw_only=True, eq=False)
class Performance(UniqueId, EqualityCheck, JSONSerializable):
    __LOGGER = CustomLogger.getLogger()
    teamId: str
    teamScore: float | int
    hasTiebreaker: bool = False
    matchupType: MatchupType = MatchupType.REGULAR_SEASON
    # This is used to link matchups that span over multiple weeks
    multiWeekMatchupId: Optional[str] = None

    def equals(
        self,
        otherPerformance: Performance,
        *,
        ignoreIds: bool = False,
        ignoreBaseIds: bool = False,
        logDifferences: bool = False,
    ) -> bool:
        """
        Checks if *this* Performance is the same as the given Performance.
        """

        return modelEquals(
            objA=self,
            objB=otherPerformance,
            baseFields={"teamId", "teamScore", "hasTiebreaker", "matchupType"},
            idFields={"multiWeekMatchupId"},
            parentKey="Performance",
            ignoreIdFields=ignoreIds,
            ignoreBaseIdField=ignoreBaseIds,
            logDifferences=logDifferences,
        )

    def __eq__(self, otherPerformance: Performance) -> bool:
        self.__LOGGER.info("Use .equals() for more options when comparing Performance instances.")
        return self.equals(otherPerformance=otherPerformance)

    def __add__(self, otherPerformance: Performance):
        """
        Adds 2 Performances together.

        Returns:
            leeger.model.league.Matchup
        """
        from leeger.model.league import Matchup
        from leeger.validate import matchupValidation

        if self.matchupType != otherPerformance.matchupType:
            raise InvalidMatchupFormatException(
                f"Cannot make a matchup from conflicting matchup types '{self.matchupType}' and '{otherPerformance.matchupType}'."
            )
        if self.multiWeekMatchupId != otherPerformance.multiWeekMatchupId:
            raise InvalidMatchupFormatException(
                f"Cannot make a matchup from conflicting multi-week matchup IDs '{self.multiWeekMatchupId}' and '{otherPerformance.multiWeekMatchupId}'."
            )
        tiebreakerInfoLost = list()
        if self.hasTiebreaker:
            tiebreakerInfoLost.append(f"Performance {self.id} had tiebreaker")
        if otherPerformance.hasTiebreaker:
            tiebreakerInfoLost.append(f"Performance {otherPerformance.id} had tiebreaker")
        if tiebreakerInfoLost:
            self.__LOGGER.warning(
                f"Combining performances caused loss of tiebreakers: {tiebreakerInfoLost}."
            )
        matchup = Matchup(
            teamAId=self.teamId,
            teamBId=otherPerformance.teamId,
            teamAScore=self.teamScore,
            teamBScore=otherPerformance.teamScore,
            matchupType=self.matchupType,
            multiWeekMatchupId=self.multiWeekMatchupId,
        )
        # validate new matchup
        matchupValidation.runAllChecks(matchup)
        return matchup

    def toJson(self) -> dict:
        return {
            "id": self.id,
            "teamId": self.teamId,
            "teamScore": self.teamScore,
            "hasTiebreaker": self.hasTiebreaker,
            "matchupType": self.matchupType.name,
            "multiWeekMatchupId": self.multiWeekMatchupId,
        }
