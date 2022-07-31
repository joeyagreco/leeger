import unittest

from leeger.league_loader import SleeperLeagueLoader


class TestSleeperLeagueLoader(unittest.TestCase):

    def test_loadLeague_intendedFailure(self):
        with self.assertRaises(ValueError) as context:
            leagueLoader = SleeperLeagueLoader("0", [2000])
            leagueLoader.loadLeague()  # 0 is a bad league ID
        self.assertEqual("Could not find years '[2000]' for league.", str(context.exception))

    def test_noYearsGiven(self):
        with self.assertRaises(ValueError) as context:
            leagueLoader = SleeperLeagueLoader("0", [])
            leagueLoader.loadLeague()
        self.assertEqual("No years given to load league with ID '0'.", str(context.exception))
