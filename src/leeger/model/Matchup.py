from dataclasses import dataclass
from decimal import Decimal


@dataclass(kw_only=True)
class Matchup:
    id: str
    teamAId: str
    teamBId: str
    teamAScore: Decimal
    teamBScore: Decimal
  