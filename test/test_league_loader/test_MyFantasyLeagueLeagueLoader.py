import unittest

from pymfl.exception import MFLAPIClientException

from leeger.league_loader import MyFantasyLeagueLeagueLoader


class TestMyFantasyLeagueLeagueLoader(unittest.TestCase):
    """
    # TODO: add better tests
    # TODO: mock intended failure test
    """

    def test_loadLeague_intendedFailure(self):
        with self.assertRaises(MFLAPIClientException) as context:
            leagueLoader = MyFantasyLeagueLeagueLoader(
                "0", [2000], mflUsername="", mflPassword="", mflUserAgentName=""
            )
            leagueLoader.loadLeague()
        self.assertEqual("Invalid Password", str(context.exception))
