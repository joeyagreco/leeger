from typing import Optional

from yahoofantasy import Context
from yahoofantasy import League as YahooLeague
from yahoofantasy import Team as YahooTeam

from src.leeger.exception.DoesNotExistException import DoesNotExistException
from src.leeger.league_loader.abstract.LeagueLoader import LeagueLoader
from src.leeger.model.league.League import League
from src.leeger.model.league.Owner import Owner
from src.leeger.model.league.Team import Team
from src.leeger.model.league.Year import Year


class YahooLeagueLoader(LeagueLoader):
    """
    Responsible for loading a League from Yahoo Fantasy Football.
    https://football.fantasysports.yahoo.com/
    """
    __NFL = "nfl"

    @classmethod
    def __initializeClassVariables(cls) -> None:
        cls.__owners: Optional[list[Owner]] = None
        cls.__yahooTeamIdToTeamMap: dict[str, Team] = dict()

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
        test = league.teams()
        if len(yahooLeagues) != len(years):
            # TODO: Give a more descriptive // accurate error message
            raise DoesNotExistException(f"Found {len(yahooLeagues)} years, expected to find {len(years)}.")
        return cls.__buildLeague(yahooLeagues)

    @classmethod
    def __buildLeague(cls, yahooLeagues: list[YahooLeague]) -> League:
        years = list()
        leagueName = None
        for yahooLeague in yahooLeagues:
            leagueName = yahooLeague.name if leagueName is None else leagueName
            cls.__loadOwners(yahooLeague.teams())
            years.append(cls.__buildYear(yahooLeague))
        return League(name=leagueName, owners=cls.__owners, years=years)

    @classmethod
    def __buildYear(cls, yahooLeague: YahooLeague) -> Year:
        teams = cls.__buildTeams(yahooLeague.teams())
        # weeks = cls.__buildWeeks(yahooLeague)
        return Year(yearNumber=yahooLeague.season, teams=teams, weeks=[])

    @classmethod
    def __buildTeams(cls, yahooTeams: list[YahooTeam]) -> list[Team]:
        teams = list()
        for yahooTeam in yahooTeams:
            owner = cls.__getOwnerByName(yahooTeam.manager.nickname)
            team = Team(ownerId=owner.id, name=yahooTeam.name)
            teams.append(team)
            cls.__yahooTeamIdToTeamMap[yahooTeam.team_id] = team
        return teams

    @classmethod
    def __loadOwners(cls, yahooTeams: list[YahooTeam]) -> None:
        if cls.__owners is None:
            owners = list()
            for yahooTeam in yahooTeams:
                owners.append(Owner(name=yahooTeam.manager.nickname))
            cls.__owners = owners

    @classmethod
    def __getOwnerByName(cls, ownerName: str) -> Owner:
        for owner in cls.__owners:
            if ownerName == owner.name:
                return owner
        raise DoesNotExistException(
            f"Owner name '{ownerName}' does not match any previously loaded owner names. To add multiple names for a single owner, use the 'ownerNamesAndAliases' keyword argument to define them.")
