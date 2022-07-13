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
            ESPNLeagueLoader.loadLeague(0, [2000])  # 0 is a bad league ID
        self.assertEqual("League 0 does not exist", str(context.exception))
