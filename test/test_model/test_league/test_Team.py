import unittest

from leeger.model.league.Team import Team
from unittest.mock import patch


class TestTeam(unittest.TestCase):
    def test_team_init(self):
        team = Team(ownerId="ownerId", name="name", divisionId="did")

        self.assertEqual("ownerId", team.ownerId)
        self.assertEqual("name", team.name)
        self.assertEqual("did", team.divisionId)

    @patch("leeger.util.CustomLogger.CustomLogger.getLogger")
    def test_team_eq_callsEqualsMethod(self, mockGetLogger):
        # create Team 1
        team_1 = Team(ownerId="1", name="1", divisionId="did")

        # create Team 2
        team_2 = Team(ownerId="1", name="1", divisionId="did")

        result = team_1 == team_2
        self.assertTrue(result)

    def test_team_eq_equal(self):
        # create Team 1
        team_1 = Team(ownerId="1", name="1", divisionId="did")

        # create Team 2
        team_2 = Team(ownerId="1", name="1", divisionId="did")

        self.assertTrue(team_1.equals(team_2))

    def test_team_eq_notEqual(self):
        # create Team 1
        team_1 = Team(ownerId="1", name="1", divisionId="did")

        # create Team 2
        team_2 = Team(ownerId="2", name="2dif", divisionId="did")

        self.assertFalse(team_1.equals(team_2))

    def test_team_toFromJson(self):
        team = Team(ownerId="", name="team", divisionId="did")

        self.assertEqual(team, Team.fromJson(team.toJson()))
