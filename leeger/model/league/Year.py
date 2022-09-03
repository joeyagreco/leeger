from __future__ import annotations

from dataclasses import dataclass

from leeger.model.abstract.UniqueId import UniqueId
from leeger.model.league.Team import Team
from leeger.model.league.Week import Week
from leeger.util.JSONSerializable import JSONSerializable


@dataclass(kw_only=True, eq=False)
class Year(UniqueId, JSONSerializable):
    yearNumber: int
    teams: list[Team]
    weeks: list[Week]

    def __eq__(self, otherYear: Year) -> bool:
        """
        Checks if *this* Year is the same as the given Year.
        Does not check for equality of IDs, just values.
        """
        equal = self.yearNumber == otherYear.yearNumber
        equal = equal and self.teams == otherYear.teams
        equal = equal and self.weeks == otherYear.weeks
        return equal

    def toJson(self) -> dict:
        return {
            "id": self.id,
            "yearNumber": self.yearNumber,
            "teams": [team.toJson() for team in self.teams],
            "weeks": [week.toJson() for week in self.weeks]
        }
