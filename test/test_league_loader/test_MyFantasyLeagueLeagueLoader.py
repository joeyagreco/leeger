import unittest
from unittest import mock
import copy
from leeger.enum.MatchupType import MatchupType

from leeger.league_loader import MyFantasyLeagueLeagueLoader
from leeger.model.league.Division import Division
from leeger.model.league.League import League
from leeger.model.league.Matchup import Matchup
from leeger.model.league.Owner import Owner
from leeger.model.league.Team import Team
from leeger.model.league.Week import Week
from leeger.model.league.Year import Year


class TestMyFantasyLeagueLeagueLoader(unittest.TestCase):
    def __addScoreToMockFranchise(
        self, *, mockFranchise: dict, score: int | float, result: str
    ) -> dict:
        dupMockFranchise = copy.deepcopy(mockFranchise)
        dupMockFranchise["score"] = score
        dupMockFranchise["result"] = result
        return dupMockFranchise

    @mock.patch("pymfl.api.config.APIConfig.add_config_for_year_and_league_id")
    @mock.patch("pymfl.api.CommonLeagueInfoAPIClient.get_league")
    @mock.patch("pymfl.api.CommonLeagueInfoAPIClient.get_schedule")
    @mock.patch("pymfl.api.CommonLeagueInfoAPIClient.get_playoff_bracket")
    def test_loadLeague_happyPath_noOwnerNamesAndAliases(
        self, mockGetPlayoffBracket, mockGetSchedule, mockGetLeague, mockAddConfig
    ):
        """
        NOTE: This also tests the following cases:
            - having 1 playoff round in a year (dict)
            - having multiple playoff rounds in a year (list)
            - having 1 playoff matchup in a playoff week (dict)
            - having multiple playoff matchups in a playoff week (list)
        """
        mockFranchise1_2022 = {"owner_name": "Owner 1", "name": "Team 1", "id": 1, "division": "1"}
        mockFranchise2_2022 = {"owner_name": "Owner 2", "name": "Team 2", "id": 2, "division": "1"}
        mockFranchise3_2022 = {"owner_name": "Owner 3", "name": "Team 3", "id": 3, "division": "1"}
        mockFranchise4_2022 = {"owner_name": "Owner 4", "name": "Team 4", "id": 4, "division": "1"}
        mockFranchise5_2022 = {"owner_name": "Owner 5", "name": "Team 5", "id": 5, "division": "2"}
        mockFranchise6_2022 = {"owner_name": "Owner 6", "name": "Team 6", "id": 6, "division": "2"}
        mockFranchise7_2022 = {"owner_name": "Owner 7", "name": "Team 7", "id": 7, "division": "2"}
        mockFranchise8_2022 = {"owner_name": "Owner 8", "name": "Team 8", "id": 8, "division": "2"}

        mockFranchise1_2023 = {"owner_name": "Owner 1", "name": "Team 1", "id": 1, "division": "1"}
        mockFranchise2_2023 = {"owner_name": "Owner 2", "name": "Team 2", "id": 2, "division": "1"}
        mockFranchise3_2023 = {"owner_name": "Owner 3", "name": "Team 3", "id": 3, "division": "1"}
        mockFranchise4_2023 = {"owner_name": "Owner 4", "name": "Team 4", "id": 4, "division": "1"}
        mockFranchise5_2023 = {"owner_name": "Owner 5", "name": "Team 5", "id": 5, "division": "2"}
        mockFranchise6_2023 = {"owner_name": "Owner 6", "name": "Team 6", "id": 6, "division": "2"}
        mockFranchise7_2023 = {"owner_name": "Owner 7", "name": "Team 7", "id": 7, "division": "2"}
        mockFranchise8_2023 = {"owner_name": "Owner 8", "name": "Team 8", "id": 8, "division": "2"}

        mockFranchise1_2024 = {"owner_name": "Owner 1", "name": "Team 1", "id": 1, "division": "1"}
        mockFranchise2_2024 = {"owner_name": "Owner 2", "name": "Team 2", "id": 2, "division": "1"}
        mockFranchise3_2024 = {"owner_name": "Owner 3", "name": "Team 3", "id": 3, "division": "1"}
        mockFranchise4_2024 = {"owner_name": "Owner 4", "name": "Team 4", "id": 4, "division": "1"}
        mockFranchise5_2024 = {"owner_name": "Owner 5", "name": "Team 5", "id": 5, "division": "2"}
        mockFranchise6_2024 = {"owner_name": "Owner 6", "name": "Team 6", "id": 6, "division": "2"}
        mockFranchise7_2024 = {"owner_name": "Owner 7", "name": "Team 7", "id": 7, "division": "2"}
        mockFranchise8_2024 = {"owner_name": "Owner 8", "name": "Team 8", "id": 8, "division": "2"}

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
                "divisions": {
                    "division": [{"id": "1", "name": "d1_2022"}, {"id": "2", "name": "d2_2022"}]
                },
            }
        }

        mockLeague2023 = {
            "league": {
                "id": 456,
                "name": "Test League 2023",
                "lastRegularSeasonWeek": "1",
                "franchises": {
                    "franchise": [
                        mockFranchise1_2023,
                        mockFranchise2_2023,
                        mockFranchise3_2023,
                        mockFranchise4_2023,
                        mockFranchise5_2023,
                        mockFranchise6_2023,
                        mockFranchise7_2023,
                        mockFranchise8_2023,
                    ]
                },
                "divisions": {
                    "division": [{"id": "1", "name": "d1_2023"}, {"id": "2", "name": "d2_2023"}]
                },
            }
        }

        mockLeague2024 = {
            "league": {
                "id": 789,
                "name": "Test League 2024",
                "lastRegularSeasonWeek": "1",
                "franchises": {
                    "franchise": [
                        mockFranchise1_2024,
                        mockFranchise2_2024,
                        mockFranchise3_2024,
                        mockFranchise4_2024,
                        mockFranchise5_2024,
                        mockFranchise6_2024,
                        mockFranchise7_2024,
                        mockFranchise8_2024,
                    ]
                },
                "divisions": {
                    "division": [{"id": "1", "name": "d1_2024"}, {"id": "2", "name": "d2_2024"}]
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
                    {
                        "week": "3",
                        "matchup": [
                            {
                                "franchise": [
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise1_2022, score=104, result="W"
                                    ),
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise2_2022, score=94, result="L"
                                    ),
                                ]
                            }
                        ],
                    },
                ]
            }
        }

        mockSchedule2023 = {
            "schedule": {
                "weeklySchedule": [
                    {
                        "week": "1",
                        "matchup": [
                            {
                                "franchise": [
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise1_2023, score=100, result="W"
                                    ),
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise2_2023, score=100, result="L"
                                    ),
                                ]
                            },
                            {
                                "franchise": [
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise3_2023, score=100.1, result="W"
                                    ),
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise4_2023, score=90.1, result="L"
                                    ),
                                ]
                            },
                            {
                                "franchise": [
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise5_2023, score=101, result="W"
                                    ),
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise6_2023, score=91, result="L"
                                    ),
                                ]
                            },
                            {
                                "franchise": [
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise7_2023, score=102, result="W"
                                    ),
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise8_2023, score=92, result="L"
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
                                        mockFranchise=mockFranchise2_2023, score=103, result="W"
                                    ),
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise3_2023, score=93, result="L"
                                    ),
                                ]
                            },
                            {
                                "franchise": [
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise4_2023, score=103, result="W"
                                    ),
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise5_2023, score=93, result="L"
                                    ),
                                ]
                            },
                        ],
                    },
                    {
                        "week": "3",
                        "matchup": [
                            {
                                "franchise": [
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise2_2023, score=104, result="W"
                                    ),
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise3_2023, score=94, result="L"
                                    ),
                                ]
                            }
                        ],
                    },
                    {
                        "week": "4",
                        "matchup": [
                            {
                                "franchise": [
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise1_2023, score=104, result="W"
                                    ),
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise2_2023, score=94, result="L"
                                    ),
                                ]
                            }
                        ],
                    },
                ]
            }
        }

        mockSchedule2024 = {
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
                                        mockFranchise=mockFranchise1_2022, score=103, result="W"
                                    ),
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise2_2022, score=93, result="L"
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
                        "week": 2,
                        "playoffGame": {"away": {"franchise_id": 2}, "home": {"franchise_id": 3}},
                    },
                    {
                        "week": 3,
                        "playoffGame": {"away": {"franchise_id": 1}, "home": {"franchise_id": 2}},
                    },
                ]
            }
        }

        mockPlayoffSchedule_2023 = {
            "playoffBracket": {
                "playoffRound": [
                    {
                        "week": 2,
                        "playoffGame": [
                            {"away": {"franchise_id": 2}, "home": {"franchise_id": 3}},
                            {"away": {"franchise_id": 4}, "home": {"franchise_id": 5}},
                        ],
                    },
                    {
                        "week": 3,
                        "playoffGame": {"away": {"franchise_id": 2}, "home": {"franchise_id": 4}},
                    },
                    {
                        "week": 4,
                        "playoffGame": {"away": {"franchise_id": 1}, "home": {"franchise_id": 2}},
                    },
                ]
            }
        }

        mockPlayoffSchedule_2024 = {
            "playoffBracket": {
                "playoffRound": {
                    "week": 2,
                    "playoffGame": {"away": {"franchise_id": 1}, "home": {"franchise_id": 2}},
                }
            }
        }

        mockGetLeague.side_effect = [mockLeague2022, mockLeague2023, mockLeague2024]
        mockGetSchedule.side_effect = [mockSchedule2022, mockSchedule2023, mockSchedule2024]
        mockGetPlayoffBracket.side_effect = [
            mockPlayoffSchedule_2022,
            mockPlayoffSchedule_2023,
            mockPlayoffSchedule_2024,
        ]

        leagueLoader = MyFantasyLeagueLeagueLoader(
            "789",
            [2022, 2023, 2024],
            mflUsername="mflu",
            mflPassword="mflp",
            mflUserAgentName="mfluan",
        )
        league = leagueLoader.loadLeague()

        # expected league

        division1_2022 = Division(name="d1_2022")
        division2_2022 = Division(name="d2_2022")

        division1_2023 = Division(name="d1_2023")
        division2_2023 = Division(name="d2_2023")

        division1_2024 = Division(name="d1_2024")
        division2_2024 = Division(name="d2_2024")

        owner1 = Owner(name="Owner 1")
        owner2 = Owner(name="Owner 2")
        owner3 = Owner(name="Owner 3")
        owner4 = Owner(name="Owner 4")
        owner5 = Owner(name="Owner 5")
        owner6 = Owner(name="Owner 6")
        owner7 = Owner(name="Owner 7")
        owner8 = Owner(name="Owner 8")

        team1_2022 = Team(ownerId=owner1.id, name="Team 1", divisionId=division1_2022.id)
        team2_2022 = Team(ownerId=owner2.id, name="Team 2", divisionId=division1_2022.id)
        team3_2022 = Team(ownerId=owner3.id, name="Team 3", divisionId=division1_2022.id)
        team4_2022 = Team(ownerId=owner4.id, name="Team 4", divisionId=division1_2022.id)
        team5_2022 = Team(ownerId=owner5.id, name="Team 5", divisionId=division2_2022.id)
        team6_2022 = Team(ownerId=owner6.id, name="Team 6", divisionId=division2_2022.id)
        team7_2022 = Team(ownerId=owner7.id, name="Team 7", divisionId=division2_2022.id)
        team8_2022 = Team(ownerId=owner8.id, name="Team 8", divisionId=division2_2022.id)

        team1_2023 = Team(ownerId=owner1.id, name="Team 1", divisionId=division1_2023.id)
        team2_2023 = Team(ownerId=owner2.id, name="Team 2", divisionId=division1_2023.id)
        team3_2023 = Team(ownerId=owner3.id, name="Team 3", divisionId=division1_2023.id)
        team4_2023 = Team(ownerId=owner4.id, name="Team 4", divisionId=division1_2023.id)
        team5_2023 = Team(ownerId=owner5.id, name="Team 5", divisionId=division2_2023.id)
        team6_2023 = Team(ownerId=owner6.id, name="Team 6", divisionId=division2_2023.id)
        team7_2023 = Team(ownerId=owner7.id, name="Team 7", divisionId=division2_2023.id)
        team8_2023 = Team(ownerId=owner8.id, name="Team 8", divisionId=division2_2023.id)

        team1_2024 = Team(ownerId=owner1.id, name="Team 1", divisionId=division1_2024.id)
        team2_2024 = Team(ownerId=owner2.id, name="Team 2", divisionId=division1_2024.id)
        team3_2024 = Team(ownerId=owner3.id, name="Team 3", divisionId=division1_2024.id)
        team4_2024 = Team(ownerId=owner4.id, name="Team 4", divisionId=division1_2024.id)
        team5_2024 = Team(ownerId=owner5.id, name="Team 5", divisionId=division2_2024.id)
        team6_2024 = Team(ownerId=owner6.id, name="Team 6", divisionId=division2_2024.id)
        team7_2024 = Team(ownerId=owner7.id, name="Team 7", divisionId=division2_2024.id)
        team8_2024 = Team(ownerId=owner8.id, name="Team 8", divisionId=division2_2024.id)

        expectedLeague = League(
            name="Test League 2024",
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
                        Week(
                            weekNumber=3,
                            matchups=[
                                Matchup(
                                    teamAId=team1_2022.id,
                                    teamBId=team2_2022.id,
                                    teamAScore=104,
                                    teamBScore=94,
                                    matchupType=MatchupType.CHAMPIONSHIP,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                )
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
                                    teamAScore=100.1,
                                    teamBScore=90.1,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team5_2023.id,
                                    teamBId=team6_2023.id,
                                    teamAScore=101,
                                    teamBScore=91,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team7_2023.id,
                                    teamBId=team8_2023.id,
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
                                    teamAId=team2_2023.id,
                                    teamBId=team3_2023.id,
                                    teamAScore=103,
                                    teamBScore=93,
                                    matchupType=MatchupType.PLAYOFF,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team4_2023.id,
                                    teamBId=team5_2023.id,
                                    teamAScore=103,
                                    teamBScore=93,
                                    matchupType=MatchupType.PLAYOFF,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                ),
                            ],
                        ),
                        Week(
                            weekNumber=3,
                            matchups=[
                                Matchup(
                                    teamAId=team2_2023.id,
                                    teamBId=team4_2023.id,
                                    teamAScore=104,
                                    teamBScore=94,
                                    matchupType=MatchupType.PLAYOFF,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                )
                            ],
                        ),
                        Week(
                            weekNumber=4,
                            matchups=[
                                Matchup(
                                    teamAId=team1_2023.id,
                                    teamBId=team2_2023.id,
                                    teamAScore=104,
                                    teamBScore=94,
                                    matchupType=MatchupType.CHAMPIONSHIP,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                )
                            ],
                        ),
                    ],
                    yearSettings=None,
                    divisions=[division1_2023, division2_2023],
                ),
                Year(
                    yearNumber=2024,
                    teams=[
                        team1_2024,
                        team2_2024,
                        team3_2024,
                        team4_2024,
                        team5_2024,
                        team6_2024,
                        team7_2024,
                        team8_2024,
                    ],
                    weeks=[
                        Week(
                            weekNumber=1,
                            matchups=[
                                Matchup(
                                    teamAId=team1_2024.id,
                                    teamBId=team2_2024.id,
                                    teamAScore=100,
                                    teamBScore=100,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team3_2024.id,
                                    teamBId=team4_2024.id,
                                    teamAScore=100.1,
                                    teamBScore=90.1,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team5_2024.id,
                                    teamBId=team6_2024.id,
                                    teamAScore=101,
                                    teamBScore=91,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team7_2024.id,
                                    teamBId=team8_2024.id,
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
                                    teamAId=team1_2024.id,
                                    teamBId=team2_2024.id,
                                    teamAScore=103,
                                    teamBScore=93,
                                    matchupType=MatchupType.CHAMPIONSHIP,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                )
                            ],
                        ),
                    ],
                    yearSettings=None,
                    divisions=[division1_2024, division2_2024],
                ),
            ],
        )

        self.assertTrue(league.equals(expectedLeague, ignoreBaseId=True, ignoreIds=True))
        # check multiWeekMatchupIds
        for year in league.years:
            for week in year.weeks:
                for matchup in week.matchups:
                    self.assertIsNone(matchup.multiWeekMatchupId)

    @mock.patch("pymfl.api.config.APIConfig.add_config_for_year_and_league_id")
    @mock.patch("pymfl.api.CommonLeagueInfoAPIClient.get_league")
    @mock.patch("pymfl.api.CommonLeagueInfoAPIClient.get_schedule")
    @mock.patch("pymfl.api.CommonLeagueInfoAPIClient.get_playoff_bracket")
    def test_loadLeague_happyPath_withOwnerNamesAndAliases(
        self, mockGetPlayoffBracket, mockGetSchedule, mockGetLeague, mockAddConfig
    ):
        """
        NOTE: This also tests the following cases:
            - having 1 playoff round in a year (dict)
            - having multiple playoff rounds in a year (list)
            - having 1 playoff matchup in a playoff week (dict)
            - having multiple playoff matchups in a playoff week (list)
        """
        mockFranchise1_2022 = {"owner_name": "Owner 1", "name": "Team 1", "id": 1, "division": "1"}
        mockFranchise2_2022 = {"owner_name": "Owner 2", "name": "Team 2", "id": 2, "division": "1"}
        mockFranchise3_2022 = {"owner_name": "Owner 3", "name": "Team 3", "id": 3, "division": "1"}
        mockFranchise4_2022 = {"owner_name": "Owner 4", "name": "Team 4", "id": 4, "division": "1"}
        mockFranchise5_2022 = {"owner_name": "Owner 5", "name": "Team 5", "id": 5, "division": "2"}
        mockFranchise6_2022 = {"owner_name": "Owner 6", "name": "Team 6", "id": 6, "division": "2"}
        mockFranchise7_2022 = {"owner_name": "Owner 7", "name": "Team 7", "id": 7, "division": "2"}
        mockFranchise8_2022 = {"owner_name": "Owner 8", "name": "Team 8", "id": 8, "division": "2"}

        mockFranchise1_2023 = {"owner_name": "Owner 1", "name": "Team 1", "id": 1, "division": "1"}
        mockFranchise2_2023 = {"owner_name": "Owner 2", "name": "Team 2", "id": 2, "division": "1"}
        mockFranchise3_2023 = {"owner_name": "Owner 3", "name": "Team 3", "id": 3, "division": "1"}
        mockFranchise4_2023 = {"owner_name": "Owner 4", "name": "Team 4", "id": 4, "division": "1"}
        mockFranchise5_2023 = {"owner_name": "Owner 5", "name": "Team 5", "id": 5, "division": "2"}
        mockFranchise6_2023 = {"owner_name": "Owner 6", "name": "Team 6", "id": 6, "division": "2"}
        mockFranchise7_2023 = {"owner_name": "Owner 7", "name": "Team 7", "id": 7, "division": "2"}
        mockFranchise8_2023 = {"owner_name": "Owner 8", "name": "Team 8", "id": 8, "division": "2"}

        mockFranchise1_2024 = {"owner_name": "Owner 1", "name": "Team 1", "id": 1, "division": "1"}
        mockFranchise2_2024 = {"owner_name": "Owner 2", "name": "Team 2", "id": 2, "division": "1"}
        mockFranchise3_2024 = {"owner_name": "Owner 3", "name": "Team 3", "id": 3, "division": "1"}
        mockFranchise4_2024 = {"owner_name": "Owner 4", "name": "Team 4", "id": 4, "division": "1"}
        mockFranchise5_2024 = {"owner_name": "Owner 5", "name": "Team 5", "id": 5, "division": "2"}
        mockFranchise6_2024 = {"owner_name": "Owner 6", "name": "Team 6", "id": 6, "division": "2"}
        mockFranchise7_2024 = {"owner_name": "Owner 7", "name": "Team 7", "id": 7, "division": "2"}
        mockFranchise8_2024 = {"owner_name": "Owner 8", "name": "Team 8", "id": 8, "division": "2"}

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
                "divisions": {
                    "division": [{"id": "1", "name": "d1_2022"}, {"id": "2", "name": "d2_2022"}]
                },
            }
        }

        mockLeague2023 = {
            "league": {
                "id": 456,
                "name": "Test League 2023",
                "lastRegularSeasonWeek": "1",
                "franchises": {
                    "franchise": [
                        mockFranchise1_2023,
                        mockFranchise2_2023,
                        mockFranchise3_2023,
                        mockFranchise4_2023,
                        mockFranchise5_2023,
                        mockFranchise6_2023,
                        mockFranchise7_2023,
                        mockFranchise8_2023,
                    ]
                },
                "divisions": {
                    "division": [{"id": "1", "name": "d1_2023"}, {"id": "2", "name": "d2_2023"}]
                },
            }
        }

        mockLeague2024 = {
            "league": {
                "id": 789,
                "name": "Test League 2024",
                "lastRegularSeasonWeek": "1",
                "franchises": {
                    "franchise": [
                        mockFranchise1_2024,
                        mockFranchise2_2024,
                        mockFranchise3_2024,
                        mockFranchise4_2024,
                        mockFranchise5_2024,
                        mockFranchise6_2024,
                        mockFranchise7_2024,
                        mockFranchise8_2024,
                    ]
                },
                "divisions": {
                    "division": [{"id": "1", "name": "d1_2024"}, {"id": "2", "name": "d2_2024"}]
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
                    {
                        "week": "3",
                        "matchup": [
                            {
                                "franchise": [
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise1_2022, score=104, result="W"
                                    ),
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise2_2022, score=94, result="L"
                                    ),
                                ]
                            }
                        ],
                    },
                ]
            }
        }

        mockSchedule2023 = {
            "schedule": {
                "weeklySchedule": [
                    {
                        "week": "1",
                        "matchup": [
                            {
                                "franchise": [
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise1_2023, score=100, result="W"
                                    ),
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise2_2023, score=100, result="L"
                                    ),
                                ]
                            },
                            {
                                "franchise": [
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise3_2023, score=100.1, result="W"
                                    ),
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise4_2023, score=90.1, result="L"
                                    ),
                                ]
                            },
                            {
                                "franchise": [
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise5_2023, score=101, result="W"
                                    ),
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise6_2023, score=91, result="L"
                                    ),
                                ]
                            },
                            {
                                "franchise": [
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise7_2023, score=102, result="W"
                                    ),
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise8_2023, score=92, result="L"
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
                                        mockFranchise=mockFranchise2_2023, score=103, result="W"
                                    ),
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise3_2023, score=93, result="L"
                                    ),
                                ]
                            },
                            {
                                "franchise": [
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise4_2023, score=103, result="W"
                                    ),
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise5_2023, score=93, result="L"
                                    ),
                                ]
                            },
                        ],
                    },
                    {
                        "week": "3",
                        "matchup": [
                            {
                                "franchise": [
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise2_2023, score=104, result="W"
                                    ),
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise3_2023, score=94, result="L"
                                    ),
                                ]
                            }
                        ],
                    },
                    {
                        "week": "4",
                        "matchup": [
                            {
                                "franchise": [
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise1_2023, score=104, result="W"
                                    ),
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise2_2023, score=94, result="L"
                                    ),
                                ]
                            }
                        ],
                    },
                ]
            }
        }

        mockSchedule2024 = {
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
                                        mockFranchise=mockFranchise1_2022, score=103, result="W"
                                    ),
                                    self.__addScoreToMockFranchise(
                                        mockFranchise=mockFranchise2_2022, score=93, result="L"
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
                        "week": 2,
                        "playoffGame": {"away": {"franchise_id": 2}, "home": {"franchise_id": 3}},
                    },
                    {
                        "week": 3,
                        "playoffGame": {"away": {"franchise_id": 1}, "home": {"franchise_id": 2}},
                    },
                ]
            }
        }

        mockPlayoffSchedule_2023 = {
            "playoffBracket": {
                "playoffRound": [
                    {
                        "week": 2,
                        "playoffGame": [
                            {"away": {"franchise_id": 2}, "home": {"franchise_id": 3}},
                            {"away": {"franchise_id": 4}, "home": {"franchise_id": 5}},
                        ],
                    },
                    {
                        "week": 3,
                        "playoffGame": {"away": {"franchise_id": 2}, "home": {"franchise_id": 4}},
                    },
                    {
                        "week": 4,
                        "playoffGame": {"away": {"franchise_id": 1}, "home": {"franchise_id": 2}},
                    },
                ]
            }
        }

        mockPlayoffSchedule_2024 = {
            "playoffBracket": {
                "playoffRound": {
                    "week": 2,
                    "playoffGame": {"away": {"franchise_id": 1}, "home": {"franchise_id": 2}},
                }
            }
        }

        mockGetLeague.side_effect = [mockLeague2022, mockLeague2023, mockLeague2024]
        mockGetSchedule.side_effect = [mockSchedule2022, mockSchedule2023, mockSchedule2024]
        mockGetPlayoffBracket.side_effect = [
            mockPlayoffSchedule_2022,
            mockPlayoffSchedule_2023,
            mockPlayoffSchedule_2024,
        ]

        leagueLoader = MyFantasyLeagueLeagueLoader(
            "789",
            [2022, 2023, 2024],
            mflUsername="mflu",
            mflPassword="mflp",
            mflUserAgentName="mfluan",
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
        league = leagueLoader.loadLeague()

        # expected league

        division1_2022 = Division(name="d1_2022")
        division2_2022 = Division(name="d2_2022")

        division1_2023 = Division(name="d1_2023")
        division2_2023 = Division(name="d2_2023")

        division1_2024 = Division(name="d1_2024")
        division2_2024 = Division(name="d2_2024")

        owner1 = Owner(name="o1")
        owner2 = Owner(name="o2")
        owner3 = Owner(name="o3")
        owner4 = Owner(name="o4")
        owner5 = Owner(name="o5")
        owner6 = Owner(name="o6")
        owner7 = Owner(name="o7")
        owner8 = Owner(name="o8")

        team1_2022 = Team(ownerId=owner1.id, name="Team 1", divisionId=division1_2022.id)
        team2_2022 = Team(ownerId=owner2.id, name="Team 2", divisionId=division1_2022.id)
        team3_2022 = Team(ownerId=owner3.id, name="Team 3", divisionId=division1_2022.id)
        team4_2022 = Team(ownerId=owner4.id, name="Team 4", divisionId=division1_2022.id)
        team5_2022 = Team(ownerId=owner5.id, name="Team 5", divisionId=division2_2022.id)
        team6_2022 = Team(ownerId=owner6.id, name="Team 6", divisionId=division2_2022.id)
        team7_2022 = Team(ownerId=owner7.id, name="Team 7", divisionId=division2_2022.id)
        team8_2022 = Team(ownerId=owner8.id, name="Team 8", divisionId=division2_2022.id)

        team1_2023 = Team(ownerId=owner1.id, name="Team 1", divisionId=division1_2023.id)
        team2_2023 = Team(ownerId=owner2.id, name="Team 2", divisionId=division1_2023.id)
        team3_2023 = Team(ownerId=owner3.id, name="Team 3", divisionId=division1_2023.id)
        team4_2023 = Team(ownerId=owner4.id, name="Team 4", divisionId=division1_2023.id)
        team5_2023 = Team(ownerId=owner5.id, name="Team 5", divisionId=division2_2023.id)
        team6_2023 = Team(ownerId=owner6.id, name="Team 6", divisionId=division2_2023.id)
        team7_2023 = Team(ownerId=owner7.id, name="Team 7", divisionId=division2_2023.id)
        team8_2023 = Team(ownerId=owner8.id, name="Team 8", divisionId=division2_2023.id)

        team1_2024 = Team(ownerId=owner1.id, name="Team 1", divisionId=division1_2024.id)
        team2_2024 = Team(ownerId=owner2.id, name="Team 2", divisionId=division1_2024.id)
        team3_2024 = Team(ownerId=owner3.id, name="Team 3", divisionId=division1_2024.id)
        team4_2024 = Team(ownerId=owner4.id, name="Team 4", divisionId=division1_2024.id)
        team5_2024 = Team(ownerId=owner5.id, name="Team 5", divisionId=division2_2024.id)
        team6_2024 = Team(ownerId=owner6.id, name="Team 6", divisionId=division2_2024.id)
        team7_2024 = Team(ownerId=owner7.id, name="Team 7", divisionId=division2_2024.id)
        team8_2024 = Team(ownerId=owner8.id, name="Team 8", divisionId=division2_2024.id)

        expectedLeague = League(
            name="Test League 2024",
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
                        Week(
                            weekNumber=3,
                            matchups=[
                                Matchup(
                                    teamAId=team1_2022.id,
                                    teamBId=team2_2022.id,
                                    teamAScore=104,
                                    teamBScore=94,
                                    matchupType=MatchupType.CHAMPIONSHIP,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                )
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
                                    teamAScore=100.1,
                                    teamBScore=90.1,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team5_2023.id,
                                    teamBId=team6_2023.id,
                                    teamAScore=101,
                                    teamBScore=91,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team7_2023.id,
                                    teamBId=team8_2023.id,
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
                                    teamAId=team2_2023.id,
                                    teamBId=team3_2023.id,
                                    teamAScore=103,
                                    teamBScore=93,
                                    matchupType=MatchupType.PLAYOFF,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team4_2023.id,
                                    teamBId=team5_2023.id,
                                    teamAScore=103,
                                    teamBScore=93,
                                    matchupType=MatchupType.PLAYOFF,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                ),
                            ],
                        ),
                        Week(
                            weekNumber=3,
                            matchups=[
                                Matchup(
                                    teamAId=team2_2023.id,
                                    teamBId=team4_2023.id,
                                    teamAScore=104,
                                    teamBScore=94,
                                    matchupType=MatchupType.PLAYOFF,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                )
                            ],
                        ),
                        Week(
                            weekNumber=4,
                            matchups=[
                                Matchup(
                                    teamAId=team1_2023.id,
                                    teamBId=team2_2023.id,
                                    teamAScore=104,
                                    teamBScore=94,
                                    matchupType=MatchupType.CHAMPIONSHIP,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                )
                            ],
                        ),
                    ],
                    yearSettings=None,
                    divisions=[division1_2023, division2_2023],
                ),
                Year(
                    yearNumber=2024,
                    teams=[
                        team1_2024,
                        team2_2024,
                        team3_2024,
                        team4_2024,
                        team5_2024,
                        team6_2024,
                        team7_2024,
                        team8_2024,
                    ],
                    weeks=[
                        Week(
                            weekNumber=1,
                            matchups=[
                                Matchup(
                                    teamAId=team1_2024.id,
                                    teamBId=team2_2024.id,
                                    teamAScore=100,
                                    teamBScore=100,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team3_2024.id,
                                    teamBId=team4_2024.id,
                                    teamAScore=100.1,
                                    teamBScore=90.1,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team5_2024.id,
                                    teamBId=team6_2024.id,
                                    teamAScore=101,
                                    teamBScore=91,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team7_2024.id,
                                    teamBId=team8_2024.id,
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
                                    teamAId=team1_2024.id,
                                    teamBId=team2_2024.id,
                                    teamAScore=103,
                                    teamBScore=93,
                                    matchupType=MatchupType.CHAMPIONSHIP,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                )
                            ],
                        ),
                    ],
                    yearSettings=None,
                    divisions=[division1_2024, division2_2024],
                ),
            ],
        )

        self.assertTrue(league.equals(expectedLeague, ignoreBaseId=True, ignoreIds=True))
        # check multiWeekMatchupIds
        for year in league.years:
            for week in year.weeks:
                for matchup in week.matchups:
                    self.assertIsNone(matchup.multiWeekMatchupId)
