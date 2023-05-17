from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from leeger.exception import DoesNotExistException
from leeger.model.abstract.UniqueId import UniqueId
from leeger.model.league.Division import Division
from leeger.model.league.Team import Team
from leeger.model.league.Week import Week
from leeger.model.league.YearSettings import YearSettings
from leeger.util.CustomLogger import CustomLogger
from leeger.util.GeneralUtil import GeneralUtil
from leeger.util.JSONDeserializable import JSONDeserializable
from leeger.util.JSONSerializable import JSONSerializable


@dataclass(kw_only=True, eq=False)
class Year(UniqueId, JSONSerializable, JSONDeserializable):
    __LOGGER = CustomLogger.getLogger()
    yearNumber: int
    teams: list[Team]
    weeks: list[Week]
    divisions: Optional[list[Division]] = None
    yearSettings: Optional[YearSettings] = None

    def __post_init__(self):
        if self.divisions is None:
            self.divisions = list()
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
        if not equal:
            differences = GeneralUtil.findDifferentFields(
                self.toJson(),
                otherYear.toJson(),
                parentKey="Year",
                ignoreKeyNames=["id", "ownerId", "teamAId", "teamBId"],
            )
            self.__LOGGER.info(f"Differences: {differences}")
        return equal

    def getTeamByName(self, teamName: str) -> Team:
        """
        Returns the Team with the given team name.
        """
        for team in self.teams:
            if team.name == teamName:
                return team
        raise DoesNotExistException(f"Year does not have a team with name '{teamName}'.")

    def getWeekByWeekNumber(self, weekNumber: int) -> Week:
        """
        Returns the Week with the given week number.
        """
        for week in self.weeks:
            if week.weekNumber == weekNumber:
                return week
        raise DoesNotExistException(f"Year does not have a week with week number {weekNumber}.")

    def toJson(self) -> dict:
        return {
            "id": self.id,
            "yearNumber": self.yearNumber,
            "teams": [team.toJson() for team in self.teams],
            "weeks": [week.toJson() for week in self.weeks],
            "yearSettings": self.yearSettings.toJson(),
        }

    @staticmethod
    def fromJson(d: dict) -> Year:
        teams = list()
        for teamDict in d["teams"]:
            teams.append(Team.fromJson(teamDict))
        weeks = list()
        for weekDict in d["weeks"]:
            weeks.append(Week.fromJson(weekDict))
        year = Year(
            yearNumber=d["yearNumber"],
            teams=teams,
            weeks=weeks,
            yearSettings=YearSettings.fromJson(d.get("yearSettings")),
        )
        year.id = d["id"]
        return year
