import unittest
from unittest.mock import MagicMock, Mock, patch

from leeger.enum.MatchupType import MatchupType
from leeger.league_loader.ESPNLeagueLoader import ESPNLeagueLoader
from leeger.model.league.Division import Division
from leeger.model.league.League import League
from leeger.model.league.Matchup import Matchup
from leeger.model.league.Owner import Owner
from leeger.model.league.Team import Team
from leeger.model.league.Week import Week
from leeger.model.league.Year import Year


class TestESPNLeagueLoader(unittest.TestCase):
    def __getMockOwnersList(self, firstName: str, lastName: str) -> list[dict]:
        return [{"firstName": firstName, "lastName": lastName}]

    def test_loadLeague_nonIntPassingStringForLeagueId(self):
        with self.assertRaises(ValueError) as context:
            ESPNLeagueLoader("a", [2000])
        self.assertEqual(
            "League ID 'a' could not be turned into an int.", str(context.exception)
        )

    @patch("espn_api.football.League")
    def test_load_league_happyPath(self, mockLeague):
        # mock first year (2022)
        mockEspnLeague2022 = Mock()
        mockEspnLeague2022.year = 2022
        mockEspnLeague2022.current_week = 4
        mockEspnLeague2022.settings.name = "Test League 2022"
        mockEspnLeague2022.settings.reg_season_count = 2
        mockEspnLeague2022.settings.playoff_team_count = 3
        mockEspnLeague2022.settings.division_map = {0: "d1_2022", 1: "d2_2022"}
        mockTeam1_2022 = Mock(
            team_id=1,
            owners=self.__getMockOwnersList("Owner", "1"),
            team_name="Team 1",
            outcomes=["W", "W", "U", "W"],
            scores=[100, 110, 0, 100],
            standing=1,
            division_id=0,
        )
        mockTeam2_2022 = Mock(
            team_id=2,
            owners=self.__getMockOwnersList("Owner", "2"),
            team_name="Team 2",
            outcomes=["L", "L", "L", "L"],
            scores=[100, 70, 1, 1],
            standing=7,
            division_id=0,
        )
        mockTeam3_2022 = Mock(
            team_id=3,
            owners=self.__getMockOwnersList("Owner", "3"),
            team_name="Team 3",
            outcomes=["W", "L", "L", "W"],
            scores=[90.5, 100, 80, 2],
            standing=3,
            division_id=0,
        )
        mockTeam4_2022 = Mock(
            team_id=4,
            owners=self.__getMockOwnersList("Owner", "4"),
            team_name="Team 4",
            outcomes=["L", "W", "U", "L"],
            scores=[70.5, 80, 0, 1],
            standing=5,
            division_id=0,
        )
        mockTeam5_2022 = Mock(
            team_id=5,
            owners=self.__getMockOwnersList("Owner", "5"),
            team_name="Team 5",
            outcomes=["W", "L", "W", "W"],
            scores=[110, 80, 2, 2],
            standing=4,
            division_id=1,
        )
        mockTeam6_2022 = Mock(
            team_id=6,
            owners=self.__getMockOwnersList("Owner", "6"),
            team_name="Team 6",
            outcomes=["L", "W", "W", "W"],
            scores=[60, 90, 2, 2],
            standing=6,
            division_id=1,
        )
        mockTeam7_2022 = Mock(
            team_id=7,
            owners=self.__getMockOwnersList("Owner", "7"),
            team_name="Team 7",
            outcomes=["W", "W", "W", "L"],
            scores=[120, 130, 90, 90],
            standing=2,
            division_id=1,
        )
        mockTeam8_2022 = Mock(
            team_id=8,
            owners=self.__getMockOwnersList("Owner", "8"),
            team_name="Team 8",
            outcomes=["L", "L", "L", "L"],
            scores=[50, 40, 1, 1],
            standing=8,
            division_id=1,
        )
        # playoff seeds:
        # Team1: 1
        # Team7: 2
        # Team3: 3
        mockTeam1_2022.schedule = [
            mockTeam2_2022,
            mockTeam3_2022,
            mockTeam4_2022,
            mockTeam7_2022,
        ]
        mockTeam2_2022.schedule = [
            mockTeam1_2022,
            mockTeam4_2022,
            mockTeam5_2022,
            mockTeam3_2022,
        ]
        mockTeam3_2022.schedule = [
            mockTeam4_2022,
            mockTeam1_2022,
            mockTeam7_2022,
            mockTeam2_2022,
        ]
        mockTeam4_2022.schedule = [
            mockTeam3_2022,
            mockTeam2_2022,
            mockTeam1_2022,
            mockTeam5_2022,
        ]
        mockTeam5_2022.schedule = [
            mockTeam6_2022,
            mockTeam7_2022,
            mockTeam2_2022,
            mockTeam4_2022,
        ]
        mockTeam6_2022.schedule = [
            mockTeam5_2022,
            mockTeam8_2022,
            mockTeam8_2022,
            mockTeam8_2022,
        ]
        mockTeam7_2022.schedule = [
            mockTeam8_2022,
            mockTeam5_2022,
            mockTeam3_2022,
            mockTeam1_2022,
        ]
        mockTeam8_2022.schedule = [
            mockTeam7_2022,
            mockTeam6_2022,
            mockTeam6_2022,
            mockTeam6_2022,
        ]
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
        mockEspnLeague2023.settings.division_map = {0: "d1_2023", 1: "d2_2023"}
        mockTeam1_2023 = Mock(
            team_id=1,
            owners=self.__getMockOwnersList("Owner", "1"),
            team_name="Team 1",
            outcomes=["W"],
            scores=[100],
            division_id=0,
        )
        mockTeam2_2023 = Mock(
            team_id=2,
            owners=self.__getMockOwnersList("Owner", "2"),
            team_name="Team 2",
            outcomes=["L"],
            scores=[100],
            division_id=0,
        )
        mockTeam3_2023 = Mock(
            team_id=3,
            owners=self.__getMockOwnersList("Owner", "3"),
            team_name="Team 3",
            outcomes=["W"],
            scores=[90.5],
            division_id=0,
        )
        mockTeam4_2023 = Mock(
            team_id=4,
            owners=self.__getMockOwnersList("Owner", "4"),
            team_name="Team 4",
            outcomes=["L"],
            scores=[70.5],
            division_id=0,
        )
        mockTeam5_2023 = Mock(
            team_id=5,
            owners=self.__getMockOwnersList("Owner", "5"),
            team_name="Team 5",
            outcomes=["W"],
            scores=[110],
            division_id=1,
        )
        mockTeam6_2023 = Mock(
            team_id=6,
            owners=self.__getMockOwnersList("Owner", "6"),
            team_name="Team 6",
            outcomes=["L"],
            scores=[60],
            division_id=1,
        )
        mockTeam7_2023 = Mock(
            team_id=7,
            owners=self.__getMockOwnersList("Owner", "7"),
            team_name="Team 7",
            outcomes=["W"],
            scores=[120],
            division_id=1,
        )
        mockTeam8_2023 = Mock(
            team_id=8,
            owners=self.__getMockOwnersList("Owner", "8"),
            team_name="Team 8",
            outcomes=["L"],
            scores=[50],
            division_id=1,
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

        owner1 = Owner(name="Owner 1")
        owner2 = Owner(name="Owner 2")
        owner3 = Owner(name="Owner 3")
        owner4 = Owner(name="Owner 4")
        owner5 = Owner(name="Owner 5")
        owner6 = Owner(name="Owner 6")
        owner7 = Owner(name="Owner 7")
        owner8 = Owner(name="Owner 8")

        division1_2022 = Division(name="d1_2022")
        division2_2022 = Division(name="d2_2022")

        division1_2023 = Division(name="d1_2023")
        division2_2023 = Division(name="d2_2023")

        team1_2022 = Team(
            ownerId=owner1.id, name="Team 1", divisionId=division1_2022.id
        )
        team2_2022 = Team(
            ownerId=owner2.id, name="Team 2", divisionId=division1_2022.id
        )
        team3_2022 = Team(
            ownerId=owner3.id, name="Team 3", divisionId=division1_2022.id
        )
        team4_2022 = Team(
            ownerId=owner4.id, name="Team 4", divisionId=division1_2022.id
        )
        team5_2022 = Team(
            ownerId=owner5.id, name="Team 5", divisionId=division2_2022.id
        )
        team6_2022 = Team(
            ownerId=owner6.id, name="Team 6", divisionId=division2_2022.id
        )
        team7_2022 = Team(
            ownerId=owner7.id, name="Team 7", divisionId=division2_2022.id
        )
        team8_2022 = Team(
            ownerId=owner8.id, name="Team 8", divisionId=division2_2022.id
        )

        team1_2023 = Team(
            ownerId=owner1.id, name="Team 1", divisionId=division1_2023.id
        )
        team2_2023 = Team(
            ownerId=owner2.id, name="Team 2", divisionId=division1_2023.id
        )
        team3_2023 = Team(
            ownerId=owner3.id, name="Team 3", divisionId=division1_2023.id
        )
        team4_2023 = Team(
            ownerId=owner4.id, name="Team 4", divisionId=division1_2023.id
        )
        team5_2023 = Team(
            ownerId=owner5.id, name="Team 5", divisionId=division2_2023.id
        )
        team6_2023 = Team(
            ownerId=owner6.id, name="Team 6", divisionId=division2_2023.id
        )
        team7_2023 = Team(
            ownerId=owner7.id, name="Team 7", divisionId=division2_2023.id
        )
        team8_2023 = Team(
            ownerId=owner8.id, name="Team 8", divisionId=division2_2023.id
        )

        expectedLeague = League(
            name="Test League 2023",
            owners=[owner1, owner2, owner3, owner4, owner5, owner6, owner7, owner8],
            years=[
                Year(
                    yearNumber=2022,
                    teams=[
                        team1_2022,
                        team2_2022,
                        team3_2022,
                        team4_2022,
                        team5_2022,
                        team6_2022,
                        team7_2022,
                        team8_2022,
                    ],
                    weeks=[
                        Week(
                            weekNumber=1,
                            matchups=[
                                Matchup(
                                    teamAId=team1_2022.id,
                                    teamBId=team2_2022.id,
                                    teamAScore=100,
                                    teamBScore=100,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team3_2022.id,
                                    teamBId=team4_2022.id,
                                    teamAScore=90.5,
                                    teamBScore=70.5,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team5_2022.id,
                                    teamBId=team6_2022.id,
                                    teamAScore=110,
                                    teamBScore=60,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team7_2022.id,
                                    teamBId=team8_2022.id,
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
                                    teamAId=team1_2022.id,
                                    teamBId=team3_2022.id,
                                    teamAScore=110,
                                    teamBScore=100,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team2_2022.id,
                                    teamBId=team4_2022.id,
                                    teamAScore=70,
                                    teamBScore=80,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team5_2022.id,
                                    teamBId=team7_2022.id,
                                    teamAScore=80,
                                    teamBScore=130,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team6_2022.id,
                                    teamBId=team8_2022.id,
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
                                    teamAId=team2_2022.id,
                                    teamBId=team5_2022.id,
                                    teamAScore=1,
                                    teamBScore=2,
                                    matchupType=MatchupType.IGNORE,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team3_2022.id,
                                    teamBId=team7_2022.id,
                                    teamAScore=80,
                                    teamBScore=90,
                                    matchupType=MatchupType.PLAYOFF,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team6_2022.id,
                                    teamBId=team8_2022.id,
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
                                    teamAId=team1_2022.id,
                                    teamBId=team7_2022.id,
                                    teamAScore=100,
                                    teamBScore=90,
                                    matchupType=MatchupType.CHAMPIONSHIP,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team2_2022.id,
                                    teamBId=team3_2022.id,
                                    teamAScore=1,
                                    teamBScore=2,
                                    matchupType=MatchupType.IGNORE,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team4_2022.id,
                                    teamBId=team5_2022.id,
                                    teamAScore=1,
                                    teamBScore=2,
                                    matchupType=MatchupType.IGNORE,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team6_2022.id,
                                    teamBId=team8_2022.id,
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
                    divisions=[division1_2022, division2_2022],
                ),
                Year(
                    yearNumber=2023,
                    teams=[
                        team1_2023,
                        team2_2023,
                        team3_2023,
                        team4_2023,
                        team5_2023,
                        team6_2023,
                        team7_2023,
                        team8_2023,
                    ],
                    weeks=[
                        Week(
                            weekNumber=1,
                            matchups=[
                                Matchup(
                                    teamAId=team1_2023.id,
                                    teamBId=team2_2023.id,
                                    teamAScore=100,
                                    teamBScore=100,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team3_2023.id,
                                    teamBId=team4_2023.id,
                                    teamAScore=90.5,
                                    teamBScore=70.5,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team5_2023.id,
                                    teamBId=team6_2023.id,
                                    teamAScore=110,
                                    teamBScore=60,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team7_2023.id,
                                    teamBId=team8_2023.id,
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
                    divisions=[division1_2023, division2_2023],
                ),
            ],
        )
        self.assertTrue(
            league.equals(expectedLeague, ignoreBaseIds=True, ignoreIds=True)
        )
        # check multiWeekMatchupIds
        for year in league.years:
            for week in year.weeks:
                for matchup in week.matchups:
                    self.assertIsNone(matchup.multiWeekMatchupId)

    @patch("espn_api.football.League")
    def test_load_league_happyPath_withOwnerNamesAndAliases(self, mockLeague):
        # mock first year (2022)
        mockEspnLeague2022 = Mock()
        mockEspnLeague2022.year = 2022
        mockEspnLeague2022.current_week = 4
        mockEspnLeague2022.settings.name = "Test League 2022"
        mockEspnLeague2022.settings.reg_season_count = 2
        mockEspnLeague2022.settings.playoff_team_count = 3
        mockEspnLeague2022.settings.division_map = {0: "d1_2022", 1: "d2_2022"}
        mockTeam1_2022 = Mock(
            team_id=1,
            owners=self.__getMockOwnersList("Owner", "1"),
            team_name="Team 1",
            outcomes=["W", "W", "U", "W"],
            scores=[100, 110, 0, 100],
            standing=1,
            division_id=0,
        )
        mockTeam2_2022 = Mock(
            team_id=2,
            owners=self.__getMockOwnersList("Owner", "2"),
            team_name="Team 2",
            outcomes=["L", "L", "L", "L"],
            scores=[100, 70, 1, 1],
            standing=7,
            division_id=0,
        )
        mockTeam3_2022 = Mock(
            team_id=3,
            owners=self.__getMockOwnersList("Owner", "3"),
            team_name="Team 3",
            outcomes=["W", "L", "L", "W"],
            scores=[90.5, 100, 80, 2],
            standing=3,
            division_id=0,
        )
        mockTeam4_2022 = Mock(
            team_id=4,
            owners=self.__getMockOwnersList("Owner", "4"),
            team_name="Team 4",
            outcomes=["L", "W", "U", "L"],
            scores=[70.5, 80, 0, 1],
            standing=5,
            division_id=0,
        )
        mockTeam5_2022 = Mock(
            team_id=5,
            owners=self.__getMockOwnersList("Owner", "5"),
            team_name="Team 5",
            outcomes=["W", "L", "W", "W"],
            scores=[110, 80, 2, 2],
            standing=4,
            division_id=1,
        )
        mockTeam6_2022 = Mock(
            team_id=6,
            owners=self.__getMockOwnersList("Owner", "6"),
            team_name="Team 6",
            outcomes=["L", "W", "W", "W"],
            scores=[60, 90, 2, 2],
            standing=6,
            division_id=1,
        )
        mockTeam7_2022 = Mock(
            team_id=7,
            owners=self.__getMockOwnersList("Owner", "7"),
            team_name="Team 7",
            outcomes=["W", "W", "W", "L"],
            scores=[120, 130, 90, 90],
            standing=2,
            division_id=1,
        )
        mockTeam8_2022 = Mock(
            team_id=8,
            owners=self.__getMockOwnersList("Owner", "8"),
            team_name="Team 8",
            outcomes=["L", "L", "L", "L"],
            scores=[50, 40, 1, 1],
            standing=8,
            division_id=1,
        )
        # playoff seeds:
        # Team1: 1
        # Team7: 2
        # Team3: 3
        mockTeam1_2022.schedule = [
            mockTeam2_2022,
            mockTeam3_2022,
            mockTeam4_2022,
            mockTeam7_2022,
        ]
        mockTeam2_2022.schedule = [
            mockTeam1_2022,
            mockTeam4_2022,
            mockTeam5_2022,
            mockTeam3_2022,
        ]
        mockTeam3_2022.schedule = [
            mockTeam4_2022,
            mockTeam1_2022,
            mockTeam7_2022,
            mockTeam2_2022,
        ]
        mockTeam4_2022.schedule = [
            mockTeam3_2022,
            mockTeam2_2022,
            mockTeam1_2022,
            mockTeam5_2022,
        ]
        mockTeam5_2022.schedule = [
            mockTeam6_2022,
            mockTeam7_2022,
            mockTeam2_2022,
            mockTeam4_2022,
        ]
        mockTeam6_2022.schedule = [
            mockTeam5_2022,
            mockTeam8_2022,
            mockTeam8_2022,
            mockTeam8_2022,
        ]
        mockTeam7_2022.schedule = [
            mockTeam8_2022,
            mockTeam5_2022,
            mockTeam3_2022,
            mockTeam1_2022,
        ]
        mockTeam8_2022.schedule = [
            mockTeam7_2022,
            mockTeam6_2022,
            mockTeam6_2022,
            mockTeam6_2022,
        ]
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
        mockEspnLeague2023.settings.division_map = {0: "d1_2023", 1: "d2_2023"}
        mockTeam1_2023 = Mock(
            team_id=1,
            owners=self.__getMockOwnersList("Owner", "1"),
            team_name="Team 1",
            outcomes=["W"],
            scores=[100],
            division_id=0,
        )
        mockTeam2_2023 = Mock(
            team_id=2,
            owners=self.__getMockOwnersList("Owner", "2"),
            team_name="Team 2",
            outcomes=["L"],
            scores=[100],
            division_id=0,
        )
        mockTeam3_2023 = Mock(
            team_id=3,
            owners=self.__getMockOwnersList("Owner", "3"),
            team_name="Team 3",
            outcomes=["W"],
            scores=[90.5],
            division_id=0,
        )
        mockTeam4_2023 = Mock(
            team_id=4,
            owners=self.__getMockOwnersList("Owner", "4"),
            team_name="Team 4",
            outcomes=["L"],
            scores=[70.5],
            division_id=0,
        )
        mockTeam5_2023 = Mock(
            team_id=5,
            owners=self.__getMockOwnersList("Owner", "5"),
            team_name="Team 5",
            outcomes=["W"],
            scores=[110],
            division_id=1,
        )
        mockTeam6_2023 = Mock(
            team_id=6,
            owners=self.__getMockOwnersList("Owner", "6"),
            team_name="Team 6",
            outcomes=["L"],
            scores=[60],
            division_id=1,
        )
        mockTeam7_2023 = Mock(
            team_id=7,
            owners=self.__getMockOwnersList("Owner", "7"),
            team_name="Team 7",
            outcomes=["W"],
            scores=[120],
            division_id=1,
        )
        mockTeam8_2023 = Mock(
            team_id=8,
            owners=self.__getMockOwnersList("Owner", "8"),
            team_name="Team 8",
            outcomes=["L"],
            scores=[50],
            division_id=1,
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

        loader = ESPNLeagueLoader(
            "123",
            [2022, 2023],
            ownerNamesAndAliases={
                "o1": ["Owner 1"],
                "o2": ["Owner 2"],
                "o3": ["Owner 3"],
                "o4": ["Owner 4"],
                "o5": ["Owner 5"],
                "o6": ["Owner 6"],
                "o7": ["Owner 7"],
                "o8": ["Owner 8"],
            },
        )
        league = loader.loadLeague()

        # expected league

        owner1 = Owner(name="o1")
        owner2 = Owner(name="o2")
        owner3 = Owner(name="o3")
        owner4 = Owner(name="o4")
        owner5 = Owner(name="o5")
        owner6 = Owner(name="o6")
        owner7 = Owner(name="o7")
        owner8 = Owner(name="o8")

        division1_2022 = Division(name="d1_2022")
        division2_2022 = Division(name="d2_2022")

        division1_2023 = Division(name="d1_2023")
        division2_2023 = Division(name="d2_2023")

        team1_2022 = Team(
            ownerId=owner1.id, name="Team 1", divisionId=division1_2022.id
        )
        team2_2022 = Team(
            ownerId=owner2.id, name="Team 2", divisionId=division1_2022.id
        )
        team3_2022 = Team(
            ownerId=owner3.id, name="Team 3", divisionId=division1_2022.id
        )
        team4_2022 = Team(
            ownerId=owner4.id, name="Team 4", divisionId=division1_2022.id
        )
        team5_2022 = Team(
            ownerId=owner5.id, name="Team 5", divisionId=division2_2022.id
        )
        team6_2022 = Team(
            ownerId=owner6.id, name="Team 6", divisionId=division2_2022.id
        )
        team7_2022 = Team(
            ownerId=owner7.id, name="Team 7", divisionId=division2_2022.id
        )
        team8_2022 = Team(
            ownerId=owner8.id, name="Team 8", divisionId=division2_2022.id
        )

        team1_2023 = Team(
            ownerId=owner1.id, name="Team 1", divisionId=division1_2023.id
        )
        team2_2023 = Team(
            ownerId=owner2.id, name="Team 2", divisionId=division1_2023.id
        )
        team3_2023 = Team(
            ownerId=owner3.id, name="Team 3", divisionId=division1_2023.id
        )
        team4_2023 = Team(
            ownerId=owner4.id, name="Team 4", divisionId=division1_2023.id
        )
        team5_2023 = Team(
            ownerId=owner5.id, name="Team 5", divisionId=division2_2023.id
        )
        team6_2023 = Team(
            ownerId=owner6.id, name="Team 6", divisionId=division2_2023.id
        )
        team7_2023 = Team(
            ownerId=owner7.id, name="Team 7", divisionId=division2_2023.id
        )
        team8_2023 = Team(
            ownerId=owner8.id, name="Team 8", divisionId=division2_2023.id
        )

        expectedLeague = League(
            name="Test League 2023",
            owners=[owner1, owner2, owner3, owner4, owner5, owner6, owner7, owner8],
            years=[
                Year(
                    yearNumber=2022,
                    teams=[
                        team1_2022,
                        team2_2022,
                        team3_2022,
                        team4_2022,
                        team5_2022,
                        team6_2022,
                        team7_2022,
                        team8_2022,
                    ],
                    weeks=[
                        Week(
                            weekNumber=1,
                            matchups=[
                                Matchup(
                                    teamAId=team1_2022.id,
                                    teamBId=team2_2022.id,
                                    teamAScore=100,
                                    teamBScore=100,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team3_2022.id,
                                    teamBId=team4_2022.id,
                                    teamAScore=90.5,
                                    teamBScore=70.5,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team5_2022.id,
                                    teamBId=team6_2022.id,
                                    teamAScore=110,
                                    teamBScore=60,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team7_2022.id,
                                    teamBId=team8_2022.id,
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
                                    teamAId=team1_2022.id,
                                    teamBId=team3_2022.id,
                                    teamAScore=110,
                                    teamBScore=100,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team2_2022.id,
                                    teamBId=team4_2022.id,
                                    teamAScore=70,
                                    teamBScore=80,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team5_2022.id,
                                    teamBId=team7_2022.id,
                                    teamAScore=80,
                                    teamBScore=130,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team6_2022.id,
                                    teamBId=team8_2022.id,
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
                                    teamAId=team2_2022.id,
                                    teamBId=team5_2022.id,
                                    teamAScore=1,
                                    teamBScore=2,
                                    matchupType=MatchupType.IGNORE,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team3_2022.id,
                                    teamBId=team7_2022.id,
                                    teamAScore=80,
                                    teamBScore=90,
                                    matchupType=MatchupType.PLAYOFF,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team6_2022.id,
                                    teamBId=team8_2022.id,
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
                                    teamAId=team1_2022.id,
                                    teamBId=team7_2022.id,
                                    teamAScore=100,
                                    teamBScore=90,
                                    matchupType=MatchupType.CHAMPIONSHIP,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team2_2022.id,
                                    teamBId=team3_2022.id,
                                    teamAScore=1,
                                    teamBScore=2,
                                    matchupType=MatchupType.IGNORE,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team4_2022.id,
                                    teamBId=team5_2022.id,
                                    teamAScore=1,
                                    teamBScore=2,
                                    matchupType=MatchupType.IGNORE,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team6_2022.id,
                                    teamBId=team8_2022.id,
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
                    divisions=[division1_2022, division2_2022],
                ),
                Year(
                    yearNumber=2023,
                    teams=[
                        team1_2023,
                        team2_2023,
                        team3_2023,
                        team4_2023,
                        team5_2023,
                        team6_2023,
                        team7_2023,
                        team8_2023,
                    ],
                    weeks=[
                        Week(
                            weekNumber=1,
                            matchups=[
                                Matchup(
                                    teamAId=team1_2023.id,
                                    teamBId=team2_2023.id,
                                    teamAScore=100,
                                    teamBScore=100,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team3_2023.id,
                                    teamBId=team4_2023.id,
                                    teamAScore=90.5,
                                    teamBScore=70.5,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team5_2023.id,
                                    teamBId=team6_2023.id,
                                    teamAScore=110,
                                    teamBScore=60,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team7_2023.id,
                                    teamBId=team8_2023.id,
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
                    divisions=[division1_2023, division2_2023],
                ),
            ],
        )
        self.assertTrue(
            league.equals(expectedLeague, ignoreBaseIds=True, ignoreIds=True)
        )
        # check multiWeekMatchupIds
        for year in league.years:
            for week in year.weeks:
                for matchup in week.matchups:
                    self.assertIsNone(matchup.multiWeekMatchupId)

    @patch("espn_api.football.League")
    def test_load_league_withLeagueName(self, mockLeague):
        # mock first year (2022)
        mockEspnLeague2022 = Mock()
        mockEspnLeague2022.year = 2022
        mockEspnLeague2022.current_week = 4
        mockEspnLeague2022.settings.name = "Test League 2022"
        mockEspnLeague2022.settings.reg_season_count = 2
        mockEspnLeague2022.settings.playoff_team_count = 3
        mockEspnLeague2022.settings.division_map = {0: "d1_2022", 1: "d2_2022"}
        mockTeam1_2022 = Mock(
            team_id=1,
            owners=self.__getMockOwnersList("Owner", "1"),
            team_name="Team 1",
            outcomes=["W", "W", "U", "W"],
            scores=[100, 110, 0, 100],
            standing=1,
            division_id=0,
        )
        mockTeam2_2022 = Mock(
            team_id=2,
            owners=self.__getMockOwnersList("Owner", "2"),
            team_name="Team 2",
            outcomes=["L", "L", "L", "L"],
            scores=[100, 70, 1, 1],
            standing=7,
            division_id=0,
        )
        mockTeam3_2022 = Mock(
            team_id=3,
            owners=self.__getMockOwnersList("Owner", "3"),
            team_name="Team 3",
            outcomes=["W", "L", "L", "W"],
            scores=[90.5, 100, 80, 2],
            standing=3,
            division_id=0,
        )
        mockTeam4_2022 = Mock(
            team_id=4,
            owners=self.__getMockOwnersList("Owner", "4"),
            team_name="Team 4",
            outcomes=["L", "W", "U", "L"],
            scores=[70.5, 80, 0, 1],
            standing=5,
            division_id=0,
        )
        mockTeam5_2022 = Mock(
            team_id=5,
            owners=self.__getMockOwnersList("Owner", "5"),
            team_name="Team 5",
            outcomes=["W", "L", "W", "W"],
            scores=[110, 80, 2, 2],
            standing=4,
            division_id=1,
        )
        mockTeam6_2022 = Mock(
            team_id=6,
            owners=self.__getMockOwnersList("Owner", "6"),
            team_name="Team 6",
            outcomes=["L", "W", "W", "W"],
            scores=[60, 90, 2, 2],
            standing=6,
            division_id=1,
        )
        mockTeam7_2022 = Mock(
            team_id=7,
            owners=self.__getMockOwnersList("Owner", "7"),
            team_name="Team 7",
            outcomes=["W", "W", "W", "L"],
            scores=[120, 130, 90, 90],
            standing=2,
            division_id=1,
        )
        mockTeam8_2022 = Mock(
            team_id=8,
            owners=self.__getMockOwnersList("Owner", "8"),
            team_name="Team 8",
            outcomes=["L", "L", "L", "L"],
            scores=[50, 40, 1, 1],
            standing=8,
            division_id=1,
        )
        # playoff seeds:
        # Team1: 1
        # Team7: 2
        # Team3: 3
        mockTeam1_2022.schedule = [
            mockTeam2_2022,
            mockTeam3_2022,
            mockTeam4_2022,
            mockTeam7_2022,
        ]
        mockTeam2_2022.schedule = [
            mockTeam1_2022,
            mockTeam4_2022,
            mockTeam5_2022,
            mockTeam3_2022,
        ]
        mockTeam3_2022.schedule = [
            mockTeam4_2022,
            mockTeam1_2022,
            mockTeam7_2022,
            mockTeam2_2022,
        ]
        mockTeam4_2022.schedule = [
            mockTeam3_2022,
            mockTeam2_2022,
            mockTeam1_2022,
            mockTeam5_2022,
        ]
        mockTeam5_2022.schedule = [
            mockTeam6_2022,
            mockTeam7_2022,
            mockTeam2_2022,
            mockTeam4_2022,
        ]
        mockTeam6_2022.schedule = [
            mockTeam5_2022,
            mockTeam8_2022,
            mockTeam8_2022,
            mockTeam8_2022,
        ]
        mockTeam7_2022.schedule = [
            mockTeam8_2022,
            mockTeam5_2022,
            mockTeam3_2022,
            mockTeam1_2022,
        ]
        mockTeam8_2022.schedule = [
            mockTeam7_2022,
            mockTeam6_2022,
            mockTeam6_2022,
            mockTeam6_2022,
        ]
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
        mockEspnLeague2023.settings.division_map = {0: "d1_2023", 1: "d2_2023"}
        mockTeam1_2023 = Mock(
            team_id=1,
            owners=self.__getMockOwnersList("Owner", "1"),
            team_name="Team 1",
            outcomes=["W"],
            scores=[100],
            division_id=0,
        )
        mockTeam2_2023 = Mock(
            team_id=2,
            owners=self.__getMockOwnersList("Owner", "2"),
            team_name="Team 2",
            outcomes=["L"],
            scores=[100],
            division_id=0,
        )
        mockTeam3_2023 = Mock(
            team_id=3,
            owners=self.__getMockOwnersList("Owner", "3"),
            team_name="Team 3",
            outcomes=["W"],
            scores=[90.5],
            division_id=0,
        )
        mockTeam4_2023 = Mock(
            team_id=4,
            owners=self.__getMockOwnersList("Owner", "4"),
            team_name="Team 4",
            outcomes=["L"],
            scores=[70.5],
            division_id=0,
        )
        mockTeam5_2023 = Mock(
            team_id=5,
            owners=self.__getMockOwnersList("Owner", "5"),
            team_name="Team 5",
            outcomes=["W"],
            scores=[110],
            division_id=1,
        )
        mockTeam6_2023 = Mock(
            team_id=6,
            owners=self.__getMockOwnersList("Owner", "6"),
            team_name="Team 6",
            outcomes=["L"],
            scores=[60],
            division_id=1,
        )
        mockTeam7_2023 = Mock(
            team_id=7,
            owners=self.__getMockOwnersList("Owner", "7"),
            team_name="Team 7",
            outcomes=["W"],
            scores=[120],
            division_id=1,
        )
        mockTeam8_2023 = Mock(
            team_id=8,
            owners=self.__getMockOwnersList("Owner", "8"),
            team_name="Team 8",
            outcomes=["L"],
            scores=[50],
            division_id=1,
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

        loader = ESPNLeagueLoader("123", [2022, 2023], leagueName="custom name")
        league = loader.loadLeague()

        self.assertEqual("custom name", league.name)
