import unittest

from leeger.league_loader import SleeperLeagueLoader
from unittest.mock import patch, Mock
from sleeper.model import League as SleeperLeague


class TestSleeperLeagueLoader(unittest.TestCase):
    """
    # TODO: Add better tests.
    """

    def test_loadLeague_intendedFailure(self):
        with self.assertRaises(ValueError) as context:
            leagueLoader = SleeperLeagueLoader("0", [2000])
            leagueLoader.loadLeague()  # 0 is a bad league ID
        self.assertEqual("Could not find years '[2000]' for league.", str(context.exception))

    @patch("sleeper.api.LeagueAPIClient.get_league")
    def test_load_league(self, mock_get_league):
        # create mock SleeperLeague object
        mockSleeperLeague2022 = Mock()
        mockSleeperLeague2022.season = 2022
        mockSleeperLeague2022.status = "active"
        mockSleeperLeague2022.playoff_matchups = []
        mockSleeperLeague2022.settings.name = "Test League 2022"
        mockSleeperLeague2022.settings.reg_season_count = 2
        mockSleeperLeague2022.settings.playoff_team_count = 3
        mockSleeperLeague2022.teams = []

        mock_get_league.side_effect = [mockSleeperLeague2022]

        # create instance of SleeperLeagueLoader and call load_league method
        sleeper_league_loader = SleeperLeagueLoader("123", [2022])
        league = sleeper_league_loader.loadLeague()
