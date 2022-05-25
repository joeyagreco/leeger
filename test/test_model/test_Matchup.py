import unittest
from decimal import Decimal

from src.leeger.model.Matchup import Matchup


class TestMatchup(unittest.TestCase):

    def test_matchup_init(self):
        matchup = Matchup(teamAId="teamAId", teamBId="teamBId", teamAScore=Decimal(1.1), teamBScore=Decimal(2.2))

        self.assertEqual("teamAId", matchup.teamAId)
        self.assertEqual("teamBId", matchup.teamBId)
        self.assertIsInstance(matchup.teamAScore, Decimal)
        self.assertIsInstance(matchup.teamBScore, Decimal)
        self.assertEqual(1.1, matchup.teamAScore)
        self.assertEqual(2.2, matchup.teamBScore)
