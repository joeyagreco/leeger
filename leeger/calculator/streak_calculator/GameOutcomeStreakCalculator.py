from leeger.calculator.parent.StreakCalculator import StreakCalculator
from leeger.decorator.validators import validateLeague
from leeger.model.league.League import League
from leeger.model.league.Team import Team
from leeger.model.stat.Streak import Streak
from leeger.util.navigator.LeagueNavigator import LeagueNavigator
from leeger.util.navigator.MatchupNavigator import MatchupNavigator


class GameOutcomeStreakCalculator(StreakCalculator):
    """
    Used to calculate all Streaks for Game Outcomes.
    """

    @classmethod
    @validateLeague
    def getWinStreaks(cls, league: League, **kwargs) -> list[Streak]:
        """
        Returns all win streaks in the given League.
        """
        streakFilters = cls._getStreakFilters(league, **kwargs)
        allFilteredMatchupsByWeek = cls._getAllFilteredMatchupsByWeek(league, streakFilters, validateLeague=False)
        weekNumberAndTeamsThatWon: dict[int, list[Team]] = dict()
        for weekNumber in allFilteredMatchupsByWeek.keys():
            weekNumberAndTeamsThatWon[weekNumber] = list()
            matchups = allFilteredMatchupsByWeek[weekNumber]
            for matchup in matchups:
                teamIdOfMatchupWinner = MatchupNavigator.getTeamIdOfMatchupWinner(matchup, validateMatchup=False)
                if teamIdOfMatchupWinner is not None:
                    team = LeagueNavigator.getTeamById(teamIdOfMatchupWinner)
                    weekNumberAndTeamsThatWon[weekNumber].append(team)

        currentStreaks: list[Streak] = list()
        for weekNumber in weekNumberAndTeamsThatWon.keys():
            for winningTeam in weekNumberAndTeamsThatWon[weekNumber]:
                ...

    @classmethod
    def __ownerIsOnStreak(cls, league: League, team: Team, currentWeekNumber: int,
                          currentStreaks: list[Streak]) -> bool:
        """
        Returns whether the Owner of the given Team is on a streak or not based on the list of current Streaks.
        """
        streaksWithThisOwner = [streak for streak in currentStreaks if
                                LeagueNavigator.getTeamById(league, streak.teamIdStart).ownerId == team.ownerId]
        return
