import itertools
from typing import Optional

from sleeper.api import LeagueAPIClient
from sleeper.enum import Sport as SleeperSport
from sleeper.enum import SeasonStatus as SleeperSeasonStatus
from sleeper.enum import PlayoffRoundType as SleeperPlayoffRoundType
from sleeper.model import League as SleeperLeague
from sleeper.model import Matchup as SleeperMatchup
from sleeper.model import PlayoffMatchup as SleeperPlayoffMatchup
from sleeper.model import User as SleeperUser
from sleeper.model import SportState as SleeperSportState

from leeger.enum.MatchupType import MatchupType
from leeger.exception.DoesNotExistException import DoesNotExistException
from leeger.league_loader.LeagueLoader import LeagueLoader
from leeger.model.league import YearSettings
from leeger.model.league.League import League
from leeger.model.league.Matchup import Matchup
from leeger.model.league.Owner import Owner
from leeger.model.league.Team import Team
from leeger.model.league.Week import Week
from leeger.model.league.Year import Year
from leeger.validate import leagueValidation
from leeger.exception.LeagueLoaderException import LeagueLoaderException


class SleeperLeagueLoader(LeagueLoader):
    """
    Responsible for loading a League from Sleeper Fantasy Football.
    https://sleeper.com/
    """

    __INVALID_SLEEPER_LEAGUE_IDS = [None, "0"]
    __SLEEPER_USERS_BY_LEAGUE_ID_CACHE = dict()  # functions as a cache for Sleeper Users
    __SLEEPER_SPORT_STATE_CACHE: SleeperSportState = (
        None  # functions as a cache for Sleeper SportState
    )

    def __init__(
        self,
        mostRecentLeagueId: str,
        years: list[int],
        *,
        ownerNamesAndAliases: Optional[dict[str, list[str]]] = None,
    ):
        super().__init__(mostRecentLeagueId, years, ownerNamesAndAliases=ownerNamesAndAliases)

        self.__sleeperUserIdToOwnerMap: dict[str, Owner] = dict()
        self.__sleeperRosterIdToTeamMap: dict[int, Team] = dict()

    def __resetCaches(self) -> None:
        self.__SLEEPER_USERS_BY_LEAGUE_ID_CACHE = dict()
        self.__SLEEPER_SPORT_STATE_CACHE = None

    def __getSleeperUsers(self, leagueId: str) -> list[SleeperUser]:
        if leagueId not in self.__SLEEPER_USERS_BY_LEAGUE_ID_CACHE:
            # don't have these users loaded yet
            sleeperUsers = LeagueAPIClient.get_users_in_league(league_id=leagueId)
            self.__SLEEPER_USERS_BY_LEAGUE_ID_CACHE[leagueId] = sleeperUsers
            return sleeperUsers
        # do have these users loaded
        return self.__SLEEPER_USERS_BY_LEAGUE_ID_CACHE[leagueId]

    @classmethod
    def __getSleeperSportState(cls):
        if cls.__SLEEPER_SPORT_STATE_CACHE is None:
            cls.__SLEEPER_SPORT_STATE_CACHE = LeagueAPIClient.get_sport_state(
                sport=SleeperSport.NFL
            )
        return cls.__SLEEPER_SPORT_STATE_CACHE

    def __getAllLeagues(self) -> list[SleeperLeague]:
        sleeperLeagues = list()
        years = self._years.copy()
        currentLeagueId = self._leagueId
        while len(years) > 0 and currentLeagueId not in self.__INVALID_SLEEPER_LEAGUE_IDS:
            currentLeague: SleeperLeague = LeagueAPIClient.get_league(league_id=currentLeagueId)
            if int(currentLeague.season) in years:
                # we only want to add valid seasons
                # NOTE: Not sure if we want to include SleeperSeasonStatus.POSTPONED here or not
                if currentLeague.status not in (
                    SleeperSeasonStatus.COMPLETE,
                    SleeperSeasonStatus.IN_SEASON,
                    SleeperSeasonStatus.POST_SEASON,
                ):
                    raise LeagueLoaderException(
                        f"Year {currentLeague.season} has a status that is not supported: '{currentLeague.status}'"
                    )
                sleeperLeagues.append(currentLeague)
                years.remove(int(currentLeague.season))
            currentLeagueId = currentLeague.previous_league_id

        if len(years) > 0:
            raise LeagueLoaderException(f"Could not find years '{years}' for league.")

        # reverse list so most recent is last in list
        sleeperLeagues = sleeperLeagues[::-1]
        return sleeperLeagues

    def getOwnerNames(self) -> dict[int, list[str]]:
        yearToOwnerNamesMap: dict[int, list[str]] = dict()
        sleeperLeagues = self.__getAllLeagues()
        for sleeperLeague in sleeperLeagues:
            yearToOwnerNamesMap[int(sleeperLeague.season)] = list()
            sleeperUsers = self.__getSleeperUsers(sleeperLeague.league_id)
            for sleeperUser in sleeperUsers:
                ownerName = sleeperUser.display_name
                yearToOwnerNamesMap[int(sleeperLeague.season)].append(ownerName)
        return yearToOwnerNamesMap

    def loadLeague(self, validate: bool = True) -> League:
        sleeperLeagues = self.__getAllLeagues()
        league = self.__buildLeague(sleeperLeagues)
        if validate:
            # validate new league
            leagueValidation.runAllChecks(league)
        self.__resetCaches()
        return league

    def __buildLeague(self, sleeperLeagues: list[SleeperLeague]) -> League:
        years = list()
        leagueName = None
        self.__loadOwners(sleeperLeagues)
        owners = list(self.__sleeperUserIdToOwnerMap.values())
        for sleeperLeague in sleeperLeagues:
            leagueName = sleeperLeague.name if leagueName is None else leagueName
            year = self.__buildYear(sleeperLeague)
            if len(year.weeks) > 0:
                years.append(year)
            else:
                self._LOGGER.warning(
                    f"Year '{year.yearNumber}' discarded for not having any weeks."
                )
        # make sure years are ordered oldest -> newest
        years = sorted(years, key=lambda y: y.yearNumber)
        return League(name=leagueName, owners=owners, years=years)

    def __buildYear(self, sleeperLeague: SleeperLeague) -> Year:
        teams = self.__buildTeams(sleeperLeague)
        weeks = self.__buildWeeks(sleeperLeague)
        # add YearSettings
        yearSettings = YearSettings()
        if sleeperLeague.settings.league_average_match == 1:
            yearSettings.leagueMedianGames = True
        return Year(
            yearNumber=int(sleeperLeague.season),
            teams=teams,
            weeks=weeks,
            yearSettings=yearSettings,
        )

    def __buildWeeks(self, sleeperLeague: SleeperLeague) -> list[Week]:
        weeks = list()
        # get regular season weeks
        # once we have found an incomplete week, all weeks after will also be incomplete
        foundIncompleteWeek = False
        for i in range(sleeperLeague.settings.playoff_week_start - 1):
            if not foundIncompleteWeek and self.__isCompletedWeek(i + 1, sleeperLeague):
                # get each teams matchup for that week
                matchups = list()
                sleeperMatchupsForThisWeek = LeagueAPIClient.get_matchups_for_week(
                    league_id=sleeperLeague.league_id, week=i + 1
                )
                sleeperMatchupIdToSleeperMatchupMap: dict[int, list[SleeperMatchup]] = dict()
                for sleeperMatchup in sleeperMatchupsForThisWeek:
                    if sleeperMatchup.matchup_id in sleeperMatchupIdToSleeperMatchupMap.keys():
                        sleeperMatchupIdToSleeperMatchupMap[sleeperMatchup.matchup_id].append(
                            sleeperMatchup
                        )
                    else:
                        sleeperMatchupIdToSleeperMatchupMap[sleeperMatchup.matchup_id] = [
                            sleeperMatchup
                        ]

                for sleeperMatchupPair in sleeperMatchupIdToSleeperMatchupMap.values():
                    # team A
                    teamASleeperMatchup = sleeperMatchupPair[0]
                    teamA = self.__sleeperRosterIdToTeamMap[teamASleeperMatchup.roster_id]

                    # team B
                    teamBSleeperMatchup = sleeperMatchupPair[1]
                    teamB = self.__sleeperRosterIdToTeamMap[teamBSleeperMatchup.roster_id]

                    # sleeper does not have tiebreakers for regular season games
                    # Source: https://support.sleeper.app/en/articles/4238872-can-i-set-tiebreakers#:~:text=We%20do%20not%20offer%20any,and%20adjust%20the%20point%20total.
                    matchups.append(
                        Matchup(
                            teamAId=teamA.id,
                            teamBId=teamB.id,
                            teamAScore=teamASleeperMatchup.points,
                            teamBScore=teamBSleeperMatchup.points,
                            teamAHasTiebreaker=False,
                            teamBHasTiebreaker=False,
                            matchupType=MatchupType.REGULAR_SEASON,
                        )
                    )
                weeks.append(Week(weekNumber=i + 1, matchups=matchups))
            else:
                foundIncompleteWeek = True
        # get playoff weeks
        # NOTE: bye weeks will not be returned here. That's ok because we don't want those anyways
        allSleeperPlayoffMatchups = LeagueAPIClient.get_winners_bracket(
            league_id=sleeperLeague.league_id
        )
        if len(allSleeperPlayoffMatchups) > 0:
            # sort sleeperPlayoffMatchups by round into a dict
            playoffRoundAndSleeperPlayoffMatchups: dict[int, list[SleeperPlayoffMatchup]] = dict()
            for sleeperPlayoffMatchup in allSleeperPlayoffMatchups:
                if sleeperPlayoffMatchup.round in playoffRoundAndSleeperPlayoffMatchups.keys():
                    playoffRoundAndSleeperPlayoffMatchups[sleeperPlayoffMatchup.round].append(
                        sleeperPlayoffMatchup
                    )
                else:
                    playoffRoundAndSleeperPlayoffMatchups[sleeperPlayoffMatchup.round] = [
                        sleeperPlayoffMatchup
                    ]
            numberOfPlayoffRounds = max(
                [playoffMatchup.round for playoffMatchup in allSleeperPlayoffMatchups]
            )  # don't know a better way to determine this
            numberOfPlayoffWeeks = self.__calculate_number_of_playoff_weeks(
                sleeperLeague, allSleeperPlayoffMatchups
            )
            playoffWeeks = list(
                range(
                    sleeperLeague.settings.playoff_week_start,
                    sleeperLeague.settings.playoff_week_start + numberOfPlayoffWeeks,
                )
            )
            playoffWeekRoundList = self.__create_playoff_week_round_list(
                sleeperLeague, playoffWeeks, numberOfPlayoffRounds
            )
            for weekNumber, roundNumber in playoffWeekRoundList:
                # get each teams matchup for that week
                matchups = list()
                sleeperMatchupsForThisWeek = LeagueAPIClient.get_matchups_for_week(
                    league_id=sleeperLeague.league_id, week=weekNumber
                )
                # used to check if a Sleeper playoff matchup is in this week's matchups
                sleeperMatchupIdsForThisWeek = [
                    sleeperMatchup.matchup_id for sleeperMatchup in sleeperMatchupsForThisWeek
                ]
                if self.__isCompletedWeek(weekNumber, sleeperLeague):
                    # sort matchups by roster IDs
                    rosterIdToSleeperMatchupMap: dict[int, SleeperMatchup] = dict()
                    for sleeperMatchup in sleeperMatchupsForThisWeek:
                        rosterIdToSleeperMatchupMap[sleeperMatchup.roster_id] = sleeperMatchup
                    for sleeperPlayoffMatchup in playoffRoundAndSleeperPlayoffMatchups[roundNumber]:
                        # check if this matchup is in this week (needed for leagues with multiple weeks in a single round)
                        if sleeperPlayoffMatchup.matchup_id in sleeperMatchupIdsForThisWeek:
                            # team A
                            teamARosterId = sleeperPlayoffMatchup.team_1_roster_id
                            teamA = self.__sleeperRosterIdToTeamMap[teamARosterId]
                            teamAPoints = rosterIdToSleeperMatchupMap[teamARosterId].points
                            teamAHasTiebreaker = (
                                sleeperPlayoffMatchup.winning_roster_id
                                == sleeperPlayoffMatchup.team_1_roster_id
                            )
                            # team B
                            teamBRosterId = sleeperPlayoffMatchup.team_2_roster_id
                            teamB = self.__sleeperRosterIdToTeamMap[teamBRosterId]
                            teamBPoints = rosterIdToSleeperMatchupMap[teamBRosterId].points
                            teamBHasTiebreaker = (
                                sleeperPlayoffMatchup.winning_roster_id
                                == sleeperPlayoffMatchup.team_2_roster_id
                            )

                            multiWeekMatchupId = None
                            # determine if this is a championship matchup or not
                            matchupType = MatchupType.PLAYOFF
                            if sleeperPlayoffMatchup.p == 1:
                                matchupType = MatchupType.CHAMPIONSHIP
                                if (
                                    sleeperLeague.settings.playoff_round_type_enum
                                    == SleeperPlayoffRoundType.TWO_WEEK_CHAMPIONSHIP_ROUND
                                ):
                                    multiWeekMatchupId = f"{teamA.id}{teamB.id}"
                            if (
                                sleeperLeague.settings.playoff_round_type_enum
                                == SleeperPlayoffRoundType.TWO_WEEKS_PER_ROUND
                            ):
                                multiWeekMatchupId = f"{teamA.id}{teamB.id}"
                            matchups.append(
                                Matchup(
                                    teamAId=teamA.id,
                                    teamBId=teamB.id,
                                    teamAScore=teamAPoints,
                                    teamBScore=teamBPoints,
                                    teamAHasTiebreaker=teamAHasTiebreaker,
                                    teamBHasTiebreaker=teamBHasTiebreaker,
                                    matchupType=matchupType,
                                    multiWeekMatchupId=multiWeekMatchupId,
                                )
                            )
                    weeks.append(Week(weekNumber=weekNumber, matchups=matchups))
        return weeks

    @classmethod
    def __isCompletedWeek(cls, weekNumber: int, sleeperLeague: SleeperLeague) -> bool:
        # see if this is the current year/week of the NFL
        sportState = cls.__getSleeperSportState()
        return not (
            sportState.season == sleeperLeague.season
            and sportState.leg <= weekNumber
            and sleeperLeague.status != SleeperSeasonStatus.COMPLETE
        )

    def __buildTeams(self, sleeperLeague: SleeperLeague) -> list[Team]:
        teams = list()
        sleeperUsers = self.__getSleeperUsers(sleeperLeague.league_id)
        sleeperRosters = LeagueAPIClient.get_rosters(league_id=sleeperLeague.league_id)
        for sleeperUser in sleeperUsers:
            # connect a sleeperUser to a sleeperRoster
            rosterId = None
            for sleeperRoster in sleeperRosters:
                if sleeperRoster.owner_id == sleeperUser.user_id:
                    rosterId = sleeperRoster.roster_id
            if rosterId is None:
                raise DoesNotExistException(
                    f"No Roster ID match found for Sleeper User with ID: '{sleeperUser.user_id}'."
                )
            owner = self.__sleeperUserIdToOwnerMap[sleeperUser.user_id]
            teamName = sleeperUser.display_name
            # if we can find a team name for this user, use it instead of their display name
            if (
                isinstance(sleeperUser.metadata, dict)
                and "team_name" in sleeperUser.metadata.keys()
            ):
                teamName = sleeperUser.metadata["team_name"]
            team = Team(ownerId=owner.id, name=teamName)
            teams.append(team)
            self.__sleeperRosterIdToTeamMap[rosterId] = team
        return teams

    def __loadOwners(self, sleeperLeagues: list[SleeperLeague]) -> None:
        for sleeperLeague in sleeperLeagues:
            sleeperUsers = self.__getSleeperUsers(sleeperLeague.league_id)
            for sleeperUser in sleeperUsers:
                ownerName = sleeperUser.display_name
                # get general owner name if there is one
                generalOwnerName = self._getGeneralOwnerNameFromGivenOwnerName(ownerName)
                ownerName = generalOwnerName if generalOwnerName is not None else ownerName
                self.__sleeperUserIdToOwnerMap[sleeperUser.user_id] = Owner(name=ownerName)

    @staticmethod
    def __calculate_number_of_playoff_weeks(
        sleeperLeague: SleeperLeague, sleeperPlayoffMatchups: list[SleeperPlayoffMatchup]
    ) -> int:
        # sort sleeperPlayoffMatchups by round into a dict
        playoffRoundAndSleeperPlayoffMatchups: dict[int, list[SleeperPlayoffMatchup]] = dict()
        for sleeperPlayoffMatchup in sleeperPlayoffMatchups:
            if sleeperPlayoffMatchup.round in playoffRoundAndSleeperPlayoffMatchups.keys():
                playoffRoundAndSleeperPlayoffMatchups[sleeperPlayoffMatchup.round].append(
                    sleeperPlayoffMatchup
                )
            else:
                playoffRoundAndSleeperPlayoffMatchups[sleeperPlayoffMatchup.round] = [
                    sleeperPlayoffMatchup
                ]
        numberOfPlayoffRounds = max(
            [playoffMatchup.round for playoffMatchup in sleeperPlayoffMatchups]
        )  # don't know a better way to determine this
        match sleeperLeague.settings.playoff_round_type_enum:
            case SleeperPlayoffRoundType.ONE_WEEK_PER_ROUND:
                return numberOfPlayoffRounds
            case SleeperPlayoffRoundType.TWO_WEEK_CHAMPIONSHIP_ROUND:
                return numberOfPlayoffRounds + 1
            case SleeperPlayoffRoundType.TWO_WEEKS_PER_ROUND:
                return numberOfPlayoffRounds * 2
            case _:
                raise LeagueLoaderException(
                    f"PlayoffRoundType '{sleeperLeague.settings.playoff_round_type_enum}' is not supported."
                )

    @staticmethod
    def __create_playoff_week_round_list(
        sleeperLeague: SleeperLeague, playoffWeeks: list, numberOfPlayoffRounds: int
    ) -> list[tuple[int, int]]:
        match sleeperLeague.settings.playoff_round_type_enum:
            case SleeperPlayoffRoundType.ONE_WEEK_PER_ROUND:
                return list(zip(playoffWeeks, range(1, numberOfPlayoffRounds + 1)))
            case SleeperPlayoffRoundType.TWO_WEEK_CHAMPIONSHIP_ROUND:
                return list(
                    itertools.zip_longest(
                        playoffWeeks,
                        range(1, numberOfPlayoffRounds + 1),
                        fillvalue=numberOfPlayoffRounds,
                    )
                )
            case SleeperPlayoffRoundType.TWO_WEEKS_PER_ROUND:
                playoffRounds = [
                    playoffRound
                    for playoffRound in range(1, numberOfPlayoffRounds + 1)
                    for _ in range(1, numberOfPlayoffRounds + 1)
                ]
                return list(zip(playoffWeeks, playoffRounds))
