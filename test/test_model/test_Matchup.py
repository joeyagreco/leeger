import unittest

from src.leeger.model.Matchup import Matchup


class TestMatchup(unittest.TestCase):
    def test_matchup_init(self):
        matchup = Matchup(
            teamAId="teamAId",
            teamBId="teamBId",
            teamAScore=1.1,
            teamBScore=2.2,
            isChampionshipMatchup=True
        )

        self.assertEqual("teamAId", matchup.teamAId)
        self.assertEqual("teamBId", matchup.teamBId)
        self.assertEqual(1.1, matchup.teamAScore)
        self.assertEqual(2.2, matchup.teamBScore)
        self.assertTrue(matchup.isChampionshipMatchup)

    def test_matchup_init_isChampionshipMatchupNotGiven_defaultsToFalse(self):
        matchup = Matchup(
            teamAId="teamAId",
            teamBId="teamBId",
            teamAScore=1.1,
            teamBScore=2.2
        )

        self.assertEqual("teamAId", matchup.teamAId)
        self.assertEqual("teamBId", matchup.teamBId)
        self.assertEqual(1.1, matchup.teamAScore)
        self.assertEqual(2.2, matchup.teamBScore)
        self.assertFalse(matchup.isChampionshipMatchup)
