from __future__ import annotations

from dataclasses import dataclass

from leeger.enum.MatchupType import MatchupType
from leeger.model.abstract.UniqueId import UniqueId
from leeger.model.league.Matchup import Matchup


@dataclass(kw_only=True, eq=False)
class Week(UniqueId):
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
