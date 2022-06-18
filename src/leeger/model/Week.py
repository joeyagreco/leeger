from dataclasses import dataclass

from src.leeger.model.Matchup import Matchup
from src.leeger.model.abstract.UniqueId import UniqueId


@dataclass(kw_only=True)
class Week(UniqueId):
    weekNumber: int
    matchups: list[Matchup]

    @property
    def isPlayoffWeek(self) -> bool:
        isPlayoffWeek = False
        for matchup in self.matchups:
            if matchup.isPlayoffMatchup:
                isPlayoffWeek = True
                break
        return isPlayoffWeek

    @property
    def isChampionshipWeek(self) -> bool:
        isChampionshipWeek = False
        for matchup in self.matchups:
            if matchup.isChampionshipMatchup:
                isChampionshipWeek = True
                break
        return isChampionshipWeek
