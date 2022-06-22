from src.leeger.decorator.validate.validators import validateYear
from src.leeger.model.Year import Year
from src.leeger.model.YearFilters import YearFilters


class YearNavigator:
    """
    Used to navigate the Year model.
    """

    @staticmethod
    @validateYear
    def getAllTeamIds(year: Year, **kwargs) -> list[str]:
        return [team.id for team in year.teams]

    @classmethod
    @validateYear
    def getNumberOfGamesPlayed(cls, year: Year, yearFilters: YearFilters) -> dict[str, int]:
        """
        Returns the number of games played for each team in the given Year.

        Example response:
            {
            "someTeamId": 4,
            "someOtherTeamId": 6,
            "yetAnotherTeamId": 11,
            ...
            }
        """

        teamIdAndNumberOfGamesPlayed = dict()
        allTeamIds = YearNavigator.getAllTeamIds(year)
        for teamId in allTeamIds:
            teamIdAndNumberOfGamesPlayed[teamId] = 0

        for i in range(yearFilters.weekNumberStart - 1, yearFilters.weekNumberEnd):
            week = year.weeks[i]
            for matchup in week.matchups:
                if matchup.matchupType in yearFilters.includeMatchupTypes:
                    teamIdAndNumberOfGamesPlayed[matchup.teamAId] += 1
                    teamIdAndNumberOfGamesPlayed[matchup.teamBId] += 1
        return teamIdAndNumberOfGamesPlayed
