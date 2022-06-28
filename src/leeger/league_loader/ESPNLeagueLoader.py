from typing import Optional

import espn_api.football as espn
from espn_api.football import League as ESPNLeague
from espn_api.football import Team as ESPNTeam

from src.leeger.enum.MatchupType import MatchupType
from src.leeger.exception.DoesNotExistException import DoesNotExistException
from src.leeger.league_loader.abstract.LeagueLoader import LeagueLoader
from src.leeger.model.league.League import League
from src.leeger.model.league.Matchup import Matchup
from src.leeger.model.league.Owner import Owner
from src.leeger.model.league.Team import Team
from src.leeger.model.league.Week import Week
from src.leeger.model.league.Year import Year


class ESPNLeagueLoader(LeagueLoader):
    """
    Responsible for loading a League from ESPN Fantasy Football.
    https://www.espn.com/fantasy/football/
    """
    __ESPN_WIN_OUTCOME: str = "W"
    __ESPN_LOSS_OUTCOME: str = "L"
    __ESPN_TIE_OUTCOME: str = "T"
    __TEAMS_IN_PLAYOFFS_TO_PLAYOFF_WEEK_COUNT_MAP: dict[int, int] = {
        2: 1,
        3: 2,
        4: 2,
        6: 3,
        7: 3,
        8: 3
    }

    @classmethod
    def __initializeClassVariables(cls) -> None:
        cls.__owners: Optional[list[Owner]] = None
        cls.__espnTeamIdToTeamMap: dict[str, Team] = dict()
        cls.__ownerNamesAndAliases: dict[str, list[str]] = dict()

    @classmethod
    def loadLeague(cls, leagueId: int, years: list[int], **kwargs) -> League:
        cls.__initializeClassVariables()
        # owners may have multiple names across different years,
        # defining owner names and aliases allows users to have multiple names that can belong to the same owner.
        # this prevents issues where an owner with a name change across years is counted as 2 different owners.
        # this should be formatted like so:
        # ownerNamesAndAliases = {"someOwnerNameIWant": ["alias1", "alias2"],
        #                           someOtherOwnerNameIWant: ["alias3", "alias4"]}
        cls.__ownerNamesAndAliases = kwargs.get("ownerNamesAndAliases", dict())
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
            cls.__loadOwners(espnLeague.teams)
            years.append(cls.__buildYear(espnLeague))

        return League(name=leagueName, owners=cls.__owners, years=years)

    @classmethod
    def __buildYear(cls, espnLeague: ESPNLeague) -> Year:
        teams = cls.__buildTeams(espnLeague.teams)
        weeks = cls.__buildWeeks(espnLeague)
        return Year(yearNumber=espnLeague.year, teams=teams, weeks=weeks)

    @classmethod
    def __buildWeeks(cls, espnLeague: ESPNLeague) -> list[Week]:
        weeks = list()
        for i in range(espnLeague.current_week):  # current week seems to be the last week in the test_league
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
                teamBScore = cls.__getESPNTeamByESPNId(espnTeam.schedule[i].team_id, espnLeague.teams).scores[i]
                # figure out tiebreakers if there needs to be one
                teamAHasTiebreaker = teamAScore == teamBScore and espnTeamA.outcomes[i] == cls.__ESPN_WIN_OUTCOME
                teamBHasTiebreaker = teamAScore == teamBScore and espnTeamB.outcomes[i] == cls.__ESPN_WIN_OUTCOME
                matchupType = cls.__getMatchupType(espnLeague, i + 1, espnTeamA.team_id)
                matchups.append(Matchup(teamAId=teamA.id,
                                        teamBId=teamB.id,
                                        teamAScore=teamAScore,
                                        teamBScore=teamBScore,
                                        teamAHasTiebreaker=teamAHasTiebreaker,
                                        teamBHasTiebreaker=teamBHasTiebreaker,
                                        matchupType=matchupType))
                espnTeamIDsWithMatchups.append(espnTeam.team_id)
                espnTeamIDsWithMatchups.append(espnTeam.schedule[i].team_id)
            weeks.append(Week(weekNumber=i + 1, matchups=matchups))
        return weeks

    @classmethod
    def __getMatchupType(cls, espnLeague: ESPNLeague, weekNumber: int, espnTeamId: int) -> MatchupType:
        isPlayoffWeek = weekNumber > espnLeague.settings.reg_season_count
        if isPlayoffWeek:
            # figure out if this team made the playoffs
            playoffTeamCount = espnLeague.settings.playoff_team_count
            espnTeam = cls.__getESPNTeamByESPNId(espnTeamId, espnLeague.teams)
            if playoffTeamCount >= espnTeam.standing:
                # this team made the playoffs
                # figure out if this is the last week of playoffs (the championship week)
                numberOfPlayoffWeeks = cls.__TEAMS_IN_PLAYOFFS_TO_PLAYOFF_WEEK_COUNT_MAP[playoffTeamCount]
                # TODO: Raise specific exception here if not found in map
                if weekNumber == espnLeague.settings.reg_season_count + numberOfPlayoffWeeks:
                    # this is the championship week
                    # figure out if this team has lost in the playoffs yet
                    playoffOutcomes = espnTeam.outcomes[-numberOfPlayoffWeeks:]
                    hasLostInPlayoffs = playoffOutcomes.count(cls.__ESPN_WIN_OUTCOME) != len(playoffOutcomes)
                    if hasLostInPlayoffs:
                        return MatchupType.PLAYOFF
                    else:
                        return MatchupType.CHAMPIONSHIP
            else:
                # this matchup was played by teams that missed the playoffs during a playoff week.
                # ignore it.
                return MatchupType.IGNORE
        else:
            return MatchupType.REGULAR_SEASON

    @staticmethod
    def __getESPNTeamByESPNId(espnTeamId: int, espnTeams: list[ESPNTeam]) -> ESPNTeam:
        for espnTeam in espnTeams:
            if espnTeam.team_id == espnTeamId:
                return espnTeam

    @classmethod
    def __buildTeams(cls, espnTeams: list[ESPNTeam]) -> list[Team]:
        teams = list()
        for espnTeam in espnTeams:
            owner = cls.__getOwnerByName(espnTeam.owner)
            team = Team(ownerId=owner.id, name=espnTeam.team_name)
            teams.append(team)
            cls.__espnTeamIdToTeamMap[espnTeam.team_id] = team

        return teams

    @classmethod
    def __loadOwners(cls, espnTeams: list[ESPNTeam]) -> None:
        if cls.__owners is None:
            owners = list()
            for espnTeam in espnTeams:
                # get general owner name if there is one
                generalOwnerName = cls.__getGeneralOwnerNameFromGivenOwnerName(espnTeam.owner)
                ownerName = generalOwnerName if generalOwnerName is not None else espnTeam.owner
                owners.append(Owner(name=ownerName))
            cls.__owners = owners

    @classmethod
    def __getGeneralOwnerNameFromGivenOwnerName(cls, givenOwnerName: str) -> Optional[str]:
        foundGeneralOwnerName = None
        for generalOwnerName, aliases in cls.__ownerNamesAndAliases.items():
            if givenOwnerName in aliases:
                foundGeneralOwnerName = generalOwnerName
                break
        return foundGeneralOwnerName

    @classmethod
    def __getOwnerByName(cls, ownerName: str) -> Owner:
        generalOwnerName = cls.__getGeneralOwnerNameFromGivenOwnerName(ownerName)
        for owner in cls.__owners:
            if ownerName == owner.name or generalOwnerName == owner.name:
                return owner
        raise DoesNotExistException(
            f"Owner name '{ownerName}' does not match any previously loaded owner names. To add multiple names for a single owner, use the 'ownerNamesAndAliases' keyword argument to define them.")
