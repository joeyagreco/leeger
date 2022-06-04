from dataclasses import dataclass

from src.leeger.model.Owner import Owner
from src.leeger.model.Year import Year
from src.leeger.model.abstract.UniqueId import UniqueId


@dataclass(kw_only=True)
class League(UniqueId):
    name: str
    owners: list[Owner]
    years: list[Year]
