from __future__ import annotations

from abc import ABC, abstractmethod


class JSONDeserializable(ABC):
    @staticmethod
    @abstractmethod
    def fromJson(d: dict) -> JSONDeserializable:
        """
        Takes a dict and turns it into an instance of *this* class.
        """
        pass
