from src.leeger.decorator.validate.validators import validateYear
from src.leeger.model.Year import Year
from src.leeger.model.YearFilters import YearFilters
from src.leeger.util.Deci import Deci


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
    def getNumberOfGamesPlayed(cls, year: Year, yearFilters: YearFilters) -> dict[str, Deci]:
        """
        Returns the number of games played for each team in the given Year.

        Example response:
            {
            "someTeamId": Deci("4"),
            "someOtherTeamId": Deci("4"),
            "yetAnotherTeamId": Deci("5"),
            ...
            }
        """

        teamIdAndNumberOfGamesPlayed = dict()
        allTeamIds = YearNavigator.getAllTeamIds(year)
        for teamId in allTeamIds:
            teamIdAndNumberOfGamesPlayed[teamId] = Deci(0)

        for i in range(yearFilters.weekNumberStart - 1, yearFilters.weekNumberEnd):
            week = year.weeks[i]
            for matchup in week.matchups:
                if matchup.matchupType in yearFilters.includeMatchupTypes:
                    teamIdAndNumberOfGamesPlayed[matchup.teamAId] += Deci(1)
                    teamIdAndNumberOfGamesPlayed[matchup.teamBId] += Deci(1)
        return teamIdAndNumberOfGamesPlayed
