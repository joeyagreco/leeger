import unittest

from src.leeger.league_loader.YahooLeagueLoader import YahooLeagueLoader


class TestESPNLeagueLoader(unittest.TestCase):
    """
    # TODO: Add better tests.
    """

    def test_loadLeague_intendedFailure(self):
        with self.assertRaises(ValueError) as context:
            YahooLeagueLoader.loadLeague(0, [2000])  # 0 is a bad league ID
        self.assertEqual("Client ID, secret, and refresh token are required. Did you run 'yahoofantasy login' already?",
                         str(context.exception))
