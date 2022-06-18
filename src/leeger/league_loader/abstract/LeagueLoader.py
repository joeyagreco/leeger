from abc import ABC, abstractmethod

from src.leeger.model.League import League


class LeagueLoader(ABC):
    """
    League Loader classes should inherit this.
    The point of a league loader is to load a League object from different Fantasy Football sources.
    """

    @abstractmethod
    def loadLeague(self, *args, **kwargs) -> League:
        ...
