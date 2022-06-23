from dataclasses import dataclass

from src.leeger.model.abstract.UniqueId import UniqueId
from src.leeger.model.league.Team import Team
from src.leeger.model.league.Week import Week


@dataclass(kw_only=True)
class Year(UniqueId):
    yearNumber: int
    teams: list[Team]
    weeks: list[Week]
