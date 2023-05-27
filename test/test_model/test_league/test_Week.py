import unittest

from leeger.enum.MatchupType import MatchupType
from leeger.exception import DoesNotExistException
from leeger.model.league.Matchup import Matchup
from leeger.model.league.Week import Week
from test.helper.prototypes import getNDefaultOwnersAndTeams


class TestWeek(unittest.TestCase):
    def test_week_init(self):
        matchup1 = Matchup(teamAId="", teamBId="", teamAScore=0, teamBScore=0)
        matchup2 = Matchup(
            teamAId="", teamBId="", teamAScore=0, teamBScore=0, matchupType=MatchupType.PLAYOFF
        )
        matchup3 = Matchup(
            teamAId="", teamBId="", teamAScore=0, teamBScore=0, matchupType=MatchupType.CHAMPIONSHIP
        )
        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        self.assertEqual(1, week1.weekNumber)
        self.assertFalse(week1.isPlayoffWeek)
        self.assertFalse(week1.isChampionshipWeek)
        self.assertTrue(week2.isPlayoffWeek)
        self.assertFalse(week2.isChampionshipWeek)
        self.assertTrue(week3.isPlayoffWeek)
        self.assertTrue(week3.isChampionshipWeek)
        self.assertEqual(1, len(week1.matchups))
        self.assertEqual(matchup1.id, week1.matchups[0].id)
        self.assertEqual(matchup2.id, week2.matchups[0].id)
        self.assertEqual(matchup3.id, week3.matchups[0].id)

    def test_isPlayoffWeek_weekHasPlayoffMatchups_returnsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])

        response = week1.isPlayoffWeek

        self.assertIsInstance(response, bool)
        self.assertTrue(response)

    def test_isPlayoffWeek_weekDoesNotHavePlayoffMatchups_returnsFalse(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.REGULAR_SEASON,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])

        response = week1.isPlayoffWeek

        self.assertIsInstance(response, bool)
        self.assertFalse(response)

    def test_isChampionshipWeek_weekHasAChampionshipMatchup_returnsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])

        response1 = week1.isChampionshipWeek
        response2 = week1.isPlayoffWeek

        self.assertIsInstance(response1, bool)
        self.assertTrue(response1)
        self.assertIsInstance(response2, bool)
        self.assertTrue(response2)

    def test_isChampionshipWeek_weekDoesNotHaveAnyChampionshipMatchups_returnsFalse(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.REGULAR_SEASON,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])

        response = week1.isChampionshipWeek

        self.assertIsInstance(response, bool)
        self.assertFalse(response)

    def test_isRegularSeasonWeek_weekHasAllRegularSeasonMatchups_returnsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(4)

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.IGNORE,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2])

        response = week1.isRegularSeasonWeek

        self.assertIsInstance(response, bool)
        self.assertTrue(response)

    def test_isChampionshipWeek_weekHasANonRegularSeasonMatchup_returnsFalse(self):
        owners, teams = getNDefaultOwnersAndTeams(4)

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2])

        response = week1.isRegularSeasonWeek

        self.assertIsInstance(response, bool)
        self.assertFalse(response)

    def test_week_eq_callsEqualsMethod(self):
        # create Week 1
        _, teams_1 = getNDefaultOwnersAndTeams(2)
        matchup_1 = Matchup(
            teamAId=teams_1[0].id,
            teamBId=teams_1[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        week_1 = Week(weekNumber=1, matchups=[matchup_1])

        # create Week 2
        matchup_2 = Matchup(
            teamAId=teams_1[0].id,
            teamBId=teams_1[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        week_2 = Week(weekNumber=1, matchups=[matchup_2])

        week_2.id = week_1.id
        matchup_2.id = matchup_1.id

        result = week_1 == week_2

        self.assertTrue(result)

    def test_week_eq_equal(self):
        # create Week 1
        _, teams_1 = getNDefaultOwnersAndTeams(2)
        matchup_1 = Matchup(
            teamAId=teams_1[0].id,
            teamBId=teams_1[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        week_1 = Week(weekNumber=1, matchups=[matchup_1])

        # create Week 2
        matchup_2 = Matchup(
            teamAId=teams_1[0].id,
            teamBId=teams_1[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        week_2 = Week(weekNumber=1, matchups=[matchup_2])

        result = week_1.equals(week_2, ignoreBaseId=True)

        self.assertTrue(result)

    def test_week_eq_notEqual(self):
        # create Week 1
        _, teams_1 = getNDefaultOwnersAndTeams(2)
        matchup_1 = Matchup(
            teamAId=teams_1[0].id,
            teamBId=teams_1[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        week_1 = Week(weekNumber=1, matchups=[matchup_1])

        # create Week 2
        _, teams_2 = getNDefaultOwnersAndTeams(2)
        matchup_2 = Matchup(
            teamAId=teams_2[0].id,
            teamBId=teams_2[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        week_2 = Week(weekNumber=1, matchups=[matchup_2])

        result = week_1.equals(week_2, ignoreBaseId=True)

        self.assertFalse(result)

    def test_week_toJson(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup_1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        week = Week(weekNumber=1, matchups=[matchup_1])
        weekJson = week.toJson()

        self.assertIsInstance(weekJson, dict)
        self.assertEqual(1, weekJson["weekNumber"])
        self.assertEqual(1, len(weekJson["matchups"]))
        self.assertEqual(teams[0].id, weekJson["matchups"][0]["teamAId"])
        self.assertEqual(teams[1].id, weekJson["matchups"][0]["teamBId"])
        self.assertEqual(1.1, weekJson["matchups"][0]["teamAScore"])
        self.assertEqual(2.2, weekJson["matchups"][0]["teamBScore"])
        self.assertEqual("REGULAR_SEASON", weekJson["matchups"][0]["matchupType"])
        self.assertFalse(weekJson["matchups"][0]["teamAHasTiebreaker"])
        self.assertFalse(weekJson["matchups"][0]["teamBHasTiebreaker"])

    def test_getMatchupWithTeamId_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup_1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        week = Week(weekNumber=1, matchups=[matchup_1])

        response = week.getMatchupWithTeamId(teams[0].id)
        self.assertEqual(matchup_1, response)

    def test_getMatchupWithTeamId_teamIdNotInMatchups_raisesException(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup_1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        week = Week(weekNumber=1, matchups=[matchup_1])

        with self.assertRaises(DoesNotExistException) as context:
            week.getMatchupWithTeamId("bad ID")
        self.assertEqual(
            "Week does not have a matchup with team ID 'bad ID'.", str(context.exception)
        )

    def test_week_fromJson(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup_1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        week = Week(weekNumber=1, matchups=[matchup_1])
        weekJson = week.toJson()
        weekDerived = Week.fromJson(weekJson)
        self.assertEqual(week, weekDerived)
        self.assertEqual(week.id, weekDerived.id)
