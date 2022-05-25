from dataclasses import dataclass


@dataclass(kw_only=True)
class Team:
    id: str
    ownerId: str
    name: str
