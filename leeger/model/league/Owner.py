from __future__ import annotations

from dataclasses import dataclass

from leeger.model.abstract.UniqueId import UniqueId
from leeger.util.JSONDeserializable import JSONDeserializable
from leeger.util.JSONSerializable import JSONSerializable


@dataclass(kw_only=True, eq=False)
class Owner(UniqueId, JSONSerializable, JSONDeserializable):
    name: str

    def __eq__(self, otherOwner: Owner) -> bool:
        """
        Checks if *this* Owner is the same as the given Owner.
        Does not check for equality of IDs, just values.
        """
        return self.name == otherOwner.name

    def toJson(self) -> dict:
        return {
            "id": self.id,
            "name": self.name
        }

    @staticmethod
    def fromJson(d: dict) -> Owner:
        owner = Owner(name=d["name"])
        owner.id = d["id"]
        return owner
