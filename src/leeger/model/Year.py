from dataclasses import dataclass, field
from typing import List

from src.leeger.model.Team import Team
from src.leeger.model.Week import Week
from src.leeger.util.IdGenerator import IdGenerator


@dataclass(kw_only=True)
class Year:
    yearNumber: int
    teams: List[Team]
    weeks: List[Week]
    id: str = field(default_factory=IdGenerator.generateId, init=False)
