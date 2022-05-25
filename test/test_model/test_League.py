import unittest
from decimal import Decimal

from src.leeger.model.League import League
from src.leeger.model.Matchup import Matchup
from src.leeger.model.Owner import Owner
from src.leeger.model.Team import Team
from src.leeger.model.Week import Week
from src.leeger.model.Year import Year


class TestLeague(unittest.TestCase):

    def test_league_init(self):
        matchup = Matchup(teamAId="", teamBId="", teamAScore=Decimal(),
                          teamBScore=Decimal())
        week = Week(weekNumber=0, matchups=[matchup])
        team = Team(ownerId="", name="")
        year = Year(yearNumber=0, teams=[team], weeks=[week])
        owner = Owner(name="")
        league = League(name="leagueName", owners=[owner], years=[year])

        self.assertIsNotNone(league.id)
        self.assertIsInstance(league.id, str)
        self.assertEqual("leagueName", league.name)
        self.assertEqual(1, len(league.owners))
        self.assertEqual(1, len(league.years))
        self.assertEqual(owner.id, league.owners[0].id)
        self.assertEqual(year.id, league.years[0].id)
