from src.leeger.decorator.validate.validators import validateWeek
from src.leeger.model.Week import Week


class WeekNavigator:
    """
    Used to navigate the Week model.
    """

    @staticmethod
    @validateWeek
    def getAllScoresByTeamId(week: Week, **kwargs) -> dict[str, float | int]:
        """
        Returns all scores for each team in the given Week.

        Example response:
            {
            "someTeamId": 110,
            "someOtherTeamId": 101.2,
            "yetAnotherTeamId": 88.4,
            ...
            }
        """
        teamIdAndScores = dict()
        for matchup in week.matchups:
            teamIdAndScores[matchup.teamAId] = matchup.teamAScore
            teamIdAndScores[matchup.teamBId] = matchup.teamBScore
        return teamIdAndScores
