import multiprocessing
import subprocess
from typing import Optional

from yahoofantasy import Context as YahooContext
from yahoofantasy import League as YahooLeague
from yahoofantasy import Matchup as YahooMatchup
from yahoofantasy import Team as YahooTeam
from yahoofantasy import Week as YahooWeek

from leeger.enum.MatchupType import MatchupType
from leeger.exception.DoesNotExistException import DoesNotExistException
from leeger.league_loader.LeagueLoader import LeagueLoader
from leeger.model.league.League import League
from leeger.model.league.Matchup import Matchup
from leeger.model.league.Owner import Owner
from leeger.model.league.Team import Team
from leeger.model.league.Week import Week
from leeger.model.league.Year import Year
from leeger.validate import leagueValidation


class YahooLeagueLoader(LeagueLoader):
    """
    Responsible for loading a League from Yahoo Fantasy Football.
    https://football.fantasysports.yahoo.com/
    """

    __NFL = "nfl"

    def __init__(
        self,
        leagueId: str,
        years: list[int],
        *,
        clientId: str,
        clientSecret: str,
        loginTimeoutSeconds: Optional[int] = 20,
        ownerNamesAndAliases: Optional[dict[str, list[str]]] = None,
    ):
        # validation
        try:
            int(leagueId)
        except ValueError:
            raise ValueError(f"League ID '{leagueId}' could not be turned into an int.")
        super().__init__(leagueId, years, ownerNamesAndAliases=ownerNamesAndAliases)
        self.__clientId = clientId
        self.__clientSecret = clientSecret
        self.__timeoutSeconds = loginTimeoutSeconds
        self.__yahooManagerIdToOwnerMap: dict[int, Owner] = dict()
        self.__yahooTeamIdToTeamMap: dict[str, Team] = dict()
        self.__yearToTeamIdHasLostInPlayoffs: dict[int, dict[int, bool]] = dict()

    @classmethod
    def __login(cls, clientId: str, clientSecret: str) -> None:
        """
        Logs in via Yahoo OAuth.
        Will open up a browser window.
        """
        CLIENT_ID_OPTION = "--client-id"
        CLIENT_SECRET_OPTION = "--client-secret"
        subprocess.call(
            [
                "yahoofantasy",
                "login",
                CLIENT_ID_OPTION,
                clientId,
                CLIENT_SECRET_OPTION,
                clientSecret,
            ]
        )

    def __getAllLeagues(self) -> list[YahooLeague]:
        loginProcess = multiprocessing.Process(
            target=self.__login, args=(self.__clientId, self.__clientSecret)
        )
        loginProcess.start()
        loginProcess.join(self.__timeoutSeconds)
        if loginProcess.is_alive():
            loginProcess.terminate()
            raise TimeoutError("Login to yahoofantasy timed out.")
        yahooContext = YahooContext()
        yahooLeagues = list()
        nextLeagueId = self._leagueId
        remainingYears = self._years.copy()
        foundYears = list()
        while len(remainingYears) > 0 and nextLeagueId is not None:
            # get all leagues this user was in for this year
            currentYear = remainingYears[0]
            leagues = yahooContext.get_leagues(self.__NFL, currentYear)
            # find the league ID we want
            for league in leagues:
                if str(league.league_id) == nextLeagueId:
                    yahooLeagues.append(league)
                    foundYears.append(currentYear)
                    nextLeagueId = league.renew
                    if nextLeagueId is not None:
                        nextLeagueId = str(nextLeagueId)[3:]
                        break
            remainingYears.pop(0)

        if len(yahooLeagues) != len(self._years):
            # TODO: Give a more descriptive // accurate error message
            raise DoesNotExistException(
                f"Found years {foundYears}, expected to find {self._years}."
            )
        return yahooLeagues

    def getOwnerNames(self) -> dict[int, list[str]]:
        yearToOwnerNamesMap: dict[int, list[str]] = dict()
        yahooLeagues = self.__getAllLeagues()
        for yahooLeague in yahooLeagues:
            yearToOwnerNamesMap[yahooLeague.season] = list()
            yahooTeams = yahooLeague.teams()
            for yahooTeam in yahooTeams:
                ownerName = yahooTeam.manager.nickname
                yearToOwnerNamesMap[yahooLeague.season].append(ownerName)
        return yearToOwnerNamesMap

    def loadLeague(self, validate: bool = True) -> League:
        yahooLeagues = self.__getAllLeagues()
        league = self.__buildLeague(yahooLeagues)
        if validate:
            # validate new league
            leagueValidation.runAllChecks(league)
        return league

    def __buildLeague(self, yahooLeagues: list[YahooLeague]) -> League:
        years = list()
        leagueName = None
        for yahooLeague in yahooLeagues:
            leagueName = yahooLeague.name if leagueName is None else leagueName
            self.__loadOwners(yahooLeague.teams())
            years.append(self.__buildYear(yahooLeague))
        return League(
            name=leagueName, owners=list(self.__yahooManagerIdToOwnerMap.values()), years=years
        )

    def __buildYear(self, yahooLeague: YahooLeague) -> Year:
        self.__yearToTeamIdHasLostInPlayoffs[yahooLeague.season] = dict()
        teams = self.__buildTeams(yahooLeague.teams())
        weeks = self.__buildWeeks(yahooLeague)
        return Year(yearNumber=yahooLeague.season, teams=teams, weeks=weeks)

    def __buildWeeks(self, yahooLeague: YahooLeague) -> list[Week]:
        weeks = list()
        for i in range(
            yahooLeague.current_week
        ):  # current week seems to be the last week in the league
            yahooWeek: YahooWeek = yahooLeague.weeks()[i]
            # get each teams matchup for that week
            matchups = list()
            # only get matchups that are completed
            validMatchups = [m for m in yahooWeek.matchups if m.status == "postevent"]
            for yahooMatchup in validMatchups:
                # team A is *this* team
                yahooTeamA = yahooMatchup.team1
                teamA = self.__yahooTeamIdToTeamMap[yahooMatchup.team1.team_id]
                teamAScore = yahooMatchup.teams.team[0].team_points.total
                # team B is their opponent
                yahooTeamB = yahooMatchup.team2
                teamB = self.__yahooTeamIdToTeamMap[yahooMatchup.team2.team_id]
                teamBScore = yahooMatchup.teams.team[1].team_points.total
                # figure out tiebreakers if there needs to be one
                teamAHasTiebreaker = False
                teamBHasTiebreaker = False
                if yahooMatchup.is_tied == 0:
                    # non-tied matchup
                    teamAHasTiebreaker = yahooMatchup.winner_team_key == yahooTeamA.team_key
                    teamBHasTiebreaker = yahooMatchup.winner_team_key == yahooTeamB.team_key
                matchupType = self.__getMatchupType(yahooMatchup)
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
            if len(matchups) > 0:
                weeks.append(Week(weekNumber=i + 1, matchups=matchups))
        return weeks

    def __getMatchupType(self, yahooMatchup: YahooMatchup) -> MatchupType:
        team1Id = yahooMatchup.team1.team_id
        team2Id = yahooMatchup.team2.team_id
        # check if this is a playoff week
        if yahooMatchup.is_playoffs == 1:
            # figure out if this is the last week of playoffs (the championship week)
            if yahooMatchup.week == yahooMatchup.league.end_week:
                # this is the championship week
                # figure out if either team has lost in the playoffs yet
                if (
                    team1Id in self.__yearToTeamIdHasLostInPlayoffs[yahooMatchup.league.season]
                    and not self.__yearToTeamIdHasLostInPlayoffs[yahooMatchup.league.season][
                        team1Id
                    ]
                    and team2Id in self.__yearToTeamIdHasLostInPlayoffs[yahooMatchup.league.season]
                    and not self.__yearToTeamIdHasLostInPlayoffs[yahooMatchup.league.season][
                        team2Id
                    ]
                    and yahooMatchup.is_consolation == 0
                ):
                    return MatchupType.CHAMPIONSHIP
            # update class dict with the team that lost
            for yahooTeamResult in yahooMatchup.teams.team:
                if yahooTeamResult.win_probability == 0:
                    self.__yearToTeamIdHasLostInPlayoffs[yahooMatchup.league.season][
                        yahooTeamResult.team_id
                    ] = True
                elif yahooTeamResult.win_probability == 1:
                    self.__yearToTeamIdHasLostInPlayoffs[yahooMatchup.league.season][
                        yahooTeamResult.team_id
                    ] = False
            return MatchupType.PLAYOFF
        else:
            return MatchupType.REGULAR_SEASON

    def __buildTeams(self, yahooTeams: list[YahooTeam]) -> list[Team]:
        teams = list()
        for yahooTeam in yahooTeams:
            owner = self.__getOwnerByYahooTeam(yahooTeam)
            team = Team(ownerId=owner.id, name=yahooTeam.name)
            teams.append(team)
            self.__yahooTeamIdToTeamMap[yahooTeam.team_id] = team
        return teams

    def __loadOwners(self, yahooTeams: list[YahooTeam]) -> None:
        if len(self.__yahooManagerIdToOwnerMap.values()) == 0:
            yahooManagerIdToOwnerMap = dict()
            yahooOwnerTeamNames = list()
            for yahooTeam in yahooTeams:
                ownerName = yahooTeam.manager.nickname
                # get general owner name if there is one
                generalOwnerName = self._getGeneralOwnerNameFromGivenOwnerName(ownerName)
                ownerName = generalOwnerName if generalOwnerName is not None else ownerName
                # prevent duplicate owner names
                i = 2
                while ownerName in yahooOwnerTeamNames:
                    ownerName = f"{yahooTeam.manager.nickname}({i})"
                yahooManagerIdToOwnerMap[yahooTeam.manager.manager_id] = Owner(name=ownerName)
                yahooOwnerTeamNames.append(ownerName)
            self.__yahooManagerIdToOwnerMap = yahooManagerIdToOwnerMap

    def __getOwnerByYahooTeam(self, yahooTeam: YahooTeam) -> Owner:
        yahooManagerId = yahooTeam.manager.manager_id
        if yahooManagerId in self.__yahooManagerIdToOwnerMap:
            return self.__yahooManagerIdToOwnerMap[yahooManagerId]
        raise DoesNotExistException(
            f"Yahoo Manager ID {yahooManagerId} not found in saved Yahoo Manager IDs."
        )
