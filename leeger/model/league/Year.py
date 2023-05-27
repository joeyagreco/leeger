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
from leeger.util.JSONDeserializable import JSONDeserializable
from leeger.util.JSONSerializable import JSONSerializable
from leeger.util.equality import modelEquals


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

    def equals(
        self,
        otherYear: Year,
        *,
        ignoreIds: bool = False,
        ignoreBaseId: bool = False,
        logDifferences: bool = False,
    ) -> bool:
        """
        Checks if *this* Year is the same as the given Year.
        """

        def listsEqual(
            list1: list[Team | Week | Division],
            list2: list[Team | Week | Division],
            *,
            ignoreIds: bool,
            ignoreBaseId: bool,
        ) -> bool:
            if len(list1) != len(list2):
                return False
            equal = True
            for item1, item2 in zip(list1, list2):
                equal = equal and item1.equals(
                    item2, ignoreIds=ignoreIds, ignoreBaseId=ignoreBaseId
                )
            return equal

        def yearSettingsEqual(
            yearSettings1: YearSettings,
            yearSettings2: YearSettings,
            *,
            ignoreIds: bool,
            ignoreBaseId: bool,
        ) -> bool:
            return yearSettings1.equals(
                yearSettings2, ignoreIds=ignoreIds, ignoreBaseId=ignoreBaseId
            )

        return modelEquals(
            objA=self,
            objB=otherYear,
            baseFields={"yearNumber", "teams", "weeks", "divisions", "yearSettings"},
            parentKey="Year",
            ignoreIdFields=ignoreIds,
            ignoreBaseIdField=ignoreBaseId,
            logDifferences=logDifferences,
            equalityFunctionMap={
                "teams": listsEqual,
                "weeks": listsEqual,
                "divisions": listsEqual,
                "yearSettings": yearSettingsEqual,
            },
            equalityFunctionKwargsMap={
                "teams": {"ignoreIds": ignoreIds, "ignoreBaseId": ignoreBaseId},
                "weeks": {"ignoreIds": ignoreIds, "ignoreBaseId": ignoreBaseId},
                "divisions": {"ignoreIds": ignoreIds, "ignoreBaseId": ignoreBaseId},
                "yearSettings": {"ignoreIds": ignoreIds, "ignoreBaseId": ignoreBaseId},
            },
        )

    def __eq__(self, otherYear: Year) -> bool:
        self.__LOGGER.info("Use .equals() for more options when comparing Year instances.")
        return self.equals(otherYear=otherYear)

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
            "divisions": [division.toJson() for division in self.divisions],
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
        divisions = list()
        for divisionDict in d["divisions"]:
            divisions.append(Division.fromJson(divisionDict))
        year = Year(
            yearNumber=d["yearNumber"],
            teams=teams,
            weeks=weeks,
            divisions=divisions,
            yearSettings=YearSettings.fromJson(d.get("yearSettings")),
        )
        year.id = d["id"]
        return year
