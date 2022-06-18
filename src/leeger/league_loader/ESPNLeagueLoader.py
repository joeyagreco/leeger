import espn_api.football as espn
from espn_api.football import League as ESPNLeague
from espn_api.football import Team as ESPNTeam

from src.leeger.league_loader.abstract.LeagueLoader import LeagueLoader
from src.leeger.model.League import League
from src.leeger.model.Matchup import Matchup
from src.leeger.model.Owner import Owner
from src.leeger.model.Team import Team
from src.leeger.model.Week import Week
from src.leeger.model.Year import Year


class ESPNLeagueLoader(LeagueLoader):
    """
    Responsible for loading a League from ESPN Fantasy Football.
    https://www.espn.com/fantasy/football/
    """
    __owners = None
    __espnTeamIdToTeamMap = dict()
    __espnWinOutcome = "W"
    __espnLossOutcome = "L"
    __espnTieOutcome = "T"

    @classmethod
    def loadLeague(cls, leagueId: int, years: list[int]) -> League:
        espnLeagueYears = list()
        for year in years:
            espnLeagueYears.append(espn.League(league_id=leagueId, year=year))
        return cls.__buildLeague(espnLeagueYears)

    @classmethod
    def __buildLeague(cls, espnLeagues: list[ESPNLeague]) -> League:
        years = list()
        owners = None
        leagueName = None
        for espnLeague in espnLeagues:
            leagueName = espnLeague.settings.name if leagueName is None else leagueName
            owners = cls.__buildOwners(espnLeague.teams) if owners is None else owners
            years.append(cls.__buildYear(espnLeague, owners))

        return League(name=leagueName, owners=owners, years=years)

    @classmethod
    def __buildYear(cls, espnLeague: ESPNLeague, owners: list[Owner]) -> Year:
        teams = cls.__buildTeams(espnLeague.teams, owners)
        weeks = cls.__buildWeeks(espnLeague)
        return Year(yearNumber=espnLeague.year, teams=teams, weeks=weeks)

    @classmethod
    def __buildWeeks(cls, espnLeague: ESPNLeague) -> list[Week]:
        weeks = list()
        for i in range(espnLeague.current_week):  # current week seems to be the last week in the league
            # get each teams matchup for that week
            matchups = list()
            # to avoid adding matchups twice, we keep track of the ESPN team IDs that have already had a matchup added
            espnTeamIDsWithMatchups = list()
            for espnTeam in espnLeague.teams:
                if espnTeam.team_id in espnTeamIDsWithMatchups:
                    continue
                # team A is *this* team
                espnTeamA = espnTeam
                teamA = cls.__espnTeamIdToTeamMap[espnTeam.team_id]
                teamAScore = espnTeam.scores[i]
                # team B is their opponent
                espnTeamB = espnTeam.schedule[i]
                teamB = cls.__espnTeamIdToTeamMap[espnTeam.schedule[i].team_id]
                teamBScore = cls.__getESPNTeamById(espnTeam.schedule[i].team_id, espnLeague.teams).scores[i]
                # figure out tiebreakers if there needs to be one
                teamAHasTiebreaker = False
                teamBHasTiebreaker = False
                if teamAScore == teamBScore and espnTeamA.outcomes[i] == cls.__espnWinOutcome:
                    teamAHasTiebreaker = True
                elif teamAScore == teamBScore and espnTeamB.outcomes[i] == cls.__espnWinOutcome:
                    teamBHasTiebreaker = True
                matchups.append(Matchup(teamAId=teamA.id,
                                        teamBId=teamB.id,
                                        teamAScore=teamAScore,
                                        teamBScore=teamBScore,
                                        teamAHasTiebreaker=teamAHasTiebreaker,
                                        teamBHasTiebreaker=teamBHasTiebreaker))
                # TODO: figure out if this is a championship matchup
                espnTeamIDsWithMatchups.append(espnTeam.team_id)
                espnTeamIDsWithMatchups.append(espnTeam.schedule[i].team_id)
            weeks.append(Week(weekNumber=i + 1, matchups=matchups))
            # TODO: figure out if this is a playoff week
        return weeks

    @staticmethod
    def __getESPNTeamById(espnTeamId: int, espnTeams: list[ESPNTeam]) -> ESPNTeam:
        for espnTeam in espnTeams:
            if espnTeam.team_id == espnTeamId:
                return espnTeam

    @classmethod
    def __buildTeams(cls, espnTeams: list[ESPNTeam], owners: list[Owner]) -> list[Team]:
        teams = list()
        for espnTeam in espnTeams:
            owner = cls.__getOwnerByName(espnTeam.owner, owners)
            team = Team(ownerId=owner.id, name=espnTeam.team_name)
            teams.append(team)
            cls.__espnTeamIdToTeamMap[espnTeam.team_id] = team

        return teams

    @classmethod
    def __buildOwners(cls, espnTeams: list[ESPNTeam]) -> list[Owner]:
        if cls.__owners is None:
            owners = list()
            for espnTeam in espnTeams:
                owners.append(Owner(name=espnTeam.owner))
            cls.__owners = owners
        return cls.__owners

    @staticmethod
    def __getOwnerByName(ownerName: str, owners: list[Owner]) -> Owner:
        for owner in owners:
            if ownerName == owner.name:
                return owner
        # TODO: Raise exception if owner not found and handle it
