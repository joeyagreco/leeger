from dataclasses import dataclass

from src.leeger.model.abstract.UniqueId import UniqueId


@dataclass(kw_only=True)
class Team(UniqueId):
    ownerId: str
    name: str
