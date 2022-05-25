from dataclasses import dataclass
from typing import List

from src.leeger.model.Matchup import Matchup


@dataclass(kw_only=True)
class Week:
    id: str
    weekNumber: int
    matchups: List[Matchup]
