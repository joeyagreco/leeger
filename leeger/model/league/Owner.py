from __future__ import annotations

from dataclasses import dataclass

from leeger.model.abstract.EqualityCheck import EqualityCheck
from leeger.model.abstract.UniqueId import UniqueId
from leeger.util.CustomLogger import CustomLogger
from leeger.util.equality import modelEquals
from leeger.util.JSONDeserializable import JSONDeserializable
from leeger.util.JSONSerializable import JSONSerializable


@dataclass(kw_only=True, eq=False)
class Owner(UniqueId, EqualityCheck, JSONSerializable, JSONDeserializable):
    __LOGGER = CustomLogger.getLogger()
    name: str

    def equals(
        self,
        otherOwner: Owner,
        *,
        ignoreIds: bool = False,
        ignoreBaseIds: bool = False,
        logDifferences: bool = False,
    ) -> bool:
        """
        Checks if *this* Owner is the same as the given Owner.
        """

        return modelEquals(
            objA=self,
            objB=otherOwner,
            baseFields={"name"},
            parentKey="Owner",
            ignoreIdFields=ignoreIds,
            ignoreBaseIdField=ignoreBaseIds,
            logDifferences=logDifferences,
        )

    def __eq__(self, otherOwner: Owner) -> bool:
        self.__LOGGER.info("Use .equals() for more options when comparing Owner instances.")
        return self.equals(otherOwner=otherOwner)

    def toJson(self) -> dict:
        return {"id": self.id, "name": self.name}

    @staticmethod
    def fromJson(d: dict) -> Owner:
        owner = Owner(name=d["name"])
        owner.id = d["id"]
        return owner
