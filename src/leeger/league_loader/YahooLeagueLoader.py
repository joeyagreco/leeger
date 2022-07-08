from typing import Optional

from yahoofantasy import Context
from yahoofantasy import League as YahooLeague
from yahoofantasy import Team as YahooTeam

from src.leeger.exception.DoesNotExistException import DoesNotExistException
from src.leeger.league_loader.abstract.LeagueLoader import LeagueLoader
from src.leeger.model.league.League import League
from src.leeger.model.league.Owner import Owner


class YahooLeagueLoader(LeagueLoader):
    """
    Responsible for loading a League from Yahoo Fantasy Football.
    https://football.fantasysports.yahoo.com/
    """
    __NFL = "nfl"

    @classmethod
    def __initializeClassVariables(cls) -> None:
        cls.__owners: Optional[list[Owner]] = None

    @classmethod
    def loadLeague(cls, leagueId: int, years: list[int], **kwargs) -> League:
        cls.__initializeClassVariables()
        ctx = Context()
        yahooLeagues = list()
        for year in years:
            leagues = ctx.get_leagues(cls.__NFL, year)
            for league in leagues:
                if league.league_id == leagueId:
                    yahooLeagues.append(league)
        if len(yahooLeagues) != len(years):
            raise DoesNotExistException(f"Found {len(yahooLeagues)} years, expected to find {len(years)}.")
        return cls.__buildLeague(yahooLeagues)

    @classmethod
    def __buildLeague(cls, yahooLeagues: list[YahooLeague]) -> League:
        years = list()
        leagueName = None
        for yahooLeague in yahooLeagues:
            leagueName = yahooLeague.name if leagueName is None else leagueName
            cls.__loadOwners(yahooLeague.teams())
            # years.append(cls.__buildYear(yahooLeague))
        return League(name=leagueName, owners=cls.__owners, years=[])

    @classmethod
    def __loadOwners(cls, yahooTeams: list[YahooTeam]) -> None:
        if cls.__owners is None:
            owners = list()
            for yahooTeam in yahooTeams:
                owners.append(Owner(name=yahooTeam.manager.nickname))
            cls.__owners = owners
