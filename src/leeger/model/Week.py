from dataclasses import dataclass, field
from typing import List

from src.leeger.model.Matchup import Matchup
from src.leeger.util.IdGenerator import IdGenerator


@dataclass(kw_only=True)
class Week:
    weekNumber: int
    matchups: List[Matchup]
    id: str = field(default_factory=IdGenerator.generateId, init=False)
