import unittest
from unittest import mock
from unittest.mock import Mock

from leeger.league_loader import YahooLeagueLoader


class TestYahooLeagueLoader(unittest.TestCase):
    """
    # TODO: add better tests
    # TODO: mock failure tests
    """

    # TODO
    # def test_loadLeague_intendedFailure(self):
    #     with self.assertRaises(TimeoutError) as context:
    #         badClientId = badClientSecret = "bad"
    #         badLeagueId = 0
    #         yahooLeagueLoader = YahooLeagueLoader(
    #             badLeagueId,
    #             [2000],
    #             clientId=badClientId,
    #             clientSecret=badClientSecret,
    #             loginTimeoutSeconds=1,
    #         )
    #         yahooLeagueLoader.loadLeague()
    #     self.assertEqual("Login to yahoofantasy timed out.", str(context.exception))

    def test_loadLeague_nonIntPassingStringForLeagueId(self):
        with self.assertRaises(ValueError) as context:
            badClientId = badClientSecret = "bad"
            badLeagueId = "a"
            YahooLeagueLoader(
                badLeagueId,
                [2000],
                clientId=badClientId,
                clientSecret=badClientSecret,
                loginTimeoutSeconds=1,
            )
        self.assertEqual("League ID 'a' could not be turned into an int.", str(context.exception))

    @mock.patch("subprocess.call")
    @mock.patch("multiprocessing.Process")
    @mock.patch("yahoofantasy.Context.__init__")
    @mock.patch("yahoofantasy.Context.get_leagues")
    def test_get_all_leagues(
        self,
        mockYahooContextGetLeagues,
        mockYahooContextInit,
        mockMultiprocessingProcess,
        mockSubprocessCall,
    ):
        yahooLeagueLoader = YahooLeagueLoader("123", [2022], clientId="cid", clientSecret="cs")
        # TODO: assert that the login() method is called with the correct params
        mockLeague2022 = Mock()
        mockLeague2022.league_id = "123"
        mockLeague2022.renew = None
        mockYahooContextInit.side_effect = [None]
        mockYahooContextGetLeagues.side_effect = [[mockLeague2022]]
        mockLoginProcess = mockMultiprocessingProcess.return_value
        mockLoginProcess.is_alive.return_value = False  # Simulate login process completion

        yahooLeagueLoader.loadLeague()
