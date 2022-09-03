from abc import ABC, abstractmethod


class JSONSerializable(ABC):

    @abstractmethod
    def toJson(self) -> dict:
        """
        Takes *this* instance of the implemented method's class and returns its representation as a dictionary.
        """
        pass
