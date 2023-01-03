from __future__ import annotations

from dataclasses import dataclass

from leeger.exception import DoesNotExistException
from leeger.model.abstract.UniqueId import UniqueId
from leeger.model.league.Team import Team
from leeger.model.league.Week import Week
from leeger.model.league.YearSettings import YearSettings
from leeger.util.JSONSerializable import JSONSerializable


@dataclass(kw_only=True, eq=False)
class Year(UniqueId, JSONSerializable):
    yearNumber: int
    teams: list[Team]
    weeks: list[Week]
    yearSettings: YearSettings = None

    def __post_init__(self):
        if self.yearSettings is None:
            self.yearSettings = YearSettings()

    def __hash__(self):
        return hash(str(self.toJson()))

    def __eq__(self, otherYear: Year) -> bool:
        """
        Checks if *this* Year is the same as the given Year.
        Does not check for equality of IDs, just values.
        """
        equal = self.yearNumber == otherYear.yearNumber
        equal = equal and self.teams == otherYear.teams
        equal = equal and self.weeks == otherYear.weeks
        equal = equal and self.yearSettings == otherYear.yearSettings
        return equal

    def getTeam(self, teamName: str) -> Team:
        """
        Returns the Team with the given team name.
        """
        for team in self.teams:
            if team.name == teamName:
                return team
        raise DoesNotExistException(f"Year does not have a team with name '{teamName}'")

    def toJson(self) -> dict:
        return {
            "id": self.id,
            "yearNumber": self.yearNumber,
            "teams": [team.toJson() for team in self.teams],
            "weeks": [week.toJson() for week in self.weeks],
            "yearSettings": self.yearSettings.toJson()
        }
