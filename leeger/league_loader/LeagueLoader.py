from abc import abstractmethod
from typing import Optional

from leeger.exception.DoesNotExistException import DoesNotExistException
from leeger.exception.LeagueLoaderException import LeagueLoaderException
from leeger.model.league.League import League
from leeger.model.league.Owner import Owner
from leeger.model.league.Year import Year
from leeger.util.CustomLogger import CustomLogger


class LeagueLoader:
    """
    League Loader classes should inherit this.
    The point of a league loader is to load a League object from different Fantasy Football sources.
    """

    def __init__(
        self,
        leagueId: str,
        years: list[int],
        *,
        ownerNamesAndAliases: Optional[dict] = None,
        leagueName: Optional[str] = None,
    ):
        self._LOGGER = CustomLogger().getLogger()
        # validation
        if len(years) == 0:
            raise ValueError(f"No years given to load league with ID '{leagueId}'.")

        if not all(isinstance(year, int) for year in years):
            raise ValueError(f"All given years must be ints.")

        self._leagueId = leagueId
        self._years = sorted(years)
        self._owners: Optional[list[Owner]] = None
        # owners may have multiple names across different years,
        # defining owner names and aliases allows users to have multiple names that can belong to the same owner.
        # this prevents issues where an owner with a name change across years is counted as 2 different owners.
        # this should be formatted like so:
        # ownerNamesAndAliases = {"someOwnerNameIWant": ["alias1", "alias2"],
        #                           someOtherOwnerNameIWant: ["alias3", "alias4"]}
        self._ownerNamesAndAliases: dict[str, list[str]] = (
            ownerNamesAndAliases if ownerNamesAndAliases else dict()
        )
        self._leagueName = leagueName
        self._leagueNameByYear: dict[int, str] = (
            dict()
        )  # will hold league name by year like {2020: "foo", 2021: "baz", ...}

    def _getLeagueName(self) -> str:
        leagueName = self._leagueName
        if self._leagueName is None:
            if len(self._leagueNameByYear.keys()) == 0:
                raise LeagueLoaderException(
                    "Tried to retrieve league name with no leagueName parameter given and no league names set."
                )
            # use most recent year league name
            mostRecentYear = sorted(self._leagueNameByYear.keys())[-1]
            leagueName = self._leagueNameByYear[mostRecentYear]
        return leagueName

    def _getValidYears(self, years: list[Year]) -> list[Year]:
        validYears = list()
        # make sure years are ordered oldest -> newest
        for year in sorted(years, key=lambda y: y.yearNumber):
            if len(year.weeks) > 0:
                validYears.append(year)
            else:
                self._LOGGER.warning(
                    f"Year '{year.yearNumber}' discarded for not having any weeks."
                )
        return validYears

    def _validateRetrievedLeagues(self, retrievedLeagues: list) -> None:
        expectedLeagueCount = len(self._years)
        actualLeagueCount = len(retrievedLeagues)
        if actualLeagueCount != expectedLeagueCount:
            raise LeagueLoaderException(
                f"Expected to retrieve {expectedLeagueCount} league/s, got {actualLeagueCount} league/s."
            )

    def _getGeneralOwnerNameFromGivenOwnerName(
        self, givenOwnerName: str
    ) -> Optional[str]:
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
            f"Owner name '{ownerName}' does not match any previously loaded owner names. To add multiple names for a single owner, use the 'ownerNamesAndAliases' keyword argument to define them."
        )

    ## validation

    def _warnForUnusedOwnerNames(self, league: League) -> None:
        """
        Logs a warning for all owner names that are not in the loaded league IF ownerNamesAndAliases is given.
        """
        if self._ownerNamesAndAliases:
            allLoadedOwnerNames = [owner.name for owner in league.owners]
            unusedOwnerNames = list()
            for ownerName in self._ownerNamesAndAliases.keys():
                if ownerName not in allLoadedOwnerNames:
                    unusedOwnerNames.append(ownerName)
            if unusedOwnerNames:
                self._LOGGER.warning(
                    f"Some owner names were given but not assigned to the loaded League: {unusedOwnerNames}"
                )

    @abstractmethod
    def loadLeague(self, validate: bool = True, *args, **kwargs) -> League: ...

    @abstractmethod
    def getOwnerNames(self, *args, **kwargs) -> dict[int, list[str]]: ...
