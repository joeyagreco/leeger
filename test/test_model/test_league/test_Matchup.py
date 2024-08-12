import unittest

from leeger.enum.MatchupType import MatchupType
from leeger.exception import DoesNotExistException
from leeger.exception.InvalidMatchupFormatException import InvalidMatchupFormatException
from leeger.model.league.Matchup import Matchup
from leeger.model.league_helper.Performance import Performance
from test.helper.prototypes import getNDefaultOwnersAndTeams


class TestMatchup(unittest.TestCase):
    def test_matchup_init(self):
        matchup = Matchup(
            teamAId="teamAId",
            teamBId="teamBId",
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.PLAYOFF,
            teamAHasTiebreaker=True,
            teamBHasTiebreaker=False,
            multiWeekMatchupId="id",
        )

        self.assertEqual("teamAId", matchup.teamAId)
        self.assertEqual("teamBId", matchup.teamBId)
        self.assertEqual(1.1, matchup.teamAScore)
        self.assertEqual(2.2, matchup.teamBScore)
        self.assertEqual(MatchupType.PLAYOFF, matchup.matchupType)
        self.assertTrue(matchup.teamAHasTiebreaker)
        self.assertFalse(matchup.teamBHasTiebreaker)
        self.assertEqual("id", matchup.multiWeekMatchupId)

    def test_matchup_init_defaultValues_1(self):
        matchup = Matchup(
            teamAId="teamAId", teamBId="teamBId", teamAScore=1.1, teamBScore=2.2
        )

        self.assertEqual("teamAId", matchup.teamAId)
        self.assertEqual("teamBId", matchup.teamBId)
        self.assertEqual(1.1, matchup.teamAScore)
        self.assertEqual(2.2, matchup.teamBScore)
        self.assertEqual(MatchupType.REGULAR_SEASON, matchup.matchupType)
        self.assertFalse(matchup.teamAHasTiebreaker)
        self.assertFalse(matchup.teamBHasTiebreaker)
        self.assertIsNone(matchup.multiWeekMatchupId)

    def test_matchup_init_defaultValues_2(self):
        matchup = Matchup(
            teamAId="teamAId",
            teamBId="teamBId",
            teamAScore=1.1,
            teamBScore=2.2,
            teamAHasTiebreaker=None,
            teamBHasTiebreaker=None,
        )

        self.assertEqual("teamAId", matchup.teamAId)
        self.assertEqual("teamBId", matchup.teamBId)
        self.assertEqual(1.1, matchup.teamAScore)
        self.assertEqual(2.2, matchup.teamBScore)
        self.assertEqual(MatchupType.REGULAR_SEASON, matchup.matchupType)
        self.assertFalse(matchup.teamAHasTiebreaker)
        self.assertFalse(matchup.teamBHasTiebreaker)
        self.assertIsNone(matchup.multiWeekMatchupId)

    def test_matchup_init_aAndBHaveTieBreakers_raisesException(self):
        with self.assertRaises(InvalidMatchupFormatException) as context:
            Matchup(
                teamAId="teamAId",
                teamBId="teamBId",
                teamAScore=1.1,
                teamBScore=2.2,
                teamAHasTiebreaker=True,
                teamBHasTiebreaker=True,
            )
        self.assertEqual(
            "Team A and Team B cannot both have the tiebreaker.", str(context.exception)
        )

    def test_matchup_eq_callsEqualsMethod(self):
        # create Matchup 1
        _, teams_1 = getNDefaultOwnersAndTeams(2)
        matchup_1 = Matchup(
            teamAId=teams_1[0].id,
            teamBId=teams_1[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            multiWeekMatchupId="1",
            matchupType=MatchupType.REGULAR_SEASON,
        )

        matchup_2 = Matchup(
            teamAId=teams_1[0].id,
            teamBId=teams_1[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            multiWeekMatchupId="1",
            matchupType=MatchupType.REGULAR_SEASON,
        )

        matchup_2.id = matchup_1.id

        result = matchup_1 == matchup_2

        self.assertTrue(result)

    def test_matchup_eq_equal(self):
        # create Matchup 1
        _, teams_1 = getNDefaultOwnersAndTeams(2)
        matchup_1 = Matchup(
            teamAId=teams_1[0].id,
            teamBId=teams_1[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            multiWeekMatchupId="1",
            matchupType=MatchupType.REGULAR_SEASON,
        )

        matchup_2 = Matchup(
            teamAId=teams_1[0].id,
            teamBId=teams_1[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            multiWeekMatchupId="1",
            matchupType=MatchupType.REGULAR_SEASON,
        )

        result = matchup_1.equals(matchup_2, ignoreBaseIds=True)

        self.assertTrue(result)

    def test_matchup_eq_notEqual(self):
        # create Matchup 1
        _, teams_1 = getNDefaultOwnersAndTeams(2)
        matchup_1 = Matchup(
            teamAId=teams_1[0].id,
            teamBId=teams_1[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            multiWeekMatchupId="1",
            matchupType=MatchupType.REGULAR_SEASON,
        )

        # create Matchup 2
        _, teams_2 = getNDefaultOwnersAndTeams(2)
        matchup_2 = Matchup(
            teamAId=teams_2[0].id,
            teamBId=teams_2[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            multiWeekMatchupId="1",
            matchupType=MatchupType.REGULAR_SEASON,
        )

        result = matchup_1.equals(matchup_2, ignoreBaseIds=True)

        self.assertFalse(result)

    def test_matchup_toJson(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            multiWeekMatchupId="1",
            matchupType=MatchupType.REGULAR_SEASON,
        )
        matchupJson = matchup.toJson()

        self.assertIsInstance(matchupJson, dict)
        self.assertEqual(teams[0].id, matchupJson["teamAId"])
        self.assertEqual(teams[1].id, matchupJson["teamBId"])
        self.assertEqual(1.1, matchupJson["teamAScore"])
        self.assertEqual(2.2, matchupJson["teamBScore"])
        self.assertEqual("REGULAR_SEASON", matchupJson["matchupType"])
        self.assertFalse(matchupJson["teamAHasTiebreaker"])
        self.assertFalse(matchupJson["teamBHasTiebreaker"])
        self.assertEqual("1", matchupJson["multiWeekMatchupId"])

    def test_splitToPerformances_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            multiWeekMatchupId="1",
            matchupType=MatchupType.REGULAR_SEASON,
        )

        responseA, responseB = matchup.splitToPerformances()

        self.assertIsInstance(responseA, Performance)
        self.assertIsInstance(responseB, Performance)
        self.assertEqual(teams[0].id, responseA.teamId)
        self.assertEqual(teams[1].id, responseB.teamId)
        self.assertEqual(1.1, responseA.teamScore)
        self.assertEqual(2.2, responseB.teamScore)
        self.assertEqual(MatchupType.REGULAR_SEASON, responseA.matchupType)
        self.assertEqual(MatchupType.REGULAR_SEASON, responseB.matchupType)
        self.assertEqual("1", responseA.multiWeekMatchupId)
        self.assertEqual("1", responseB.multiWeekMatchupId)

    def test_getPerformanceForTeamId_happyPath(self):
        matchup = Matchup(
            teamAId="1",
            teamBId="2",
            teamAScore=1.1,
            teamBScore=2.2,
            multiWeekMatchupId="1",
            matchupType=MatchupType.REGULAR_SEASON,
        )

        response = matchup.getPerformanceForTeamId("1")

        self.assertIsInstance(response, Performance)
        self.assertEqual("1", response.teamId)
        self.assertEqual(1.1, response.teamScore)
        self.assertEqual("1", response.multiWeekMatchupId)
        self.assertEqual(MatchupType.REGULAR_SEASON, response.matchupType)

    def test_getPerformanceForTeamId_teamIdNotInMatchup_raisesException(self):
        matchup = Matchup(
            teamAId="1",
            teamBId="2",
            teamAScore=1.1,
            teamBScore=2.2,
            multiWeekMatchupId="1",
            matchupType=MatchupType.REGULAR_SEASON,
        )

        with self.assertRaises(DoesNotExistException) as context:
            matchup.getPerformanceForTeamId("3")
        self.assertEqual(
            "Matchup does not have a team with ID '3'.", str(context.exception)
        )

    def test_matchup_fromJson(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            multiWeekMatchupId="1",
            matchupType=MatchupType.REGULAR_SEASON,
        )
        matchupJson = matchup.toJson()
        matchupDerived = Matchup.fromJson(matchupJson)
        self.assertEqual(matchup, matchupDerived)
        self.assertEqual(matchup.id, matchupDerived.id)
