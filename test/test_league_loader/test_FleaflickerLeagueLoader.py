import unittest
from unittest import mock
from leeger.enum.MatchupType import MatchupType

from leeger.model.league.League import League
from leeger.model.league.Matchup import Matchup
from leeger.model.league.Owner import Owner
from leeger.model.league.Team import Team
from leeger.model.league.Week import Week
from leeger.model.league.Year import Year

from leeger.league_loader.FleaflickerLeagueLoader import FleaflickerLeagueLoader


class TestFleaflickerLeagueLoader(unittest.TestCase):
    def test_init_leagueIdNotIntConvertable_raisesException(self):
        with self.assertRaises(ValueError) as context:
            FleaflickerLeagueLoader("foo", [])
        self.assertEqual("League ID 'foo' could not be turned into an int.", str(context.exception))

    @mock.patch("fleaflicker.api.LeagueInfoAPIClient.LeagueInfoAPIClient.get_league_standings")
    @mock.patch("fleaflicker.api.ScoringAPIClient.ScoringAPIClient.get_league_scoreboard")
    def test_loadLeague_happyPath_noOwnerNamesAndAliases(
        self, mockGetLeagueScoreboard, mockGetLeaguestandings
    ):
        mockTeam1_2022 = {"owners": [{"displayName": "Owner 1"}], "id": 1, "name": "Team 1"}
        mockTeam2_2022 = {"owners": [{"displayName": "Owner 2"}], "id": 2, "name": "Team 2"}
        mockTeam3_2022 = {"owners": [{"displayName": "Owner 3"}], "id": 3, "name": "Team 3"}
        mockTeam4_2022 = {"owners": [{"displayName": "Owner 4"}], "id": 4, "name": "Team 4"}
        mockTeam5_2022 = {"owners": [{"displayName": "Owner 5"}], "id": 5, "name": "Team 5"}
        mockTeam6_2022 = {"owners": [{"displayName": "Owner 6"}], "id": 6, "name": "Team 6"}
        mockTeam7_2022 = {"owners": [{"displayName": "Owner 7"}], "id": 7, "name": "Team 7"}
        mockTeam8_2022 = {"owners": [{"displayName": "Owner 8"}], "id": 8, "name": "Team 8"}

        mockTeam1_2023 = {"owners": [{"displayName": "Owner 1"}], "id": 1, "name": "Team 1"}
        mockTeam2_2023 = {"owners": [{"displayName": "Owner 2"}], "id": 2, "name": "Team 2"}
        mockTeam3_2023 = {"owners": [{"displayName": "Owner 3"}], "id": 3, "name": "Team 3"}
        mockTeam4_2023 = {"owners": [{"displayName": "Owner 4"}], "id": 4, "name": "Team 4"}
        mockTeam5_2023 = {"owners": [{"displayName": "Owner 5"}], "id": 5, "name": "Team 5"}
        mockTeam6_2023 = {"owners": [{"displayName": "Owner 6"}], "id": 6, "name": "Team 6"}
        mockTeam7_2023 = {"owners": [{"displayName": "Owner 7"}], "id": 7, "name": "Team 7"}
        mockTeam8_2023 = {"owners": [{"displayName": "Owner 8"}], "id": 8, "name": "Team 8"}

        mockLeagueStandings2022 = {
            "divisions": [
                {
                    "teams": [
                        mockTeam1_2022,
                        mockTeam2_2022,
                        mockTeam3_2022,
                        mockTeam4_2022,
                        mockTeam5_2022,
                        mockTeam6_2022,
                        mockTeam7_2022,
                        mockTeam8_2022,
                    ]
                }
            ],
            "league": {"name": "Test League 2022", "id": 123},
            "season": 2022,
        }

        mockLeagueStandings2023 = {
            "divisions": [
                {
                    "teams": [
                        mockTeam1_2023,
                        mockTeam2_2023,
                        mockTeam3_2023,
                        mockTeam4_2023,
                        mockTeam5_2023,
                        mockTeam6_2023,
                        mockTeam7_2023,
                        mockTeam8_2023,
                    ]
                }
            ],
            "league": {"name": "Test League 2023", "id": 123},
            "season": 2023,
        }

        mockWeek1_2022 = {
            "games": [
                {
                    "away": mockTeam1_2022,
                    "home": mockTeam2_2022,
                    "awayScore": {"score": {"value": 100}},
                    "homeScore": {"score": {"value": 100}},
                    "awayResult": "WIN",
                    "homeResult": "LOSS",
                    "isFinalScore": True,
                },
                {
                    "away": mockTeam3_2022,
                    "home": mockTeam4_2022,
                    "awayScore": {"score": {"value": 100}},
                    "homeScore": {"score": {"value": 90}},
                    "awayResult": "WIN",
                    "homeResult": "LOSS",
                    "isFinalScore": True,
                },
                {
                    "away": mockTeam5_2022,
                    "home": mockTeam6_2022,
                    "awayScore": {"score": {"value": 100.1}},
                    "homeScore": {"score": {"value": 90.1}},
                    "awayResult": "WIN",
                    "homeResult": "LOSS",
                    "isFinalScore": True,
                },
                {
                    "away": mockTeam7_2022,
                    "home": mockTeam8_2022,
                    "awayScore": {"score": {"value": 100.2}},
                    "homeScore": {"score": {"value": 90.2}},
                    "awayResult": "WIN",
                    "homeResult": "LOSS",
                    "isFinalScore": True,
                },
            ]
        }

        mockWeek1_2023 = {
            "games": [
                {
                    "away": mockTeam1_2023,
                    "home": mockTeam2_2023,
                    "awayScore": {"score": {"value": 100}},
                    "homeScore": {"score": {"value": 100}},
                    "awayResult": "WIN",
                    "homeResult": "LOSS",
                    "isFinalScore": True,
                },
                {
                    "away": mockTeam3_2023,
                    "home": mockTeam4_2023,
                    "awayScore": {"score": {"value": 100}},
                    "homeScore": {"score": {"value": 90}},
                    "awayResult": "WIN",
                    "homeResult": "LOSS",
                    "isFinalScore": True,
                },
                {
                    "away": mockTeam5_2023,
                    "home": mockTeam6_2023,
                    "awayScore": {"score": {"value": 100.1}},
                    "homeScore": {"score": {"value": 90.1}},
                    "awayResult": "WIN",
                    "homeResult": "LOSS",
                    "isFinalScore": True,
                },
                {
                    "away": mockTeam7_2023,
                    "home": mockTeam8_2023,
                    "awayScore": {"score": {"value": 100.2}},
                    "homeScore": {"score": {"value": 90.2}},
                    "awayResult": "WIN",
                    "homeResult": "LOSS",
                    "isFinalScore": True,
                },
            ]
        }

        mockWeek2_2022 = {
            "games": [
                {
                    "away": mockTeam2_2022,
                    "home": mockTeam3_2022,
                    "awayScore": {"score": {"value": 100.4}},
                    "homeScore": {"score": {"value": 90.4}},
                    "awayResult": "WIN",
                    "homeResult": "LOSS",
                    "isFinalScore": True,
                    "isThirdPlaceGame": True,
                }
            ]
        }

        mockWeek2_2023 = {
            "games": [
                {
                    "away": mockTeam2_2023,
                    "home": mockTeam3_2023,
                    "awayScore": {"score": {"value": 100.4}},
                    "homeScore": {"score": {"value": 90.4}},
                    "awayResult": "WIN",
                    "homeResult": "LOSS",
                    "isFinalScore": True,
                    "isThirdPlaceGame": True,
                }
            ]
        }

        mockWeek3_2022 = {
            "games": [
                {
                    "away": mockTeam1_2022,
                    "home": mockTeam2_2022,
                    "awayScore": {"score": {"value": 100.5}},
                    "homeScore": {"score": {"value": 90.5}},
                    "awayResult": "WIN",
                    "homeResult": "LOSS",
                    "isFinalScore": True,
                    "isChampionshipGame": True,
                }
            ]
        }

        mockWeek3_2023 = {
            "games": [
                {
                    "away": mockTeam1_2023,
                    "home": mockTeam2_2023,
                    "awayScore": {"score": {"value": 100.5}},
                    "homeScore": {"score": {"value": 90.5}},
                    "awayResult": "WIN",
                    "homeResult": "LOSS",
                    "isFinalScore": True,
                    "isChampionshipGame": True,
                }
            ]
        }

        mockScoreboard2022 = {
            "eligibleSchedulePeriods": [mockWeek1_2022, mockWeek2_2022, mockWeek3_2022]
        }

        mockScoreboard2023 = {
            "eligibleSchedulePeriods": [mockWeek1_2023, mockWeek2_2023, mockWeek3_2023]
        }

        mockGetLeaguestandings.side_effect = [mockLeagueStandings2022, mockLeagueStandings2023]
        mockGetLeagueScoreboard.side_effect = [
            mockScoreboard2022,
            mockWeek1_2022,
            mockWeek2_2022,
            mockWeek3_2022,
            mockScoreboard2023,
            mockWeek1_2023,
            mockWeek2_2023,
            mockWeek3_2023,
        ]

        leagueLoader = FleaflickerLeagueLoader("123", [2022, 2023])
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
                                    teamAScore=100,
                                    teamBScore=90,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team5_2022.id,
                                    teamBId=team6_2022.id,
                                    teamAScore=100.1,
                                    teamBScore=90.1,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team7_2022.id,
                                    teamBId=team8_2022.id,
                                    teamAScore=100.2,
                                    teamBScore=90.2,
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
                                    teamAScore=100.4,
                                    teamBScore=90.4,
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
                                    teamAScore=100.5,
                                    teamBScore=90.5,
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
                                    teamAScore=100,
                                    teamBScore=90,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team5_2023.id,
                                    teamBId=team6_2023.id,
                                    teamAScore=100.1,
                                    teamBScore=90.1,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team7_2023.id,
                                    teamBId=team8_2023.id,
                                    teamAScore=100.2,
                                    teamBScore=90.2,
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
                                    teamAScore=100.4,
                                    teamBScore=90.4,
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
                                    teamAScore=100.5,
                                    teamBScore=90.5,
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

        self.assertEqual(league, expectedLeague)
        # check multiWeekMatchupIds
        for year in league.years:
            for week in year.weeks:
                for matchup in week.matchups:
                    self.assertIsNone(matchup.multiWeekMatchupId)

    @mock.patch("fleaflicker.api.LeagueInfoAPIClient.LeagueInfoAPIClient.get_league_standings")
    @mock.patch("fleaflicker.api.ScoringAPIClient.ScoringAPIClient.get_league_scoreboard")
    def test_loadLeague_happyPath_withOwnerNamesAndAliases(
        self, mockGetLeagueScoreboard, mockGetLeaguestandings
    ):
        mockTeam1_2022 = {"owners": [{"displayName": "Owner 1"}], "id": 1, "name": "Team 1"}
        mockTeam2_2022 = {"owners": [{"displayName": "Owner 2"}], "id": 2, "name": "Team 2"}
        mockTeam3_2022 = {"owners": [{"displayName": "Owner 3"}], "id": 3, "name": "Team 3"}
        mockTeam4_2022 = {"owners": [{"displayName": "Owner 4"}], "id": 4, "name": "Team 4"}
        mockTeam5_2022 = {"owners": [{"displayName": "Owner 5"}], "id": 5, "name": "Team 5"}
        mockTeam6_2022 = {"owners": [{"displayName": "Owner 6"}], "id": 6, "name": "Team 6"}
        mockTeam7_2022 = {"owners": [{"displayName": "Owner 7"}], "id": 7, "name": "Team 7"}
        mockTeam8_2022 = {"owners": [{"displayName": "Owner 8"}], "id": 8, "name": "Team 8"}

        mockTeam1_2023 = {"owners": [{"displayName": "Owner 1"}], "id": 1, "name": "Team 1"}
        mockTeam2_2023 = {"owners": [{"displayName": "Owner 2"}], "id": 2, "name": "Team 2"}
        mockTeam3_2023 = {"owners": [{"displayName": "Owner 3"}], "id": 3, "name": "Team 3"}
        mockTeam4_2023 = {"owners": [{"displayName": "Owner 4"}], "id": 4, "name": "Team 4"}
        mockTeam5_2023 = {"owners": [{"displayName": "Owner 5"}], "id": 5, "name": "Team 5"}
        mockTeam6_2023 = {"owners": [{"displayName": "Owner 6"}], "id": 6, "name": "Team 6"}
        mockTeam7_2023 = {"owners": [{"displayName": "Owner 7"}], "id": 7, "name": "Team 7"}
        mockTeam8_2023 = {"owners": [{"displayName": "Owner 8"}], "id": 8, "name": "Team 8"}

        mockLeagueStandings2022 = {
            "divisions": [
                {
                    "teams": [
                        mockTeam1_2022,
                        mockTeam2_2022,
                        mockTeam3_2022,
                        mockTeam4_2022,
                        mockTeam5_2022,
                        mockTeam6_2022,
                        mockTeam7_2022,
                        mockTeam8_2022,
                    ]
                }
            ],
            "league": {"name": "Test League 2022", "id": 123},
            "season": 2022,
        }

        mockLeagueStandings2023 = {
            "divisions": [
                {
                    "teams": [
                        mockTeam1_2023,
                        mockTeam2_2023,
                        mockTeam3_2023,
                        mockTeam4_2023,
                        mockTeam5_2023,
                        mockTeam6_2023,
                        mockTeam7_2023,
                        mockTeam8_2023,
                    ]
                }
            ],
            "league": {"name": "Test League 2023", "id": 123},
            "season": 2023,
        }

        mockWeek1_2022 = {
            "games": [
                {
                    "away": mockTeam1_2022,
                    "home": mockTeam2_2022,
                    "awayScore": {"score": {"value": 100}},
                    "homeScore": {"score": {"value": 100}},
                    "awayResult": "WIN",
                    "homeResult": "LOSS",
                    "isFinalScore": True,
                },
                {
                    "away": mockTeam3_2022,
                    "home": mockTeam4_2022,
                    "awayScore": {"score": {"value": 100}},
                    "homeScore": {"score": {"value": 90}},
                    "awayResult": "WIN",
                    "homeResult": "LOSS",
                    "isFinalScore": True,
                },
                {
                    "away": mockTeam5_2022,
                    "home": mockTeam6_2022,
                    "awayScore": {"score": {"value": 100.1}},
                    "homeScore": {"score": {"value": 90.1}},
                    "awayResult": "WIN",
                    "homeResult": "LOSS",
                    "isFinalScore": True,
                },
                {
                    "away": mockTeam7_2022,
                    "home": mockTeam8_2022,
                    "awayScore": {"score": {"value": 100.2}},
                    "homeScore": {"score": {"value": 90.2}},
                    "awayResult": "WIN",
                    "homeResult": "LOSS",
                    "isFinalScore": True,
                },
            ]
        }

        mockWeek1_2023 = {
            "games": [
                {
                    "away": mockTeam1_2023,
                    "home": mockTeam2_2023,
                    "awayScore": {"score": {"value": 100}},
                    "homeScore": {"score": {"value": 100}},
                    "awayResult": "WIN",
                    "homeResult": "LOSS",
                    "isFinalScore": True,
                },
                {
                    "away": mockTeam3_2023,
                    "home": mockTeam4_2023,
                    "awayScore": {"score": {"value": 100}},
                    "homeScore": {"score": {"value": 90}},
                    "awayResult": "WIN",
                    "homeResult": "LOSS",
                    "isFinalScore": True,
                },
                {
                    "away": mockTeam5_2023,
                    "home": mockTeam6_2023,
                    "awayScore": {"score": {"value": 100.1}},
                    "homeScore": {"score": {"value": 90.1}},
                    "awayResult": "WIN",
                    "homeResult": "LOSS",
                    "isFinalScore": True,
                },
                {
                    "away": mockTeam7_2023,
                    "home": mockTeam8_2023,
                    "awayScore": {"score": {"value": 100.2}},
                    "homeScore": {"score": {"value": 90.2}},
                    "awayResult": "WIN",
                    "homeResult": "LOSS",
                    "isFinalScore": True,
                },
            ]
        }

        mockWeek2_2022 = {
            "games": [
                {
                    "away": mockTeam2_2022,
                    "home": mockTeam3_2022,
                    "awayScore": {"score": {"value": 100.4}},
                    "homeScore": {"score": {"value": 90.4}},
                    "awayResult": "WIN",
                    "homeResult": "LOSS",
                    "isFinalScore": True,
                    "isThirdPlaceGame": True,
                }
            ]
        }

        mockWeek2_2023 = {
            "games": [
                {
                    "away": mockTeam2_2023,
                    "home": mockTeam3_2023,
                    "awayScore": {"score": {"value": 100.4}},
                    "homeScore": {"score": {"value": 90.4}},
                    "awayResult": "WIN",
                    "homeResult": "LOSS",
                    "isFinalScore": True,
                    "isThirdPlaceGame": True,
                }
            ]
        }

        mockWeek3_2022 = {
            "games": [
                {
                    "away": mockTeam1_2022,
                    "home": mockTeam2_2022,
                    "awayScore": {"score": {"value": 100.5}},
                    "homeScore": {"score": {"value": 90.5}},
                    "awayResult": "WIN",
                    "homeResult": "LOSS",
                    "isFinalScore": True,
                    "isChampionshipGame": True,
                }
            ]
        }

        mockWeek3_2023 = {
            "games": [
                {
                    "away": mockTeam1_2023,
                    "home": mockTeam2_2023,
                    "awayScore": {"score": {"value": 100.5}},
                    "homeScore": {"score": {"value": 90.5}},
                    "awayResult": "WIN",
                    "homeResult": "LOSS",
                    "isFinalScore": True,
                    "isChampionshipGame": True,
                }
            ]
        }

        mockScoreboard2022 = {
            "eligibleSchedulePeriods": [mockWeek1_2022, mockWeek2_2022, mockWeek3_2022]
        }

        mockScoreboard2023 = {
            "eligibleSchedulePeriods": [mockWeek1_2023, mockWeek2_2023, mockWeek3_2023]
        }

        mockGetLeaguestandings.side_effect = [mockLeagueStandings2022, mockLeagueStandings2023]
        mockGetLeagueScoreboard.side_effect = [
            mockScoreboard2022,
            mockWeek1_2022,
            mockWeek2_2022,
            mockWeek3_2022,
            mockScoreboard2023,
            mockWeek1_2023,
            mockWeek2_2023,
            mockWeek3_2023,
        ]

        leagueLoader = FleaflickerLeagueLoader(
            "123",
            [2022, 2023],
            ownerNamesAndAliases={
                "o1": ["o1"],
                "o2": ["o2"],
                "o3": ["o3"],
                "o4": ["o4"],
                "o5": ["o5"],
                "o6": ["o6"],
                "o7": ["o7"],
                "o8": ["o8"],
            },
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
                                    teamAScore=100,
                                    teamBScore=90,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team5_2022.id,
                                    teamBId=team6_2022.id,
                                    teamAScore=100.1,
                                    teamBScore=90.1,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team7_2022.id,
                                    teamBId=team8_2022.id,
                                    teamAScore=100.2,
                                    teamBScore=90.2,
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
                                    teamAScore=100.4,
                                    teamBScore=90.4,
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
                                    teamAScore=100.5,
                                    teamBScore=90.5,
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
                                    teamAScore=100,
                                    teamBScore=90,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team5_2023.id,
                                    teamBId=team6_2023.id,
                                    teamAScore=100.1,
                                    teamBScore=90.1,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team7_2023.id,
                                    teamBId=team8_2023.id,
                                    teamAScore=100.2,
                                    teamBScore=90.2,
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
                                    teamAScore=100.4,
                                    teamBScore=90.4,
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
                                    teamAScore=100.5,
                                    teamBScore=90.5,
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

        self.assertEqual(league, expectedLeague)
        # check multiWeekMatchupIds
        for year in league.years:
            for week in year.weeks:
                for matchup in week.matchups:
                    self.assertIsNone(matchup.multiWeekMatchupId)
