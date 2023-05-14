from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from leeger.enum.MatchupType import MatchupType
from leeger.exception import DoesNotExistException
from leeger.exception.InvalidMatchupFormatException import InvalidMatchupFormatException
from leeger.model.abstract.UniqueId import UniqueId
from leeger.model.league_helper.Performance import Performance
from leeger.util.CustomLogger import CustomLogger
from leeger.util.GeneralUtil import GeneralUtil
from leeger.util.JSONDeserializable import JSONDeserializable
from leeger.util.JSONSerializable import JSONSerializable


@dataclass(kw_only=True, eq=False)
class Matchup(UniqueId, JSONSerializable, JSONDeserializable):
    __LOGGER = CustomLogger.getLogger()
    teamAId: str
    teamBId: str
    teamAScore: float | int
    teamBScore: float | int
    matchupType: MatchupType = MatchupType.REGULAR_SEASON
    teamAHasTiebreaker: Optional[bool] = False
    teamBHasTiebreaker: Optional[bool] = False
    multiWeekMatchupId: Optional[
        str
    ] = None  # This is used to link matchups that span over multiple weeks

    def __post_init__(self):
        # Team A and Team B cannot both have the tiebreaker
        if self.teamAHasTiebreaker is True and self.teamBHasTiebreaker is True:
            raise InvalidMatchupFormatException(
                "Team A and Team B cannot both have the tiebreaker."
            )

        if self.teamAHasTiebreaker is None:
            self.teamAHasTiebreaker = False
        if self.teamBHasTiebreaker is None:
            self.teamBHasTiebreaker = False

    def __eq__(self, otherMatchup: Matchup) -> bool:
        """
        Checks if *this* Matchup is the same as the given Matchup.
        Does not check for equality of IDs, just values.
        """
        equal = self.teamAScore == otherMatchup.teamAScore
        equal = equal and self.teamBScore == otherMatchup.teamBScore
        equal = equal and self.matchupType == otherMatchup.matchupType
        equal = equal and self.teamAHasTiebreaker == otherMatchup.teamAHasTiebreaker
        equal = equal and self.teamBHasTiebreaker == otherMatchup.teamBHasTiebreaker
        # warn if this is going to return True but ID based fields are not equal
        if equal:
            notEqualStrings = list()
            if self.teamAId != otherMatchup.teamAId:
                notEqualStrings.append("teamAId")
            if self.teamBId != otherMatchup.teamBId:
                notEqualStrings.append("teamBId")
            if self.multiWeekMatchupId != otherMatchup.multiWeekMatchupId:
                notEqualStrings.append("multiWeekMatchupId")
            if len(notEqualStrings) > 0:
                self.__LOGGER.warning(
                    f"Returning True for equality check when {notEqualStrings} are not equal."
                )
        else:
            differences = GeneralUtil.findDifferentFields(
                self.toJson(),
                otherMatchup.toJson(),
                parentKey="Matchup",
                ignoreKeyNames=["id", "ownerId", "teamAId", "teamBId"],
            )
            self.__LOGGER.info(f"Differences: {differences}")
        return equal

    def splitToPerformances(self) -> tuple[Performance, Performance]:
        """
        Splits this Matchup into 2 Performances.
        """
        performanceA = Performance(
            teamId=self.teamAId,
            teamScore=self.teamAScore,
            matchupType=self.matchupType,
            multiWeekMatchupId=self.multiWeekMatchupId,
        )
        performanceB = Performance(
            teamId=self.teamBId,
            teamScore=self.teamBScore,
            matchupType=self.matchupType,
            multiWeekMatchupId=self.multiWeekMatchupId,
        )
        return performanceA, performanceB

    def getPerformanceForTeamId(self, teamId: str) -> Performance:
        performances = self.splitToPerformances()
        for performance in performances:
            if performance.teamId == teamId:
                return performance
        raise DoesNotExistException(f"Matchup does not have a team with ID '{teamId}'.")

    def toJson(self) -> dict:
        return {
            "id": self.id,
            "teamAId": self.teamAId,
            "teamBId": self.teamBId,
            "teamAScore": self.teamAScore,
            "teamBScore": self.teamBScore,
            "matchupType": self.matchupType.name,
            "teamAHasTiebreaker": self.teamAHasTiebreaker,
            "teamBHasTiebreaker": self.teamBHasTiebreaker,
            "multiWeekMatchupId": self.multiWeekMatchupId,
        }

    @staticmethod
    def fromJson(d: dict) -> Matchup:
        matchup = Matchup(
            teamAId=d["teamAId"],
            teamBId=d["teamBId"],
            teamAScore=d["teamAScore"],
            teamBScore=d["teamBScore"],
            matchupType=MatchupType.fromStr(d["matchupType"]),
            teamAHasTiebreaker=d.get("teamAHasTiebreaker"),
            teamBHasTiebreaker=d.get("teamBHasTiebreaker"),
            multiWeekMatchupId=d.get("multiWeekMatchupId"),
        )
        matchup.id = d["id"]
        return matchup
