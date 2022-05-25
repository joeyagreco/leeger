from dataclasses import dataclass
from typing import List

from src.leeger.model.Matchup import Matchup
from src.leeger.model.abstract.UniqueId import UniqueId


@dataclass(kw_only=True)
class Week(UniqueId):
    weekNumber: int
    matchups: List[Matchup]
