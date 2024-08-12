import copy
import unittest
from unittest import mock
from unittest.mock import Mock

from leeger.enum.MatchupType import MatchupType
from leeger.league_loader import YahooLeagueLoader
from leeger.model.league.League import League
from leeger.model.league.Matchup import Matchup
from leeger.model.league.Owner import Owner
from leeger.model.league.Team import Team
from leeger.model.league.Week import Week
from leeger.model.league.Year import Year


class TestYahooLeagueLoader(unittest.TestCase):
    # helper methods
    def __getMockTeamsMethod(self, teams: list) -> callable:
        def mockTeamsMethod():
            return teams

        return mockTeamsMethod

    def __getMockWeeksMethod(self, weeks: list) -> callable:
        def mockWeeksMethod():
            return weeks

        return mockWeeksMethod

    def __getMockYahooTeam(
        self,
        *,
        teamId: int,
        teamKey: int,
        name: str,
        managerNickname: str,
        managerId: int,
    ) -> Mock:
        mockTeam = Mock()
        mockTeam.team_id = teamId
        mockTeam.team_key = teamKey
        mockTeam.name = name
        mockTeam.manager.nickname = managerNickname
        mockTeam.manager.manager_id = managerId
        return mockTeam

    def __getMockYahooMatchup(
        self,
        *,
        week: int,
        status: str,
        winnerTeamKey: int,
        isTied: int,
        isPlayoffs: int,
        isConsolation: int,
        league: Mock,
    ) -> Mock:
        # duplicate mockYahooTeam to avoid using the same object in memory
        dupLeague = copy.deepcopy(league)
        mockYahooMatchup = Mock()
        mockYahooMatchup.week = week
        mockYahooMatchup.status = status
        mockYahooMatchup.winner_team_key = winnerTeamKey
        mockYahooMatchup.is_tied = isTied
        mockYahooMatchup.is_playoffs = isPlayoffs
        mockYahooMatchup.is_consolation = isConsolation
        mockYahooMatchup.league = dupLeague
        return mockYahooMatchup

    def __setMockYahooTeamPoints(
        self, mockYahooTeam: Mock, teamPointsTotal: int | float
    ) -> Mock:
        # duplicate mockYahooTeam to avoid using the same object in memory
        dupMockYahooTeam = copy.deepcopy(mockYahooTeam)
        dupMockYahooTeam.team_points.total = teamPointsTotal
        return dupMockYahooTeam

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
        self.assertEqual(
            "League ID 'a' could not be turned into an int.", str(context.exception)
        )

    @mock.patch("multiprocessing.Process")
    def test_loadLeague_intendedFailure(self, mockMultiprocessingProcess):
        mockLoginProcess = mockMultiprocessingProcess.return_value
        mockLoginProcess.is_alive.return_value = True  # Simulate login process failure
        with self.assertRaises(TimeoutError) as context:
            yahooLeagueLoader = YahooLeagueLoader(
                "123", [2022], clientId="cid", clientSecret="cs"
            )
            yahooLeagueLoader.loadLeague()
        self.assertEqual("Login to yahoofantasy timed out.", str(context.exception))

    @mock.patch("multiprocessing.Process")
    @mock.patch("yahoofantasy.Context.__init__")
    @mock.patch("yahoofantasy.Context.get_leagues")
    def test_loadLeague_happyPath(
        self,
        mockYahooContextGetLeagues,
        mockYahooContextInit,
        mockMultiprocessingProcess,
    ):
        # mock real league 2022
        mockLeague2022 = Mock()
        mockLeague2022.name = "Test League 2022"
        mockLeague2022.league_id = "123"
        mockLeague2022.season = 2022
        mockLeague2022.current_week = 3
        mockLeague2022.end_week = 3

        # mock fake leagues 2022
        mockLeague2022_fake1 = Mock()
        mockLeague2022_fake1.league_id = "456"

        mockLeague2022_fake2 = Mock()
        mockLeague2022_fake2.league_id = "999"

        # mock league 2023
        mockLeague2023 = Mock()
        mockLeague2023.name = "Test League 2023"
        mockLeague2023.league_id = "456"
        mockLeague2023.season = 2023
        mockLeague2023.current_week = 3
        mockLeague2023.end_week = 3
        mockLeague2023.past_league_id = ["", "123"]

        # mock fake leagues 2023
        mockLeague2023_fake1 = Mock()
        mockLeague2023_fake1.league_id = "123"

        mockLeague2023_fake2 = Mock()
        mockLeague2023_fake2.league_id = "999"

        # mock teams 2022
        mockYahooTeam1_2022 = self.__getMockYahooTeam(
            teamId=1, teamKey=1, name="Team 1", managerNickname="Owner 1", managerId=1
        )
        mockYahooTeam2_2022 = self.__getMockYahooTeam(
            teamId=2, teamKey=2, name="Team 2", managerNickname="Owner 2", managerId=2
        )
        mockYahooTeam3_2022 = self.__getMockYahooTeam(
            teamId=3, teamKey=3, name="Team 3", managerNickname="Owner 3", managerId=3
        )
        mockYahooTeam4_2022 = self.__getMockYahooTeam(
            teamId=4, teamKey=4, name="Team 4", managerNickname="Owner 4", managerId=4
        )
        mockYahooTeam5_2022 = self.__getMockYahooTeam(
            teamId=5, teamKey=5, name="Team 5", managerNickname="Owner 5", managerId=5
        )
        mockYahooTeam6_2022 = self.__getMockYahooTeam(
            teamId=6, teamKey=6, name="Team 6", managerNickname="Owner 6", managerId=6
        )
        mockYahooTeam7_2022 = self.__getMockYahooTeam(
            teamId=7, teamKey=7, name="Team 7", managerNickname="Owner 7", managerId=7
        )
        mockYahooTeam8_2022 = self.__getMockYahooTeam(
            teamId=8, teamKey=8, name="Team 8", managerNickname="Owner 8", managerId=8
        )
        mockLeague2022.teams = self.__getMockTeamsMethod(
            [
                mockYahooTeam1_2022,
                mockYahooTeam2_2022,
                mockYahooTeam3_2022,
                mockYahooTeam4_2022,
                mockYahooTeam5_2022,
                mockYahooTeam6_2022,
                mockYahooTeam7_2022,
                mockYahooTeam8_2022,
            ]
        )

        # mock teams 2023
        mockYahooTeam1_2023 = self.__getMockYahooTeam(
            teamId=1, teamKey=1, name="Team 1", managerNickname="Owner 1", managerId=1
        )
        mockYahooTeam2_2023 = self.__getMockYahooTeam(
            teamId=2, teamKey=2, name="Team 2", managerNickname="Owner 2", managerId=2
        )
        mockYahooTeam3_2023 = self.__getMockYahooTeam(
            teamId=3, teamKey=3, name="Team 3", managerNickname="Owner 3", managerId=3
        )
        mockYahooTeam4_2023 = self.__getMockYahooTeam(
            teamId=4, teamKey=4, name="Team 4", managerNickname="Owner 4", managerId=4
        )
        mockYahooTeam5_2023 = self.__getMockYahooTeam(
            teamId=5, teamKey=5, name="Team 5", managerNickname="Owner 5", managerId=5
        )
        mockYahooTeam6_2023 = self.__getMockYahooTeam(
            teamId=6, teamKey=6, name="Team 6", managerNickname="Owner 6", managerId=6
        )
        mockYahooTeam7_2023 = self.__getMockYahooTeam(
            teamId=7, teamKey=7, name="Team 7", managerNickname="Owner 7", managerId=7
        )
        mockYahooTeam8_2023 = self.__getMockYahooTeam(
            teamId=8, teamKey=8, name="Team 8", managerNickname="Owner 8", managerId=8
        )
        mockLeague2023.teams = self.__getMockTeamsMethod(
            [
                mockYahooTeam1_2023,
                mockYahooTeam2_2023,
                mockYahooTeam3_2023,
                mockYahooTeam4_2023,
                mockYahooTeam5_2023,
                mockYahooTeam6_2023,
                mockYahooTeam7_2023,
                mockYahooTeam8_2023,
            ]
        )

        # mock matchups 2022
        # week -> matchup number -> year
        mockYahooMatchup1_1_2022 = self.__getMockYahooMatchup(
            week=1,
            status="postevent",
            winnerTeamKey=1,
            isPlayoffs=0,
            isTied=0,
            isConsolation=0,
            league=mockLeague2022,
        )
        mockYahooMatchup1_1_2022.teams.team = [
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam1_2022, teamPointsTotal=100
            ),
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam2_2022, teamPointsTotal=100
            ),
        ]
        mockYahooMatchup1_2_2022 = self.__getMockYahooMatchup(
            week=1,
            status="postevent",
            winnerTeamKey=3,
            isPlayoffs=0,
            isTied=0,
            isConsolation=0,
            league=mockLeague2022,
        )
        mockYahooMatchup1_2_2022.teams.team = [
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam3_2022, teamPointsTotal=100.1
            ),
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam4_2022, teamPointsTotal=90.1
            ),
        ]
        mockYahooMatchup1_3_2022 = self.__getMockYahooMatchup(
            week=1,
            status="postevent",
            winnerTeamKey=5,
            isPlayoffs=0,
            isTied=0,
            isConsolation=0,
            league=mockLeague2022,
        )
        mockYahooMatchup1_3_2022.teams.team = [
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam5_2022, teamPointsTotal=100
            ),
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam6_2022, teamPointsTotal=90
            ),
        ]
        mockYahooMatchup1_4_2022 = self.__getMockYahooMatchup(
            week=1,
            status="postevent",
            winnerTeamKey=7,
            isPlayoffs=0,
            isTied=0,
            isConsolation=0,
            league=mockLeague2022,
        )
        mockYahooMatchup1_4_2022.teams.team = [
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam7_2022, teamPointsTotal=100
            ),
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam8_2022, teamPointsTotal=90
            ),
        ]
        # playoffs
        mockYahooMatchup2_1_2022 = self.__getMockYahooMatchup(
            week=2,
            status="postevent",
            winnerTeamKey=2,
            isPlayoffs=1,
            isTied=0,
            isConsolation=0,
            league=mockLeague2022,
        )
        mockYahooMatchup2_1_2022.teams.team = [
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam2_2022, teamPointsTotal=101
            ),
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam3_2022, teamPointsTotal=91
            ),
        ]
        # championship
        mockYahooMatchup3_1_2022 = self.__getMockYahooMatchup(
            week=3,
            status="postevent",
            winnerTeamKey=1,
            isPlayoffs=1,
            isTied=0,
            isConsolation=0,
            league=mockLeague2022,
        )
        mockYahooMatchup3_1_2022.teams.team = [
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam1_2022, teamPointsTotal=102
            ),
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam2_2022, teamPointsTotal=92
            ),
        ]

        # mock matchups 2023
        # week -> matchup number -> year
        mockYahooMatchup1_1_2023 = self.__getMockYahooMatchup(
            week=1,
            status="postevent",
            winnerTeamKey=1,
            isPlayoffs=0,
            isTied=0,
            isConsolation=0,
            league=mockLeague2023,
        )
        mockYahooMatchup1_1_2023.teams.team = [
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam1_2023, teamPointsTotal=100
            ),
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam2_2023, teamPointsTotal=100
            ),
        ]
        mockYahooMatchup1_2_2023 = self.__getMockYahooMatchup(
            week=1,
            status="postevent",
            winnerTeamKey=3,
            isPlayoffs=0,
            isTied=0,
            isConsolation=0,
            league=mockLeague2023,
        )
        mockYahooMatchup1_2_2023.teams.team = [
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam3_2023, teamPointsTotal=100.1
            ),
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam4_2023, teamPointsTotal=90.1
            ),
        ]
        mockYahooMatchup1_3_2023 = self.__getMockYahooMatchup(
            week=1,
            status="postevent",
            winnerTeamKey=5,
            isPlayoffs=0,
            isTied=0,
            isConsolation=0,
            league=mockLeague2023,
        )
        mockYahooMatchup1_3_2023.teams.team = [
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam5_2023, teamPointsTotal=100
            ),
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam6_2023, teamPointsTotal=90
            ),
        ]
        mockYahooMatchup1_4_2023 = self.__getMockYahooMatchup(
            week=1,
            status="postevent",
            winnerTeamKey=7,
            isPlayoffs=0,
            isTied=0,
            isConsolation=0,
            league=mockLeague2023,
        )
        mockYahooMatchup1_4_2023.teams.team = [
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam7_2023, teamPointsTotal=100
            ),
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam8_2023, teamPointsTotal=90
            ),
        ]
        # playoffs
        mockYahooMatchup2_1_2023 = self.__getMockYahooMatchup(
            week=2,
            status="postevent",
            winnerTeamKey=2,
            isPlayoffs=1,
            isTied=0,
            isConsolation=0,
            league=mockLeague2023,
        )
        mockYahooMatchup2_1_2023.teams.team = [
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam2_2023, teamPointsTotal=101
            ),
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam3_2023, teamPointsTotal=91
            ),
        ]
        # championship
        mockYahooMatchup3_1_2023 = self.__getMockYahooMatchup(
            week=3,
            status="postevent",
            winnerTeamKey=1,
            isPlayoffs=1,
            isTied=0,
            isConsolation=0,
            league=mockLeague2023,
        )
        mockYahooMatchup3_1_2023.teams.team = [
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam1_2023, teamPointsTotal=102
            ),
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam2_2023, teamPointsTotal=92
            ),
        ]

        # mock weeks 2022
        mockWeek1_2022 = Mock()
        mockWeek1_2022.matchups = [
            mockYahooMatchup1_1_2022,
            mockYahooMatchup1_2_2022,
            mockYahooMatchup1_3_2022,
            mockYahooMatchup1_4_2022,
        ]

        mockWeek2_2022 = Mock()
        mockWeek2_2022.matchups = [mockYahooMatchup2_1_2022]

        mockWeek3_2022 = Mock()
        mockWeek3_2022.matchups = [mockYahooMatchup3_1_2022]

        mockLeague2022.weeks = self.__getMockWeeksMethod(
            [mockWeek1_2022, mockWeek2_2022, mockWeek3_2022]
        )

        # mock weeks 2023
        mockWeek1_2023 = Mock()
        mockWeek1_2023.matchups = [
            mockYahooMatchup1_1_2023,
            mockYahooMatchup1_2_2023,
            mockYahooMatchup1_3_2023,
            mockYahooMatchup1_4_2023,
        ]

        mockWeek2_2023 = Mock()
        mockWeek2_2023.matchups = [mockYahooMatchup2_1_2023]

        mockWeek3_2023 = Mock()
        mockWeek3_2023.matchups = [mockYahooMatchup3_1_2023]

        mockLeague2023.weeks = self.__getMockWeeksMethod(
            [mockWeek1_2023, mockWeek2_2023, mockWeek3_2023]
        )

        mockYahooContextInit.side_effect = [None]
        mockYahooContextGetLeagues.side_effect = [
            [mockLeague2023_fake1, mockLeague2023, mockLeague2023_fake2],
            [mockLeague2022_fake1, mockLeague2022, mockLeague2022_fake2],
        ]
        mockLoginProcess = mockMultiprocessingProcess.return_value
        mockLoginProcess.is_alive.return_value = (
            False  # Simulate login process completion
        )

        # load league
        yahooLeagueLoader = YahooLeagueLoader(
            "456", [2022, 2023], clientId="cid", clientSecret="cs"
        )
        league = yahooLeagueLoader.loadLeague()

        # expected league
        team1_2022 = Team(ownerId=1, name="Team 1")
        team2_2022 = Team(ownerId=2, name="Team 2")
        team3_2022 = Team(ownerId=3, name="Team 3")
        team4_2022 = Team(ownerId=4, name="Team 4")
        team5_2022 = Team(ownerId=5, name="Team 5")
        team6_2022 = Team(ownerId=6, name="Team 6")
        team7_2022 = Team(ownerId=7, name="Team 7")
        team8_2022 = Team(ownerId=8, name="Team 8")

        team1_2023 = Team(ownerId=1, name="Team 1")
        team2_2023 = Team(ownerId=2, name="Team 2")
        team3_2023 = Team(ownerId=3, name="Team 3")
        team4_2023 = Team(ownerId=4, name="Team 4")
        team5_2023 = Team(ownerId=5, name="Team 5")
        team6_2023 = Team(ownerId=6, name="Team 6")
        team7_2023 = Team(ownerId=7, name="Team 7")
        team8_2023 = Team(ownerId=8, name="Team 8")

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
                                    teamAScore=100.1,
                                    teamBScore=90.1,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team5_2022.id,
                                    teamBId=team6_2022.id,
                                    teamAScore=100,
                                    teamBScore=90,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team7_2022.id,
                                    teamBId=team8_2022.id,
                                    teamAScore=100,
                                    teamBScore=90,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                ),
                            ],
                        ),
                        Week(
                            weekNumber=2,
                            matchups=[
                                Matchup(
                                    teamAId=team2_2022.id,
                                    teamBId=team3_2022.id,
                                    teamAScore=101,
                                    teamBScore=91,
                                    matchupType=MatchupType.PLAYOFF,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                )
                            ],
                        ),
                        Week(
                            weekNumber=3,
                            matchups=[
                                Matchup(
                                    teamAId=team1_2022.id,
                                    teamBId=team2_2022.id,
                                    teamAScore=102,
                                    teamBScore=92,
                                    matchupType=MatchupType.CHAMPIONSHIP,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                )
                            ],
                        ),
                    ],
                    yearSettings=None,
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
                                    teamAScore=100.1,
                                    teamBScore=90.1,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team5_2023.id,
                                    teamBId=team6_2023.id,
                                    teamAScore=100,
                                    teamBScore=90,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team7_2023.id,
                                    teamBId=team8_2023.id,
                                    teamAScore=100,
                                    teamBScore=90,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                ),
                            ],
                        ),
                        Week(
                            weekNumber=2,
                            matchups=[
                                Matchup(
                                    teamAId=team2_2023.id,
                                    teamBId=team3_2023.id,
                                    teamAScore=101,
                                    teamBScore=91,
                                    matchupType=MatchupType.PLAYOFF,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                )
                            ],
                        ),
                        Week(
                            weekNumber=3,
                            matchups=[
                                Matchup(
                                    teamAId=team1_2023.id,
                                    teamBId=team2_2023.id,
                                    teamAScore=102,
                                    teamBScore=92,
                                    matchupType=MatchupType.CHAMPIONSHIP,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                )
                            ],
                        ),
                    ],
                    yearSettings=None,
                ),
            ],
        )

        # make sure we called login correctly
        mockMultiprocessingProcess.assert_called_once_with(
            target=yahooLeagueLoader.login, args=("cid", "cs")
        )

        self.assertTrue(
            league.equals(expectedLeague, ignoreBaseIds=True, ignoreIds=True)
        )
        # check multiWeekMatchupIds
        for year in league.years:
            for week in year.weeks:
                for matchup in week.matchups:
                    self.assertIsNone(matchup.multiWeekMatchupId)

    @mock.patch("multiprocessing.Process")
    @mock.patch("yahoofantasy.Context.__init__")
    @mock.patch("yahoofantasy.Context.get_leagues")
    def test_loadLeague_withOwnerNamesAndAliases(
        self,
        mockYahooContextGetLeagues,
        mockYahooContextInit,
        mockMultiprocessingProcess,
    ):
        # mock real league 2022
        mockLeague2022 = Mock()
        mockLeague2022.name = "Test League 2022"
        mockLeague2022.league_id = "123"
        mockLeague2022.season = 2022
        mockLeague2022.current_week = 3
        mockLeague2022.end_week = 3

        # mock fake leagues 2022
        mockLeague2022_fake1 = Mock()
        mockLeague2022_fake1.league_id = "456"

        mockLeague2022_fake2 = Mock()
        mockLeague2022_fake2.league_id = "999"

        # mock league 2023
        mockLeague2023 = Mock()
        mockLeague2023.name = "Test League 2023"
        mockLeague2023.league_id = "456"
        mockLeague2023.season = 2023
        mockLeague2023.current_week = 3
        mockLeague2023.end_week = 3
        mockLeague2023.past_league_id = ["", "123"]

        # mock fake leagues 2023
        mockLeague2023_fake1 = Mock()
        mockLeague2023_fake1.league_id = "123"

        mockLeague2023_fake2 = Mock()
        mockLeague2023_fake2.league_id = "999"

        # mock teams 2022
        mockYahooTeam1_2022 = self.__getMockYahooTeam(
            teamId=1, teamKey=1, name="Team 1", managerNickname="Owner 1", managerId=1
        )
        mockYahooTeam2_2022 = self.__getMockYahooTeam(
            teamId=2, teamKey=2, name="Team 2", managerNickname="Owner 2", managerId=2
        )
        mockYahooTeam3_2022 = self.__getMockYahooTeam(
            teamId=3, teamKey=3, name="Team 3", managerNickname="Owner 3", managerId=3
        )
        mockYahooTeam4_2022 = self.__getMockYahooTeam(
            teamId=4, teamKey=4, name="Team 4", managerNickname="Owner 4", managerId=4
        )
        mockYahooTeam5_2022 = self.__getMockYahooTeam(
            teamId=5, teamKey=5, name="Team 5", managerNickname="Owner 5", managerId=5
        )
        mockYahooTeam6_2022 = self.__getMockYahooTeam(
            teamId=6, teamKey=6, name="Team 6", managerNickname="Owner 6", managerId=6
        )
        mockYahooTeam7_2022 = self.__getMockYahooTeam(
            teamId=7, teamKey=7, name="Team 7", managerNickname="Owner 7", managerId=7
        )
        mockYahooTeam8_2022 = self.__getMockYahooTeam(
            teamId=8, teamKey=8, name="Team 8", managerNickname="Owner 8", managerId=8
        )
        mockLeague2022.teams = self.__getMockTeamsMethod(
            [
                mockYahooTeam1_2022,
                mockYahooTeam2_2022,
                mockYahooTeam3_2022,
                mockYahooTeam4_2022,
                mockYahooTeam5_2022,
                mockYahooTeam6_2022,
                mockYahooTeam7_2022,
                mockYahooTeam8_2022,
            ]
        )

        # mock teams 2023
        mockYahooTeam1_2023 = self.__getMockYahooTeam(
            teamId=1, teamKey=1, name="Team 1", managerNickname="Owner 1", managerId=1
        )
        mockYahooTeam2_2023 = self.__getMockYahooTeam(
            teamId=2, teamKey=2, name="Team 2", managerNickname="Owner 2", managerId=2
        )
        mockYahooTeam3_2023 = self.__getMockYahooTeam(
            teamId=3, teamKey=3, name="Team 3", managerNickname="Owner 3", managerId=3
        )
        mockYahooTeam4_2023 = self.__getMockYahooTeam(
            teamId=4, teamKey=4, name="Team 4", managerNickname="Owner 4", managerId=4
        )
        mockYahooTeam5_2023 = self.__getMockYahooTeam(
            teamId=5, teamKey=5, name="Team 5", managerNickname="Owner 5", managerId=5
        )
        mockYahooTeam6_2023 = self.__getMockYahooTeam(
            teamId=6, teamKey=6, name="Team 6", managerNickname="Owner 6", managerId=6
        )
        mockYahooTeam7_2023 = self.__getMockYahooTeam(
            teamId=7, teamKey=7, name="Team 7", managerNickname="Owner 7", managerId=7
        )
        mockYahooTeam8_2023 = self.__getMockYahooTeam(
            teamId=8, teamKey=8, name="Team 8", managerNickname="Owner 8", managerId=8
        )
        mockLeague2023.teams = self.__getMockTeamsMethod(
            [
                mockYahooTeam1_2023,
                mockYahooTeam2_2023,
                mockYahooTeam3_2023,
                mockYahooTeam4_2023,
                mockYahooTeam5_2023,
                mockYahooTeam6_2023,
                mockYahooTeam7_2023,
                mockYahooTeam8_2023,
            ]
        )

        # mock matchups 2022
        # week -> matchup number -> year
        mockYahooMatchup1_1_2022 = self.__getMockYahooMatchup(
            week=1,
            status="postevent",
            winnerTeamKey=1,
            isPlayoffs=0,
            isTied=0,
            isConsolation=0,
            league=mockLeague2022,
        )
        mockYahooMatchup1_1_2022.teams.team = [
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam1_2022, teamPointsTotal=100
            ),
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam2_2022, teamPointsTotal=100
            ),
        ]
        mockYahooMatchup1_2_2022 = self.__getMockYahooMatchup(
            week=1,
            status="postevent",
            winnerTeamKey=3,
            isPlayoffs=0,
            isTied=0,
            isConsolation=0,
            league=mockLeague2022,
        )
        mockYahooMatchup1_2_2022.teams.team = [
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam3_2022, teamPointsTotal=100.1
            ),
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam4_2022, teamPointsTotal=90.1
            ),
        ]
        mockYahooMatchup1_3_2022 = self.__getMockYahooMatchup(
            week=1,
            status="postevent",
            winnerTeamKey=5,
            isPlayoffs=0,
            isTied=0,
            isConsolation=0,
            league=mockLeague2022,
        )
        mockYahooMatchup1_3_2022.teams.team = [
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam5_2022, teamPointsTotal=100
            ),
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam6_2022, teamPointsTotal=90
            ),
        ]
        mockYahooMatchup1_4_2022 = self.__getMockYahooMatchup(
            week=1,
            status="postevent",
            winnerTeamKey=7,
            isPlayoffs=0,
            isTied=0,
            isConsolation=0,
            league=mockLeague2022,
        )
        mockYahooMatchup1_4_2022.teams.team = [
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam7_2022, teamPointsTotal=100
            ),
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam8_2022, teamPointsTotal=90
            ),
        ]
        # playoffs
        mockYahooMatchup2_1_2022 = self.__getMockYahooMatchup(
            week=2,
            status="postevent",
            winnerTeamKey=2,
            isPlayoffs=1,
            isTied=0,
            isConsolation=0,
            league=mockLeague2022,
        )
        mockYahooMatchup2_1_2022.teams.team = [
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam2_2022, teamPointsTotal=101
            ),
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam3_2022, teamPointsTotal=91
            ),
        ]
        # championship
        mockYahooMatchup3_1_2022 = self.__getMockYahooMatchup(
            week=3,
            status="postevent",
            winnerTeamKey=1,
            isPlayoffs=1,
            isTied=0,
            isConsolation=0,
            league=mockLeague2022,
        )
        mockYahooMatchup3_1_2022.teams.team = [
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam1_2022, teamPointsTotal=102
            ),
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam2_2022, teamPointsTotal=92
            ),
        ]

        # mock matchups 2023
        # week -> matchup number -> year
        mockYahooMatchup1_1_2023 = self.__getMockYahooMatchup(
            week=1,
            status="postevent",
            winnerTeamKey=1,
            isPlayoffs=0,
            isTied=0,
            isConsolation=0,
            league=mockLeague2023,
        )
        mockYahooMatchup1_1_2023.teams.team = [
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam1_2023, teamPointsTotal=100
            ),
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam2_2023, teamPointsTotal=100
            ),
        ]
        mockYahooMatchup1_2_2023 = self.__getMockYahooMatchup(
            week=1,
            status="postevent",
            winnerTeamKey=3,
            isPlayoffs=0,
            isTied=0,
            isConsolation=0,
            league=mockLeague2023,
        )
        mockYahooMatchup1_2_2023.teams.team = [
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam3_2023, teamPointsTotal=100.1
            ),
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam4_2023, teamPointsTotal=90.1
            ),
        ]
        mockYahooMatchup1_3_2023 = self.__getMockYahooMatchup(
            week=1,
            status="postevent",
            winnerTeamKey=5,
            isPlayoffs=0,
            isTied=0,
            isConsolation=0,
            league=mockLeague2023,
        )
        mockYahooMatchup1_3_2023.teams.team = [
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam5_2023, teamPointsTotal=100
            ),
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam6_2023, teamPointsTotal=90
            ),
        ]
        mockYahooMatchup1_4_2023 = self.__getMockYahooMatchup(
            week=1,
            status="postevent",
            winnerTeamKey=7,
            isPlayoffs=0,
            isTied=0,
            isConsolation=0,
            league=mockLeague2023,
        )
        mockYahooMatchup1_4_2023.teams.team = [
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam7_2023, teamPointsTotal=100
            ),
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam8_2023, teamPointsTotal=90
            ),
        ]
        # playoffs
        mockYahooMatchup2_1_2023 = self.__getMockYahooMatchup(
            week=2,
            status="postevent",
            winnerTeamKey=2,
            isPlayoffs=1,
            isTied=0,
            isConsolation=0,
            league=mockLeague2023,
        )
        mockYahooMatchup2_1_2023.teams.team = [
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam2_2023, teamPointsTotal=101
            ),
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam3_2023, teamPointsTotal=91
            ),
        ]
        # championship
        mockYahooMatchup3_1_2023 = self.__getMockYahooMatchup(
            week=3,
            status="postevent",
            winnerTeamKey=1,
            isPlayoffs=1,
            isTied=0,
            isConsolation=0,
            league=mockLeague2023,
        )
        mockYahooMatchup3_1_2023.teams.team = [
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam1_2023, teamPointsTotal=102
            ),
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam2_2023, teamPointsTotal=92
            ),
        ]

        # mock weeks 2022
        mockWeek1_2022 = Mock()
        mockWeek1_2022.matchups = [
            mockYahooMatchup1_1_2022,
            mockYahooMatchup1_2_2022,
            mockYahooMatchup1_3_2022,
            mockYahooMatchup1_4_2022,
        ]

        mockWeek2_2022 = Mock()
        mockWeek2_2022.matchups = [mockYahooMatchup2_1_2022]

        mockWeek3_2022 = Mock()
        mockWeek3_2022.matchups = [mockYahooMatchup3_1_2022]

        mockLeague2022.weeks = self.__getMockWeeksMethod(
            [mockWeek1_2022, mockWeek2_2022, mockWeek3_2022]
        )

        # mock weeks 2023
        mockWeek1_2023 = Mock()
        mockWeek1_2023.matchups = [
            mockYahooMatchup1_1_2023,
            mockYahooMatchup1_2_2023,
            mockYahooMatchup1_3_2023,
            mockYahooMatchup1_4_2023,
        ]

        mockWeek2_2023 = Mock()
        mockWeek2_2023.matchups = [mockYahooMatchup2_1_2023]

        mockWeek3_2023 = Mock()
        mockWeek3_2023.matchups = [mockYahooMatchup3_1_2023]

        mockLeague2023.weeks = self.__getMockWeeksMethod(
            [mockWeek1_2023, mockWeek2_2023, mockWeek3_2023]
        )

        mockYahooContextInit.side_effect = [None]
        mockYahooContextGetLeagues.side_effect = [
            [mockLeague2023_fake1, mockLeague2023, mockLeague2023_fake2],
            [mockLeague2022_fake1, mockLeague2022, mockLeague2022_fake2],
        ]
        mockLoginProcess = mockMultiprocessingProcess.return_value
        mockLoginProcess.is_alive.return_value = (
            False  # Simulate login process completion
        )

        # load league
        yahooLeagueLoader = YahooLeagueLoader(
            "456",
            [2022, 2023],
            clientId="cid",
            clientSecret="cs",
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
        league = yahooLeagueLoader.loadLeague()

        # expected league
        team1_2022 = Team(ownerId=1, name="Team 1")
        team2_2022 = Team(ownerId=2, name="Team 2")
        team3_2022 = Team(ownerId=3, name="Team 3")
        team4_2022 = Team(ownerId=4, name="Team 4")
        team5_2022 = Team(ownerId=5, name="Team 5")
        team6_2022 = Team(ownerId=6, name="Team 6")
        team7_2022 = Team(ownerId=7, name="Team 7")
        team8_2022 = Team(ownerId=8, name="Team 8")

        team1_2023 = Team(ownerId=1, name="Team 1")
        team2_2023 = Team(ownerId=2, name="Team 2")
        team3_2023 = Team(ownerId=3, name="Team 3")
        team4_2023 = Team(ownerId=4, name="Team 4")
        team5_2023 = Team(ownerId=5, name="Team 5")
        team6_2023 = Team(ownerId=6, name="Team 6")
        team7_2023 = Team(ownerId=7, name="Team 7")
        team8_2023 = Team(ownerId=8, name="Team 8")

        expectedLeague = League(
            name="Test League 2023",
            owners=[
                Owner(name="o1"),
                Owner(name="o2"),
                Owner(name="o3"),
                Owner(name="o4"),
                Owner(name="o5"),
                Owner(name="o6"),
                Owner(name="o7"),
                Owner(name="o8"),
            ],
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
                                    teamAScore=100.1,
                                    teamBScore=90.1,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team5_2022.id,
                                    teamBId=team6_2022.id,
                                    teamAScore=100,
                                    teamBScore=90,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team7_2022.id,
                                    teamBId=team8_2022.id,
                                    teamAScore=100,
                                    teamBScore=90,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                ),
                            ],
                        ),
                        Week(
                            weekNumber=2,
                            matchups=[
                                Matchup(
                                    teamAId=team2_2022.id,
                                    teamBId=team3_2022.id,
                                    teamAScore=101,
                                    teamBScore=91,
                                    matchupType=MatchupType.PLAYOFF,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                )
                            ],
                        ),
                        Week(
                            weekNumber=3,
                            matchups=[
                                Matchup(
                                    teamAId=team1_2022.id,
                                    teamBId=team2_2022.id,
                                    teamAScore=102,
                                    teamBScore=92,
                                    matchupType=MatchupType.CHAMPIONSHIP,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                )
                            ],
                        ),
                    ],
                    yearSettings=None,
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
                                    teamAScore=100.1,
                                    teamBScore=90.1,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team5_2023.id,
                                    teamBId=team6_2023.id,
                                    teamAScore=100,
                                    teamBScore=90,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team7_2023.id,
                                    teamBId=team8_2023.id,
                                    teamAScore=100,
                                    teamBScore=90,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                ),
                            ],
                        ),
                        Week(
                            weekNumber=2,
                            matchups=[
                                Matchup(
                                    teamAId=team2_2023.id,
                                    teamBId=team3_2023.id,
                                    teamAScore=101,
                                    teamBScore=91,
                                    matchupType=MatchupType.PLAYOFF,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                )
                            ],
                        ),
                        Week(
                            weekNumber=3,
                            matchups=[
                                Matchup(
                                    teamAId=team1_2023.id,
                                    teamBId=team2_2023.id,
                                    teamAScore=102,
                                    teamBScore=92,
                                    matchupType=MatchupType.CHAMPIONSHIP,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                )
                            ],
                        ),
                    ],
                    yearSettings=None,
                ),
            ],
        )

        # make sure we called login correctly
        mockMultiprocessingProcess.assert_called_once_with(
            target=yahooLeagueLoader.login, args=("cid", "cs")
        )

        self.assertTrue(
            league.equals(expectedLeague, ignoreBaseIds=True, ignoreIds=True)
        )
        # check multiWeekMatchupIds
        for year in league.years:
            for week in year.weeks:
                for matchup in week.matchups:
                    self.assertIsNone(matchup.multiWeekMatchupId)

    @mock.patch("multiprocessing.Process")
    @mock.patch("yahoofantasy.Context.__init__")
    @mock.patch("yahoofantasy.Context.get_leagues")
    def test_loadLeague_happyPath(
        self,
        mockYahooContextGetLeagues,
        mockYahooContextInit,
        mockMultiprocessingProcess,
    ):
        # mock real league 2022
        mockLeague2022 = Mock()
        mockLeague2022.name = "Test League 2022"
        mockLeague2022.league_id = "123"
        mockLeague2022.season = 2022
        mockLeague2022.current_week = 3
        mockLeague2022.end_week = 3

        # mock fake leagues 2022
        mockLeague2022_fake1 = Mock()
        mockLeague2022_fake1.league_id = "456"

        mockLeague2022_fake2 = Mock()
        mockLeague2022_fake2.league_id = "999"

        # mock league 2023
        mockLeague2023 = Mock()
        mockLeague2023.name = "Test League 2023"
        mockLeague2023.league_id = "456"
        mockLeague2023.season = 2023
        mockLeague2023.current_week = 3
        mockLeague2023.end_week = 3
        mockLeague2023.past_league_id = ["", "123"]

        # mock fake leagues 2023
        mockLeague2023_fake1 = Mock()
        mockLeague2023_fake1.league_id = "123"

        mockLeague2023_fake2 = Mock()
        mockLeague2023_fake2.league_id = "999"

        # mock teams 2022
        mockYahooTeam1_2022 = self.__getMockYahooTeam(
            teamId=1, teamKey=1, name="Team 1", managerNickname="Owner 1", managerId=1
        )
        mockYahooTeam2_2022 = self.__getMockYahooTeam(
            teamId=2, teamKey=2, name="Team 2", managerNickname="Owner 2", managerId=2
        )
        mockYahooTeam3_2022 = self.__getMockYahooTeam(
            teamId=3, teamKey=3, name="Team 3", managerNickname="Owner 3", managerId=3
        )
        mockYahooTeam4_2022 = self.__getMockYahooTeam(
            teamId=4, teamKey=4, name="Team 4", managerNickname="Owner 4", managerId=4
        )
        mockYahooTeam5_2022 = self.__getMockYahooTeam(
            teamId=5, teamKey=5, name="Team 5", managerNickname="Owner 5", managerId=5
        )
        mockYahooTeam6_2022 = self.__getMockYahooTeam(
            teamId=6, teamKey=6, name="Team 6", managerNickname="Owner 6", managerId=6
        )
        mockYahooTeam7_2022 = self.__getMockYahooTeam(
            teamId=7, teamKey=7, name="Team 7", managerNickname="Owner 7", managerId=7
        )
        mockYahooTeam8_2022 = self.__getMockYahooTeam(
            teamId=8, teamKey=8, name="Team 8", managerNickname="Owner 8", managerId=8
        )
        mockLeague2022.teams = self.__getMockTeamsMethod(
            [
                mockYahooTeam1_2022,
                mockYahooTeam2_2022,
                mockYahooTeam3_2022,
                mockYahooTeam4_2022,
                mockYahooTeam5_2022,
                mockYahooTeam6_2022,
                mockYahooTeam7_2022,
                mockYahooTeam8_2022,
            ]
        )

        # mock teams 2023
        mockYahooTeam1_2023 = self.__getMockYahooTeam(
            teamId=1, teamKey=1, name="Team 1", managerNickname="Owner 1", managerId=1
        )
        mockYahooTeam2_2023 = self.__getMockYahooTeam(
            teamId=2, teamKey=2, name="Team 2", managerNickname="Owner 2", managerId=2
        )
        mockYahooTeam3_2023 = self.__getMockYahooTeam(
            teamId=3, teamKey=3, name="Team 3", managerNickname="Owner 3", managerId=3
        )
        mockYahooTeam4_2023 = self.__getMockYahooTeam(
            teamId=4, teamKey=4, name="Team 4", managerNickname="Owner 4", managerId=4
        )
        mockYahooTeam5_2023 = self.__getMockYahooTeam(
            teamId=5, teamKey=5, name="Team 5", managerNickname="Owner 5", managerId=5
        )
        mockYahooTeam6_2023 = self.__getMockYahooTeam(
            teamId=6, teamKey=6, name="Team 6", managerNickname="Owner 6", managerId=6
        )
        mockYahooTeam7_2023 = self.__getMockYahooTeam(
            teamId=7, teamKey=7, name="Team 7", managerNickname="Owner 7", managerId=7
        )
        mockYahooTeam8_2023 = self.__getMockYahooTeam(
            teamId=8, teamKey=8, name="Team 8", managerNickname="Owner 8", managerId=8
        )
        mockLeague2023.teams = self.__getMockTeamsMethod(
            [
                mockYahooTeam1_2023,
                mockYahooTeam2_2023,
                mockYahooTeam3_2023,
                mockYahooTeam4_2023,
                mockYahooTeam5_2023,
                mockYahooTeam6_2023,
                mockYahooTeam7_2023,
                mockYahooTeam8_2023,
            ]
        )

        # mock matchups 2022
        # week -> matchup number -> year
        mockYahooMatchup1_1_2022 = self.__getMockYahooMatchup(
            week=1,
            status="postevent",
            winnerTeamKey=1,
            isPlayoffs=0,
            isTied=0,
            isConsolation=0,
            league=mockLeague2022,
        )
        mockYahooMatchup1_1_2022.teams.team = [
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam1_2022, teamPointsTotal=100
            ),
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam2_2022, teamPointsTotal=100
            ),
        ]
        mockYahooMatchup1_2_2022 = self.__getMockYahooMatchup(
            week=1,
            status="postevent",
            winnerTeamKey=3,
            isPlayoffs=0,
            isTied=0,
            isConsolation=0,
            league=mockLeague2022,
        )
        mockYahooMatchup1_2_2022.teams.team = [
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam3_2022, teamPointsTotal=100.1
            ),
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam4_2022, teamPointsTotal=90.1
            ),
        ]
        mockYahooMatchup1_3_2022 = self.__getMockYahooMatchup(
            week=1,
            status="postevent",
            winnerTeamKey=5,
            isPlayoffs=0,
            isTied=0,
            isConsolation=0,
            league=mockLeague2022,
        )
        mockYahooMatchup1_3_2022.teams.team = [
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam5_2022, teamPointsTotal=100
            ),
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam6_2022, teamPointsTotal=90
            ),
        ]
        mockYahooMatchup1_4_2022 = self.__getMockYahooMatchup(
            week=1,
            status="postevent",
            winnerTeamKey=7,
            isPlayoffs=0,
            isTied=0,
            isConsolation=0,
            league=mockLeague2022,
        )
        mockYahooMatchup1_4_2022.teams.team = [
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam7_2022, teamPointsTotal=100
            ),
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam8_2022, teamPointsTotal=90
            ),
        ]
        # playoffs
        mockYahooMatchup2_1_2022 = self.__getMockYahooMatchup(
            week=2,
            status="postevent",
            winnerTeamKey=2,
            isPlayoffs=1,
            isTied=0,
            isConsolation=0,
            league=mockLeague2022,
        )
        mockYahooMatchup2_1_2022.teams.team = [
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam2_2022, teamPointsTotal=101
            ),
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam3_2022, teamPointsTotal=91
            ),
        ]
        # championship
        mockYahooMatchup3_1_2022 = self.__getMockYahooMatchup(
            week=3,
            status="postevent",
            winnerTeamKey=1,
            isPlayoffs=1,
            isTied=0,
            isConsolation=0,
            league=mockLeague2022,
        )
        mockYahooMatchup3_1_2022.teams.team = [
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam1_2022, teamPointsTotal=102
            ),
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam2_2022, teamPointsTotal=92
            ),
        ]

        # mock matchups 2023
        # week -> matchup number -> year
        mockYahooMatchup1_1_2023 = self.__getMockYahooMatchup(
            week=1,
            status="postevent",
            winnerTeamKey=1,
            isPlayoffs=0,
            isTied=0,
            isConsolation=0,
            league=mockLeague2023,
        )
        mockYahooMatchup1_1_2023.teams.team = [
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam1_2023, teamPointsTotal=100
            ),
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam2_2023, teamPointsTotal=100
            ),
        ]
        mockYahooMatchup1_2_2023 = self.__getMockYahooMatchup(
            week=1,
            status="postevent",
            winnerTeamKey=3,
            isPlayoffs=0,
            isTied=0,
            isConsolation=0,
            league=mockLeague2023,
        )
        mockYahooMatchup1_2_2023.teams.team = [
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam3_2023, teamPointsTotal=100.1
            ),
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam4_2023, teamPointsTotal=90.1
            ),
        ]
        mockYahooMatchup1_3_2023 = self.__getMockYahooMatchup(
            week=1,
            status="postevent",
            winnerTeamKey=5,
            isPlayoffs=0,
            isTied=0,
            isConsolation=0,
            league=mockLeague2023,
        )
        mockYahooMatchup1_3_2023.teams.team = [
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam5_2023, teamPointsTotal=100
            ),
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam6_2023, teamPointsTotal=90
            ),
        ]
        mockYahooMatchup1_4_2023 = self.__getMockYahooMatchup(
            week=1,
            status="postevent",
            winnerTeamKey=7,
            isPlayoffs=0,
            isTied=0,
            isConsolation=0,
            league=mockLeague2023,
        )
        mockYahooMatchup1_4_2023.teams.team = [
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam7_2023, teamPointsTotal=100
            ),
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam8_2023, teamPointsTotal=90
            ),
        ]
        # playoffs
        mockYahooMatchup2_1_2023 = self.__getMockYahooMatchup(
            week=2,
            status="postevent",
            winnerTeamKey=2,
            isPlayoffs=1,
            isTied=0,
            isConsolation=0,
            league=mockLeague2023,
        )
        mockYahooMatchup2_1_2023.teams.team = [
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam2_2023, teamPointsTotal=101
            ),
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam3_2023, teamPointsTotal=91
            ),
        ]
        # championship
        mockYahooMatchup3_1_2023 = self.__getMockYahooMatchup(
            week=3,
            status="postevent",
            winnerTeamKey=1,
            isPlayoffs=1,
            isTied=0,
            isConsolation=0,
            league=mockLeague2023,
        )
        mockYahooMatchup3_1_2023.teams.team = [
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam1_2023, teamPointsTotal=102
            ),
            self.__setMockYahooTeamPoints(
                mockYahooTeam=mockYahooTeam2_2023, teamPointsTotal=92
            ),
        ]

        # mock weeks 2022
        mockWeek1_2022 = Mock()
        mockWeek1_2022.matchups = [
            mockYahooMatchup1_1_2022,
            mockYahooMatchup1_2_2022,
            mockYahooMatchup1_3_2022,
            mockYahooMatchup1_4_2022,
        ]

        mockWeek2_2022 = Mock()
        mockWeek2_2022.matchups = [mockYahooMatchup2_1_2022]

        mockWeek3_2022 = Mock()
        mockWeek3_2022.matchups = [mockYahooMatchup3_1_2022]

        mockLeague2022.weeks = self.__getMockWeeksMethod(
            [mockWeek1_2022, mockWeek2_2022, mockWeek3_2022]
        )

        # mock weeks 2023
        mockWeek1_2023 = Mock()
        mockWeek1_2023.matchups = [
            mockYahooMatchup1_1_2023,
            mockYahooMatchup1_2_2023,
            mockYahooMatchup1_3_2023,
            mockYahooMatchup1_4_2023,
        ]

        mockWeek2_2023 = Mock()
        mockWeek2_2023.matchups = [mockYahooMatchup2_1_2023]

        mockWeek3_2023 = Mock()
        mockWeek3_2023.matchups = [mockYahooMatchup3_1_2023]

        mockLeague2023.weeks = self.__getMockWeeksMethod(
            [mockWeek1_2023, mockWeek2_2023, mockWeek3_2023]
        )

        mockYahooContextInit.side_effect = [None]
        mockYahooContextGetLeagues.side_effect = [
            [mockLeague2023_fake1, mockLeague2023, mockLeague2023_fake2],
            [mockLeague2022_fake1, mockLeague2022, mockLeague2022_fake2],
        ]
        mockLoginProcess = mockMultiprocessingProcess.return_value
        mockLoginProcess.is_alive.return_value = (
            False  # Simulate login process completion
        )

        # load league
        yahooLeagueLoader = YahooLeagueLoader(
            "456",
            [2022, 2023],
            clientId="cid",
            clientSecret="cs",
            leagueName="custom name",
        )
        league = yahooLeagueLoader.loadLeague()

        self.assertEqual("custom name", league.name)
