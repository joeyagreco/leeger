from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class EqualityCheck(ABC):
    """
    Model classes should inherit this in order to have a .equals() method.
    """

    @abstractmethod
    def equals(
        self,
        otherInstance: Any,
        *,
        ignoreIds: bool = False,
        ignoreBaseIds: bool = False,
        logDifferences: bool = False,
    ) -> bool: ...
