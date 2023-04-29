import unittest

from leeger.league_loader.FleaflickerLeagueLoader import FleaflickerLeagueLoader


class TestFleaflickerLeagueLoader(unittest.TestCase):
    def test_noYearsGiven(self):
        with self.assertRaises(ValueError) as context:
            leagueLoader = FleaflickerLeagueLoader("0", [])
        self.assertEqual("No years given to load league with ID '0'.", str(context.exception))
