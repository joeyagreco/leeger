from typing import Optional
from fleaflicker.api.LeagueInfoAPIClient import LeagueInfoAPIClient
from fleaflicker.api.ScoringAPIClient import ScoringAPIClient
from fleaflicker.enum.Sport import Sport
from sleeper.enum import Sport

from leeger.enum.MatchupType import MatchupType
from leeger.exception.LeagueLoaderException import LeagueLoaderException
from leeger.league_loader.LeagueLoader import LeagueLoader
from leeger.model.league.League import League
from leeger.model.league.Matchup import Matchup
from leeger.model.league.Owner import Owner
from leeger.model.league.Team import Team
from leeger.model.league.Week import Week
from leeger.model.league.Year import Year
from leeger.validate import leagueValidation


class FleaflickerLeagueLoader(LeagueLoader):
    """
    Responsible for loading a League from Fleaflicker.
    https://www.fleaflicker.com/
    """

    def __init__(
        self,
        leagueId: str,
        years: list[int],
        *,
        ownerNamesAndAliases: Optional[dict[str, list[str]]] = None,
    ):
        # validation
        try:
            int(leagueId)
        except ValueError:
            raise ValueError(f"League ID '{leagueId}' could not be turned into an int.")
        super().__init__(leagueId, years, ownerNamesAndAliases=ownerNamesAndAliases)

        self.__fleaflickerTeamIdToOwnerMap: dict[int, Owner] = dict()
        self.__fleaflickerTeamIdToTeamMap: dict[int, Team] = dict()

    def __getAllLeagues(self) -> list[dict]:
        # return a list of all leagues
        fleaflickerLeagues = list()
        for year in self._years:
            fleaflickerLeagues.append(
                LeagueInfoAPIClient.get_league_standings(
                    sport=Sport.NFL, league_id=int(self._leagueId), season=year
                )
            )
        # TODO: add some validation here to make sure we got all years
        return fleaflickerLeagues

    def getOwnerNames(self) -> dict[int, list[str]]:
        yearToOwnerNamesMap: dict[int, list[str]] = dict()
        fleaflickerLeagues = self.__getAllLeagues()
        for fleaflickerLeague in fleaflickerLeagues:
            yearToOwnerNamesMap[int(fleaflickerLeague["season"])] = list()
            for division in fleaflickerLeague["divisions"]:
                for team in division["teams"]:
                    ownerName = team["owners"][0]["displayName"]
                    yearToOwnerNamesMap[self._years[0]].append(ownerName)
        return yearToOwnerNamesMap

    def loadLeague(self, validate: bool = True) -> League:
        fleaflickerLeagues = self.__getAllLeagues()
        league = self.__buildLeague(fleaflickerLeagues)
        if validate:
            # validate new league
            leagueValidation.runAllChecks(league)
        return league

    def __buildLeague(self, fleaflickerLeagues: list[dict]) -> League:
        years = list()
        leagueName = None
        self.__loadOwners(fleaflickerLeagues)
        owners = list(self.__fleaflickerTeamIdToOwnerMap.values())
        for fleaflickerLeague in fleaflickerLeagues:
            leagueName = fleaflickerLeague["league"]["name"] if leagueName is None else leagueName
            year = self.__buildYear(fleaflickerLeague)
            if len(year.weeks) > 0:
                years.append(year)
            else:
                self._LOGGER.warning(
                    f"Year '{year.yearNumber}' discarded for not having any weeks."
                )
        return League(name=leagueName, owners=owners, years=years)

    def __buildYear(self, fleaflickerLeague: dict) -> Year:
        teams = self.__buildTeams(fleaflickerLeague)
        weeks = self.__buildWeeks(fleaflickerLeague)
        return Year(yearNumber=int(fleaflickerLeague["season"]), teams=teams, weeks=weeks)

    def __buildWeeks(self, fleaflickerLeague: dict) -> list[Week]:
        weeks = list()
        # get all weeks
        fleaflicker_league_scoreboard = ScoringAPIClient.get_league_scoreboard(
            sport=Sport.NFL,
            league_id=fleaflickerLeague["league"]["id"],
            season=fleaflickerLeague["season"],
        )
        number_of_scoring_periods = (
            len(fleaflicker_league_scoreboard["eligibleSchedulePeriods"]) + 1
        )
        for scoring_period in range(1, number_of_scoring_periods):
            matchups = list()
            # get all games for this week
            current_scoreboard = ScoringAPIClient.get_league_scoreboard(
                sport=Sport.NFL,
                league_id=fleaflickerLeague["league"]["id"],
                season=fleaflickerLeague["season"],
                scoring_period=scoring_period,
            )
            for game in current_scoreboard.get("games", list()):
                # team A
                teamAFleaflicker: dict = game["away"]
                teamA = self.__fleaflickerTeamIdToTeamMap[teamAFleaflicker["id"]]
                teamAScore = game["awayScore"]["score"].get(
                    "value", 0
                )  # if "value" isn't found, score is 0

                # team B
                teamBFleaflicker: dict = game["home"]
                teamB = self.__fleaflickerTeamIdToTeamMap[teamBFleaflicker["id"]]
                teamBScore = game["homeScore"]["score"].get(
                    "value", 0
                )  # if "value" isn't found, score is 0

                # figure out tiebreakers
                teamAHasTieBreaker = game.get("awayResult") == "WIN"
                teamBHasTieBreaker = game.get("homeResult") == "WIN"

                # figure out matchup type
                matchupType = MatchupType.REGULAR_SEASON
                if (
                    game.get("isPlayoffs")
                    or game.get("isConsolation")
                    or game.get("isThirdPlaceGame")
                ):
                    matchupType = MatchupType.PLAYOFF
                if game.get("isChampionshipGame"):
                    matchupType = MatchupType.CHAMPIONSHIP

                # only add matchup if it is completed
                if game.get("isFinalScore"):
                    matchups.append(
                        Matchup(
                            teamAId=teamA.id,
                            teamBId=teamB.id,
                            teamAScore=teamAScore,
                            teamBScore=teamBScore,
                            teamAHasTiebreaker=teamAHasTieBreaker,
                            teamBHasTiebreaker=teamBHasTieBreaker,
                            matchupType=matchupType,
                        )
                    )
            if len(matchups) > 0:
                weeks.append(Week(weekNumber=scoring_period, matchups=matchups))
        return weeks

    def __buildTeams(self, fleaflickerLeague: dict) -> list[Team]:
        teams = list()
        for division in fleaflickerLeague["divisions"]:
            for team in division["teams"]:
                teamName = team["name"]
                teamId = team["id"]
                owner = self.__fleaflickerTeamIdToOwnerMap[teamId]
                team = Team(ownerId=owner.id, name=teamName)
                teams.append(team)
                self.__fleaflickerTeamIdToTeamMap[teamId] = team
        return teams

    def __loadOwners(self, fleaflickerLeagues: list[dict]) -> None:
        for fleaflickerLeague in fleaflickerLeagues:
            for division in fleaflickerLeague["divisions"]:
                for team in division["teams"]:
                    if "owners" not in team:
                        # some teams don't have owners listed in them, use the team name instead
                        ownerName = team["name"]
                    else:
                        ownerName = team["owners"][0]["displayName"]
                    # get general owner name if there is one
                    generalOwnerName = self._getGeneralOwnerNameFromGivenOwnerName(ownerName)
                    ownerName = generalOwnerName if generalOwnerName is not None else ownerName
                    self.__fleaflickerTeamIdToOwnerMap[team["id"]] = Owner(name=ownerName)
