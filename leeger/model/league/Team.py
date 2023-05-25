from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from leeger.model.abstract.UniqueId import UniqueId
from leeger.util.ConfigReader import ConfigReader
from leeger.util.CustomLogger import CustomLogger
from leeger.util.GeneralUtil import GeneralUtil
from leeger.util.JSONDeserializable import JSONDeserializable
from leeger.util.JSONSerializable import JSONSerializable
from leeger.util.equality import equals


@dataclass(kw_only=True, eq=False)
class Team(UniqueId, JSONSerializable, JSONDeserializable):
    __LOGGER = CustomLogger.getLogger()
    ownerId: str
    name: str
    divisionId: Optional[str] = None

    def equals(
        self, otherTeam: Team, *, ignoreIds: bool = False, logDifferences: bool = False
    ) -> bool:
        """
        Checks if *this* Team is the same as the given Team.
        """
        ignoreKeyNames = ConfigReader.get(
            "EQUALITY_CHECK", "IGNORE_KEY_NAMES", asType=list, propFile="league.properties"
        )
        return equals(
            objA=self,
            objB=otherTeam,
            baseFields={"name"},
            idFields={"ownerId", "divisionId"},
            parentKey="Team",
            ignoreIdFields=ignoreIds,
            logDifferences=logDifferences,
            ignoreKeyNames=ignoreKeyNames,
        )

    def __eq__(self, otherTeam: Team) -> bool:
        """
        Checks if *this* Team is the same as the given Team.
        Does not check for equality of IDs, just values.
        TODO: REMOVE THIS
        """
        equal = self.name == otherTeam.name
        # warn if this is going to return True but ID based fields are not equal
        if equal:
            notEqualStrings = list()
            if self.ownerId != otherTeam.ownerId:
                notEqualStrings.append("ownerId")
            if self.divisionId != otherTeam.divisionId:
                notEqualStrings.append("divisionId")

            if len(notEqualStrings) > 0:
                self.__LOGGER.warning(
                    f"Returning True for equality check when {notEqualStrings} are not equal."
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
