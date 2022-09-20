import unittest

from espn_api.requests.espn_requests import ESPNInvalidLeague

from leeger.league_loader.ESPNLeagueLoader import ESPNLeagueLoader


class TestESPNLeagueLoader(unittest.TestCase):
    """
    Currently, there is not a good way to test this class due to an issue addressed here: https://github.com/cwendt94/espn-api/issues/338
    For now, we can do some very basic tests.
    """

    def test_loadLeague_intendedFailure(self):
        with self.assertRaises(ESPNInvalidLeague) as context:
            leagueLoader = ESPNLeagueLoader("0", [2000])
            leagueLoader.loadLeague()  # 0 is a bad league ID
        self.assertEqual("League 0 does not exist", str(context.exception))

    def test_loadLeague_nonIntPassingStringForLeagueId(self):
        with self.assertRaises(ValueError) as context:
            leagueLoader = ESPNLeagueLoader("a", [2000])
        self.assertEqual("League ID 'a' could not be turned into an int.", str(context.exception))

    def test_noYearsGiven(self):
        with self.assertRaises(ValueError) as context:
            leagueLoader = ESPNLeagueLoader("0", [])
        self.assertEqual("No years given to load league with ID '0'.", str(context.exception))
