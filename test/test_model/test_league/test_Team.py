import unittest

from leeger.model.league.Team import Team


class TestTeam(unittest.TestCase):
    def test_team_init(self):
        team = Team(ownerId="ownerId", name="name")

        self.assertEqual("ownerId", team.ownerId)
        self.assertEqual("name", team.name)
