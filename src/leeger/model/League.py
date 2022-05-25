from dataclasses import dataclass
from typing import List

from src.leeger.model.Owner import Owner
from src.leeger.model.Year import Year


@dataclass(kw_only=True)
class League:
    id: str
    name: str
    owners: List[Owner]
    years: List[Year]
