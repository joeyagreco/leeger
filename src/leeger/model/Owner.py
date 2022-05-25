from dataclasses import dataclass


@dataclass(kw_only=True)
class Owner:
    id: str
    name: str
