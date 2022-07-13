from dataclasses import dataclass

from leeger.model.abstract.UniqueId import UniqueId


@dataclass(kw_only=True)
class Owner(UniqueId):
    name: str
