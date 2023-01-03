from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from leeger.enum.MatchupType import MatchupType
from leeger.exception import InvalidMatchupFormatException
from leeger.model.abstract.UniqueId import UniqueId
from leeger.model.league import Matchup
from leeger.util.CustomLogger import CustomLogger
from leeger.util.JSONSerializable import JSONSerializable


@dataclass(kw_only=True, eq=False)
class Performance(UniqueId, JSONSerializable):
    __LOGGER = CustomLogger.getLogger()
    teamId: str
    teamScore: float | int
    hasTiebreaker: bool = False
    matchupType: MatchupType = MatchupType.REGULAR_SEASON
    multiWeekMatchupId: Optional[str] = None  # This is used to link matchups that span over multiple weeks

    def __eq__(self, otherPerformance: Performance) -> bool:
        """
        Checks if *this* Performance is the same as the given Performance.
        Does not check for equality of IDs, just values.
        """
        equal = self.teamScore == otherPerformance.teamScore
        equal = equal and self.hasTiebreaker == otherPerformance.hasTiebreaker
        equal = equal and self.matchupType == otherPerformance.matchupType
        # warn if this is going to return True but ID based fields are not equal
        if equal:
            notEqualStrings = list()
            if self.teamId != otherPerformance.teamId:
                notEqualStrings.append("teamId")
            if len(notEqualStrings) > 0:
                self.__LOGGER.warning(f"Returning True for equality check when {notEqualStrings} are not equal.")
        return equal

    def __add__(self, otherPerformance: Performance) -> Matchup:
        """
        Adding 2 Performances together will give you a Matchup.
        """
        if self.matchupType != otherPerformance.matchupType:
            raise InvalidMatchupFormatException(
                f"Cannot make a matchup from conflicting matchup types '{self.matchupType}' and '{otherPerformance.matchupType}'")
        if self.multiWeekMatchupId != otherPerformance.multiWeekMatchupId:
            raise InvalidMatchupFormatException(
                f"Cannot make a matchup from conflicting multi-week matchup IDs '{self.multiWeekMatchupId}' and '{otherPerformance.multiWeekMatchupId}'")
        tiebreakerInfoLost = list()
        if self.hasTiebreaker:
            tiebreakerInfoLost.append(f"Performance {self.id} had tiebreaker")
        if otherPerformance.hasTiebreaker:
            tiebreakerInfoLost.append(f"Performance {otherPerformance.id} had tiebreaker")
        if tiebreakerInfoLost:
            self.__LOGGER.warning(f"Combining performances caused loss of tiebreakers: {tiebreakerInfoLost}")
        return Matchup(teamAId=self.teamId,
                       teamBId=otherPerformance.teamId,
                       teamAScore=self.teamScore,
                       teamBScore=otherPerformance.teamScore,
                       matchupType=self.matchupType,
                       multiWeekMatchupId=self.multiWeekMatchupId)

    def toJson(self) -> dict:
        return {
            "id": self.id,
            "teamId": self.teamId,
            "teamScore": self.teamScore,
            "hasTiebreaker": self.hasTiebreaker,
            "matchupType": self.matchupType.name,
            "multiWeekMatchupId": self.multiWeekMatchupId
        }
