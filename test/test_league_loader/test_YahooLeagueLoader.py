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
    """
    # TODO: add better tests
    # TODO: mock failure tests
    """

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
        self, *, teamId: int, teamKey: int, name: str, managerNickname: str, managerId: int
    ) -> Mock:
        mockTeam = Mock()
        mockTeam.team_id = teamId
        mockTeam.team_key = teamKey
        mockTeam.name = name
        mockTeam.manager.nickname = managerNickname
        mockTeam.manager.manager_id = managerId
        return mockTeam

    def __getMockYahooMatchup(
        self, *, status: str, winnerTeamKey: int, isTied: int, isPlayoffs: int, league: Mock
    ) -> Mock:
        mockYahooMatchup = Mock()
        mockYahooMatchup.status = status
        mockYahooMatchup.winner_team_key = winnerTeamKey
        mockYahooMatchup.is_tied = isTied
        mockYahooMatchup.is_playoffs = isPlayoffs
        mockYahooMatchup.league = league
        return mockYahooMatchup

    def __setMockYahooTeamPoints(self, mockYahooTeam: Mock, teamPointsTotal: int | float) -> Mock:
        mockYahooTeam.team_points.total = teamPointsTotal
        return mockYahooTeam

    # TODO
    # def test_loadLeague_intendedFailure(self):
    #     with self.assertRaises(TimeoutError) as context:
    #         badClientId = badClientSecret = "bad"
    #         badLeagueId = 0
    #         yahooLeagueLoader = YahooLeagueLoader(
    #             badLeagueId,
    #             [2000],
    #             clientId=badClientId,
    #             clientSecret=badClientSecret,
    #             loginTimeoutSeconds=1,
    #         )
    #         yahooLeagueLoader.loadLeague()
    #     self.assertEqual("Login to yahoofantasy timed out.", str(context.exception))

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
        self.assertEqual("League ID 'a' could not be turned into an int.", str(context.exception))

    @mock.patch("subprocess.call")
    @mock.patch("multiprocessing.Process")
    @mock.patch("yahoofantasy.Context.__init__")
    @mock.patch("yahoofantasy.Context.get_leagues")
    def test_get_all_leagues(
        self,
        mockYahooContextGetLeagues,
        mockYahooContextInit,
        mockMultiprocessingProcess,
        mockSubprocessCall,
    ):
        yahooLeagueLoader = YahooLeagueLoader("123", [2022], clientId="cid", clientSecret="cs")
        # TODO: assert that the login() method is called with the correct params
        mockLeague2022 = Mock()
        mockLeague2022.name = "Test League 2022"
        mockLeague2022.league_id = "123"
        mockLeague2022.season = 2022
        mockLeague2022.renew = None
        mockLeague2022.current_week = 1
        mockLeague2022.end_week = 5

        # mock teams
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

        # mock matchups
        mockYahooMatchup1_2022 = self.__getMockYahooMatchup(
            status="postevent", winnerTeamKey=1, isPlayoffs=0, isTied=0, league=mockLeague2022
        )
        mockYahooMatchup1_2022.teams.team = [
            self.__setMockYahooTeamPoints(mockYahooTeam=mockYahooTeam1_2022, teamPointsTotal=100),
            self.__setMockYahooTeamPoints(mockYahooTeam=mockYahooTeam2_2022, teamPointsTotal=100),
        ]
        mockYahooMatchup2_2022 = self.__getMockYahooMatchup(
            status="postevent", winnerTeamKey=3, isPlayoffs=0, isTied=0, league=mockLeague2022
        )
        mockYahooMatchup2_2022.teams.team = [
            self.__setMockYahooTeamPoints(mockYahooTeam=mockYahooTeam3_2022, teamPointsTotal=100),
            self.__setMockYahooTeamPoints(mockYahooTeam=mockYahooTeam4_2022, teamPointsTotal=90),
        ]
        mockYahooMatchup3_2022 = self.__getMockYahooMatchup(
            status="postevent", winnerTeamKey=5, isPlayoffs=0, isTied=0, league=mockLeague2022
        )
        mockYahooMatchup3_2022.teams.team = [
            self.__setMockYahooTeamPoints(mockYahooTeam=mockYahooTeam5_2022, teamPointsTotal=100),
            self.__setMockYahooTeamPoints(mockYahooTeam=mockYahooTeam6_2022, teamPointsTotal=90),
        ]
        mockYahooMatchup4_2022 = self.__getMockYahooMatchup(
            status="postevent", winnerTeamKey=7, isPlayoffs=0, isTied=0, league=mockLeague2022
        )
        mockYahooMatchup4_2022.teams.team = [
            self.__setMockYahooTeamPoints(mockYahooTeam=mockYahooTeam7_2022, teamPointsTotal=100),
            self.__setMockYahooTeamPoints(mockYahooTeam=mockYahooTeam8_2022, teamPointsTotal=90),
        ]

        # mock weeks
        mockWeek1_2022 = Mock()
        mockWeek1_2022.matchups = [
            mockYahooMatchup1_2022,
            mockYahooMatchup2_2022,
            mockYahooMatchup3_2022,
            mockYahooMatchup4_2022,
        ]
        mockLeague2022.weeks = self.__getMockWeeksMethod([mockWeek1_2022])

        mockYahooContextInit.side_effect = [None]
        mockYahooContextGetLeagues.side_effect = [[mockLeague2022]]
        mockLoginProcess = mockMultiprocessingProcess.return_value
        mockLoginProcess.is_alive.return_value = False  # Simulate login process completion

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

        expectedLeague = League(
            name="Test League 2022",
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
                                    multiWeekMatchupId=None,
                                ),
                                Matchup(
                                    teamAId=team3_2022.id,
                                    teamBId=team4_2022.id,
                                    teamAScore=100,
                                    teamBScore=90,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                ),
                                Matchup(
                                    teamAId=team5_2022.id,
                                    teamBId=team6_2022.id,
                                    teamAScore=100,
                                    teamBScore=90,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                ),
                                Matchup(
                                    teamAId=team7_2022.id,
                                    teamBId=team8_2022.id,
                                    teamAScore=100,
                                    teamBScore=90,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                ),
                            ],
                        )
                    ],
                    yearSettings=None,
                )
            ],
        )

        self.assertEqual(league, expectedLeague)
