from typing import Optional

import espn_api.football as espn
from espn_api.football import League as ESPNLeague
from espn_api.football import Team as ESPNTeam

from leeger.enum.MatchupType import MatchupType
from leeger.league_loader.LeagueLoader import LeagueLoader
from leeger.model.league.Division import Division
from leeger.model.league.League import League
from leeger.model.league.Matchup import Matchup
from leeger.model.league.Owner import Owner
from leeger.model.league.Team import Team
from leeger.model.league.Week import Week
from leeger.model.league.Year import Year
from leeger.validate import leagueValidation


class ESPNLeagueLoader(LeagueLoader):
    """
    Responsible for loading a League from ESPN Fantasy Football.
    https://www.espn.com/fantasy/football/
    """

    __ESPN_WIN_OUTCOME: str = "W"
    __ESPN_LOSS_OUTCOME: str = "L"
    __ESPN_BYE_OUTCOME: str = "U"
    __TEAMS_IN_PLAYOFFS_TO_PLAYOFF_WEEK_COUNT_MAP: dict[int, int] = {
        2: 1,
        3: 2,
        4: 2,
        6: 3,
        7: 3,
        8: 3,
    }

    def __init__(
        self,
        leagueId: str,
        years: list[int],
        *,
        espnS2: str = None,
        swid: str = None,
        ownerNamesAndAliases: Optional[dict[str, list[str]]] = None,
        leagueName: Optional[str] = None,
    ):
        # validation
        try:
            int(leagueId)
        except ValueError:
            raise ValueError(f"League ID '{leagueId}' could not be turned into an int.")
        super().__init__(
            leagueId, years, ownerNamesAndAliases=ownerNamesAndAliases, leagueName=leagueName
        )

        self.__espnS2 = espnS2
        self.__swid = swid
        self.__espnTeamIdToTeamMap: dict[str, Team] = dict()
        self.__espnDivisionIdToDivisionMap: dict[
            int, Division
        ] = dict()  # holds the division info for ONLY the current year

    def __getAllLeagues(self) -> list[ESPNLeague]:
        espnLeagueYears = list()
        for year in self._years:
            espnLeagueYears.append(
                espn.League(
                    league_id=int(self._leagueId),
                    year=year,
                    espn_s2=self.__espnS2,
                    swid=self.__swid,
                )
            )
        self._validateRetrievedLeagues(espnLeagueYears)
        return espnLeagueYears

    def getOwnerNames(self) -> dict[int, list[str]]:
        yearToOwnerNamesMap: dict[int, list[str]] = dict()
        espnLeagueYears = self.__getAllLeagues()
        for espnLeagueYear in espnLeagueYears:
            yearToOwnerNamesMap[espnLeagueYear.year] = list()
            for espnTeam in espnLeagueYear.teams:
                yearToOwnerNamesMap[espnLeagueYear.year].append(espnTeam.owner)
        return yearToOwnerNamesMap

    def loadLeague(self, validate: bool = True) -> League:
        espnLeagueYears = self.__getAllLeagues()
        league = self.__buildLeague(espnLeagueYears)
        if validate:
            # validate new league
            leagueValidation.runAllChecks(league)
        self._warnForUnusedOwnerNames(league)
        return league

    def __buildLeague(self, espnLeagues: list[ESPNLeague]) -> League:
        years = list()
        for espnLeague in espnLeagues:
            # save league name for each year
            self._leagueNameByYear[espnLeague.year] = espnLeague.settings.name
            self.__loadOwners(espnLeague.teams)
            years.append(self.__buildYear(espnLeague))
        return League(
            name=self._getLeagueName(), owners=self._owners, years=self._getValidYears(years)
        )

    def __loadOwners(self, espnTeams: list[ESPNTeam]) -> None:
        if self._owners is None:
            owners = list()
            for espnTeam in espnTeams:
                # get general owner name if there is one
                generalOwnerName = self._getGeneralOwnerNameFromGivenOwnerName(espnTeam.owner)
                ownerName = generalOwnerName if generalOwnerName is not None else espnTeam.owner
                owners.append(Owner(name=ownerName))
            self._owners = owners

    def __buildYear(self, espnLeague: ESPNLeague) -> Year:
        # save division info
        for espnDivisionId, espnDivisionName in espnLeague.settings.division_map.items():
            self.__espnDivisionIdToDivisionMap[espnDivisionId] = Division(name=espnDivisionName)
        teams = self.__buildTeams(espnLeague.teams)
        weeks = self.__buildWeeks(espnLeague)
        # TODO: see if there are cases where ESPN leagues do NOT have divisions
        year = Year(
            yearNumber=espnLeague.year,
            teams=teams,
            weeks=weeks,
            divisions=list(self.__espnDivisionIdToDivisionMap.values()),
        )
        # clear division info
        self.__espnDivisionIdToDivisionMap = dict()
        return year

    def __buildWeeks(self, espnLeague: ESPNLeague) -> list[Week]:
        weeks = list()
        # current week seems to be the last week in the league
        for i in range(espnLeague.current_week):
            # get each teams matchup for that week
            matchups = list()
            # to avoid adding matchups twice, we keep track of the ESPN team IDs that have already had a matchup added
            espnTeamIDsWithMatchups = list()
            for espnTeam in espnLeague.teams:
                # skip if we already have this team in a matchup
                # OR
                # this team is on a bye
                if (
                    espnTeam.team_id in espnTeamIDsWithMatchups
                    or espnTeam.outcomes[i] == self.__ESPN_BYE_OUTCOME
                ):
                    continue
                # team A is *this* team
                espnTeamA = espnTeam
                teamA = self.__espnTeamIdToTeamMap[espnTeam.team_id]
                teamAScore = espnTeam.scores[i]
                # team B is their opponent
                espnTeamB = espnTeam.schedule[i]
                teamB = self.__espnTeamIdToTeamMap[espnTeam.schedule[i].team_id]
                teamBScore = self.__getESPNTeamByESPNId(
                    espnTeam.schedule[i].team_id, espnLeague.teams
                ).scores[i]
                # figure out tiebreakers if there needs to be one
                teamAHasTiebreaker = (
                    teamAScore == teamBScore and espnTeamA.outcomes[i] == self.__ESPN_WIN_OUTCOME
                )
                teamBHasTiebreaker = (
                    teamAScore == teamBScore and espnTeamB.outcomes[i] == self.__ESPN_WIN_OUTCOME
                )
                matchupType = self.__getMatchupType(espnLeague, i + 1, espnTeamA.team_id)
                matchups.append(
                    Matchup(
                        teamAId=teamA.id,
                        teamBId=teamB.id,
                        teamAScore=teamAScore,
                        teamBScore=teamBScore,
                        teamAHasTiebreaker=teamAHasTiebreaker,
                        teamBHasTiebreaker=teamBHasTiebreaker,
                        matchupType=matchupType,
                    )
                )
                espnTeamIDsWithMatchups.append(espnTeam.team_id)
                espnTeamIDsWithMatchups.append(espnTeam.schedule[i].team_id)
            if len(matchups) > 0:
                weeks.append(Week(weekNumber=i + 1, matchups=matchups))
        return weeks

    def __getMatchupType(
        self, espnLeague: ESPNLeague, weekNumber: int, espnTeamId: int
    ) -> MatchupType:
        isPlayoffWeek = weekNumber > espnLeague.settings.reg_season_count
        if isPlayoffWeek:
            # figure out if this team made the playoffs
            playoffTeamCount = espnLeague.settings.playoff_team_count
            espnTeam = self.__getESPNTeamByESPNId(espnTeamId, espnLeague.teams)
            if playoffTeamCount >= espnTeam.standing:
                # this team made the playoffs
                # figure out if this is the last week of playoffs (the championship week)
                numberOfPlayoffWeeks = self.__TEAMS_IN_PLAYOFFS_TO_PLAYOFF_WEEK_COUNT_MAP[
                    playoffTeamCount
                ]
                # TODO: Raise specific exception here if not found in map
                if weekNumber == espnLeague.settings.reg_season_count + numberOfPlayoffWeeks:
                    # this is the championship week
                    # figure out if this team has lost in the playoffs before this week
                    playoffOutcomes = espnTeam.outcomes[-numberOfPlayoffWeeks:-1]
                    hasLostInPlayoffs = self.__ESPN_LOSS_OUTCOME in playoffOutcomes
                    if hasLostInPlayoffs:
                        return MatchupType.PLAYOFF
                    else:
                        return MatchupType.CHAMPIONSHIP
                else:
                    # this is a non-championship playoff week
                    return MatchupType.PLAYOFF
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

    def __buildTeams(self, espnTeams: list[ESPNTeam]) -> list[Team]:
        teams = list()
        for espnTeam in espnTeams:
            # TODO: see if there are cases where ESPN leagues do NOT have divisions
            divisionId = self.__espnDivisionIdToDivisionMap[espnTeam.division_id].id
            owner = self._getOwnerByName(espnTeam.owner)
            team = Team(ownerId=owner.id, name=espnTeam.team_name, divisionId=divisionId)
            teams.append(team)
            self.__espnTeamIdToTeamMap[espnTeam.team_id] = team
        return teams
