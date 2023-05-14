import unittest
from unittest import mock
from unittest.mock import Mock
import copy
from leeger.enum.MatchupType import MatchupType

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
    @mock.patch("fleaflicker.api.ScoringAPIClient.ScoringAPIClient.get_league_scoreboard")
    def test_loadLeague_happyPath_noOwnerNamesAndAliases(self, mockGetLeagueScoreboard,mockGetLeaguestandings):
        mockTeam1_2022 = {"owners": [{"displayName": "Owner 1"}], "id": 1, "name": "Team 1"}
        mockTeam2_2022 = {"owners": [{"displayName": "Owner 2"}], "id": 2, "name": "Team 2"}
        mockLeagueStandings2022 = {
            "divisions": [{"teams": [mockTeam1_2022, mockTeam2_2022]}],
            "league": {"name": "Test League 2022", "id": 123},
            "season": 2022
        }
        
        mockWeek1_2022 = {
            "games": [{"away": mockTeam1_2022, "home": mockTeam2_2022, "awayScore": {"score": {"value": 100}}, "homeScore": {"score": {"value": 90}}, "awayResult": "WIN", "homeResult": "LOSS", "isFinalScore": True}]
        }
        
        mockScoreboard2022 = {
            "eligibleSchedulePeriods": [mockWeek1_2022]
        }

        mockGetLeaguestandings.side_effect = [mockLeagueStandings2022]
        mockGetLeagueScoreboard.side_effect = [mockScoreboard2022, mockWeek1_2022]
        
        leagueLoader = FleaflickerLeagueLoader("123", [2022])
        league = leagueLoader.loadLeague()
