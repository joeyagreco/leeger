import unittest

from leeger.enum.MatchupType import MatchupType
from leeger.exception.InvalidMatchupFormatException import InvalidMatchupFormatException
from leeger.model.league.Matchup import Matchup
from test.helper.prototypes import getNDefaultOwnersAndTeams


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

    def test_matchup_eq_equal(self):
        # create Matchup 1
        _, teams_1 = getNDefaultOwnersAndTeams(2)
        matchup_1 = Matchup(teamAId=teams_1[0].id, teamBId=teams_1[1].id, teamAScore=1.1, teamBScore=2.2,
                            matchupType=MatchupType.REGULAR_SEASON)

        # create Matchup 2
        _, teams_2 = getNDefaultOwnersAndTeams(2)
        matchup_2 = Matchup(teamAId=teams_2[0].id, teamBId=teams_2[1].id, teamAScore=1.1, teamBScore=2.2,
                            matchupType=MatchupType.REGULAR_SEASON)

        self.assertEqual(matchup_1, matchup_2)

    def test_matchup_eq_notEqual(self):
        # create Matchup 1
        _, teams_1 = getNDefaultOwnersAndTeams(2)
        matchup_1 = Matchup(teamAId=teams_1[0].id, teamBId=teams_1[1].id, teamAScore=1.1, teamBScore=2.2,
                            matchupType=MatchupType.REGULAR_SEASON)

        # create Matchup 2
        _, teams_2 = getNDefaultOwnersAndTeams(2)
        matchup_2 = Matchup(teamAId=teams_2[0].id, teamBId=teams_2[1].id, teamAScore=1.1, teamBScore=2.2,
                            matchupType=MatchupType.PLAYOFF)

        self.assertNotEqual(matchup_1, matchup_2)

    def test_matchup_toJson(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.2,
                          matchupType=MatchupType.REGULAR_SEASON)
        matchupJson = matchup.toJson()

        self.assertIsInstance(matchupJson, dict)
        self.assertEqual(teams[0].id, matchupJson["teamAId"])
        self.assertEqual(teams[1].id, matchupJson["teamBId"])
        self.assertEqual(1.1, matchupJson["teamAScore"])
        self.assertEqual(2.2, matchupJson["teamBScore"])
        self.assertEqual("REGULAR_SEASON", matchupJson["matchupType"])
        self.assertFalse(matchupJson["teamAHasTieBreaker"])
        self.assertFalse(matchupJson["teamBHasTieBreaker"])
