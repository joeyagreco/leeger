from src.leeger.calculator.parent.AllTimeCalculator import AllTimeCalculator
from src.leeger.decorator.validate.validators import validateLeague
from src.leeger.enum.MatchupType import MatchupType
from src.leeger.model.league.League import League
from src.leeger.util.LeagueNavigator import LeagueNavigator
from src.leeger.util.MatchupNavigator import MatchupNavigator


class YearOutcomeAllTimeCalculator(AllTimeCalculator):
    """
    Used to calculate all year outcomes.
    """

    @classmethod
    @validateLeague
    def getChampionshipCount(cls, league: League, **kwargs) -> dict[str, int]:
        """
        Returns the number of championships for each Owner in the given League.

        NOTE: There will be at max 1 champion per year.

        Example response:
            {
            "someTeamId": 0,
            "someOtherTeamId": 1,
            "yetAnotherTeamId": 3,
            ...
            }
        """
        filters = cls._getAllTimeFilters(league, validateLeague=False, **kwargs)

        ownerIdAndChampionships = dict()
        for ownerId in LeagueNavigator.getAllOwnerIds(league):
            ownerIdAndChampionships[ownerId] = 0

        for matchup in cls._getAllFilteredMatchups(league, filters):
            if matchup.matchupType == MatchupType.CHAMPIONSHIP:
                # championship matchup, see who won
                winnerTeamId = MatchupNavigator.getTeamIdOfMatchupWinner(matchup)
                winnerOwnerId = LeagueNavigator.getTeamById(league, winnerTeamId).ownerId
                ownerIdAndChampionships[winnerOwnerId] += 1

        return ownerIdAndChampionships
