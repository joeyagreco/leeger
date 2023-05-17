from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from leeger.model.abstract.UniqueId import UniqueId
from leeger.util.ConfigReader import ConfigReader
from leeger.util.CustomLogger import CustomLogger
from leeger.util.GeneralUtil import GeneralUtil
from leeger.util.JSONDeserializable import JSONDeserializable
from leeger.util.JSONSerializable import JSONSerializable


@dataclass(kw_only=True, eq=False)
class Team(UniqueId, JSONSerializable, JSONDeserializable):
    __LOGGER = CustomLogger.getLogger()
    ownerId: str
    name: str
    divisionId: Optional[str] = None

    def __eq__(self, otherTeam: Team) -> bool:
        """
        Checks if *this* Team is the same as the given Team.
        Does not check for equality of IDs, just values.
        """
        equal = self.name == otherTeam.name
        equal = equal and self.divisionId == otherTeam.divisionId
        # warn if this is going to return True but ID based fields are not equal
        if equal:
            if self.ownerId != otherTeam.ownerId:
                self.__LOGGER.warning(
                    f"Returning True for equality check when ownerIds are not equal."
                )
        else:
            differences = GeneralUtil.findDifferentFields(
                self.toJson(),
                otherTeam.toJson(),
                parentKey="Team",
                ignoreKeyNames=ConfigReader.get(
                    "EQUALITY_CHECK", "IGNORE_KEY_NAMES", asType=list, propFile="league.properties"
                ),
            )
            self.__LOGGER.info(f"Differences: {differences}")
        return equal

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
