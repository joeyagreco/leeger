from src.leeger.decorator.validate.validators import validateWeek
from src.leeger.model.Week import Week
from src.leeger.model.WeekFilters import WeekFilters


class WeekNavigator:
    """
    Used to navigate the Week model.
    """

    @staticmethod
    @validateWeek
    def getTeamIdsAndScores(week: Week, weekFilters: WeekFilters, **kwargs) -> dict[str, float | int]:
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
            if matchup.matchupType in weekFilters.includeMatchupTypes:
                teamIdAndScores[matchup.teamAId] = matchup.teamAScore
                teamIdAndScores[matchup.teamBId] = matchup.teamBScore
        return teamIdAndScores

    @staticmethod
    @validateWeek
    def getTeamIdsAndOpponentScores(week: Week, weekFilters: WeekFilters, **kwargs) -> dict[str, float | int]:
        """
        Returns all scores for each team's opponent in the given Week.

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
            if matchup.matchupType in weekFilters.includeMatchupTypes:
                teamIdAndScores[matchup.teamAId] = matchup.teamBScore
                teamIdAndScores[matchup.teamBId] = matchup.teamAScore
        return teamIdAndScores
