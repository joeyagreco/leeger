from abc import abstractmethod
from typing import Optional

from leeger.enum.FantasySite import FantasySite
from leeger.exception.DoesNotExistException import DoesNotExistException
from leeger.model.league.League import League
from leeger.model.league.Owner import Owner
from leeger.util.CustomLogger import CustomLogger


class LeagueLoader:
    """
    League Loader classes should inherit this.
    The point of a league loader is to load a League object from different Fantasy Football sources.
    """
    # leagues will be cached here with id "{FantasySite}+{leagueId}+{yearN}+{yearN+1}+{yearN+2}"
    __leagueCache: dict[str, League] = dict()

    def __init__(self, fantasySite: FantasySite, leagueId: str, years: list[int], **kwargs):
        self._LOGGER = CustomLogger().getLogger()
        self.__fantasySite = fantasySite
        self._leagueId = leagueId
        self._years = years
        self._owners: Optional[list[Owner]] = None
        # owners may have multiple names across different years,
        # defining owner names and aliases allows users to have multiple names that can belong to the same owner.
        # this prevents issues where an owner with a name change across years is counted as 2 different owners.
        # this should be formatted like so:
        # ownerNamesAndAliases = {"someOwnerNameIWant": ["alias1", "alias2"],
        #                           someOtherOwnerNameIWant: ["alias3", "alias4"]}
        self._ownerNamesAndAliases: dict[str, list[str]] = kwargs.get("ownerNamesAndAliases", dict())
        self.cache = kwargs.get("cache", False)

        # validation
        if len(years) == 0:
            raise ValueError(f"No years given to load league with ID '{self._leagueId}'.")

    def _getGeneralOwnerNameFromGivenOwnerName(self, givenOwnerName: str) -> Optional[str]:
        foundGeneralOwnerName = None
        for generalOwnerName, aliases in self._ownerNamesAndAliases.items():
            if givenOwnerName in aliases:
                foundGeneralOwnerName = generalOwnerName
                break
        return foundGeneralOwnerName

    def _getOwnerByName(self, ownerName: str) -> Owner:
        generalOwnerName = self._getGeneralOwnerNameFromGivenOwnerName(ownerName)
        for owner in self._owners:
            if ownerName == owner.name or generalOwnerName == owner.name:
                return owner
        raise DoesNotExistException(
            f"Owner name '{ownerName}' does not match any previously loaded owner names. To add multiple names for a single owner, use the 'ownerNamesAndAliases' keyword argument to define them.")

    def getLeagueFromCache(self) -> Optional[League]:
        """
        Returns the league from the cache if found or None if not.
        """
        leagueCacheId = self.__getLeagueCacheId()
        response = None
        if leagueCacheId in self.__leagueCache:
            response = self.__leagueCache[leagueCacheId]
        return response

    def upsertLeagueToCache(self, league: League) -> None:
        """
        Upserts the given League to the cache.
        """
        self.__leagueCache[self.__getLeagueCacheId()] = league

    def __getLeagueCacheId(self) -> str:
        leagueCacheId = f"{self.__fantasySite.name}+{self._leagueId}"
        for year in sorted(self._years):
            leagueCacheId += f"+{year}"
        return leagueCacheId

    @abstractmethod
    def loadLeague(self, *args, **kwargs) -> League:
        ...
