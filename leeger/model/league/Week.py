from __future__ import annotations

from dataclasses import dataclass

from leeger.enum.MatchupType import MatchupType
from leeger.exception import DoesNotExistException
from leeger.model.abstract.UniqueId import UniqueId
from leeger.model.league.Matchup import Matchup
from leeger.util.JSONDeserializable import JSONDeserializable
from leeger.util.JSONSerializable import JSONSerializable


@dataclass(kw_only=True, eq=False)
class Week(UniqueId, JSONSerializable, JSONDeserializable):
    weekNumber: int
    matchups: list[Matchup]

    def __eq__(self, otherWeek: Week) -> bool:
        """
        Checks if *this* Week is the same as the given Week.
        Does not check for equality of IDs, just values.
        """
        equal = self.weekNumber == otherWeek.weekNumber
        equal = equal and self.matchups == otherWeek.matchups
        return equal

    @property
    def isPlayoffWeek(self) -> bool:
        isPlayoffWeek = False
        for matchup in self.matchups:
            if matchup.matchupType == MatchupType.PLAYOFF:
                isPlayoffWeek = True
                break
        return isPlayoffWeek or self.isChampionshipWeek

    @property
    def isChampionshipWeek(self) -> bool:
        isChampionshipWeek = False
        for matchup in self.matchups:
            if matchup.matchupType == MatchupType.CHAMPIONSHIP:
                isChampionshipWeek = True
                break
        return isChampionshipWeek

    @property
    def isRegularSeasonWeek(self) -> bool:
        isRegularSeasonWeek = True
        for matchup in self.matchups:
            if (
                matchup.matchupType != MatchupType.REGULAR_SEASON
                and matchup.matchupType != MatchupType.IGNORE
            ):
                isRegularSeasonWeek = False
                break
        return isRegularSeasonWeek

    def getMatchupWithTeamId(self, teamId: str) -> Matchup:
        """
        Returns the Matchup that the team with the given ID is playing in.
        """
        for matchup in self.matchups:
            if matchup.teamAId == teamId or matchup.teamBId == teamId:
                return matchup
        raise DoesNotExistException(f"Week does not have a matchup with team ID '{teamId}'.")

    def toJson(self) -> dict:
        return {
            "id": self.id,
            "weekNumber": self.weekNumber,
            "matchups": [matchup.toJson() for matchup in self.matchups],
        }

    @staticmethod
    def fromJson(d: dict) -> Week:
        matchups = list()
        for matchupDict in d["matchups"]:
            matchups.append(Matchup.fromJson(matchupDict))
        week = Week(weekNumber=d["weekNumber"], matchups=matchups)
        week.id = d["id"]
        return week
