import unittest
from unittest import mock
from unittest.mock import Mock

from leeger.league_loader import YahooLeagueLoader


class TestYahooLeagueLoader(unittest.TestCase):
    """
    # TODO: add better tests
    # TODO: mock failure tests
    """

    # helper methods
    def __getMockTeamsMethod(self, teams: list) -> callable:
        def mockTeamsMethod():
            return teams

        return mockTeamsMethod

    def __getMockWeeksMethod(self, weeks: list) -> callable:
        def mockWeeksMethod():
            return weeks

        return mockWeeksMethod

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
        mockLeague2022.name = "Test League 2022"
        mockLeague2022.league_id = "123"
        mockLeague2022.season = 2022
        mockLeague2022.renew = None
        mockLeague2022.current_week = 1
        mockLeague2022.end_week = 5

        # mock teams
        mockTeam1_2022 = Mock()
        mockTeam1_2022.team_id = 1
        mockTeam1_2022.team_key = 1
        mockTeam1_2022.manager.nickname = "Owner 1"
        mockTeam1_2022.manager.manager_id = 1
        mockTeam1_2022.team_points.total = 100
        mockTeam2_2022 = Mock()
        mockTeam2_2022.team_id = 2
        mockTeam2_2022.team_key = 2
        mockTeam1_2022.manager.nickname = "Owner 2"
        mockTeam1_2022.manager.manager_id = 2
        mockTeam2_2022.team_points.total = 90
        mockLeague2022.teams = self.__getMockTeamsMethod([mockTeam1_2022, mockTeam2_2022])

        # mock matchups
        mockMatchup1_2022 = Mock()
        mockMatchup1_2022.status = "postevent"
        mockMatchup1_2022.team1 = mockTeam1_2022
        mockMatchup1_2022.team2 = mockTeam2_2022
        mockMatchup1_2022.winner_team_key = 1
        mockMatchup1_2022.is_playoffs = 0
        mockMatchup1_2022.league = mockLeague2022
        mockMatchup1_2022.teams.team = [mockTeam1_2022, mockTeam2_2022]

        # mock weeks
        mockWeek1_2022 = Mock()
        mockWeek1_2022.matchups = [mockMatchup1_2022]
        mockLeague2022.weeks = self.__getMockWeeksMethod([mockWeek1_2022])

        mockYahooContextInit.side_effect = [None]
        mockYahooContextGetLeagues.side_effect = [[mockLeague2022]]
        mockLoginProcess = mockMultiprocessingProcess.return_value
        mockLoginProcess.is_alive.return_value = False  # Simulate login process completion

        yahooLeagueLoader.loadLeague()
