import unittest

from leeger.enum import MatchupType
from leeger.model.league.Matchup import Matchup
from leeger.util.navigator.MatchupNavigator import MatchupNavigator
from test.helper.prototypes import getNDefaultOwnersAndTeams


class TestMatchupNavigator(unittest.TestCase):
    def test_getTeamIdOfMatchupWinner_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=2, teamBScore=1)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1)

        response1 = MatchupNavigator.getTeamIdOfMatchupWinner(matchup1)
        response2 = MatchupNavigator.getTeamIdOfMatchupWinner(matchup2)
        response3 = MatchupNavigator.getTeamIdOfMatchupWinner(matchup3)

        self.assertIsInstance(response1, str)
        self.assertIsInstance(response2, str)
        self.assertEqual(teams[1].id, response1)
        self.assertEqual(teams[0].id, response2)
        self.assertIsNone(response3)

    def test_getTeamIdOfMatchupWinner_tiebreakersGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1,
                           teamAHasTiebreaker=True)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1,
                           teamBHasTiebreaker=True)

        response1 = MatchupNavigator.getTeamIdOfMatchupWinner(matchup1)
        response2 = MatchupNavigator.getTeamIdOfMatchupWinner(matchup2)

        self.assertIsInstance(response1, str)
        self.assertIsInstance(response2, str)
        self.assertEqual(teams[0].id, response1)
        self.assertEqual(teams[1].id, response2)

    def test_simplifyMultiWeekMatchups_happyPath(self):
        _, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF, teamAHasTiebreaker=True, multiWeekMatchupId="1")
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF, teamBHasTiebreaker=True, multiWeekMatchupId="1")

        response = MatchupNavigator.simplifyMultiWeekMatchups([matchup1, matchup2])

        self.assertIsInstance(response, Matchup)
        self.assertEqual(teams[0].id, response.teamAId)
        self.assertEqual(teams[1].id, response.teamBId)
        self.assertTrue(response.teamAHasTiebreaker)
        self.assertFalse(response.teamBHasTiebreaker)
        self.assertEqual(4, response.teamAScore)
        self.assertEqual(6, response.teamBScore)
        self.assertEqual(MatchupType.PLAYOFF, response.matchupType)

    def test_simplifyMultiWeekMatchups_emptyListGiven_raisesException(self):
        with self.assertRaises(ValueError) as context:
            MatchupNavigator.simplifyMultiWeekMatchups(list())
        self.assertEqual("matchups cannot be an empty list.", str(context.exception))
