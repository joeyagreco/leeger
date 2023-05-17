from __future__ import annotations

from dataclasses import dataclass

from leeger.model.abstract.UniqueId import UniqueId
from leeger.util.ConfigReader import ConfigReader
from leeger.util.CustomLogger import CustomLogger
from leeger.util.GeneralUtil import GeneralUtil
from leeger.util.JSONDeserializable import JSONDeserializable
from leeger.util.JSONSerializable import JSONSerializable


@dataclass(kw_only=True, eq=False)
class Owner(UniqueId, JSONSerializable, JSONDeserializable):
    __LOGGER = CustomLogger.getLogger()
    name: str

    def __eq__(self, otherOwner: Owner) -> bool:
        """
        Checks if *this* Owner is the same as the given Owner.
        Does not check for equality of IDs, just values.
        """
        equal = self.name == otherOwner.name
        if not equal:
            differences = GeneralUtil.findDifferentFields(
                self.toJson(),
                otherOwner.toJson(),
                parentKey="Owner",
                ignoreKeyNames=ConfigReader.get("EQUALITY_CHECK", "IGNORE_KEY_NAMES", asType=list, propFile="league.properties"),
            )
            self.__LOGGER.info(f"Differences: {differences}")
        return equal

    def toJson(self) -> dict:
        return {"id": self.id, "name": self.name}

    @staticmethod
    def fromJson(d: dict) -> Owner:
        owner = Owner(name=d["name"])
        owner.id = d["id"]
        return owner
