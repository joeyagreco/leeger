import unittest

from pymfl.exception import MFLAPIClientException

from leeger.league_loader import MyFantasyLeagueLeagueLoader


class TestMyFantasyLeagueLeagueLoader(unittest.TestCase):

    def test_loadLeague_intendedFailure(self):
        with self.assertRaises(MFLAPIClientException) as context:
            leagueLoader = MyFantasyLeagueLeagueLoader("0", [2000], mflUsername="", mflPassword="", mflUserAgentName="")
            leagueLoader.loadLeague()
        self.assertEqual("Invalid Password", str(context.exception))

    def test_noYearsGiven(self):
        with self.assertRaises(ValueError) as context:
            leagueLoader = MyFantasyLeagueLeagueLoader("0", [], mflUsername="", mflPassword="", mflUserAgentName="")
            leagueLoader.loadLeague()
        self.assertEqual("No years given to load league with ID '0'.", str(context.exception))
