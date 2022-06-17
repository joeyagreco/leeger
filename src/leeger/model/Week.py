from dataclasses import dataclass

from src.leeger.model.Matchup import Matchup
from src.leeger.model.abstract.UniqueId import UniqueId


@dataclass(kw_only=True)
class Week(UniqueId):
    weekNumber: int
    matchups: list[Matchup]
    isPlayoffWeek: bool = False

    @property
    def isChampionshipWeek(self) -> bool:
        isChampionshipWeek = False
        for matchup in self.matchups:
            if matchup.isChampionshipMatchup:
                isChampionshipWeek = True
                break
        return isChampionshipWeek
