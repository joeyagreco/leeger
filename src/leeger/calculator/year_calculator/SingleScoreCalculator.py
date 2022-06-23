from src.leeger.decorator.validate.validators import validateYear
from src.leeger.model.league.Year import Year
from src.leeger.service.YearFiltersService import YearFiltersService


class SingleScoreCalculator:
    """
    Used to calculate all single score stats.
    """

    @classmethod
    @validateYear
    def getMaxScore(cls, year: Year, **kwargs) -> dict[str, float | int]:
        """
        Returns the Max Score for each team in the given Year.

        Example response:
            {
            "someTeamId": 100.7,
            "someOtherTeamId": 111,
            "yetAnotherTeamId": 112.2,
            ...
            }
        """
        filters = YearFiltersService.getYearFilters(year, validateYear=False, **kwargs)

        teamIdAndMaxScore = dict()

        for i in range(filters.weekNumberStart - 1, filters.weekNumberEnd):
            week = year.weeks[i]
            for matchup in week.matchups:
                if matchup.matchupType in filters.includeMatchupTypes:
                    if matchup.teamAId in teamIdAndMaxScore:
                        teamIdAndMaxScore[matchup.teamAId] = max(teamIdAndMaxScore[matchup.teamAId], matchup.teamAScore)
                    else:
                        teamIdAndMaxScore[matchup.teamAId] = matchup.teamAScore
                    if matchup.teamBId in teamIdAndMaxScore:
                        teamIdAndMaxScore[matchup.teamBId] = max(teamIdAndMaxScore[matchup.teamBId], matchup.teamBScore)
                    else:
                        teamIdAndMaxScore[matchup.teamBId] = matchup.teamBScore

        return teamIdAndMaxScore

    @classmethod
    @validateYear
    def getMinScore(cls, year: Year, **kwargs) -> dict[str, float | int]:
        """
        Returns the Min Score for each team in the given Year.

        Example response:
            {
            "someTeamId": 78.6,
            "someOtherTeamId": 102,
            "yetAnotherTeamId": 57.3,
            ...
            }
        """
        filters = YearFiltersService.getYearFilters(year, validateYear=False, **kwargs)

        teamIdAndMinScore = dict()

        for i in range(filters.weekNumberStart - 1, filters.weekNumberEnd):
            week = year.weeks[i]
            for matchup in week.matchups:
                if matchup.matchupType in filters.includeMatchupTypes:
                    if matchup.teamAId in teamIdAndMinScore:
                        teamIdAndMinScore[matchup.teamAId] = min(teamIdAndMinScore[matchup.teamAId], matchup.teamAScore)
                    else:
                        teamIdAndMinScore[matchup.teamAId] = matchup.teamAScore
                    if matchup.teamBId in teamIdAndMinScore:
                        teamIdAndMinScore[matchup.teamBId] = min(teamIdAndMinScore[matchup.teamBId], matchup.teamBScore)
                    else:
                        teamIdAndMinScore[matchup.teamBId] = matchup.teamBScore

        return teamIdAndMinScore
