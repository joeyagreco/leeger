import unittest

from leeger.model.league.Team import Team


class TestTeam(unittest.TestCase):
    def test_team_init(self):
        team = Team(ownerId="ownerId", name="name")

        self.assertEqual("ownerId", team.ownerId)
        self.assertEqual("name", team.name)

    def test_team_eq_equal(self):
        # create Team 1
        team_1 = Team(ownerId="1", name="1")

        # create Team 2
        team_2 = Team(ownerId="1", name="1")

        self.assertEqual(team_1, team_2)

    def test_team_eq_notEqual(self):
        # create Team 1
        team_1 = Team(ownerId="1", name="1")

        # create Team 2
        team_2 = Team(ownerId="2", name="2dif")

        self.assertNotEqual(team_1, team_2)
