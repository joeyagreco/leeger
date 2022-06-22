from src.leeger.decorator.validate.validators import validateYear
from src.leeger.enum.MatchupType import MatchupType
from src.leeger.model.Year import Year
from src.leeger.service.YearFiltersService import YearFiltersService
from src.leeger.util.MatchupNavigator import MatchupNavigator
from src.leeger.util.YearNavigator import YearNavigator


class YearOutcomeCalculator:
    """
    Used to calculate all year outcomes.
    """

    @classmethod
    @validateYear
    def getChampionshipCount(cls, year: Year, **kwargs) -> dict[str, int]:
        """
        Returns the number of championships for each team in the given Year.

        NOTE: There will be at max 1 champion per year.

        Example response:
            {
            "someTeamId": 0,
            "someOtherTeamId": 1,
            "yetAnotherTeamId": 0,
            ...
            }
        """
        filters = YearFiltersService.getYearFilters(year, validateYear=False, **kwargs)

        teamIdAndChampionships = dict()
        for teamId in YearNavigator.getAllTeamIds(year):
            teamIdAndChampionships[teamId] = 0

        for i in range(filters.weekNumberStart - 1, filters.weekNumberEnd):
            week = year.weeks[i]
            for matchup in week.matchups:
                if matchup.matchupType in filters.includeMatchupTypes and matchup.matchupType == MatchupType.CHAMPIONSHIP:
                    # championship matchup, see who won
                    winnerTeamId = MatchupNavigator.getTeamIdOfMatchupWinner(matchup)
                    teamIdAndChampionships[winnerTeamId] += 1
        return teamIdAndChampionships
