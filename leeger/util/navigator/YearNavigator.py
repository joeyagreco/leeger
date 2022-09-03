from leeger.enum.MatchupType import MatchupType
from leeger.model.filter.YearFilters import YearFilters
from leeger.model.league.Year import Year


class YearNavigator:
    """
    Used to navigate the Year model.
    """

    @staticmethod
    def getAllTeamIds(year: Year, **kwargs) -> list[str]:
        return [team.id for team in year.teams]

    @classmethod
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

    @staticmethod
    def getAllScoresInYear(year: Year, **kwargs) -> list[float | int]:
        """
        Returns a list of all scores for the given Year.
        Will count all scores EXCEPT for IGNORE Matchups.
        """
        allScores = list()
        for week in year.weeks:
            for matchup in week.matchups:
                if matchup.matchupType != MatchupType.IGNORE:
                    allScores.append(matchup.teamAScore)
                    allScores.append(matchup.teamBScore)
        return allScores
