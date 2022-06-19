import unittest

from src.leeger.enum.MatchupType import MatchupType
from src.leeger.model.Matchup import Matchup
from src.leeger.model.Week import Week
from src.leeger.model.WeekFilters import WeekFilters
from src.leeger.util.WeekNavigator import WeekNavigator
from test.helper.prototypes import getNDefaultOwnersAndTeams


class TestWeekNavigator(unittest.TestCase):
    def test_getTeamIdsAndScores_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.IGNORE)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        weekFilters = WeekFilters(
            includeMatchupTypes=[MatchupType.REGULAR_SEASON, MatchupType.PLAYOFF, MatchupType.CHAMPIONSHIP])
        response = WeekNavigator.getTeamIdsAndScores(week1, weekFilters)

        self.assertIsInstance(response, dict)
        self.assertEqual(4, len(response.keys()))
        self.assertEqual(1, response[teams[0].id])
        self.assertEqual(2, response[teams[1].id])
        self.assertEqual(1, response[teams[4].id])
        self.assertEqual(2, response[teams[5].id])

    def test_getTeamIdsAndOpponentScores_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.IGNORE)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        weekFilters = WeekFilters(
            includeMatchupTypes=[MatchupType.REGULAR_SEASON, MatchupType.PLAYOFF, MatchupType.CHAMPIONSHIP])
        response = WeekNavigator.getTeamIdsAndOpponentScores(week1, weekFilters)

        self.assertIsInstance(response, dict)
        self.assertEqual(4, len(response.keys()))
        self.assertEqual(2, response[teams[0].id])
        self.assertEqual(1, response[teams[1].id])
        self.assertEqual(2, response[teams[4].id])
        self.assertEqual(1, response[teams[5].id])
