import unittest

from leeger.calculator.all_time_calculator.SingleScoreAllTimeCalculator import (
    SingleScoreAllTimeCalculator,
)
from leeger.enum.MatchupType import MatchupType
from leeger.model.league.League import League
from leeger.model.league.Matchup import Matchup
from leeger.model.league.Week import Week
from leeger.model.league.Year import Year
from test.helper.prototypes import getNDefaultOwnersAndTeams, getTeamsFromOwners


class TestSingleScoreAllTimeCalculator(unittest.TestCase):
    def test_getMaxScore_happyPath(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=10,
            teamBScore=11,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3.1,
            teamBScore=4.1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4.1,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(
            teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.2, teamBScore=2.2
        )
        matchup2_b = Matchup(
            teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.2, teamBScore=4.2
        )
        matchup3_b = Matchup(
            teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.2, teamBScore=6
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1.3,
            teamBScore=2.3,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3.3,
            teamBScore=4.3,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4.3,
            teamBScore=7,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SingleScoreAllTimeCalculator.getMaxScore(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(1.3, response[owners[0].id])
        self.assertEqual(2.3, response[owners[1].id])
        self.assertEqual(3.3, response[owners[2].id])
        self.assertEqual(4.3, response[owners[3].id])
        self.assertEqual(4.3, response[owners[4].id])
        self.assertEqual(7, response[owners[5].id])

    def test_getMaxScore_noneIfNoGamesPlayed(self):
        owners, teamsA = getNDefaultOwnersAndTeams(3)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=10, teamBScore=11
        )
        matchup2_a = Matchup(
            teamAId=teamsA[1].id, teamBId=teamsA[2].id, teamAScore=3.1, teamBScore=4.1
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])

        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a])

        league = League(name="TEST", owners=owners, years=[yearA])

        response = SingleScoreAllTimeCalculator.getMaxScore(league, weekNumberEnd=1)

        self.assertIsInstance(response, dict)
        self.assertEqual(3, len(response.keys()))
        self.assertEqual(10, response[owners[0].id])
        self.assertEqual(11, response[owners[1].id])
        self.assertIsNone(response[owners[2].id])

    def test_getMaxScore_onlyPostSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=10,
            teamBScore=11,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3.1,
            teamBScore=4.1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4.1,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(
            teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=10.2, teamBScore=20.2
        )
        matchup2_b = Matchup(
            teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=30.2, teamBScore=40.2
        )
        matchup3_b = Matchup(
            teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=40.2, teamBScore=60
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1.3,
            teamBScore=2.3,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3.3,
            teamBScore=4.3,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4.3,
            teamBScore=7,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SingleScoreAllTimeCalculator.getMaxScore(league, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(1.3, response[owners[0].id])
        self.assertEqual(2.3, response[owners[1].id])
        self.assertEqual(3.3, response[owners[2].id])
        self.assertEqual(4.3, response[owners[3].id])
        self.assertEqual(4.3, response[owners[4].id])
        self.assertEqual(7, response[owners[5].id])

    def test_getMaxScore_onlyRegularSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=10,
            teamBScore=11,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3.1,
            teamBScore=4.1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4.1,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(
            teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.2, teamBScore=2.2
        )
        matchup2_b = Matchup(
            teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.2, teamBScore=4.2
        )
        matchup3_b = Matchup(
            teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.2, teamBScore=6
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1.3,
            teamBScore=2.3,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3.3,
            teamBScore=4.3,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4.3,
            teamBScore=7,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SingleScoreAllTimeCalculator.getMaxScore(
            league, onlyRegularSeason=True
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(1.2, response[owners[0].id])
        self.assertEqual(2.2, response[owners[1].id])
        self.assertEqual(3.2, response[owners[2].id])
        self.assertEqual(4.2, response[owners[3].id])
        self.assertEqual(4.2, response[owners[4].id])
        self.assertEqual(6, response[owners[5].id])

    def test_getMaxScore_onlyChampionshipIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=10,
            teamBScore=11,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3.1,
            teamBScore=4.1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4.1,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(
            teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=10.2, teamBScore=20.2
        )
        matchup2_b = Matchup(
            teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=30.2, teamBScore=40.2
        )
        matchup3_b = Matchup(
            teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=40.2, teamBScore=60
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1.3,
            teamBScore=2.3,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3.3,
            teamBScore=4.3,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4.3,
            teamBScore=7,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SingleScoreAllTimeCalculator.getMaxScore(
            league, onlyChampionship=True
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertIsNone(response[owners[0].id])
        self.assertIsNone(response[owners[1].id])
        self.assertIsNone(response[owners[2].id])
        self.assertIsNone(response[owners[3].id])
        self.assertEqual(4.3, response[owners[4].id])
        self.assertEqual(7, response[owners[5].id])

    def test_getMaxScore_yearNumberStartGivenWeekNumberStartGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=10,
            teamBScore=11,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=30.1,
            teamBScore=40.1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=40.1,
            teamBScore=50,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(
            teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=10.1, teamBScore=20.2
        )
        matchup2_b = Matchup(
            teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=30.3, teamBScore=40.4
        )
        matchup3_b = Matchup(
            teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=40.4, teamBScore=50.5
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        matchup4_b = Matchup(
            teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.1, teamBScore=2.2
        )
        matchup5_b = Matchup(
            teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.3, teamBScore=4.4
        )
        matchup6_b = Matchup(
            teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.4, teamBScore=5.5
        )
        week2_b = Week(weekNumber=2, matchups=[matchup4_b, matchup5_b, matchup6_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1.3,
            teamBScore=2.3,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3.3,
            teamBScore=4.3,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4.3,
            teamBScore=7,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SingleScoreAllTimeCalculator.getMaxScore(
            league, yearNumberStart=2001, weekNumberStart=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(1.3, response[owners[0].id])
        self.assertEqual(2.3, response[owners[1].id])
        self.assertEqual(3.3, response[owners[2].id])
        self.assertEqual(4.4, response[owners[3].id])
        self.assertEqual(4.4, response[owners[4].id])
        self.assertEqual(7, response[owners[5].id])

    def test_getMaxScore_yearNumberEndGivenWeekNumberEndGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=10,
            teamBScore=11,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3.1,
            teamBScore=4.1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4.1,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(
            teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.1, teamBScore=2.2
        )
        matchup2_b = Matchup(
            teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.3, teamBScore=4.4
        )
        matchup3_b = Matchup(
            teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.4, teamBScore=5.5
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        matchup4_b = Matchup(
            teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.1, teamBScore=2.2
        )
        matchup5_b = Matchup(
            teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.3, teamBScore=4.4
        )
        matchup6_b = Matchup(
            teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.4, teamBScore=5.5
        )
        week2_b = Week(weekNumber=2, matchups=[matchup4_b, matchup5_b, matchup6_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=10.3,
            teamBScore=20.3,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=30.3,
            teamBScore=40.3,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=40.3,
            teamBScore=70,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SingleScoreAllTimeCalculator.getMaxScore(
            league, yearNumberEnd=2001, weekNumberEnd=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(1.1, response[owners[0].id])
        self.assertEqual(2.2, response[owners[1].id])
        self.assertEqual(3.3, response[owners[2].id])
        self.assertEqual(4.4, response[owners[3].id])
        self.assertEqual(4.4, response[owners[4].id])
        self.assertEqual(5.5, response[owners[5].id])

    def test_getMaxScore_yearNumberStartGivenWeekNumberStartGivenAndYearNumberEndGivenWeekNumberEndGiven(
        self,
    ):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=10,
            teamBScore=11,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3.1,
            teamBScore=4.1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4.1,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(
            teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.1, teamBScore=2.2
        )
        matchup2_b = Matchup(
            teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.3, teamBScore=4.4
        )
        matchup3_b = Matchup(
            teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.4, teamBScore=5.5
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        matchup4_b = Matchup(
            teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.1, teamBScore=2.2
        )
        matchup5_b = Matchup(
            teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.3, teamBScore=4.4
        )
        matchup6_b = Matchup(
            teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.4, teamBScore=5.5
        )
        week2_b = Week(weekNumber=2, matchups=[matchup4_b, matchup5_b, matchup6_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=10.3,
            teamBScore=20.3,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=30.3,
            teamBScore=40.3,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=40.3,
            teamBScore=70,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SingleScoreAllTimeCalculator.getMaxScore(
            league,
            yearNumberStart=2001,
            weekNumberStart=1,
            yearNumberEnd=2001,
            weekNumberEnd=2,
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(1.1, response[owners[0].id])
        self.assertEqual(2.2, response[owners[1].id])
        self.assertEqual(3.3, response[owners[2].id])
        self.assertEqual(4.4, response[owners[3].id])
        self.assertEqual(4.4, response[owners[4].id])
        self.assertEqual(5.5, response[owners[5].id])

    def test_getMinScore_happyPath(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=10,
            teamBScore=11,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3.1,
            teamBScore=4.1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4.1,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(
            teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.2, teamBScore=2.2
        )
        matchup2_b = Matchup(
            teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.2, teamBScore=4.2
        )
        matchup3_b = Matchup(
            teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.2, teamBScore=6
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1.3,
            teamBScore=2.3,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3.3,
            teamBScore=4.3,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4.3,
            teamBScore=7,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SingleScoreAllTimeCalculator.getMinScore(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(1.2, response[owners[0].id])
        self.assertEqual(2.2, response[owners[1].id])
        self.assertEqual(3.1, response[owners[2].id])
        self.assertEqual(4.1, response[owners[3].id])
        self.assertEqual(4.1, response[owners[4].id])
        self.assertEqual(5, response[owners[5].id])

    def test_getMinScore_noneIfNoGamesPlayed(self):
        owners, teamsA = getNDefaultOwnersAndTeams(3)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=10, teamBScore=11
        )
        matchup2_a = Matchup(
            teamAId=teamsA[1].id, teamBId=teamsA[2].id, teamAScore=3.1, teamBScore=4.1
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])

        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a])

        league = League(name="TEST", owners=owners, years=[yearA])

        response = SingleScoreAllTimeCalculator.getMinScore(league, weekNumberEnd=1)

        self.assertIsInstance(response, dict)
        self.assertEqual(3, len(response.keys()))
        self.assertEqual(10, response[owners[0].id])
        self.assertEqual(11, response[owners[1].id])
        self.assertIsNone(response[owners[2].id])

    def test_getMinScore_onlyPostSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=10,
            teamBScore=11,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3.1,
            teamBScore=4.1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4.1,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(
            teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=10.2, teamBScore=20.2
        )
        matchup2_b = Matchup(
            teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=30.2, teamBScore=40.2
        )
        matchup3_b = Matchup(
            teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=40.2, teamBScore=60
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1.3,
            teamBScore=2.3,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3.3,
            teamBScore=4.3,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4.3,
            teamBScore=7,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SingleScoreAllTimeCalculator.getMinScore(league, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(1.3, response[owners[0].id])
        self.assertEqual(2.3, response[owners[1].id])
        self.assertEqual(3.1, response[owners[2].id])
        self.assertEqual(4.1, response[owners[3].id])
        self.assertEqual(4.1, response[owners[4].id])
        self.assertEqual(5, response[owners[5].id])

    def test_getMinScore_onlyRegularSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=10,
            teamBScore=11,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3.1,
            teamBScore=4.1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4.1,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(
            teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.2, teamBScore=2.2
        )
        matchup2_b = Matchup(
            teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.2, teamBScore=4.2
        )
        matchup3_b = Matchup(
            teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.2, teamBScore=6
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1.1,
            teamBScore=2.1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3.3,
            teamBScore=4.3,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4.3,
            teamBScore=7,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SingleScoreAllTimeCalculator.getMinScore(
            league, onlyRegularSeason=True
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(1.2, response[owners[0].id])
        self.assertEqual(2.2, response[owners[1].id])
        self.assertEqual(3.2, response[owners[2].id])
        self.assertEqual(4.2, response[owners[3].id])
        self.assertEqual(4.2, response[owners[4].id])
        self.assertEqual(6, response[owners[5].id])

    def test_getMinScore_onlyChampionshipIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=10,
            teamBScore=11,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3.1,
            teamBScore=4.1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4.1,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(
            teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=10.2, teamBScore=20.2
        )
        matchup2_b = Matchup(
            teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=30.2, teamBScore=40.2
        )
        matchup3_b = Matchup(
            teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=40.2, teamBScore=60
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1.3,
            teamBScore=2.3,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3.3,
            teamBScore=4.3,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4.3,
            teamBScore=7,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SingleScoreAllTimeCalculator.getMinScore(
            league, onlyChampionship=True
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertIsNone(response[owners[0].id])
        self.assertIsNone(response[owners[1].id])
        self.assertIsNone(response[owners[2].id])
        self.assertIsNone(response[owners[3].id])
        self.assertEqual(4.1, response[owners[4].id])
        self.assertEqual(5, response[owners[5].id])

    def test_getMinScore_yearNumberStartGivenWeekNumberStartGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=10,
            teamBScore=11,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=30.1,
            teamBScore=40.1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=40.1,
            teamBScore=50,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(
            teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=10.1, teamBScore=20.2
        )
        matchup2_b = Matchup(
            teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=30.3, teamBScore=40.4
        )
        matchup3_b = Matchup(
            teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=40.4, teamBScore=50.5
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        matchup4_b = Matchup(
            teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.1, teamBScore=2.2
        )
        matchup5_b = Matchup(
            teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.3, teamBScore=4.4
        )
        matchup6_b = Matchup(
            teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.4, teamBScore=5
        )
        week2_b = Week(weekNumber=2, matchups=[matchup4_b, matchup5_b, matchup6_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1.3,
            teamBScore=2.3,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3.3,
            teamBScore=4.3,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4.3,
            teamBScore=7,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SingleScoreAllTimeCalculator.getMinScore(
            league, yearNumberStart=2001, weekNumberStart=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(1.1, response[owners[0].id])
        self.assertEqual(2.2, response[owners[1].id])
        self.assertEqual(3.3, response[owners[2].id])
        self.assertEqual(4.3, response[owners[3].id])
        self.assertEqual(4.3, response[owners[4].id])
        self.assertEqual(5, response[owners[5].id])

    def test_getMinScore_yearNumberEndGivenWeekNumberEndGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=10,
            teamBScore=11,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3.1,
            teamBScore=4.1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4.1,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(
            teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=10.1, teamBScore=20.2
        )
        matchup2_b = Matchup(
            teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=30.3, teamBScore=40.4
        )
        matchup3_b = Matchup(
            teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=40.4, teamBScore=50.5
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        matchup4_b = Matchup(
            teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.1, teamBScore=2.2
        )
        matchup5_b = Matchup(
            teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.3, teamBScore=4.4
        )
        matchup6_b = Matchup(
            teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.4, teamBScore=5
        )
        week2_b = Week(weekNumber=2, matchups=[matchup4_b, matchup5_b, matchup6_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=10.3,
            teamBScore=20.3,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=30.3,
            teamBScore=40.3,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=40.3,
            teamBScore=70,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SingleScoreAllTimeCalculator.getMinScore(
            league, yearNumberEnd=2001, weekNumberEnd=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(1.1, response[owners[0].id])
        self.assertEqual(2.2, response[owners[1].id])
        self.assertEqual(3.1, response[owners[2].id])
        self.assertEqual(4.1, response[owners[3].id])
        self.assertEqual(4.1, response[owners[4].id])
        self.assertEqual(5, response[owners[5].id])

    def test_getMinScore_yearNumberStartGivenWeekNumberStartGivenAndYearNumberEndGivenWeekNumberEndGiven(
        self,
    ):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=10,
            teamBScore=11,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3.1,
            teamBScore=4.1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4.1,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(
            teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=10.1, teamBScore=20.2
        )
        matchup2_b = Matchup(
            teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=30.3, teamBScore=40.4
        )
        matchup3_b = Matchup(
            teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=40.4, teamBScore=50
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        matchup4_b = Matchup(
            teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.1, teamBScore=2.2
        )
        matchup5_b = Matchup(
            teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.3, teamBScore=4.4
        )
        matchup6_b = Matchup(
            teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.4, teamBScore=5
        )
        week2_b = Week(weekNumber=2, matchups=[matchup4_b, matchup5_b, matchup6_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=10.3,
            teamBScore=20.3,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=30.3,
            teamBScore=40.3,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=40.3,
            teamBScore=70,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SingleScoreAllTimeCalculator.getMinScore(
            league,
            yearNumberStart=2001,
            weekNumberStart=1,
            yearNumberEnd=2001,
            weekNumberEnd=2,
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(1.1, response[owners[0].id])
        self.assertEqual(2.2, response[owners[1].id])
        self.assertEqual(3.3, response[owners[2].id])
        self.assertEqual(4.4, response[owners[3].id])
        self.assertEqual(4.4, response[owners[4].id])
        self.assertEqual(5, response[owners[5].id])
