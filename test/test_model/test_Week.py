import unittest

from src.leeger.model.Matchup import Matchup
from src.leeger.model.Week import Week


class TestWeek(unittest.TestCase):
    def test_week_init(self):
        matchup = Matchup(teamAId="", teamBId="", teamAScore=0, teamBScore=0)
        week = Week(weekNumber=1, matchups=[matchup])

        self.assertEqual(1, week.weekNumber)
        self.assertEqual(1, len(week.matchups))
        self.assertEqual(matchup.id, week.matchups[0].id)
