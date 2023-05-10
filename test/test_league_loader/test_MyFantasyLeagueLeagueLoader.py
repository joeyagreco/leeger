import unittest
import unittest
from unittest import mock
from unittest.mock import Mock

from leeger.league_loader import MyFantasyLeagueLeagueLoader


class TestMyFantasyLeagueLeagueLoader(unittest.TestCase):
    """
    # TODO: add better tests
    # TODO: mock intended failure test
    """

    # def test_loadLeague_intendedFailure(self):
    #     with self.assertRaises(MFLAPIClientException) as context:
    #         leagueLoader = MyFantasyLeagueLeagueLoader(
    #             "0", [2000], mflUsername="", mflPassword="", mflUserAgentName=""
    #         )
    #         leagueLoader.loadLeague()
    #     self.assertEqual("Invalid Password", str(context.exception))

    @mock.patch("pymfl.api.config.APIConfig.add_config_for_year_and_league_id")
    @mock.patch("pymfl.api.CommonLeagueInfoAPIClient.get_league")
    @mock.patch("pymfl.api.CommonLeagueInfoAPIClient.get_schedule")
    @mock.patch("pymfl.api.CommonLeagueInfoAPIClient.get_playoff_bracket")
    def test_loadLeague_happyPath(
        self, mockGetPlayoffBracket, mockGetSchedule, mockGetLeague, mockAddConfig
    ):
        mockFranchise1 = {"owner_name": "Owner 1", "name": "Team 1", "id": 1}
        mockFranchise2 = {"owner_name": "Owner 2", "name": "Team 2", "id": 2}
        mockLeague = {
            "league": {
                "id": 123,
                "name": "Test League 2022",
                "lastRegularSeasonWeek": "1",
                "franchises": {"franchise": [mockFranchise1, mockFranchise2]},
            }
        }

        mockSchedule = {
            "schedule": {
                "weeklySchedule": [
                    {"week": "1", "matchup": [{"franchise": [mockFranchise1, mockFranchise2]}]}
                ]
            }
        }
        mockPlayoffSchedule = {"playoffBracket": {"playoffRound": []}}

        mockGetLeague.side_effect = [mockLeague]
        mockGetSchedule.side_effect = [mockSchedule]
        mockGetPlayoffBracket.side_effect = [mockPlayoffSchedule]

        leagueLoader = MyFantasyLeagueLeagueLoader(
            "123", [2022], mflUsername="mflu", mflPassword="mflp", mflUserAgentName="mfluan"
        )
        leagueLoader.loadLeague()
