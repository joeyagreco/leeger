from __future__ import annotations

from dataclasses import dataclass

from leeger.model.abstract.UniqueId import UniqueId
from leeger.util.CustomLogger import CustomLogger
from leeger.util.JSONDeserializable import JSONDeserializable
from leeger.util.JSONSerializable import JSONSerializable
from leeger.util.equality import modelEquals


@dataclass(kw_only=True, eq=False)
class Division(UniqueId, JSONSerializable, JSONDeserializable):
    __LOGGER = CustomLogger.getLogger()
    name: str

    def equals(
        self,
        otherDivision: Division,
        *,
        ignoreIds: bool = False,
        ignoreBaseId: bool = False,
        logDifferences: bool = False,
    ) -> bool:
        """
        Checks if *this* Division is the same as the given Division.
        """

        return modelEquals(
            objA=self,
            objB=otherDivision,
            baseFields={"name"},
            parentKey="Division",
            ignoreIdFields=ignoreIds,
            ignoreBaseIdField=ignoreBaseId,
            logDifferences=logDifferences,
        )

    def __eq__(self, otherDivision: Division) -> bool:
        self.__LOGGER.info("Use .equals() for more options when comparing Division instances.")
        return self.equals(otherDivision=otherDivision)

    def toJson(self) -> dict:
        return {"id": self.id, "name": self.name}

    @staticmethod
    def fromJson(d: dict) -> Division:
        division = Division(name=d["name"])
        division.id = d["id"]
        return division
