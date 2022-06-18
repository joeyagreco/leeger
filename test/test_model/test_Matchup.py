import unittest

from src.leeger.enum.MatchupType import MatchupType
from src.leeger.model.Matchup import Matchup


class TestMatchup(unittest.TestCase):
    def test_matchup_init(self):
        matchup = Matchup(
            teamAId="teamAId",
            teamBId="teamBId",
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR
        )

        self.assertEqual("teamAId", matchup.teamAId)
        self.assertEqual("teamBId", matchup.teamBId)
        self.assertEqual(1.1, matchup.teamAScore)
        self.assertEqual(2.2, matchup.teamBScore)
        self.assertEqual(MatchupType.REGULAR, matchup.matchupType)
