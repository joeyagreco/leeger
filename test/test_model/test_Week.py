import unittest

from src.leeger.model.Matchup import Matchup
from src.leeger.model.Week import Week


class TestWeek(unittest.TestCase):
    def test_week_init(self):
        matchup = Matchup(teamAId="", teamBId="", teamAScore=0, teamBScore=0)
        week1 = Week(weekNumber=1, isPlayoffWeek=False, matchups=[matchup])
        week2 = Week(weekNumber=2, isPlayoffWeek=True, matchups=[])

        self.assertEqual(1, week1.weekNumber)
        self.assertFalse(week1.isPlayoffWeek)
        self.assertTrue(week2.isPlayoffWeek)
        self.assertEqual(1, len(week1.matchups))
        self.assertEqual(matchup.id, week1.matchups[0].id)
