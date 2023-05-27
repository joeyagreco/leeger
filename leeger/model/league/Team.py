from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from leeger.model.abstract.UniqueId import UniqueId
from leeger.util.CustomLogger import CustomLogger
from leeger.util.JSONDeserializable import JSONDeserializable
from leeger.util.JSONSerializable import JSONSerializable
from leeger.util.equality import modelEquals


@dataclass(kw_only=True, eq=False)
class Team(UniqueId, JSONSerializable, JSONDeserializable):
    __LOGGER = CustomLogger.getLogger()
    ownerId: str
    name: str
    divisionId: Optional[str] = None

    def equals(
        self,
        otherTeam: Team,
        *,
        ignoreIds: bool = False,
        ignoreBaseId: bool = False,
        logDifferences: bool = False,
    ) -> bool:
        """
        Checks if *this* Team is the same as the given Team.
        """

        return modelEquals(
            objA=self,
            objB=otherTeam,
            baseFields={"name"},
            idFields={"ownerId", "divisionId"},
            parentKey="Team",
            ignoreIdFields=ignoreIds,
            ignoreBaseIdField=ignoreBaseId,
            logDifferences=logDifferences,
        )

    def __eq__(self, otherTeam: Team) -> bool:
        self.__LOGGER.info("Use .equals() for more options when comparing Team instances.")
        return self.equals(otherTeam=otherTeam)

    def toJson(self) -> dict:
        return {
            "id": self.id,
            "ownerId": self.ownerId,
            "name": self.name,
            "divisionId": self.divisionId,
        }

    @staticmethod
    def fromJson(d: dict) -> Team:
        team = Team(ownerId=d["ownerId"], name=d["name"], divisionId=d.get("divisionId"))
        team.id = d["id"]
        return team
