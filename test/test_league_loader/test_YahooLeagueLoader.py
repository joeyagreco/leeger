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
            yahooLeagueLoader = YahooLeagueLoader(badLeagueId, [2000], clientId=badClientId,
                                                  clientSecret=badClientSecret, loginTimeoutSeconds=1)
            yahooLeagueLoader.loadLeague()
        self.assertEqual("Login to yahoofantasy timed out.", str(context.exception))

    def test_loadLeague_nonIntPassingStringForLeagueId(self):
        with self.assertRaises(ValueError) as context:
            badClientId = badClientSecret = "bad"
            badLeagueId = "a"
            yahooLeagueLoader = YahooLeagueLoader(badLeagueId, [2000], clientId=badClientId,
                                                  clientSecret=badClientSecret, loginTimeoutSeconds=1)
        self.assertEqual("League ID 'a' could not be turned into an int.", str(context.exception))

    def test_noYearsGiven(self):
        with self.assertRaises(ValueError) as context:
            leagueLoader = YahooLeagueLoader("0", [], clientId="", clientSecret="")
        self.assertEqual("No years given to load league with ID '0'.", str(context.exception))
