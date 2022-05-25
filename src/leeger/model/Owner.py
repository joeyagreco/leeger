from dataclasses import dataclass, field

from src.leeger.util.IdGenerator import IdGenerator


@dataclass(kw_only=True)
class Owner:
    name: str
    id: str = field(default_factory=IdGenerator.generateId, init=False)
