from leeger.model.filter.WeekFilters import WeekFilters
from leeger.model.league.Week import Week


class WeekNavigator:
    """
    Used to navigate the Week model.
    """

    @staticmethod
    def getTeamIdsAndScores(
        week: Week, weekFilters: WeekFilters
    ) -> dict[str, float | int]:
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
    def getTeamIdsAndOpponentScores(
        week: Week, weekFilters: WeekFilters, **kwargs
    ) -> dict[str, float | int]:
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

    @classmethod
    def getNumberOfValidTeamsInWeek(
        cls, week: Week, weekFilters: WeekFilters, **kwargs
    ) -> int:
        """
        Returns the number of valid teams that are playing in the given week.
        A valid team is a team that is NOT in a matchup that is marked to be ignored and also matches the given filters.
        """

        numberOfValidTeams = 0
        for matchup in week.matchups:
            if matchup.matchupType in weekFilters.includeMatchupTypes:
                numberOfValidTeams += 2
        return numberOfValidTeams
