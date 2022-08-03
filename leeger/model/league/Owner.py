from __future__ import annotations

from dataclasses import dataclass

from leeger.model.abstract.UniqueId import UniqueId


@dataclass(kw_only=True)
class Owner(UniqueId):
    name: str

    def __eq__(self, otherOwner: Owner) -> bool:
        """
        Checks if *this* Owner is the same as the given Owner.
        Does not check for equality of IDs, just values.
        """
        return self.name == otherOwner.name
