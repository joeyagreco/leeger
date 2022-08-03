from __future__ import annotations

from dataclasses import dataclass

from leeger.model.abstract.UniqueId import UniqueId
from leeger.util.CustomLogger import CustomLogger


@dataclass(kw_only=True, eq=False)
class Team(UniqueId):
    __LOGGER = CustomLogger.getLogger()
    ownerId: str
    name: str

    def __eq__(self, otherTeam: Team) -> bool:
        """
        Checks if *this* Team is the same as the given Team.
        Does not check for equality of IDs, just values.
        """
        equal = self.name == otherTeam.name
        # warn if this is going to return True but ID based fields are not equal
        if equal:
            notEqualStrings = list()
            if self.ownerId != otherTeam.ownerId:
                notEqualStrings.append("teamAId")
            if len(notEqualStrings) > 0:
                self.__LOGGER.warning(f"Returning True for equality check when {notEqualStrings} are not equal.")
        return equal
