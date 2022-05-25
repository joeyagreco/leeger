from dataclasses import dataclass
from typing import List

from src.leeger.model.Team import Team
from src.leeger.model.Week import Week


@dataclass(kw_only=True)
class Year:
    id: str
    yearNumber: int
    teams: List[Team]
    weeks: List[Week]
