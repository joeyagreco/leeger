from dataclasses import dataclass
from typing import List

from src.leeger.model.Team import Team
from src.leeger.model.Week import Week
from src.leeger.model.abstract.UniqueId import UniqueId


@dataclass(kw_only=True)
class Year(UniqueId):
    yearNumber: int
    teams: List[Team]
    weeks: List[Week]
