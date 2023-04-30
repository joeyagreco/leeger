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
            Mock(
                team_id=3,
                owner="Owner 3",
                team_name="Team 3",
                outcomes=["W"],
                scores=[90],
                schedule=[Mock(team_id=4)],
            ),
            Mock(
                team_id=4,
                owner="Owner 4",
                team_name="Team 4",
                outcomes=["L"],
                scores=[70],
                schedule=[Mock(team_id=3)],
            ),
            Mock(
                team_id=5,
                owner="Owner 5",
                team_name="Team 5",
                outcomes=["W"],
                scores=[110],
                schedule=[Mock(team_id=6)],
            ),
            Mock(
                team_id=6,
                owner="Owner 6",
                team_name="Team 6",
                outcomes=["L"],
                scores=[60],
                schedule=[Mock(team_id=5)],
            ),
            Mock(
                team_id=7,
                owner="Owner 7",
                team_name="Team 7",
                outcomes=["W"],
                scores=[120],
                schedule=[Mock(team_id=8)],
            ),
            Mock(
                team_id=8,
                owner="Owner 8",
                team_name="Team 8",
                outcomes=["L"],
                scores=[50],
                schedule=[Mock(team_id=7)],
            ),
        ]
        mock_league.return_value = mock_espn_league

        loader = ESPNLeagueLoader("123", [2022])
        league = loader.loadLeague()

        # expected league
        teams = [
            Team(ownerId=1, name="Team 1"),
            Team(ownerId=2, name="Team 2"),
            Team(ownerId=3, name="Team 3"),
            Team(ownerId=4, name="Team 4"),
            Team(ownerId=5, name="Team 5"),
            Team(ownerId=6, name="Team 6"),
            Team(ownerId=7, name="Team 7"),
            Team(ownerId=8, name="Team 8"),
        ]
        expected_league = League(
            name="Test League",
            owners=[
                Owner(name="Owner 1"),
                Owner(name="Owner 2"),
                Owner(name="Owner 3"),
                Owner(name="Owner 4"),
                Owner(name="Owner 5"),
                Owner(name="Owner 6"),
                Owner(name="Owner 7"),
                Owner(name="Owner 8"),
            ],
            years=[
                Year(
                    yearNumber=2022,
                    teams=teams,
                    weeks=[
                        Week(
                            weekNumber=1,
                            matchups=[
                                Matchup(
                                    teamAId=teams[0].id,
                                    teamBId=teams[1].id,
                                    teamAScore=100,
                                    teamBScore=80,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                ),
                                Matchup(
                                    teamAId=teams[2].id,
                                    teamBId=teams[3].id,
                                    teamAScore=90,
                                    teamBScore=70,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                ),
                                Matchup(
                                    teamAId=teams[4].id,
                                    teamBId=teams[5].id,
                                    teamAScore=110,
                                    teamBScore=60,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                ),
                                Matchup(
                                    teamAId=teams[6].id,
                                    teamBId=teams[7].id,
                                    teamAScore=120,
                                    teamBScore=50,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                ),
                            ],
                        )
                    ],
                )
            ],
        )
        self.assertEqual(league, expected_league)
