from abc import ABC
from dataclasses import field, dataclass

from src.leeger.util.IdGenerator import IdGenerator


@dataclass
class UniqueId(ABC):
    """
    Model classes should inherit this in order to have a unique ID on init.
    """
    __id: str = field(default_factory=IdGenerator.generateId, init=False)

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value: str):
        raise Exception("ID cannot be set.")

    @id.deleter
    def id(self):
        raise Exception("ID cannot be deleted.")
