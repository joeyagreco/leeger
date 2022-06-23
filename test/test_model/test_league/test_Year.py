import unittest

from src.leeger.model.league.Team import Team
from src.leeger.model.league.Week import Week
from src.leeger.model.league.Year import Year


class TestYear(unittest.TestCase):
    def test_league_init(self):
        week = Week(weekNumber=0, matchups=[])
        team = Team(ownerId="", name="")
        year = Year(yearNumber=2000, teams=[team], weeks=[week])

        self.assertEqual(2000, year.yearNumber)
        self.assertEqual(1, len(year.teams))
        self.assertEqual(1, len(year.weeks))
        self.assertEqual(week.id, year.weeks[0].id)
        self.assertEqual(team.id, year.teams[0].id)
