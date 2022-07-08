import subprocess

from yahoofantasy import Context
from yahoofantasy import League as YahooLeague
from yahoofantasy import Matchup as YahooMatchup
from yahoofantasy import Team as YahooTeam
from yahoofantasy import Week as YahooWeek

from src.leeger.enum.MatchupType import MatchupType
from src.leeger.exception.DoesNotExistException import DoesNotExistException
from src.leeger.league_loader.abstract.LeagueLoader import LeagueLoader
from src.leeger.model.league.League import League
from src.leeger.model.league.Matchup import Matchup
from src.leeger.model.league.Owner import Owner
from src.leeger.model.league.Team import Team
from src.leeger.model.league.Week import Week
from src.leeger.model.league.Year import Year


class YahooLeagueLoader(LeagueLoader):
    """
    Responsible for loading a League from Yahoo Fantasy Football.
    https://football.fantasysports.yahoo.com/
    """
    __NFL = "nfl"

    @classmethod
    def __initializeClassVariables(cls) -> None:
        cls.__yahooManagerIdToOwnerMap: dict[int, Owner] = dict()
        cls.__yahooTeamIdToTeamMap: dict[str, Team] = dict()
        cls.__yearToTeamIdHasLostInPlayoffs: dict[int, dict[int, bool]] = dict()

    @classmethod
    def __login(cls, clientId: str, clientSecret: str) -> None:
        """
        Logs in via Yahoo OAuth.
        Will open up a browser window.
        """
        CLIENT_ID_OPTION = "--client-id"
        CLIENT_SECRET_OPTION = "--client-secret"
        subprocess.call(["yahoofantasy", "login", CLIENT_ID_OPTION, clientId, CLIENT_SECRET_OPTION, clientSecret])

    @classmethod
    def loadLeague(cls, leagueId: int, years: list[int], *, clientId: str, clientSecret: str, **kwargs) -> League:
        cls.__initializeClassVariables()
        cls.__login(clientId, clientSecret)
        ctx = Context()
        yahooLeagues = list()
        for year in years:
            leagues = ctx.get_leagues(cls.__NFL, year)
            for league in leagues:
                if league.league_id == leagueId:
                    yahooLeagues.append(league)
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
        return League(name=leagueName, owners=list(cls.__yahooManagerIdToOwnerMap.values()), years=years)

    @classmethod
    def __buildYear(cls, yahooLeague: YahooLeague) -> Year:
        cls.__yearToTeamIdHasLostInPlayoffs[yahooLeague.season] = dict()
        teams = cls.__buildTeams(yahooLeague.teams())
        weeks = cls.__buildWeeks(yahooLeague)
        return Year(yearNumber=yahooLeague.season, teams=teams, weeks=weeks)

    @classmethod
    def __buildWeeks(cls, yahooLeague: YahooLeague) -> list[Week]:
        weeks = list()
        for i in range(yahooLeague.current_week):  # current week seems to be the last week in the league
            yahooWeek: YahooWeek = yahooLeague.weeks()[i]
            # get each teams matchup for that week
            matchups = list()
            for yahooMatchup in yahooWeek.matchups:
                # team A is *this* team
                yahooTeamA = yahooMatchup.team1
                teamA = cls.__yahooTeamIdToTeamMap[yahooMatchup.team1.team_id]
                teamAScore = yahooMatchup.teams.team[0].team_points.total
                # team B is their opponent
                yahooTeamB = yahooMatchup.team2
                teamB = cls.__yahooTeamIdToTeamMap[yahooMatchup.team2.team_id]
                teamBScore = yahooMatchup.teams.team[1].team_points.total
                # figure out tiebreakers if there needs to be one
                teamAHasTiebreaker = yahooMatchup.winner_team_key == yahooTeamA.team_key and yahooMatchup.is_tied == 0
                teamBHasTiebreaker = yahooMatchup.winner_team_key == yahooTeamB.team_key and yahooMatchup.is_tied == 0
                matchupType = cls.__getMatchupType(yahooMatchup)
                matchups.append(Matchup(teamAId=teamA.id,
                                        teamBId=teamB.id,
                                        teamAScore=teamAScore,
                                        teamBScore=teamBScore,
                                        teamAHasTiebreaker=teamAHasTiebreaker,
                                        teamBHasTiebreaker=teamBHasTiebreaker,
                                        matchupType=matchupType))
            weeks.append(Week(weekNumber=i + 1, matchups=matchups))
        return weeks

    @classmethod
    def __getMatchupType(cls, yahooMatchup: YahooMatchup) -> MatchupType:
        team1Id = yahooMatchup.team1.team_id
        team2Id = yahooMatchup.team2.team_id
        # check if this is a playoff week
        if yahooMatchup.is_playoffs == 1:
            # figure out if this is the last week of playoffs (the championship week)
            if yahooMatchup.week == yahooMatchup.league.end_week:
                # this is the championship week
                # figure out if either team has lost in the playoffs yet
                if team1Id in cls.__yearToTeamIdHasLostInPlayoffs[yahooMatchup.league.season] \
                        and not cls.__yearToTeamIdHasLostInPlayoffs[yahooMatchup.league.season][team1Id] \
                        and team2Id in cls.__yearToTeamIdHasLostInPlayoffs[yahooMatchup.league.season] \
                        and not cls.__yearToTeamIdHasLostInPlayoffs[yahooMatchup.league.season][team2Id]:
                    return MatchupType.CHAMPIONSHIP
            # update class dict with the team that lost
            for yahooTeamResult in yahooMatchup.teams.team:
                if yahooTeamResult.win_probability == 0:
                    cls.__yearToTeamIdHasLostInPlayoffs[yahooMatchup.league.season][yahooTeamResult.team_id] = True
                elif yahooTeamResult.win_probability == 1:
                    cls.__yearToTeamIdHasLostInPlayoffs[yahooMatchup.league.season][yahooTeamResult.team_id] = False
            return MatchupType.PLAYOFF
        else:
            return MatchupType.REGULAR_SEASON

    @classmethod
    def __buildTeams(cls, yahooTeams: list[YahooTeam]) -> list[Team]:
        teams = list()
        for yahooTeam in yahooTeams:
            owner = cls.__getOwnerByYahooTeam(yahooTeam)
            team = Team(ownerId=owner.id, name=yahooTeam.name)
            teams.append(team)
            cls.__yahooTeamIdToTeamMap[yahooTeam.team_id] = team
        return teams

    @classmethod
    def __loadOwners(cls, yahooTeams: list[YahooTeam]) -> None:
        if len(cls.__yahooManagerIdToOwnerMap.values()) == 0:
            yahooManagerIdToOwnerMap = dict()
            yahooOwnerTeamNames = list()
            for yahooTeam in yahooTeams:
                ownerName = yahooTeam.manager.nickname
                # prevent duplicate owner names
                i = 2
                while ownerName in yahooOwnerTeamNames:
                    ownerName = f"{yahooTeam.manager.nickname}({i})"
                yahooManagerIdToOwnerMap[yahooTeam.manager.manager_id] = Owner(name=ownerName)
                yahooOwnerTeamNames.append(ownerName)
            cls.__yahooManagerIdToOwnerMap = yahooManagerIdToOwnerMap

    @classmethod
    def __getOwnerByYahooTeam(cls, yahooTeam: YahooTeam) -> Owner:
        yahooManagerId = yahooTeam.manager.manager_id
        if yahooManagerId in cls.__yahooManagerIdToOwnerMap:
            return cls.__yahooManagerIdToOwnerMap[yahooManagerId]
        raise DoesNotExistException(
            f"Yahoo Manager ID {yahooManagerId} not found in saved Yahoo Manager IDs.")
