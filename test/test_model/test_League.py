import unittest

from src.leeger.model.League import League
from src.leeger.model.Owner import Owner
from src.leeger.model.Year import Year


class TestLeague(unittest.TestCase):
    def test_league_init(self):
        year = Year(yearNumber=0, teams=[], weeks=[])
        owner = Owner(name="")
        league = League(name="leagueName", owners=[owner], years=[year])

        self.assertEqual("leagueName", league.name)
        self.assertEqual(1, len(league.owners))
        self.assertEqual(1, len(league.years))
        self.assertEqual(owner.id, league.owners[0].id)
        self.assertEqual(year.id, league.years[0].id)
