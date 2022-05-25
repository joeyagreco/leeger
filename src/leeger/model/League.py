from dataclasses import dataclass, field
from typing import List

from src.leeger.model.Owner import Owner
from src.leeger.model.Year import Year
from src.leeger.util.IdGenerator import IdGenerator


@dataclass(kw_only=True)
class League:
    name: str
    owners: List[Owner]
    years: List[Year]
    id: str = field(default_factory=IdGenerator.generateId, init=False)
