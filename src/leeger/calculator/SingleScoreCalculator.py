from src.leeger.calculator.parent.YearCalculator import YearCalculator
from src.leeger.decorator.validate.validators import validateYear
from src.leeger.model.Year import Year


class SingleScoreCalculator(YearCalculator):
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
        cls.loadFilters(year, validateYear=False, **kwargs)

        teamIdAndMaxScore = dict()

        for i in range(cls._weekNumberStart - 1, cls._weekNumberEnd):
            week = year.weeks[i]
            if (week.isPlayoffWeek and not cls._onlyRegularSeason) or (
                    not week.isPlayoffWeek and not cls._onlyPostSeason):
                for matchup in week.matchups:
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
        cls.loadFilters(year, validateYear=False, **kwargs)

        teamIdAndMinScore = dict()

        for i in range(cls._weekNumberStart - 1, cls._weekNumberEnd):
            week = year.weeks[i]
            if (week.isPlayoffWeek and not cls._onlyRegularSeason) or (
                    not week.isPlayoffWeek and not cls._onlyPostSeason):
                for matchup in week.matchups:
                    if matchup.teamAId in teamIdAndMinScore:
                        teamIdAndMinScore[matchup.teamAId] = min(teamIdAndMinScore[matchup.teamAId], matchup.teamAScore)
                    else:
                        teamIdAndMinScore[matchup.teamAId] = matchup.teamAScore
                    if matchup.teamBId in teamIdAndMinScore:
                        teamIdAndMinScore[matchup.teamBId] = min(teamIdAndMinScore[matchup.teamBId], matchup.teamBScore)
                    else:
                        teamIdAndMinScore[matchup.teamBId] = matchup.teamBScore

        return teamIdAndMinScore
