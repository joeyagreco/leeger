import unittest

from src.leeger.model.Matchup import Matchup
from src.leeger.model.Week import Week
from src.leeger.util.WeekNavigator import WeekNavigator
from test.helper.prototypes import getNDefaultOwnersAndTeams


class TestWeekNavigator(unittest.TestCase):
    def test_getTeamIdsAndScores_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])

        response = WeekNavigator.getTeamIdsAndScores(week1)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(1, response[teams[0].id])
        self.assertEqual(2, response[teams[1].id])

    def test_getTeamIdsAndOpponentScores_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])

        response = WeekNavigator.getTeamIdsAndOpponentScores(week1)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(2, response[teams[0].id])
        self.assertEqual(1, response[teams[1].id])
