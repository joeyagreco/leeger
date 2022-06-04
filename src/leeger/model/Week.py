from dataclasses import dataclass

from src.leeger.exception.InvalidWeekFormatException import InvalidWeekFormatException
from src.leeger.model.Matchup import Matchup
from src.leeger.model.abstract.UniqueId import UniqueId


@dataclass(kw_only=True)
class Week(UniqueId):
    weekNumber: int
    isPlayoffWeek: bool
    isChampionshipWeek: bool
    matchups: list[Matchup]

    def __post_init__(self):
        # a week cannot be a championship week and NOT a playoff week
        if self.isChampionshipWeek is True and self.isPlayoffWeek is False:
            raise InvalidWeekFormatException("A championship week must be a playoff week.")
