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
    # TODO: test ownerNamesAndAliases
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

    @patch("espn_api.football.League")
    def test_load_league_happyPath(self, mockLeague):
        # mock first year (2022)
        mockEspnLeague2022 = Mock()
        mockEspnLeague2022.year = 2022
        mockEspnLeague2022.current_week = 4
        mockEspnLeague2022.settings.name = "Test League 2022"
        mockEspnLeague2022.settings.reg_season_count = 2
        mockEspnLeague2022.settings.playoff_team_count = 3
        mockTeam1_2022 = Mock(
            team_id=1,
            owner="Owner 1",
            team_name="Team 1",
            outcomes=["W", "W", "U", "W"],
            scores=[100, 110, 0, 100],
            standing=1,
        )
        mockTeam2_2022 = Mock(
            team_id=2,
            owner="Owner 2",
            team_name="Team 2",
            outcomes=["L", "L", "L", "L"],
            scores=[100, 70, 1, 1],
            standing=7,
        )
        mockTeam3_2022 = Mock(
            team_id=3,
            owner="Owner 3",
            team_name="Team 3",
            outcomes=["W", "L", "L", "W"],
            scores=[90.5, 100, 80, 2],
            standing=3,
        )
        mockTeam4_2022 = Mock(
            team_id=4,
            owner="Owner 4",
            team_name="Team 4",
            outcomes=["L", "W", "U", "L"],
            scores=[70.5, 80, 0, 1],
            standing=5,
        )
        mockTeam5_2022 = Mock(
            team_id=5,
            owner="Owner 5",
            team_name="Team 5",
            outcomes=["W", "L", "W", "W"],
            scores=[110, 80, 2, 2],
            standing=4,
        )
        mockTeam6_2022 = Mock(
            team_id=6,
            owner="Owner 6",
            team_name="Team 6",
            outcomes=["L", "W", "W", "W"],
            scores=[60, 90, 2, 2],
            standing=6,
        )
        mockTeam7_2022 = Mock(
            team_id=7,
            owner="Owner 7",
            team_name="Team 7",
            outcomes=["W", "W", "W", "L"],
            scores=[120, 130, 90, 90],
            standing=2,
        )
        mockTeam8_2022 = Mock(
            team_id=8,
            owner="Owner 8",
            team_name="Team 8",
            outcomes=["L", "L", "L", "L"],
            scores=[50, 40, 1, 1],
            standing=8,
        )
        # playoff seeds:
        # Team1: 1
        # Team7: 2
        # Team3: 3
        mockTeam1_2022.schedule = [mockTeam2_2022, mockTeam3_2022, mockTeam4_2022, mockTeam7_2022]
        mockTeam2_2022.schedule = [mockTeam1_2022, mockTeam4_2022, mockTeam5_2022, mockTeam3_2022]
        mockTeam3_2022.schedule = [mockTeam4_2022, mockTeam1_2022, mockTeam7_2022, mockTeam2_2022]
        mockTeam4_2022.schedule = [mockTeam3_2022, mockTeam2_2022, mockTeam1_2022, mockTeam5_2022]
        mockTeam5_2022.schedule = [mockTeam6_2022, mockTeam7_2022, mockTeam2_2022, mockTeam4_2022]
        mockTeam6_2022.schedule = [mockTeam5_2022, mockTeam8_2022, mockTeam8_2022, mockTeam8_2022]
        mockTeam7_2022.schedule = [mockTeam8_2022, mockTeam5_2022, mockTeam3_2022, mockTeam1_2022]
        mockTeam8_2022.schedule = [mockTeam7_2022, mockTeam6_2022, mockTeam6_2022, mockTeam6_2022]
        mockEspnLeague2022.teams = [
            mockTeam1_2022,
            mockTeam2_2022,
            mockTeam3_2022,
            mockTeam4_2022,
            mockTeam5_2022,
            mockTeam6_2022,
            mockTeam7_2022,
            mockTeam8_2022,
        ]

        # mock second year (2023)
        mockEspnLeague2023 = Mock()
        mockEspnLeague2023.year = 2023
        mockEspnLeague2023.current_week = 1
        mockEspnLeague2023.settings.name = "Test League 2023"
        mockEspnLeague2023.settings.reg_season_count = 1
        mockTeam1_2023 = Mock(
            team_id=1, owner="Owner 1", team_name="Team 1", outcomes=["W"], scores=[100]
        )
        mockTeam2_2023 = Mock(
            team_id=2, owner="Owner 2", team_name="Team 2", outcomes=["L"], scores=[100]
        )
        mockTeam3_2023 = Mock(
            team_id=3, owner="Owner 3", team_name="Team 3", outcomes=["W"], scores=[90.5]
        )
        mockTeam4_2023 = Mock(
            team_id=4, owner="Owner 4", team_name="Team 4", outcomes=["L"], scores=[70.5]
        )
        mockTeam5_2023 = Mock(
            team_id=5, owner="Owner 5", team_name="Team 5", outcomes=["W"], scores=[110]
        )
        mockTeam6_2023 = Mock(
            team_id=6, owner="Owner 6", team_name="Team 6", outcomes=["L"], scores=[60]
        )
        mockTeam7_2023 = Mock(
            team_id=7, owner="Owner 7", team_name="Team 7", outcomes=["W"], scores=[120]
        )
        mockTeam8_2023 = Mock(
            team_id=8, owner="Owner 8", team_name="Team 8", outcomes=["L"], scores=[50]
        )
        mockTeam1_2023.schedule = [mockTeam2_2023]
        mockTeam2_2023.schedule = [mockTeam1_2023]
        mockTeam3_2023.schedule = [mockTeam4_2023]
        mockTeam4_2023.schedule = [mockTeam3_2023]
        mockTeam5_2023.schedule = [mockTeam6_2023]
        mockTeam6_2023.schedule = [mockTeam5_2023]
        mockTeam7_2023.schedule = [mockTeam8_2023]
        mockTeam8_2023.schedule = [mockTeam7_2023]
        mockEspnLeague2023.teams = [
            mockTeam1_2023,
            mockTeam2_2023,
            mockTeam3_2023,
            mockTeam4_2023,
            mockTeam5_2023,
            mockTeam6_2023,
            mockTeam7_2023,
            mockTeam8_2023,
        ]

        mockLeague.side_effect = [mockEspnLeague2022, mockEspnLeague2023]

        loader = ESPNLeagueLoader("123", [2022, 2023])
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
        expectedLeague = League(
            name="Test League 2023",
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
                                    teamAId=team2.id,
                                    teamBId=team5.id,
                                    teamAScore=1,
                                    teamBScore=2,
                                    matchupType=MatchupType.IGNORE,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team3.id,
                                    teamBId=team7.id,
                                    teamAScore=80,
                                    teamBScore=90,
                                    matchupType=MatchupType.PLAYOFF,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team6.id,
                                    teamBId=team8.id,
                                    teamAScore=2,
                                    teamBScore=1,
                                    matchupType=MatchupType.IGNORE,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
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
                                ),
                                Matchup(
                                    teamAId=team2.id,
                                    teamBId=team3.id,
                                    teamAScore=1,
                                    teamBScore=2,
                                    matchupType=MatchupType.IGNORE,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team4.id,
                                    teamBId=team5.id,
                                    teamAScore=1,
                                    teamBScore=2,
                                    matchupType=MatchupType.IGNORE,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team6.id,
                                    teamBId=team8.id,
                                    teamAScore=2,
                                    teamBScore=1,
                                    matchupType=MatchupType.IGNORE,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                            ],
                        ),
                    ],
                    yearSettings=None,
                ),
                Year(
                    yearNumber=2023,
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
                        )
                    ],
                    yearSettings=None,
                ),
            ],
        )
        self.assertEqual(league, expectedLeague)
