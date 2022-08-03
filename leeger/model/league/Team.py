from __future__ import annotations

from dataclasses import dataclass

from leeger.model.abstract.UniqueId import UniqueId


@dataclass(kw_only=True)
class Team(UniqueId):
    ownerId: str
    name: str

    def __eq__(self, otherTeam: Team) -> bool:
        """
        Checks if *this* Team is the same as the given Team.
        Does not check for equality of IDs, just values.
        """
        equal = self.ownerId == otherTeam.ownerId
        equal = equal and self.name == otherTeam.name
        return equal
