from sleeper.api import LeagueAPIClient
from sleeper.model import League as SleeperLeague
from sleeper.model import Matchup as SleeperMatchup
from sleeper.model import PlayoffMatchup as SleeperPlayoffMatchup

from leeger import Owner, Year, Team, Week, Matchup
from leeger.enum.MatchupType import MatchupType
from leeger.exception.DoesNotExistException import DoesNotExistException
from leeger.league_loader.abstract.LeagueLoader import LeagueLoader
from leeger.model.league.League import League


class SleeperLeagueLoader(LeagueLoader):
    """
    Responsible for loading a League from Sleeper Fantasy Football.
    https://sleeper.com/
    """
    __INVALID_SLEEPER_LEAGUE_IDS = [None, "0"]

    @classmethod
    def __initializeClassVariables(cls) -> None:
        cls.__sleeperUserIdToOwnerMap: dict[int, Owner] = dict()
        cls.__sleeperRosterIdToTeamMap: dict[str, Team] = dict()

    @classmethod
    def loadLeague(cls, mostRecentLeagueId: str, **kwargs) -> League:
        cls.__initializeClassVariables()
        # get all leagues
        mostRecentLeague: SleeperLeague = LeagueAPIClient.get_league(league_id=mostRecentLeagueId)
        sleeperLeagues = [mostRecentLeague]
        previousLeagueId = mostRecentLeague.previous_league_id
        while previousLeagueId not in cls.__INVALID_SLEEPER_LEAGUE_IDS:
            previousLeague = LeagueAPIClient.get_league(league_id=previousLeagueId)
            sleeperLeagues.append(previousLeague)
            previousLeagueId = previousLeague.previous_league_id
        # reverse list so most recent is last in list
        sleeperLeagues = sleeperLeagues[::-1]
        return cls.__buildLeague(sleeperLeagues)

    @classmethod
    def __buildLeague(cls, sleeperLeagues: list[SleeperLeague]) -> League:
        years = list()
        leagueName = None
        cls.__loadOwners(sleeperLeagues)
        owners = list(cls.__sleeperUserIdToOwnerMap.values())
        for sleeperLeague in sleeperLeagues:
            leagueName = sleeperLeague.name if leagueName is None else leagueName
            years.append(cls.__buildYear(sleeperLeague))
        return League(name=leagueName, owners=owners, years=years)

    @classmethod
    def __buildYear(cls, sleeperLeague: SleeperLeague) -> Year:
        teams = cls.__buildTeams(sleeperLeague)
        weeks = cls.__buildWeeks(sleeperLeague)
        return Year(yearNumber=int(sleeperLeague.season), teams=teams, weeks=weeks)

    @classmethod
    def __buildWeeks(cls, sleeperLeague: SleeperLeague) -> list[Week]:
        weeks = list()
        # get regular season weeks
        for i in range(sleeperLeague.settings.playoff_week_start):
            # get each teams matchup for that week
            matchups = list()
            sleeperMatchups = LeagueAPIClient.get_matchups_for_week(league_id=sleeperLeague.league_id, week=i + 1)
            if cls.__isCompletedWeek(sleeperMatchups):
                sleeperMatchupIdToSleeperMatchupMap: dict[int, list[SleeperMatchup]] = dict()
                for sleeperMatchup in sleeperMatchups:
                    if sleeperMatchup.matchup_id in sleeperMatchupIdToSleeperMatchupMap.keys():
                        sleeperMatchupIdToSleeperMatchupMap[sleeperMatchup.matchup_id].append(sleeperMatchup)
                    else:
                        sleeperMatchupIdToSleeperMatchupMap[sleeperMatchup.matchup_id] = [sleeperMatchup]

                for sleeperMatchupPair in sleeperMatchupIdToSleeperMatchupMap.values():
                    # team A
                    teamASleeperMatchup = sleeperMatchupPair[0]
                    teamA = cls.__sleeperRosterIdToTeamMap[teamASleeperMatchup.roster_id]

                    # team B
                    teamBSleeperMatchup = sleeperMatchupPair[1]
                    teamB = cls.__sleeperRosterIdToTeamMap[teamBSleeperMatchup.roster_id]

                    matchups.append(Matchup(teamAId=teamA.id,
                                            teamBId=teamB.id,
                                            teamAScore=teamASleeperMatchup.points,
                                            teamBScore=teamBSleeperMatchup.points,
                                            teamAHasTiebreaker=False,  # TODO: Find way to get tiebreaker
                                            teamBHasTiebreaker=False,  # TODO: Find way to get tiebreaker
                                            matchupType=MatchupType.REGULAR_SEASON))
                weeks.append(Week(weekNumber=i + 1, matchups=matchups))
        # get playoff weeks
        sleeperPlayoffMatchups = LeagueAPIClient.get_winners_bracket(league_id=sleeperLeague.league_id)
        # sort sleeperPlayoffMatchups by round into a dict
        playoffRoundAndSleeperPlayoffMatchups: dict[int, list[SleeperPlayoffMatchup]] = dict()
        for sleeperPlayoffMatchup in sleeperPlayoffMatchups:
            if sleeperPlayoffMatchup.round in playoffRoundAndSleeperPlayoffMatchups.keys():
                playoffRoundAndSleeperPlayoffMatchups[sleeperPlayoffMatchup.round].append(sleeperPlayoffMatchup)
            else:
                playoffRoundAndSleeperPlayoffMatchups[sleeperPlayoffMatchup.round] = [sleeperPlayoffMatchup]
        numberOfPlayoffWeeks = max([playoffMatchup.round for playoffMatchup in
                                    sleeperPlayoffMatchups])  # don't know a better way to determine this
        for i in range(1, numberOfPlayoffWeeks + 1):
            weekNumber = sleeperLeague.settings.playoff_week_start + i
            # get each teams matchup for that week
            matchups = list()
            sleeperMatchups = LeagueAPIClient.get_matchups_for_week(league_id=sleeperLeague.league_id, week=weekNumber)
            if cls.__isCompletedWeek(sleeperMatchups):
                # sort matchups by roster IDs
                rosterIdToSleeperMatchupMap: dict[int, SleeperMatchup] = dict()
                for sleeperMatchup in sleeperMatchups:
                    rosterIdToSleeperMatchupMap[sleeperMatchup.roster_id] = sleeperMatchup
                # here, "i" will be the round of the playoffs
                for sleeperPlayoffMatchup in playoffRoundAndSleeperPlayoffMatchups[i]:
                    # team A
                    teamARosterId = sleeperPlayoffMatchup.team_1_roster_id
                    teamA = cls.__sleeperRosterIdToTeamMap[teamARosterId]
                    teamAPoints = rosterIdToSleeperMatchupMap[teamARosterId].points
                    teamAHasTiebreaker = sleeperPlayoffMatchup.winning_roster_id == sleeperPlayoffMatchup.team_1_roster_id
                    # team B
                    teamBRosterId = sleeperPlayoffMatchup.team_2_roster_id
                    teamB = cls.__sleeperRosterIdToTeamMap[teamBRosterId]
                    teamBPoints = rosterIdToSleeperMatchupMap[teamBRosterId].points
                    teamBHasTiebreaker = sleeperPlayoffMatchup.winning_roster_id == sleeperPlayoffMatchup.team_2_roster_id
                    # determine if this is a championship matchup or not
                    matchupType = MatchupType.PLAYOFF
                    if i == numberOfPlayoffWeeks and sleeperPlayoffMatchup.p == 1:
                        matchupType = MatchupType.CHAMPIONSHIP
                    matchups.append(Matchup(teamAId=teamA.id,
                                            teamBId=teamB.id,
                                            teamAScore=teamAPoints,
                                            teamBScore=teamBPoints,
                                            teamAHasTiebreaker=teamAHasTiebreaker,
                                            teamBHasTiebreaker=teamBHasTiebreaker,
                                            matchupType=matchupType))
                weeks.append(Week(weekNumber=weekNumber, matchups=matchups))

        return weeks

    @classmethod
    def __isCompletedWeek(cls, sleeperMatchups: list[SleeperMatchup]) -> bool:
        # there might be a better way of determining this
        return sum([sleeperMatchup.points for sleeperMatchup in sleeperMatchups]) != 0

    @classmethod
    def __buildTeams(cls, sleeperLeague: SleeperLeague) -> list[Team]:
        teams = list()
        sleeperUsers = LeagueAPIClient.get_users_in_league(league_id=sleeperLeague.league_id)
        sleeperRosters = LeagueAPIClient.get_rosters(league_id=sleeperLeague.league_id)
        for sleeperUser in sleeperUsers:
            # connect a sleeperUser to a sleeperRoster
            rosterId = None
            for sleeperRoster in sleeperRosters:
                if sleeperRoster.owner_id == sleeperUser.user_id:
                    rosterId = sleeperRoster.roster_id
            if rosterId is None:
                raise DoesNotExistException(
                    f"No Roster ID match found for Sleeper User with ID: '{sleeperUser.user_id}'.")
            owner = cls.__sleeperUserIdToOwnerMap[sleeperUser.user_id]
            teamName = sleeperUser.display_name
            # if we can find a team name for this user, use it instead of their display name
            if isinstance(sleeperUser.metadata, dict) and "team_name" in sleeperUser.metadata.keys():
                teamName = sleeperUser.metadata["team_name"]
            team = Team(ownerId=owner.id, name=teamName)
            teams.append(team)
            cls.__sleeperRosterIdToTeamMap[rosterId] = team
        return teams

    @classmethod
    def __loadOwners(cls, sleeperLeagues: list[SleeperLeague]) -> None:
        for sleeperLeague in sleeperLeagues:
            sleeperUsers = LeagueAPIClient.get_users_in_league(league_id=sleeperLeague.league_id)
            for sleeperUser in sleeperUsers:
                cls.__sleeperUserIdToOwnerMap[sleeperUser.user_id] = Owner(name=sleeperUser.display_name)

    @classmethod
    def __loadRosters(cls, sleeperLeagues: list[SleeperLeague]) -> None:
        for sleeperLeague in sleeperLeagues:
            sleeperRosters = LeagueAPIClient.get_rosters(league_id=sleeperLeague.league_id)
            for sleeperRoster in sleeperRosters:
                cls.__sleeperRosterIdToSleeperOwnerIdMap[sleeperRoster.roster_id] = sleeperRoster.owner_id
