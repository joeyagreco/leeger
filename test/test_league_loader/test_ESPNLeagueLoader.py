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
    def test_load_league_happyPath(self, mock_league):
        mock_espn_league = Mock()
        mock_espn_league.year = 2022
        mock_espn_league.current_week = 4
        mock_espn_league.settings.name = "Test League"
        mock_espn_league.settings.reg_season_count = 2
        mock_espn_league.settings.playoff_team_count = 3
        mockTeam1 = Mock(
            team_id=1,
            owner="Owner 1",
            team_name="Team 1",
            outcomes=["W", "W", "U", "W"],
            scores=[100, 110, 0, 100],
            standing=1,
        )
        mockTeam2 = Mock(
            team_id=2,
            owner="Owner 2",
            team_name="Team 2",
            outcomes=["L", "L", "U", "U"],
            scores=[100, 70, 0, 0],
            standing=7,
        )
        mockTeam3 = Mock(
            team_id=3,
            owner="Owner 3",
            team_name="Team 3",
            outcomes=["W", "L", "L", "U"],
            scores=[90.5, 100, 80, 0],
            standing=3,
        )
        mockTeam4 = Mock(
            team_id=4,
            owner="Owner 4",
            team_name="Team 4",
            outcomes=["L", "W", "U", "U"],
            scores=[70.5, 80, 0, 0],
            standing=5,
        )
        mockTeam5 = Mock(
            team_id=5,
            owner="Owner 5",
            team_name="Team 5",
            outcomes=["W", "L", "U", "U"],
            scores=[110, 80, 0, 0],
            standing=4,
        )
        mockTeam6 = Mock(
            team_id=6,
            owner="Owner 6",
            team_name="Team 6",
            outcomes=["L", "W", "U", "U"],
            scores=[60, 90, 0, 0],
            standing=6,
        )
        mockTeam7 = Mock(
            team_id=7,
            owner="Owner 7",
            team_name="Team 7",
            outcomes=["W", "W", "W", "L"],
            scores=[120, 130, 90, 90],
            standing=2,
        )
        mockTeam8 = Mock(
            team_id=8,
            owner="Owner 8",
            team_name="Team 8",
            outcomes=["L", "L", "U", "U"],
            scores=[50, 40, 0, 0],
            standing=8,
        )
        # playoff seeds:
        # Team1: 1
        # Team7: 2
        # Team3: 3
        mockTeam1.schedule = [mockTeam2, mockTeam3, mockTeam4, mockTeam7]
        mockTeam2.schedule = [mockTeam1, mockTeam4, mockTeam5, mockTeam3]
        mockTeam3.schedule = [mockTeam4, mockTeam1, mockTeam7, mockTeam2]
        mockTeam4.schedule = [mockTeam3, mockTeam2, mockTeam1, mockTeam5]
        mockTeam5.schedule = [mockTeam6, mockTeam7, mockTeam2, mockTeam4]
        mockTeam6.schedule = [mockTeam5, mockTeam8, mockTeam8, mockTeam8]
        mockTeam7.schedule = [mockTeam8, mockTeam5, mockTeam3, mockTeam1]
        mockTeam8.schedule = [mockTeam7, mockTeam6, mockTeam6, mockTeam6]
        mock_espn_league.teams = [
            mockTeam1,
            mockTeam2,
            mockTeam3,
            mockTeam4,
            mockTeam5,
            mockTeam6,
            mockTeam7,
            mockTeam8,
        ]
        mock_league.return_value = mock_espn_league

        loader = ESPNLeagueLoader("123", [2022])
        league = loader.loadLeague()

        # expected league
        team1 = Team(ownerId=1, name="Team 1")
        team2 = Team(ownerId=2, name="Team 2")
        team3 = Team(ownerId=3, name="Team 3")
        team4 = Team(ownerId=4, name="Team 4")
        team5 = Team(ownerId=5, name="Team 5")
        team6 = Team(ownerId=6, name="Team 6")
        team7 = Team(ownerId=7, name="Team 7")
        team8 = Team(ownerId=8, name="Team 8")
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
                    teams=[team1, team2, team3, team4, team5, team6, team7, team8],
                    weeks=[
                        Week(
                            weekNumber=1,
                            matchups=[
                                Matchup(
                                    teamAId=team1.id,
                                    teamBId=team2.id,
                                    teamAScore=100,
                                    teamBScore=100,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team3.id,
                                    teamBId=team4.id,
                                    teamAScore=90.5,
                                    teamBScore=70.5,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team5.id,
                                    teamBId=team6.id,
                                    teamAScore=110,
                                    teamBScore=60,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team7.id,
                                    teamBId=team8.id,
                                    teamAScore=120,
                                    teamBScore=50,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                            ],
                        ),
                        Week(
                            weekNumber=2,
                            matchups=[
                                Matchup(
                                    teamAId=team1.id,
                                    teamBId=team3.id,
                                    teamAScore=110,
                                    teamBScore=100,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team2.id,
                                    teamBId=team4.id,
                                    teamAScore=70,
                                    teamBScore=80,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team5.id,
                                    teamBId=team7.id,
                                    teamAScore=80,
                                    teamBScore=130,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team6.id,
                                    teamBId=team8.id,
                                    teamAScore=90,
                                    teamBScore=40,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                            ],
                        ),
                        Week(
                            weekNumber=3,
                            matchups=[
                                Matchup(
                                    teamAId=team3.id,
                                    teamBId=team7.id,
                                    teamAScore=80,
                                    teamBScore=90,
                                    matchupType=MatchupType.PLAYOFF,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                )
                            ],
                        ),
                        Week(
                            weekNumber=4,
                            matchups=[
                                Matchup(
                                    teamAId=team1.id,
                                    teamBId=team7.id,
                                    teamAScore=100,
                                    teamBScore=90,
                                    matchupType=MatchupType.CHAMPIONSHIP,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                )
                            ],
                        ),
                    ],
                    yearSettings=None,
                )
            ],
        )
        self.assertEqual(league, expected_league)
