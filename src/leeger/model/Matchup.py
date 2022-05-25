from dataclasses import dataclass, field
from decimal import Decimal

from src.leeger.util.IdGenerator import IdGenerator


@dataclass(kw_only=True)
class Matchup:
    teamAId: str
    teamBId: str
    teamAScore: Decimal
    teamBScore: Decimal
    id: str = field(default_factory=IdGenerator.generateId, init=False)
