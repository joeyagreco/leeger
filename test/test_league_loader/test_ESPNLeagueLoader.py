import unittest
from unittest.mock import patch, Mock

from espn_api.requests.espn_requests import ESPNInvalidLeague
from leeger.enum.MatchupType import MatchupType

from leeger.league_loader.ESPNLeagueLoader import ESPNLeagueLoader
from leeger.model.league.League import League
from leeger.model.league.Matchup import Matchup
from leeger.model.league.Owner import Owner
from leeger.model.league.Team import Team
from leeger.model.league.Week import Week
from leeger.model.league.Year import Year


class TestESPNLeagueLoader(unittest.TestCase):
    """
    Currently, there is not a good way to test this class due to an issue addressed here: https://github.com/cwendt94/espn-api/issues/338
    For now, we can do some very basic tests.
    # TODO: Add better tests.
    """

    def test_loadLeague_intendedFailure(self):
        with self.assertRaises(ESPNInvalidLeague) as context:
            leagueLoader = ESPNLeagueLoader("0", [2000])
            leagueLoader.loadLeague()  # 0 is a bad league ID
        self.assertEqual("League 0 does not exist", str(context.exception))

    def test_loadLeague_nonIntPassingStringForLeagueId(self):
        with self.assertRaises(ValueError) as context:
            ESPNLeagueLoader("a", [2000])
        self.assertEqual("League ID 'a' could not be turned into an int.", str(context.exception))

    def test_noYearsGiven(self):
        with self.assertRaises(ValueError) as context:
            ESPNLeagueLoader("0", [])
        self.assertEqual("No years given to load league with ID '0'.", str(context.exception))

    @patch("espn_api.football.League")
    def test_load_league(self, mock_league):
        mock_espn_league = Mock()
        mock_espn_league.year = 2022
        mock_espn_league.current_week = 1
        mock_espn_league.settings.name = "Test League"
        mock_espn_league.settings.reg_season_count = 12
        mock_espn_league.teams = [
            Mock(
                team_id=1,
                owner="Owner 1",
                team_name="Team 1",
                outcomes=["W"],
                scores=[100],
                schedule=[Mock(team_id=2)],
            ),
            Mock(
                team_id=2,
                owner="Owner 2",
                team_name="Team 2",
                outcomes=["L"],
                scores=[80],
                schedule=[Mock(team_id=1)],
            ),
        ]
        mock_league.return_value = mock_espn_league

        loader = ESPNLeagueLoader("123", [2022])
        league = loader.loadLeague()

        # expected league
        team1 = Team(ownerId=1, name="Team 1")
        team2 = Team(ownerId=2, name="Team 2")

        expected_league = League(
            name="Test League",
            owners=[Owner(name="Owner 1"), Owner(name="Owner 2")],
            years=[
                Year(
                    yearNumber=2022,
                    teams=[team1, team2],
                    weeks=[
                        Week(
                            weekNumber=1,
                            matchups=[
                                Matchup(
                                    teamAId=team1.id,
                                    teamBId=team2.id,
                                    teamAScore=100,
                                    teamBScore=80,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                )
                            ],
                        )
                    ],
                )
            ],
        )
        print(league)
        self.assertEqual(league, expected_league)
