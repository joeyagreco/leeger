import unittest
from unittest import mock
from unittest.mock import Mock
import copy
from leeger.enum.MatchupType import MatchupType

from leeger.league_loader import MyFantasyLeagueLeagueLoader
from leeger.model.league.League import League
from leeger.model.league.Matchup import Matchup
from leeger.model.league.Owner import Owner
from leeger.model.league.Team import Team
from leeger.model.league.Week import Week
from leeger.model.league.Year import Year

from leeger.league_loader.FleaflickerLeagueLoader import FleaflickerLeagueLoader


class TestFleaflickerLeagueLoader(unittest.TestCase):
    """
    # TODO: Add better tests.
    """

    def test_init_leagueIdNotIntConvertable_raisesException(self):
        with self.assertRaises(ValueError) as context:
            FleaflickerLeagueLoader("foo", [])
        self.assertEqual("League ID 'foo' could not be turned into an int.", str(context.exception))

    @mock.patch("fleaflicker.api.LeagueInfoAPIClient.LeagueInfoAPIClient.get_league_standings")
    def test_loadLeague_happyPath_noOwnerNamesAndAliases(self, mockGetLeaguestandings):
        mockLeagueStandings2022 = {
            "divisions": [{"teams": [{"owners": [{"displayName": "Owner 1"}]}]}]
        }

        mockGetLeaguestandings.side_effect = [mockLeagueStandings2022]
