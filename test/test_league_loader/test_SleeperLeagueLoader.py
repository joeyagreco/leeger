import unittest

from leeger.league_loader import SleeperLeagueLoader


class TestSleeperLeagueLoader(unittest.TestCase):
    """
    # TODO: Add better tests.
    """

    def test_loadLeague_intendedFailure(self):
        with self.assertRaises(ValueError) as context:
            leagueLoader = SleeperLeagueLoader("0", [2000])
            leagueLoader.loadLeague()  # 0 is a bad league ID
        self.assertEqual("Could not find years '[2000]' for league.", str(context.exception))
