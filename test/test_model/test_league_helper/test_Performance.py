import unittest

from leeger.enum.MatchupType import MatchupType
from leeger.model.league_helper.Performance import Performance
from test.helper.prototypes import getNDefaultOwnersAndTeams


class TestPerformance(unittest.TestCase):
    def test_performance_init(self):
        performance = Performance(
            teamId="teamId",
            teamScore=1.1,
            matchupType=MatchupType.PLAYOFF,
            hasTiebreaker=True,
            multiWeekMatchupId="id"
        )

        self.assertEqual("teamId", performance.teamId)
        self.assertEqual(1.1, performance.teamScore)
        self.assertEqual(MatchupType.PLAYOFF, performance.matchupType)
        self.assertTrue(performance.hasTiebreaker)
        self.assertEqual("id", performance.multiWeekMatchupId)

    def test_performance_init_defaultValues(self):
        performance = Performance(
            teamId="teamId",
            teamScore=1.1
        )

        self.assertEqual("teamId", performance.teamId)
        self.assertEqual(1.1, performance.teamScore)
        self.assertEqual(MatchupType.REGULAR_SEASON, performance.matchupType)
        self.assertFalse(performance.hasTiebreaker)
        self.assertIsNone(performance.multiWeekMatchupId)

    def test_performance_eq_equal(self):
        # create Performance 1
        _, teams_1 = getNDefaultOwnersAndTeams(2)
        performance_1 = Performance(teamId=teams_1[0].id,
                                    teamScore=1.1,
                                    hasTiebreaker=True,
                                    multiWeekMatchupId="1",
                                    matchupType=MatchupType.REGULAR_SEASON)

        # create Matchup 2
        _, teams_2 = getNDefaultOwnersAndTeams(2)
        performance_2 = Performance(teamId=teams_2[0].id,
                                    teamScore=1.1,
                                    hasTiebreaker=True,
                                    multiWeekMatchupId="1",
                                    matchupType=MatchupType.REGULAR_SEASON)

        self.assertEqual(performance_1, performance_2)

    def test_performance_eq_notEqual(self):
        # create Performance 1
        _, teams_1 = getNDefaultOwnersAndTeams(2)
        performance_1 = Performance(teamId=teams_1[0].id,
                                    teamScore=1.1,
                                    hasTiebreaker=True,
                                    multiWeekMatchupId="1",
                                    matchupType=MatchupType.PLAYOFF)

        # create Matchup 2
        _, teams_2 = getNDefaultOwnersAndTeams(2)
        performance_2 = Performance(teamId=teams_2[0].id,
                                    teamScore=1.1,
                                    hasTiebreaker=True,
                                    multiWeekMatchupId="1",
                                    matchupType=MatchupType.REGULAR_SEASON)

        self.assertNotEqual(performance_1, performance_2)

    def test_performance_toJson(self):
        performance = Performance(
            teamId="teamId",
            teamScore=1.1,
            matchupType=MatchupType.PLAYOFF,
            hasTiebreaker=True,
            multiWeekMatchupId="id"
        )
        performanceJson = performance.toJson()

        self.assertIsInstance(performanceJson, dict)
        self.assertEqual("teamId", performanceJson["teamId"])
        self.assertEqual(1.1, performanceJson["teamScore"])
        self.assertEqual("PLAYOFF", performanceJson["matchupType"])
        self.assertTrue(performanceJson["hasTiebreaker"])
        self.assertEqual("id", performanceJson["multiWeekMatchupId"])
    #
    # def test_splitToPerformances_happyPath(self):
    #     owners, teams = getNDefaultOwnersAndTeams(2)
    #
    #     matchup = Matchup(teamAId=teams[0].id,
    #                       teamBId=teams[1].id,
    #                       teamAScore=1.1,
    #                       teamBScore=2.2,
    #                       multiWeekMatchupId="1",
    #                       matchupType=MatchupType.REGULAR_SEASON)
    #
    #     responseA, responseB = matchup.splitToPerformances()
    #
    #     self.assertIsInstance(responseA, Performance)
    #     self.assertIsInstance(responseB, Performance)
    #     self.assertEqual(teams[0].id, responseA.teamId)
    #     self.assertEqual(teams[1].id, responseB.teamId)
    #     self.assertEqual(1.1, responseA.teamScore)
    #     self.assertEqual(2.2, responseB.teamScore)
    #     self.assertEqual(MatchupType.REGULAR_SEASON, responseA.matchupType)
    #     self.assertEqual(MatchupType.REGULAR_SEASON, responseB.matchupType)
    #     self.assertEqual("1", responseA.multiWeekMatchupId)
    #     self.assertEqual("1", responseB.multiWeekMatchupId)
