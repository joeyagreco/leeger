import unittest

from src.leeger.enum.MatchupType import MatchupType
from src.leeger.exception.InvalidMatchupFormatException import InvalidMatchupFormatException
from src.leeger.model.Matchup import Matchup


class TestMatchup(unittest.TestCase):
    def test_matchup_init(self):
        matchup = Matchup(
            teamAId="teamAId",
            teamBId="teamBId",
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.PLAYOFF,
            teamAHasTiebreaker=True,
            teamBHasTiebreaker=False
        )

        self.assertEqual("teamAId", matchup.teamAId)
        self.assertEqual("teamBId", matchup.teamBId)
        self.assertEqual(1.1, matchup.teamAScore)
        self.assertEqual(2.2, matchup.teamBScore)
        self.assertEqual(MatchupType.PLAYOFF, matchup.matchupType)
        self.assertTrue(matchup.teamAHasTiebreaker)
        self.assertFalse(matchup.teamBHasTiebreaker)

    def test_matchup_init_defaultValues(self):
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
        self.assertEqual(MatchupType.REGULAR_SEASON, matchup.matchupType)
        self.assertFalse(matchup.teamAHasTiebreaker)
        self.assertFalse(matchup.teamBHasTiebreaker)

    def test_matchup_init_aAndBHaveTieBreakers_raisesException(self):
        with self.assertRaises(InvalidMatchupFormatException) as context:
            Matchup(
                teamAId="teamAId",
                teamBId="teamBId",
                teamAScore=1.1,
                teamBScore=2.2,
                teamAHasTiebreaker=True,
                teamBHasTiebreaker=True
            )
        self.assertEqual("Team A and Team B cannot both have the tiebreaker.", str(context.exception))
