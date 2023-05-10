import unittest
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


class TestMyFantasyLeagueLeagueLoader(unittest.TestCase):
    """
    # TODO: add better tests
    # TODO: mock intended failure test
    # TODO: test 1 round of playoff vs multiple weeks (dict vs list)
    # TODO: test 1 playoff matchup in playoff week vs multiple matchups (dict vs list)
    """

    def __addScoreToMockFranchise(
        self, *, mockFranchise: dict, score: int | float, result: str
    ) -> dict:
        dupMockFranchise = copy.deepcopy(mockFranchise)
        dupMockFranchise["score"] = score
        dupMockFranchise["result"] = result
        return dupMockFranchise

    # def test_loadLeague_intendedFailure(self):
    #     with self.assertRaises(MFLAPIClientException) as context:
    #         leagueLoader = MyFantasyLeagueLeagueLoader(
    #             "0", [2000], mflUsername="", mflPassword="", mflUserAgentName=""
    #         )
    #         leagueLoader.loadLeague()
    #     self.assertEqual("Invalid Password", str(context.exception))

    @mock.patch("pymfl.api.config.APIConfig.add_config_for_year_and_league_id")
    @mock.patch("pymfl.api.CommonLeagueInfoAPIClient.get_league")
    @mock.patch("pymfl.api.CommonLeagueInfoAPIClient.get_schedule")
    @mock.patch("pymfl.api.CommonLeagueInfoAPIClient.get_playoff_bracket")
    def test_loadLeague_happyPath(
        self, mockGetPlayoffBracket, mockGetSchedule, mockGetLeague, mockAddConfig
    ):
        mockFranchise1_2022 = {"owner_name": "Owner 1", "name": "Team 1", "id": 1}
        mockFranchise2_2022 = {"owner_name": "Owner 2", "name": "Team 2", "id": 2}
        mockFranchise3_2022 = {"owner_name": "Owner 3", "name": "Team 3", "id": 3}
        mockFranchise4_2022 = {"owner_name": "Owner 4", "name": "Team 4", "id": 4}
        mockFranchise5_2022 = {"owner_name": "Owner 5", "name": "Team 5", "id": 5}
        mockFranchise6_2022 = {"owner_name": "Owner 6", "name": "Team 6", "id": 6}
        mockFranchise7_2022 = {"owner_name": "Owner 7", "name": "Team 7", "id": 7}
        mockFranchise8_2022 = {"owner_name": "Owner 8", "name": "Team 8", "id": 8}
        mockLeague2022 = {
            "league": {
                "id": 123,
                "name": "Test League 2022",
                "lastRegularSeasonWeek": "1",
                "franchises": {
                    "franchise": [
                        mockFranchise1_2022,
                        mockFranchise2_2022,
                        mockFranchise3_2022,
                        mockFranchise4_2022,
                        mockFranchise5_2022,
                        mockFranchise6_2022,
                        mockFranchise7_2022,
                        mockFranchise8_2022,
                    ]
                },
            }
        }

        mockSchedule2022 = {
            "schedule": {
                "weeklySchedule": [
                    {
                        "week": "1",
                        "matchup": [
                            {
                                "franchise": [
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise1_2022, score=100, result="W"
                                    ),
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise2_2022, score=100, result="L"
                                    ),
                                ]
                            },
                            {
                                "franchise": [
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise3_2022, score=100.1, result="W"
                                    ),
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise4_2022, score=90.1, result="L"
                                    ),
                                ]
                            },
                            {
                                "franchise": [
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise5_2022, score=101, result="W"
                                    ),
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise6_2022, score=91, result="L"
                                    ),
                                ]
                            },
                            {
                                "franchise": [
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise7_2022, score=102, result="W"
                                    ),
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise8_2022, score=92, result="L"
                                    ),
                                ]
                            },
                        ],
                    },
                    {
                        "week": "2",
                        "matchup": [
                            {
                                "franchise": [
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise2_2022, score=103, result="W"
                                    ),
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise3_2022, score=93, result="L"
                                    ),
                                ]
                            }
                        ],
                    },
                ]
            }
        }
        mockPlayoffSchedule_2022 = {
            "playoffBracket": {
                "playoffRound": [
                    {
                        "week": 1,
                        "playoffGame": {"away": {"franchise_id": 2}, "home": {"franchise_id": 3}},
                    }
                ]
            }
        }

        mockGetLeague.side_effect = [mockLeague2022]
        mockGetSchedule.side_effect = [mockSchedule2022]
        mockGetPlayoffBracket.side_effect = [mockPlayoffSchedule_2022]

        leagueLoader = MyFantasyLeagueLeagueLoader(
            "123", [2022], mflUsername="mflu", mflPassword="mflp", mflUserAgentName="mfluan"
        )
        league = leagueLoader.loadLeague()

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
                                    teamAScore=101,
                                    teamBScore=91,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team7_2022.id,
                                    teamBId=team8_2022.id,
                                    teamAScore=102,
                                    teamBScore=92,
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
                                    teamAScore=103,
                                    teamBScore=93,
                                    matchupType=MatchupType.PLAYOFF,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                )
                            ],
                        ),
                    ],
                    yearSettings=None,
                )
            ],
        )

        self.assertEqual(league, expectedLeague)
