from typing import Optional

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
    __ownerNamesAndAliases = dict()
    __ESPN_WIN_OUTCOME = "W"
    __ESPN_LOSS_OUTCOME = "L"
    __ESPN_TIE_OUTCOME = "T"
    __TEAMS_IN_PLAYOFFS_TO_PLAYOFF_WEEK_COUNT_MAP = {
        2: 1,
        3: 2,
        4: 2,
        6: 3,
        7: 3,
        8: 3
    }

    @classmethod
    def loadLeague(cls, leagueId: int, years: list[int], **kwargs) -> League:
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
                if teamAScore == teamBScore and espnTeamA.outcomes[i] == cls.__ESPN_WIN_OUTCOME:
                    teamAHasTiebreaker = True
                elif teamAScore == teamBScore and espnTeamB.outcomes[i] == cls.__ESPN_WIN_OUTCOME:
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
            isPlayoffWeek = cls.__isPlayoffWeek(espnLeague, i + 1)
            weeks.append(Week(weekNumber=i + 1, matchups=matchups, isPlayoffWeek=isPlayoffWeek))
        return weeks

    @classmethod
    def __isPlayoffWeek(cls, espnLeague: ESPNLeague, weekNumber: int) -> bool:
        numberOfPlayoffWeeks = cls.__TEAMS_IN_PLAYOFFS_TO_PLAYOFF_WEEK_COUNT_MAP.get(
            espnLeague.settings.playoff_team_count, None)
        # TODO: raise exception if numberOfPlayoffWeeks is None, as this is not a number of playoff weeks that is currently supported
        numberOfWeeks = len(espnLeague.settings.matchup_periods)
        return weekNumber > numberOfWeeks - numberOfPlayoffWeeks

    @staticmethod
    def __getESPNTeamById(espnTeamId: int, espnTeams: list[ESPNTeam]) -> ESPNTeam:
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
        # TODO: Raise exception if owner not found and handle it
