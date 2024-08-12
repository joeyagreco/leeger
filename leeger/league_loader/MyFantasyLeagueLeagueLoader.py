from typing import Optional

from pymfl.api import CommonLeagueInfoAPIClient
from pymfl.api.config import APIConfig

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


class MyFantasyLeagueLeagueLoader(LeagueLoader):
    """
    Responsible for loading a League from MyFantasyLeague.
    http://home.myfantasyleague.com/
    """

    def __init__(
        self,
        leagueId: str,
        years: list[int],
        *,
        mflUsername: str,
        mflPassword: str,
        mflUserAgentName: str,
        ownerNamesAndAliases: Optional[dict[str, list[str]]] = None,
        leagueName: Optional[str] = None,
    ):
        super().__init__(
            leagueId,
            years,
            ownerNamesAndAliases=ownerNamesAndAliases,
            leagueName=leagueName,
        )

        self.__mflUsername = mflUsername
        self.__mflPassword = mflPassword
        self.__mflUserAgentName = mflUserAgentName

        self.__mflLeagueIdToYearMap: dict[str, int] = dict()
        self.__mflFranchiseIdToOwnerMap: dict[str, Owner] = dict()
        self.__mflFranchiseIdToTeamMap: dict[int, Team] = dict()
        self.__mflDivisionIdToDivisionMap: dict[str, Division] = (
            dict()
        )  # holds the division info for ONLY the current year

    def __getAllLeagues(self) -> list[dict]:
        mflLeagues: list[dict] = list()

        for year in self._years:
            APIConfig.add_config_for_year_and_league_id(
                year=year,
                league_id=self._leagueId,
                username=self.__mflUsername,
                password=self.__mflPassword,
                user_agent_name=self.__mflUserAgentName,
            )

            mflLeague = CommonLeagueInfoAPIClient.get_league(
                year=year, league_id=self._leagueId
            )["league"]
            self.__mflLeagueIdToYearMap[mflLeague["id"]] = year
            mflLeagues.append(mflLeague)
        self._validateRetrievedLeagues(mflLeagues)
        return mflLeagues

    def getOwnerNames(self) -> dict[int, list[str]]:
        yearToOwnerNamesMap: dict[int, list[str]] = dict()
        mflLeagues = self.__getAllLeagues()
        for mflLeague in mflLeagues:
            yearNumber = self.__mflLeagueIdToYearMap[mflLeague["id"]]
            yearToOwnerNamesMap[yearNumber] = list()
            for franchise in mflLeague["franchises"]["franchise"]:
                ownerName = franchise["owner_name"]
                yearToOwnerNamesMap[yearNumber].append(ownerName)
        return yearToOwnerNamesMap

    def loadLeague(self, validate: bool = True) -> League:
        mflLeagues = self.__getAllLeagues()
        league = self.__buildLeague(mflLeagues)
        if validate:
            # validate new league
            leagueValidation.runAllChecks(league)
        self._warnForUnusedOwnerNames(league)
        return league

    def __buildLeague(self, mflLeagues: list[dict]) -> League:
        years = list()
        self.__loadOwners(mflLeagues)
        owners = list(self.__mflFranchiseIdToOwnerMap.values())
        for mflLeague in mflLeagues:
            # save league name for each year
            self._leagueNameByYear[self.__mflLeagueIdToYearMap[mflLeague["id"]]] = (
                mflLeague["name"]
            )
            years.append(self.__buildYear(mflLeague))
        return League(
            name=self._getLeagueName(), owners=owners, years=self._getValidYears(years)
        )

    def __buildYear(self, mflLeague: dict) -> Year:
        # save division info
        for division in mflLeague["divisions"]["division"]:
            self.__mflDivisionIdToDivisionMap[division["id"]] = Division(
                name=division["name"]
            )
        yearNumber = self.__mflLeagueIdToYearMap[mflLeague["id"]]
        teams = self.__buildTeams(mflLeague)
        weeks = self.__buildWeeks(mflLeague)
        # TODO: see if there are cases where MFL leagues do NOT have divisions
        year = Year(
            yearNumber=yearNumber,
            teams=teams,
            weeks=weeks,
            divisions=list(self.__mflDivisionIdToDivisionMap.values()),
        )
        # clear division info
        self.__mflDivisionIdToDivisionMap = dict()
        return year

    def __buildWeeks(self, mflLeague: dict) -> list[Week]:
        yearNumber = self.__mflLeagueIdToYearMap[mflLeague["id"]]
        weeks = list()
        schedule: dict = CommonLeagueInfoAPIClient.get_schedule(
            year=yearNumber, league_id=mflLeague["id"]
        )["schedule"]
        # get playoff brackets
        playoffBracket: dict = CommonLeagueInfoAPIClient.get_playoff_bracket(
            year=yearNumber, league_id=mflLeague["id"], bracket_id="1"
        )["playoffBracket"]

        # we will assume that the "true" playoff bracket (i.e. the bracket where the winner of it is the league champion)
        # will always be the playoff bracket with id "1".
        # if this changes or is not the case, this will need to be refactored to reflect that.
        # the reason we only care about this bracket (and not the other ones) is because we only need to know who won the championship from this info.
        # we can get all playoff matchup data from the regular schedule

        # if there is only 1 object in the playoffRound field, it is a dict, otherwise it is a list
        playoffWeeks = list()
        if isinstance(playoffBracket["playoffRound"], dict):
            # only 1 playoff round
            playoffWeeks.append(playoffBracket["playoffRound"])
        else:
            # multiple playoff rounds
            for playoffBracketInfo in playoffBracket["playoffRound"]:
                playoffWeeks.append(playoffBracketInfo)

        playoffWeekNumbers = [int(playoffWeek["week"]) for playoffWeek in playoffWeeks]

        playoffsStarted = False
        for week in schedule["weeklySchedule"]:
            weekNumber = int(week["week"])
            if weekNumber > int(mflLeague["lastRegularSeasonWeek"]):
                playoffsStarted = True
            # get each teams matchup for that week
            matchups = list()
            # skip weeks with no matchup. get() is a safe method that doesn't throw an error if the element is missing.
            local_matchups = week.get("matchup", {})
            if not local_matchups:
                break
            # Make sure that localMatchups is a list (some weeks just have a json element)
            if not (isinstance(local_matchups, list)):
                local_matchups = [local_matchups]
            for matchup in local_matchups:
                teamAMFLFranchiseId = matchup["franchise"][0]["id"]
                teamAId = self.__mflFranchiseIdToTeamMap[teamAMFLFranchiseId].id
                teamAScore = float(matchup["franchise"][0]["score"])
                teamAHasTiebreaker = matchup["franchise"][0]["result"] == "W"

                teamBMFLFranchiseId = matchup["franchise"][1]["id"]
                teamBId = self.__mflFranchiseIdToTeamMap[teamBMFLFranchiseId].id
                teamBScore = float(matchup["franchise"][1]["score"])
                teamBHasTiebreaker = matchup["franchise"][1]["result"] == "W"

                isChampionshipMatchup = False

                matchupType = MatchupType.REGULAR_SEASON
                if playoffsStarted:
                    # this is a playoff matchup or a championship matchup
                    # NOTE: If there are MFL leagues that have matchups during playoff weeks that are
                    # NOTE: NOT playoff matchups, this logic will need to be changed.
                    for playoffWeek in playoffWeeks:
                        currentIsChampionshipMatchup = self.__isChampionshipMatchup(
                            playoffWeek=playoffWeek,
                            playoffWeekNumbers=playoffWeekNumbers,
                            weekNumber=weekNumber,
                            teamAMFLFranchiseId=teamAMFLFranchiseId,
                            teamBMFLFranchiseId=teamBMFLFranchiseId,
                        )
                        isChampionshipMatchup = (
                            isChampionshipMatchup or currentIsChampionshipMatchup
                        )
                    matchupType = MatchupType.PLAYOFF
                    if isChampionshipMatchup:
                        matchupType = MatchupType.CHAMPIONSHIP

                matchups.append(
                    Matchup(
                        teamAId=teamAId,
                        teamBId=teamBId,
                        teamAScore=teamAScore,
                        teamBScore=teamBScore,
                        teamAHasTiebreaker=teamAHasTiebreaker,
                        teamBHasTiebreaker=teamBHasTiebreaker,
                        matchupType=matchupType,
                    )
                )
            if len(matchups) > 0:
                weeks.append(Week(weekNumber=weekNumber, matchups=matchups))

        return weeks

    @staticmethod
    def __isChampionshipMatchup(
        *,
        playoffWeek: dict,
        playoffWeekNumbers: list[int],
        weekNumber: int,
        teamAMFLFranchiseId: int,
        teamBMFLFranchiseId: int,
    ) -> tuple[bool, bool]:
        # helper method
        def isValid(*, pGame: dict, aId: int, bId: int) -> bool:
            return (
                aId == pGame["away"]["franchise_id"]
                or bId == pGame["away"]["franchise_id"]
            ) and (
                aId == pGame["home"]["franchise_id"]
                or bId == pGame["home"]["franchise_id"]
            )

        isChampionshipMatchup = False

        if weekNumber == max(playoffWeekNumbers):
            # this is the last week in the bracket, the championship week
            # if there is only 1 object in the playoffGame field, it is a dict, otherwise it is a list
            if isinstance(playoffWeek["playoffGame"], dict):
                # only 1 game
                # check if this matchup is the championship game
                isChampionshipMatchup = isValid(
                    pGame=playoffWeek["playoffGame"],
                    aId=teamAMFLFranchiseId,
                    bId=teamBMFLFranchiseId,
                )
            else:
                # multiple games
                # check if this matchup is the championship game
                for playoffGame in playoffWeek["playoffGame"]:
                    isChampionshipMatchup = isChampionshipMatchup or isValid(
                        pGame=playoffGame,
                        aId=teamAMFLFranchiseId,
                        bId=teamBMFLFranchiseId,
                    )
        return isChampionshipMatchup

    def __buildTeams(self, mflLeague: dict) -> list[Team]:
        teams = list()
        for franchise in mflLeague["franchises"]["franchise"]:
            # TODO: see if there are cases where MFL leagues do NOT have divisions
            divisionId = self.__mflDivisionIdToDivisionMap[franchise["division"]].id
            owner = self.__mflFranchiseIdToOwnerMap[franchise["id"]]
            team = Team(name=franchise["name"], ownerId=owner.id, divisionId=divisionId)
            self.__mflFranchiseIdToTeamMap[franchise["id"]] = team
            teams.append(team)
        return teams

    def __loadOwners(self, mflLeagues: list[dict]) -> None:
        for mflLeague in mflLeagues:
            for franchise in mflLeague["franchises"]["franchise"]:
                ownerName = franchise["owner_name"]
                # get general owner name if there is one
                generalOwnerName = self._getGeneralOwnerNameFromGivenOwnerName(
                    ownerName
                )
                ownerName = (
                    generalOwnerName if generalOwnerName is not None else ownerName
                )
                self.__mflFranchiseIdToOwnerMap[franchise["id"]] = Owner(name=ownerName)
