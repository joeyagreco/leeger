from dataclasses import dataclass

from src.leeger.model.abstract.UniqueId import UniqueId


@dataclass(kw_only=True)
class Matchup(UniqueId):
    teamAId: str
    teamBId: str
    teamAScore: float | int
    teamBScore: float | int
