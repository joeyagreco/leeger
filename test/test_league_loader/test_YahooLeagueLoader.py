import unittest

from leeger.league_loader.YahooLeagueLoader import YahooLeagueLoader


class TestESPNLeagueLoader(unittest.TestCase):
    """
    # TODO: Add better tests.
    """

    def test_loadLeague_intendedFailure(self):
        with self.assertRaises(TimeoutError) as context:
            badClientId = badClientSecret = "bad"
            badLeagueId = 0
            YahooLeagueLoader.loadLeague(badLeagueId, [2000], clientId=badClientId,
                                         clientSecret=badClientSecret, loginTimeoutSeconds=1)
        self.assertEqual("Login to yahoofantasy timed out.", str(context.exception))
