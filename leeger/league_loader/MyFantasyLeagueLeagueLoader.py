from typing import Optional
from pymfl.api import CommonLeagueInfoAPIClient
from pymfl.api.config import APIConfig

from leeger.enum.MatchupType import MatchupType
from leeger.league_loader.LeagueLoader import LeagueLoader
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
    ):
        super().__init__(leagueId, years, ownerNamesAndAliases=ownerNamesAndAliases)

        self.__mflUsername = mflUsername
        self.__mflPassword = mflPassword
        self.__mflUserAgentName = mflUserAgentName

        self.__mflLeagueIdToYearMap: dict[str, int] = dict()
        self.__mflFranchiseIdToOwnerMap: dict[str, Owner] = dict()
        self.__mflFranchiseIdToTeamMap: dict[int, Team] = dict()

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

            mflLeague = CommonLeagueInfoAPIClient.get_league(year=year, league_id=self._leagueId)[
                "league"
            ]
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
        return league

    def __buildLeague(self, mflLeagues: list[dict]) -> League:
        years = list()
        leagueName = None
        self.__loadOwners(mflLeagues)
        owners = list(self.__mflFranchiseIdToOwnerMap.values())
        for mflLeague in mflLeagues:
            leagueName = mflLeague["name"] if mflLeague["name"] is not None else leagueName
            year = self.__buildYear(mflLeague)
            if len(year.weeks) > 0:
                years.append(year)
            else:
                self._LOGGER.warning(
                    f"Year '{year.yearNumber}' discarded for not having any weeks."
                )
        return League(name=leagueName, owners=owners, years=years)

    def __buildYear(self, mflLeague: dict) -> Year:
        yearNumber = self.__mflLeagueIdToYearMap[mflLeague["id"]]
        teams = self.__buildTeams(mflLeague)
        weeks = self.__buildWeeks(mflLeague)
        return Year(yearNumber=yearNumber, teams=teams, weeks=weeks)

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
            for matchup in week["matchup"]:
                teamAMFLFranchiseId = matchup["franchise"][0]["id"]
                teamAId = self.__mflFranchiseIdToTeamMap[teamAMFLFranchiseId].id
                teamAScore = float(matchup["franchise"][0]["score"])
                teamAHasTiebreaker = matchup["franchise"][0]["result"] == "W"

                teamBMFLFranchiseId = matchup["franchise"][1]["id"]
                teamBId = self.__mflFranchiseIdToTeamMap[teamBMFLFranchiseId].id
                teamBScore = float(matchup["franchise"][1]["score"])
                teamBHasTiebreaker = matchup["franchise"][1]["result"] == "W"

                validPlayoffMatchup = False
                validChampionshipMatchup = False

                matchupType = MatchupType.REGULAR_SEASON
                if playoffsStarted:
                    # this is a playoff matchup or a championship matchup
                    for playoffWeek in playoffWeeks:
                        (
                            currentValidPlayoffMatchup,
                            currentValidChampionshipMatchup,
                        ) = self.__getPlayoffMatchupBooleansForPlayoffWeek(
                            playoffWeek=playoffWeek,
                            playoffWeekNumbers=playoffWeekNumbers,
                            weekNumber=weekNumber,
                            teamAMFLFranchiseId=teamAMFLFranchiseId,
                            teamBMFLFranchiseId=teamBMFLFranchiseId,
                        )
                        validPlayoffMatchup = validPlayoffMatchup or currentValidPlayoffMatchup
                        validChampionshipMatchup = (
                            validChampionshipMatchup or currentValidChampionshipMatchup
                        )
                    matchupType = MatchupType.IGNORE
                    if validPlayoffMatchup:
                        matchupType = MatchupType.PLAYOFF
                    if validChampionshipMatchup:
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
    def __getPlayoffMatchupBooleansForPlayoffWeek(
        *,
        playoffWeek: dict,
        playoffWeekNumbers: list[int],
        weekNumber: int,
        teamAMFLFranchiseId: int,
        teamBMFLFranchiseId: int,
    ) -> tuple[bool, bool]:
        """
        Will return 2 booleans.
        validPlayoffMatchup, validChampionshipMatchup
        """

        # helper method
        def isValid(*, pGame: dict, aId: int, bId: int) -> bool:
            return (
                aId == pGame["away"]["franchise_id"] or bId == pGame["away"]["franchise_id"]
            ) and (aId == pGame["home"]["franchise_id"] or bId == pGame["home"]["franchise_id"])

        # this is a playoff matchup or a championship matchup
        validPlayoffMatchup = False
        validChampionshipMatchup = False

        if weekNumber == max(playoffWeekNumbers):
            # this is the last week in the bracket, the championship week
            # if there is only 1 object in the playoffGame field, it is a dict, otherwise it is a list
            if isinstance(playoffWeek["playoffGame"], dict):
                # only 1 game
                # check if this matchup is the championship game
                validChampionshipMatchup = isValid(
                    pGame=playoffWeek["playoffGame"],
                    aId=teamAMFLFranchiseId,
                    bId=teamBMFLFranchiseId,
                )
            else:
                # multiple games
                # check if this matchup is the championship game
                for playoffGame in playoffWeek["playoffGame"]:
                    validChampionshipMatchup = validChampionshipMatchup or isValid(
                        pGame=playoffGame, aId=teamAMFLFranchiseId, bId=teamBMFLFranchiseId
                    )
        else:
            # playoff week, but not the championship week
            # if there is only 1 object in the playoffGame field, it is a dict, otherwise it is a list
            if isinstance(playoffWeek["playoffGame"], dict):
                # only 1 game
                # check if this matchup is a valid playoff matchup
                validPlayoffMatchup = isValid(
                    pGame=playoffWeek["playoffGame"],
                    aId=teamAMFLFranchiseId,
                    bId=teamBMFLFranchiseId,
                )
            else:
                # multiple games
                for playoffGame in playoffWeek["playoffGame"]:
                    # check if this matchup is a valid playoff matchup
                    validPlayoffMatchup = validPlayoffMatchup or isValid(
                        pGame=playoffGame, aId=teamAMFLFranchiseId, bId=teamBMFLFranchiseId
                    )
        return validPlayoffMatchup, validChampionshipMatchup

    def __buildTeams(self, mflLeague: dict) -> list[Team]:
        teams = list()
        for franchise in mflLeague["franchises"]["franchise"]:
            owner = self.__mflFranchiseIdToOwnerMap[franchise["id"]]
            team = Team(name=franchise["name"], ownerId=owner.id)
            self.__mflFranchiseIdToTeamMap[franchise["id"]] = team
            teams.append(team)
        return teams

    def __loadOwners(self, mflLeagues: list[dict]) -> None:
        for mflLeague in mflLeagues:
            for franchise in mflLeague["franchises"]["franchise"]:
                ownerName = franchise["owner_name"]
                # get general owner name if there is one
                generalOwnerName = self._getGeneralOwnerNameFromGivenOwnerName(ownerName)
                ownerName = generalOwnerName if generalOwnerName is not None else ownerName
                self.__mflFranchiseIdToOwnerMap[franchise["id"]] = Owner(name=ownerName)
