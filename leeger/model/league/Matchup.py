from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from leeger.enum.MatchupType import MatchupType
from leeger.exception import DoesNotExistException
from leeger.exception.InvalidMatchupFormatException import InvalidMatchupFormatException
from leeger.model.abstract.EqualityCheck import EqualityCheck
from leeger.model.abstract.UniqueId import UniqueId
from leeger.model.league_helper.Performance import Performance
from leeger.util.CustomLogger import CustomLogger
from leeger.util.equality import modelEquals
from leeger.util.JSONDeserializable import JSONDeserializable
from leeger.util.JSONSerializable import JSONSerializable


@dataclass(kw_only=True, eq=False)
class Matchup(UniqueId, EqualityCheck, JSONSerializable, JSONDeserializable):
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

    def equals(
        self,
        otherMatchup: Matchup,
        *,
        ignoreIds: bool = False,
        ignoreBaseIds: bool = False,
        logDifferences: bool = False,
    ) -> bool:
        """
        Checks if *this* Matchup is the same as the given Matchup.
        """

        return modelEquals(
            objA=self,
            objB=otherMatchup,
            baseFields={
                "teamAScore",
                "teamBScore",
                "matchupType",
                "teamAHasTiebreaker",
                "teamBHasTiebreaker",
            },
            idFields={"teamAId", "teamBId", "multiWeekMatchupId"},
            parentKey="Matchup",
            ignoreIdFields=ignoreIds,
            ignoreBaseIdField=ignoreBaseIds,
            logDifferences=logDifferences,
        )

    def __eq__(self, otherMatchup: Matchup) -> bool:
        self.__LOGGER.info("Use .equals() for more options when comparing Matchup instances.")
        return self.equals(otherMatchup=otherMatchup)

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
