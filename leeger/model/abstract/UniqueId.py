from abc import ABC
from dataclasses import field, dataclass

from leeger.util.IdGenerator import IdGenerator


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
        self.__id = value

    @id.deleter
    def id(self):
        raise Exception("ID cannot be deleted.")
