import unittest

from leeger.enum.MatchupType import MatchupType
from leeger.exception import InvalidMatchupFormatException
from leeger.model.league import Matchup
from leeger.model.league_helper.Performance import Performance
from test.helper.prototypes import getNDefaultOwnersAndTeams


class TestPerformance(unittest.TestCase):
    def test_performance_init(self):
        performance = Performance(
            teamId="teamId",
            teamScore=1.1,
            matchupType=MatchupType.PLAYOFF,
            hasTiebreaker=True,
            multiWeekMatchupId="id",
        )

        self.assertEqual("teamId", performance.teamId)
        self.assertEqual(1.1, performance.teamScore)
        self.assertEqual(MatchupType.PLAYOFF, performance.matchupType)
        self.assertTrue(performance.hasTiebreaker)
        self.assertEqual("id", performance.multiWeekMatchupId)

    def test_performance_init_defaultValues(self):
        performance = Performance(teamId="teamId", teamScore=1.1)

        self.assertEqual("teamId", performance.teamId)
        self.assertEqual(1.1, performance.teamScore)
        self.assertEqual(MatchupType.REGULAR_SEASON, performance.matchupType)
        self.assertFalse(performance.hasTiebreaker)
        self.assertIsNone(performance.multiWeekMatchupId)

    def test_performance_eq_callsEqualsMethod(self):
        # create Performance 1
        _, teams_1 = getNDefaultOwnersAndTeams(2)
        performance_1 = Performance(
            teamId=teams_1[0].id,
            teamScore=1.1,
            hasTiebreaker=True,
            multiWeekMatchupId="1",
            matchupType=MatchupType.REGULAR_SEASON,
        )

        self.assertTrue(performance_1 == performance_1)

    def test_performance_eq_equal(self):
        # create Performance 1
        _, teams_1 = getNDefaultOwnersAndTeams(2)
        performance_1 = Performance(
            teamId=teams_1[0].id,
            teamScore=1.1,
            hasTiebreaker=True,
            multiWeekMatchupId="1",
            matchupType=MatchupType.REGULAR_SEASON,
        )

        # create Matchup 2
        performance_2 = Performance(
            teamId=teams_1[0].id,
            teamScore=1.1,
            hasTiebreaker=True,
            multiWeekMatchupId="1",
            matchupType=MatchupType.REGULAR_SEASON,
        )

        self.assertTrue(performance_1.equals(performance_2, ignoreBaseIds=True))

    def test_performance_eq_notEqual(self):
        # create Performance 1
        _, teams_1 = getNDefaultOwnersAndTeams(2)
        performance_1 = Performance(
            teamId=teams_1[0].id,
            teamScore=1.1,
            hasTiebreaker=True,
            multiWeekMatchupId="1",
            matchupType=MatchupType.PLAYOFF,
        )

        # create Matchup 2
        _, teams_2 = getNDefaultOwnersAndTeams(2)
        performance_2 = Performance(
            teamId=teams_2[0].id,
            teamScore=1.1,
            hasTiebreaker=True,
            multiWeekMatchupId="1",
            matchupType=MatchupType.REGULAR_SEASON,
        )

        self.assertFalse(performance_1.equals(performance_2, ignoreBaseIds=True))

    def test_performance_toJson(self):
        performance = Performance(
            teamId="teamId",
            teamScore=1.1,
            matchupType=MatchupType.PLAYOFF,
            hasTiebreaker=True,
            multiWeekMatchupId="id",
        )
        performanceJson = performance.toJson()

        self.assertIsInstance(performanceJson, dict)
        self.assertEqual("teamId", performanceJson["teamId"])
        self.assertEqual(1.1, performanceJson["teamScore"])
        self.assertEqual("PLAYOFF", performanceJson["matchupType"])
        self.assertTrue(performanceJson["hasTiebreaker"])
        self.assertEqual("id", performanceJson["multiWeekMatchupId"])

    def test_performance_add_happyPath(self):
        performance_1 = Performance(
            teamId="team1Id",
            teamScore=1.1,
            matchupType=MatchupType.REGULAR_SEASON,
            hasTiebreaker=True,
            multiWeekMatchupId="id",
        )

        performance_2 = Performance(
            teamId="team2Id",
            teamScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
            hasTiebreaker=True,
            multiWeekMatchupId="id",
        )

        response = performance_1 + performance_2
        self.assertIsInstance(response, Matchup)
        self.assertEqual("team1Id", response.teamAId)
        self.assertEqual("team2Id", response.teamBId)
        self.assertEqual(1.1, response.teamAScore)
        self.assertEqual(2.2, response.teamBScore)
        self.assertEqual(MatchupType.REGULAR_SEASON, response.matchupType)
        self.assertFalse(response.teamAHasTiebreaker)
        self.assertFalse(response.teamBHasTiebreaker)
        self.assertEqual("id", response.multiWeekMatchupId)

    def test_performance_add_performancesHaveDifferentMatchupTypes_raisesException(self):
        performance_1 = Performance(
            teamId="team1Id",
            teamScore=1.1,
            matchupType=MatchupType.PLAYOFF,
            hasTiebreaker=True,
            multiWeekMatchupId="id",
        )

        performance_2 = Performance(
            teamId="team2Id",
            teamScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
            hasTiebreaker=True,
            multiWeekMatchupId="id",
        )

        with self.assertRaises(InvalidMatchupFormatException) as context:
            performance_1 + performance_2
        self.assertEqual(
            "Cannot make a matchup from conflicting matchup types 'MatchupType.PLAYOFF' and 'MatchupType.REGULAR_SEASON'.",
            str(context.exception),
        )

    def test_performance_add_performancesHaveDifferentMultiWeekMatchupIds_raisesException(self):
        performance_1 = Performance(
            teamId="team1Id",
            teamScore=1.1,
            matchupType=MatchupType.REGULAR_SEASON,
            hasTiebreaker=True,
            multiWeekMatchupId=None,
        )

        performance_2 = Performance(
            teamId="team2Id",
            teamScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
            hasTiebreaker=True,
            multiWeekMatchupId="id",
        )

        with self.assertRaises(InvalidMatchupFormatException) as context:
            performance_1 + performance_2
        self.assertEqual(
            "Cannot make a matchup from conflicting multi-week matchup IDs 'None' and 'id'.",
            str(context.exception),
        )
