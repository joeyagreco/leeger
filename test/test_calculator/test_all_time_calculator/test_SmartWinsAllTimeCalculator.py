import math
import unittest
from test.helper.prototypes import getNDefaultOwnersAndTeams, getTeamsFromOwners

from leeger.calculator.all_time_calculator.SmartWinsAllTimeCalculator import (
    SmartWinsAllTimeCalculator,
)
from leeger.enum.MatchupType import MatchupType
from leeger.model.league.League import League
from leeger.model.league.Matchup import Matchup
from leeger.model.league.Week import Week
from leeger.model.league.Year import Year
from leeger.util.Deci import Deci


class TestSmartWinsAllTimeCalculator(unittest.TestCase):
    def test_getSmartWins_happyPath(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3, teamBScore=4)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4, teamBScore=5)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3, teamBScore=4)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4, teamBScore=5)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SmartWinsAllTimeCalculator.getSmartWins(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.06666666666666666666666666666"), response[owners[0].id])
        self.assertEqual(Deci("0.3333333333333333333333333334"), response[owners[1].id])
        self.assertEqual(Deci("0.9999999999999999999999999999"), response[owners[2].id])
        self.assertEqual(Deci("1.9"), response[owners[3].id])
        self.assertEqual(Deci("1.9"), response[owners[4].id])
        self.assertEqual(Deci("2.8"), response[owners[5].id])

    def test_getSmartWins_multiWeekMatchups(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            multiWeekMatchupId="1",
        )
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3, teamBScore=4)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4, teamBScore=5)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])

        matchup4_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            multiWeekMatchupId="1",
        )
        matchup5_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3, teamBScore=4)
        matchup6_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4, teamBScore=5)
        week2_a = Week(weekNumber=2, matchups=[matchup4_a, matchup5_a, matchup6_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        league = League(name="TEST", owners=owners, years=[yearA, yearB])

        response = SmartWinsAllTimeCalculator.getSmartWins(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.1"), response[owners[0].id])
        self.assertEqual(Deci("0.7"), response[owners[1].id])
        self.assertTrue(math.isclose(Deci("0.8"), response[owners[2].id]))
        self.assertEqual(Deci("1.8"), response[owners[3].id])
        self.assertEqual(Deci("1.8"), response[owners[4].id])
        self.assertEqual(Deci("2.8"), response[owners[5].id])

    def test_getSmartWins_noneIfNoGamesPlayed(self):
        owners, teamsA = getNDefaultOwnersAndTeams(3)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[1].id, teamBId=teamsA[2].id, teamAScore=3, teamBScore=4)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a])

        league = League(name="TEST", owners=owners, years=[yearA])

        response = SmartWinsAllTimeCalculator.getSmartWins(league, weekNumberEnd=1)

        self.assertIsInstance(response, dict)
        self.assertEqual(3, len(response.keys()))
        self.assertEqual(Deci("0"), response[owners[0].id])
        self.assertEqual(Deci("0.3333333333333333333333333333"), response[owners[1].id])
        self.assertIsNone(response[owners[2].id])

    def test_getSmartWins_onlyPostSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SmartWinsAllTimeCalculator.getSmartWins(league, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.03333333333333333333333333333"), response[owners[0].id])
        self.assertEqual(Deci("0.1666666666666666666666666667"), response[owners[1].id])
        self.assertEqual(Deci("0.6666666666666666666666666666"), response[owners[2].id])
        self.assertEqual(Deci("1.266666666666666666666666667"), response[owners[3].id])
        self.assertEqual(Deci("1.266666666666666666666666667"), response[owners[4].id])
        self.assertEqual(Deci("1.866666666666666666666666667"), response[owners[5].id])

    def test_getSmartWins_onlyRegularSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SmartWinsAllTimeCalculator.getSmartWins(league, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.03333333333333333333333333333"), response[owners[0].id])
        self.assertEqual(Deci("0.1666666666666666666666666667"), response[owners[1].id])
        self.assertEqual(Deci("0.3333333333333333333333333333"), response[owners[2].id])
        self.assertEqual(Deci("0.6333333333333333333333333333"), response[owners[3].id])
        self.assertEqual(Deci("0.6333333333333333333333333333"), response[owners[4].id])
        self.assertEqual(Deci("0.9333333333333333333333333333"), response[owners[5].id])

    def test_getSmartWins_onlyChampionshipIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SmartWinsAllTimeCalculator.getSmartWins(league, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertIsNone(response[owners[0].id])
        self.assertIsNone(response[owners[1].id])
        self.assertIsNone(response[owners[2].id])
        self.assertIsNone(response[owners[3].id])
        self.assertEqual(Deci("1.266666666666666666666666667"), response[owners[4].id])
        self.assertEqual(Deci("1.866666666666666666666666667"), response[owners[5].id])

    def test_getSmartWins_yearNumberStartGivenWeekNumberStartGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        matchup4_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup5_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup6_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week2_b = Week(weekNumber=2, matchups=[matchup4_b, matchup5_b, matchup6_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SmartWinsAllTimeCalculator.getSmartWins(
            league, yearNumberStart=2001, weekNumberStart=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.09523809523809523809523809524"), response[owners[0].id])
        self.assertEqual(Deci("0.3809523809523809523809523810"), response[owners[1].id])
        self.assertEqual(Deci("0.7142857142857142857142857142"), response[owners[2].id])
        self.assertEqual(Deci("1.285714285714285714285714286"), response[owners[3].id])
        self.assertEqual(Deci("1.285714285714285714285714286"), response[owners[4].id])
        self.assertEqual(Deci("1.857142857142857142857142857"), response[owners[5].id])

    def test_getSmartWins_yearNumberEndGivenWeekNumberEndGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        matchup4_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup5_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup6_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week2_b = Week(weekNumber=2, matchups=[matchup4_b, matchup5_b, matchup6_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SmartWinsAllTimeCalculator.getSmartWins(
            league, yearNumberEnd=2001, weekNumberEnd=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.09523809523809523809523809524"), response[owners[0].id])
        self.assertEqual(Deci("0.3809523809523809523809523810"), response[owners[1].id])
        self.assertEqual(Deci("1.071428571428571428571428571"), response[owners[2].id])
        self.assertEqual(Deci("1.928571428571428571428571429"), response[owners[3].id])
        self.assertEqual(Deci("1.928571428571428571428571429"), response[owners[4].id])
        self.assertEqual(Deci("2.785714285714285714285714286"), response[owners[5].id])

    def test_getSmartWins_yearNumberStartGivenWeekNumberStartGivenAndYearNumberEndGivenWeekNumberEndGiven(
        self,
    ):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        matchup4_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup5_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup6_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week2_b = Week(weekNumber=2, matchups=[matchup4_b, matchup5_b, matchup6_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SmartWinsAllTimeCalculator.getSmartWins(
            league, yearNumberStart=2001, weekNumberStart=1, yearNumberEnd=2001, weekNumberEnd=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.09523809523809523809523809524"), response[owners[0].id])
        self.assertEqual(Deci("0.3809523809523809523809523810"), response[owners[1].id])
        self.assertEqual(Deci("0.7142857142857142857142857142"), response[owners[2].id])
        self.assertEqual(Deci("1.285714285714285714285714286"), response[owners[3].id])
        self.assertEqual(Deci("1.285714285714285714285714286"), response[owners[4].id])
        self.assertEqual(Deci("1.857142857142857142857142857"), response[owners[5].id])

    def test_getSmartWinsPerGame_happyPath(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3, teamBScore=4)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4, teamBScore=5)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3, teamBScore=4)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4, teamBScore=5)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SmartWinsAllTimeCalculator.getSmartWinsPerGame(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.03333333333333333333333333333"), response[owners[0].id])
        self.assertEqual(Deci("0.1666666666666666666666666667"), response[owners[1].id])
        self.assertEqual(Deci("0.3333333333333333333333333333"), response[owners[2].id])
        self.assertEqual(Deci("0.6333333333333333333333333333"), response[owners[3].id])
        self.assertEqual(Deci("0.6333333333333333333333333333"), response[owners[4].id])
        self.assertEqual(Deci("0.9333333333333333333333333333"), response[owners[5].id])

    def test_getSmartWinsPerGame_multiWeekMatchups(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            multiWeekMatchupId="1",
        )
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3, teamBScore=4)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4, teamBScore=5)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])

        matchup4_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            multiWeekMatchupId="1",
        )
        matchup5_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3, teamBScore=4)
        matchup6_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4, teamBScore=5)
        week2_a = Week(weekNumber=2, matchups=[matchup4_a, matchup5_a, matchup6_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        league = League(name="TEST", owners=owners, years=[yearA, yearB])

        response = SmartWinsAllTimeCalculator.getSmartWinsPerGame(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.05"), response[owners[0].id])
        self.assertEqual(Deci("0.35"), response[owners[1].id])
        self.assertEqual(Deci("0.2666666666666666666666666667"), response[owners[2].id])
        self.assertEqual(Deci("0.6"), response[owners[3].id])
        self.assertEqual(Deci("0.6"), response[owners[4].id])
        self.assertEqual(Deci("0.9333333333333333333333333333"), response[owners[5].id])

    def test_getSmartWinsPerGame_noneIfNoGamesPlayed(self):
        owners, teamsA = getNDefaultOwnersAndTeams(3)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[1].id, teamBId=teamsA[2].id, teamAScore=3, teamBScore=4)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a])

        league = League(name="TEST", owners=owners, years=[yearA])

        response = SmartWinsAllTimeCalculator.getSmartWinsPerGame(league, weekNumberEnd=1)

        self.assertIsInstance(response, dict)
        self.assertEqual(3, len(response.keys()))
        self.assertEqual(Deci("0"), response[owners[0].id])
        self.assertEqual(Deci("0.3333333333333333333333333333"), response[owners[1].id])
        self.assertIsNone(response[owners[2].id])

    def test_getSmartWinsPerGame_onlyPostSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SmartWinsAllTimeCalculator.getSmartWinsPerGame(league, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.03333333333333333333333333333"), response[owners[0].id])
        self.assertEqual(Deci("0.1666666666666666666666666667"), response[owners[1].id])
        self.assertEqual(Deci("0.3333333333333333333333333333"), response[owners[2].id])
        self.assertEqual(Deci("0.6333333333333333333333333335"), response[owners[3].id])
        self.assertEqual(Deci("0.6333333333333333333333333335"), response[owners[4].id])
        self.assertEqual(Deci("0.9333333333333333333333333335"), response[owners[5].id])

    def test_getSmartWinsPerGame_onlyRegularSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SmartWinsAllTimeCalculator.getSmartWinsPerGame(league, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.03333333333333333333333333333"), response[owners[0].id])
        self.assertEqual(Deci("0.1666666666666666666666666667"), response[owners[1].id])
        self.assertEqual(Deci("0.3333333333333333333333333333"), response[owners[2].id])
        self.assertEqual(Deci("0.6333333333333333333333333333"), response[owners[3].id])
        self.assertEqual(Deci("0.6333333333333333333333333333"), response[owners[4].id])
        self.assertEqual(Deci("0.9333333333333333333333333333"), response[owners[5].id])

    def test_getSmartWinsPerGame_onlyChampionshipIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SmartWinsAllTimeCalculator.getSmartWinsPerGame(league, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertIsNone(response[owners[0].id])
        self.assertIsNone(response[owners[1].id])
        self.assertIsNone(response[owners[2].id])
        self.assertIsNone(response[owners[3].id])
        self.assertEqual(Deci("0.6333333333333333333333333335"), response[owners[4].id])
        self.assertEqual(Deci("0.9333333333333333333333333335"), response[owners[5].id])

    def test_getSmartWinsPerGame_yearNumberStartGivenWeekNumberStartGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        matchup4_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup5_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup6_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week2_b = Week(weekNumber=2, matchups=[matchup4_b, matchup5_b, matchup6_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SmartWinsAllTimeCalculator.getSmartWinsPerGame(
            league, yearNumberStart=2001, weekNumberStart=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.04761904761904761904761904762"), response[owners[0].id])
        self.assertEqual(Deci("0.1904761904761904761904761905"), response[owners[1].id])
        self.assertEqual(Deci("0.3571428571428571428571428571"), response[owners[2].id])
        self.assertEqual(Deci("0.642857142857142857142857143"), response[owners[3].id])
        self.assertEqual(Deci("0.642857142857142857142857143"), response[owners[4].id])
        self.assertEqual(Deci("0.9285714285714285714285714285"), response[owners[5].id])

    def test_getSmartWinsPerGame_yearNumberEndGivenWeekNumberEndGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        matchup4_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup5_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup6_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week2_b = Week(weekNumber=2, matchups=[matchup4_b, matchup5_b, matchup6_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SmartWinsAllTimeCalculator.getSmartWinsPerGame(
            league, yearNumberEnd=2001, weekNumberEnd=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.04761904761904761904761904762"), response[owners[0].id])
        self.assertEqual(Deci("0.1904761904761904761904761905"), response[owners[1].id])
        self.assertEqual(Deci("0.357142857142857142857142857"), response[owners[2].id])
        self.assertEqual(Deci("0.642857142857142857142857143"), response[owners[3].id])
        self.assertEqual(Deci("0.642857142857142857142857143"), response[owners[4].id])
        self.assertEqual(Deci("0.9285714285714285714285714287"), response[owners[5].id])

    def test_getSmartWinsPerGame_yearNumberStartGivenWeekNumberStartGivenAndYearNumberEndGivenWeekNumberEndGiven(
        self,
    ):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        matchup4_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup5_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup6_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week2_b = Week(weekNumber=2, matchups=[matchup4_b, matchup5_b, matchup6_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SmartWinsAllTimeCalculator.getSmartWinsPerGame(
            league, yearNumberStart=2001, weekNumberStart=1, yearNumberEnd=2001, weekNumberEnd=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.04761904761904761904761904762"), response[owners[0].id])
        self.assertEqual(Deci("0.1904761904761904761904761905"), response[owners[1].id])
        self.assertEqual(Deci("0.3571428571428571428571428571"), response[owners[2].id])
        self.assertEqual(Deci("0.642857142857142857142857143"), response[owners[3].id])
        self.assertEqual(Deci("0.642857142857142857142857143"), response[owners[4].id])
        self.assertEqual(Deci("0.9285714285714285714285714285"), response[owners[5].id])

    def test_getOpponentSmartWins_happyPath(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3, teamBScore=4)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4, teamBScore=5)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3, teamBScore=4)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4, teamBScore=5)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SmartWinsAllTimeCalculator.getOpponentSmartWins(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.3333333333333333333333333334"), response[owners[0].id])
        self.assertEqual(Deci("0.06666666666666666666666666666"), response[owners[1].id])
        self.assertEqual(Deci("1.9"), response[owners[2].id])
        self.assertEqual(Deci("0.9999999999999999999999999999"), response[owners[3].id])
        self.assertEqual(Deci("2.8"), response[owners[4].id])
        self.assertEqual(Deci("1.9"), response[owners[5].id])

    def test_getOpponentSmartWins_multiWeekMatchups(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            multiWeekMatchupId="1",
        )
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3, teamBScore=4)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4, teamBScore=5)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])

        matchup4_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            multiWeekMatchupId="1",
        )
        matchup5_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3, teamBScore=4)
        matchup6_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4, teamBScore=5)
        week2_a = Week(weekNumber=2, matchups=[matchup4_a, matchup5_a, matchup6_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        league = League(name="TEST", owners=owners, years=[yearA, yearB])

        response = SmartWinsAllTimeCalculator.getOpponentSmartWins(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.7"), response[owners[0].id])
        self.assertEqual(Deci("0.1"), response[owners[1].id])
        self.assertEqual(Deci("1.8"), response[owners[2].id])
        self.assertTrue(math.isclose(Deci("0.8"), response[owners[3].id]))
        self.assertEqual(Deci("2.8"), response[owners[4].id])
        self.assertEqual(Deci("1.8"), response[owners[5].id])

    def test_getOpponentSmartWins_noneIfNoGamesPlayed(self):
        owners, teamsA = getNDefaultOwnersAndTeams(3)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[1].id, teamBId=teamsA[2].id, teamAScore=3, teamBScore=4)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a])

        league = League(name="TEST", owners=owners, years=[yearA])

        response = SmartWinsAllTimeCalculator.getOpponentSmartWins(league, weekNumberEnd=1)

        self.assertIsInstance(response, dict)
        self.assertEqual(3, len(response.keys()))
        self.assertEqual(Deci("0.3333333333333333333333333333"), response[owners[0].id])
        self.assertEqual(Deci("0"), response[owners[1].id])
        self.assertIsNone(response[owners[2].id])

    def test_getOpponentSmartWins_onlyPostSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SmartWinsAllTimeCalculator.getOpponentSmartWins(league, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.1666666666666666666666666667"), response[owners[0].id])
        self.assertEqual(Deci("0.03333333333333333333333333333"), response[owners[1].id])
        self.assertEqual(Deci("1.266666666666666666666666667"), response[owners[2].id])
        self.assertEqual(Deci("0.6666666666666666666666666666"), response[owners[3].id])
        self.assertEqual(Deci("1.866666666666666666666666667"), response[owners[4].id])
        self.assertEqual(Deci("1.266666666666666666666666667"), response[owners[5].id])

    def test_getOpponentSmartWins_onlyRegularSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SmartWinsAllTimeCalculator.getOpponentSmartWins(league, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.1666666666666666666666666667"), response[owners[0].id])
        self.assertEqual(Deci("0.03333333333333333333333333333"), response[owners[1].id])
        self.assertEqual(Deci("0.6333333333333333333333333333"), response[owners[2].id])
        self.assertEqual(Deci("0.3333333333333333333333333333"), response[owners[3].id])
        self.assertEqual(Deci("0.9333333333333333333333333333"), response[owners[4].id])
        self.assertEqual(Deci("0.6333333333333333333333333333"), response[owners[5].id])

    def test_getOpponentSmartWins_onlyChampionshipIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SmartWinsAllTimeCalculator.getOpponentSmartWins(league, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertIsNone(response[owners[0].id])
        self.assertIsNone(response[owners[1].id])
        self.assertIsNone(response[owners[2].id])
        self.assertIsNone(response[owners[3].id])
        self.assertEqual(Deci("1.866666666666666666666666667"), response[owners[4].id])
        self.assertEqual(Deci("1.266666666666666666666666667"), response[owners[5].id])

    def test_getOpponentSmartWins_yearNumberStartGivenWeekNumberStartGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        matchup4_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup5_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup6_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week2_b = Week(weekNumber=2, matchups=[matchup4_b, matchup5_b, matchup6_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SmartWinsAllTimeCalculator.getOpponentSmartWins(
            league, yearNumberStart=2001, weekNumberStart=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.3809523809523809523809523810"), response[owners[0].id])
        self.assertEqual(Deci("0.09523809523809523809523809524"), response[owners[1].id])
        self.assertEqual(Deci("1.285714285714285714285714286"), response[owners[2].id])
        self.assertEqual(Deci("0.7142857142857142857142857142"), response[owners[3].id])
        self.assertEqual(Deci("1.857142857142857142857142857"), response[owners[4].id])
        self.assertEqual(Deci("1.285714285714285714285714286"), response[owners[5].id])

    def test_getOpponentSmartWins_yearNumberEndGivenWeekNumberEndGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        matchup4_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup5_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup6_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week2_b = Week(weekNumber=2, matchups=[matchup4_b, matchup5_b, matchup6_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SmartWinsAllTimeCalculator.getOpponentSmartWins(
            league, yearNumberEnd=2001, weekNumberEnd=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.3809523809523809523809523810"), response[owners[0].id])
        self.assertEqual(Deci("0.09523809523809523809523809524"), response[owners[1].id])
        self.assertEqual(Deci("1.928571428571428571428571429"), response[owners[2].id])
        self.assertEqual(Deci("1.071428571428571428571428571"), response[owners[3].id])
        self.assertEqual(Deci("2.785714285714285714285714286"), response[owners[4].id])
        self.assertEqual(Deci("1.928571428571428571428571429"), response[owners[5].id])

    def test_getOpponentSmartWins_yearNumberStartGivenWeekNumberStartGivenAndYearNumberEndGivenWeekNumberEndGiven(
        self,
    ):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        matchup4_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup5_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup6_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week2_b = Week(weekNumber=2, matchups=[matchup4_b, matchup5_b, matchup6_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SmartWinsAllTimeCalculator.getOpponentSmartWins(
            league, yearNumberStart=2001, weekNumberStart=1, yearNumberEnd=2001, weekNumberEnd=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.3809523809523809523809523810"), response[owners[0].id])
        self.assertEqual(Deci("0.09523809523809523809523809524"), response[owners[1].id])
        self.assertEqual(Deci("1.285714285714285714285714286"), response[owners[2].id])
        self.assertEqual(Deci("0.7142857142857142857142857142"), response[owners[3].id])
        self.assertEqual(Deci("1.857142857142857142857142857"), response[owners[4].id])
        self.assertEqual(Deci("1.285714285714285714285714286"), response[owners[5].id])

    def test_getOpponentSmartWinsPerGame_happyPath(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3, teamBScore=4)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4, teamBScore=5)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3, teamBScore=4)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4, teamBScore=5)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SmartWinsAllTimeCalculator.getOpponentSmartWinsPerGame(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.1666666666666666666666666667"), response[owners[0].id])
        self.assertEqual(Deci("0.03333333333333333333333333333"), response[owners[1].id])
        self.assertEqual(Deci("0.6333333333333333333333333333"), response[owners[2].id])
        self.assertEqual(Deci("0.3333333333333333333333333333"), response[owners[3].id])
        self.assertEqual(Deci("0.9333333333333333333333333333"), response[owners[4].id])
        self.assertEqual(Deci("0.6333333333333333333333333333"), response[owners[5].id])

    def test_getOpponentSmartWinsPerGame_multiWeekMatchups(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            multiWeekMatchupId="1",
        )
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3, teamBScore=4)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4, teamBScore=5)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])

        matchup4_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            multiWeekMatchupId="1",
        )
        matchup5_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3, teamBScore=4)
        matchup6_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4, teamBScore=5)
        week2_a = Week(weekNumber=2, matchups=[matchup4_a, matchup5_a, matchup6_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        league = League(name="TEST", owners=owners, years=[yearA, yearB])

        response = SmartWinsAllTimeCalculator.getOpponentSmartWinsPerGame(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.35"), response[owners[0].id])
        self.assertEqual(Deci("0.05"), response[owners[1].id])
        self.assertEqual(Deci("0.6"), response[owners[2].id])
        self.assertEqual(Deci("0.2666666666666666666666666667"), response[owners[3].id])
        self.assertEqual(Deci("0.9333333333333333333333333333"), response[owners[4].id])
        self.assertEqual(Deci("0.6"), response[owners[5].id])

    def test_getOpponentSmartWinsPerGame_noneIfNoGamesPlayed(self):
        owners, teamsA = getNDefaultOwnersAndTeams(3)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[1].id, teamBId=teamsA[2].id, teamAScore=3, teamBScore=4)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a])

        league = League(name="TEST", owners=owners, years=[yearA])

        response = SmartWinsAllTimeCalculator.getOpponentSmartWinsPerGame(league, weekNumberEnd=1)

        self.assertIsInstance(response, dict)
        self.assertEqual(3, len(response.keys()))
        self.assertEqual(Deci("0.3333333333333333333333333333"), response[owners[0].id])
        self.assertEqual(Deci("0"), response[owners[1].id])
        self.assertIsNone(response[owners[2].id])

    def test_getOpponentSmartWinsPerGame_onlyPostSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SmartWinsAllTimeCalculator.getOpponentSmartWinsPerGame(
            league, onlyPostSeason=True
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.1666666666666666666666666667"), response[owners[0].id])
        self.assertEqual(Deci("0.03333333333333333333333333333"), response[owners[1].id])
        self.assertEqual(Deci("0.6333333333333333333333333335"), response[owners[2].id])
        self.assertEqual(Deci("0.3333333333333333333333333333"), response[owners[3].id])
        self.assertEqual(Deci("0.9333333333333333333333333335"), response[owners[4].id])
        self.assertEqual(Deci("0.6333333333333333333333333335"), response[owners[5].id])

    def test_getOpponentSmartWinsPerGame_onlyRegularSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SmartWinsAllTimeCalculator.getOpponentSmartWinsPerGame(
            league, onlyRegularSeason=True
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.1666666666666666666666666667"), response[owners[0].id])
        self.assertEqual(Deci("0.03333333333333333333333333333"), response[owners[1].id])
        self.assertEqual(Deci("0.6333333333333333333333333333"), response[owners[2].id])
        self.assertEqual(Deci("0.3333333333333333333333333333"), response[owners[3].id])
        self.assertEqual(Deci("0.9333333333333333333333333333"), response[owners[4].id])
        self.assertEqual(Deci("0.6333333333333333333333333333"), response[owners[5].id])

    def test_getOpponentSmartWinsPerGame_onlyChampionshipIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SmartWinsAllTimeCalculator.getOpponentSmartWinsPerGame(
            league, onlyChampionship=True
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertIsNone(response[owners[0].id])
        self.assertIsNone(response[owners[1].id])
        self.assertIsNone(response[owners[2].id])
        self.assertIsNone(response[owners[3].id])
        self.assertEqual(Deci("0.9333333333333333333333333335"), response[owners[4].id])
        self.assertEqual(Deci("0.6333333333333333333333333335"), response[owners[5].id])

    def test_getOpponentSmartWinsPerGame_yearNumberStartGivenWeekNumberStartGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        matchup4_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup5_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup6_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week2_b = Week(weekNumber=2, matchups=[matchup4_b, matchup5_b, matchup6_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SmartWinsAllTimeCalculator.getOpponentSmartWinsPerGame(
            league, yearNumberStart=2001, weekNumberStart=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.1904761904761904761904761905"), response[owners[0].id])
        self.assertEqual(Deci("0.04761904761904761904761904762"), response[owners[1].id])
        self.assertEqual(Deci("0.642857142857142857142857143"), response[owners[2].id])
        self.assertEqual(Deci("0.3571428571428571428571428571"), response[owners[3].id])
        self.assertEqual(Deci("0.9285714285714285714285714285"), response[owners[4].id])
        self.assertEqual(Deci("0.642857142857142857142857143"), response[owners[5].id])

    def test_getOpponentSmartWinsPerGame_yearNumberEndGivenWeekNumberEndGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        matchup4_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup5_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup6_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week2_b = Week(weekNumber=2, matchups=[matchup4_b, matchup5_b, matchup6_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SmartWinsAllTimeCalculator.getOpponentSmartWinsPerGame(
            league, yearNumberEnd=2001, weekNumberEnd=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.1904761904761904761904761905"), response[owners[0].id])
        self.assertEqual(Deci("0.04761904761904761904761904762"), response[owners[1].id])
        self.assertEqual(Deci("0.642857142857142857142857143"), response[owners[2].id])
        self.assertEqual(Deci("0.357142857142857142857142857"), response[owners[3].id])
        self.assertEqual(Deci("0.9285714285714285714285714287"), response[owners[4].id])
        self.assertEqual(Deci("0.642857142857142857142857143"), response[owners[5].id])

    def test_getOpponentSmartWinsPerGame_yearNumberStartGivenWeekNumberStartGivenAndYearNumberEndGivenWeekNumberEndGiven(
        self,
    ):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        matchup4_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup5_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup6_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week2_b = Week(weekNumber=2, matchups=[matchup4_b, matchup5_b, matchup6_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SmartWinsAllTimeCalculator.getOpponentSmartWinsPerGame(
            league, yearNumberStart=2001, weekNumberStart=1, yearNumberEnd=2001, weekNumberEnd=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.1904761904761904761904761905"), response[owners[0].id])
        self.assertEqual(Deci("0.04761904761904761904761904762"), response[owners[1].id])
        self.assertEqual(Deci("0.642857142857142857142857143"), response[owners[2].id])
        self.assertEqual(Deci("0.3571428571428571428571428571"), response[owners[3].id])
        self.assertEqual(Deci("0.9285714285714285714285714285"), response[owners[4].id])
        self.assertEqual(Deci("0.642857142857142857142857143"), response[owners[5].id])
