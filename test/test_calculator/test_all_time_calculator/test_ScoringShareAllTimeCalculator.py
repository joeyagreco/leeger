import math
import unittest
from test.helper.prototypes import getNDefaultOwnersAndTeams, getTeamsFromOwners

from leeger.calculator.all_time_calculator.ScoringShareAllTimeCalculator import (
    ScoringShareAllTimeCalculator,
)
from leeger.enum.MatchupType import MatchupType
from leeger.model.league.League import League
from leeger.model.league.Matchup import Matchup
from leeger.model.league.Week import Week
from leeger.model.league.Year import Year
from leeger.util.Deci import Deci


class TestScoringShareAllTimeCalculator(unittest.TestCase):
    def test_getScoringShare_happyPath(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3.3,
            teamBScore=4.4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4.4,
            teamBScore=5.5,
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
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3.3,
            teamBScore=4.4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4.4,
            teamBScore=5.5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getScoringShare(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("100"), sum(response.values()))
        self.assertEqual(Deci("3.703703703703703703703703704"), response[owners[0].id])
        self.assertEqual(Deci("7.407407407407407407407407407"), response[owners[1].id])
        self.assertEqual(Deci("16.66666666666666666666666667"), response[owners[2].id])
        self.assertEqual(Deci("22.22222222222222222222222222"), response[owners[3].id])
        self.assertEqual(Deci("22.22222222222222222222222222"), response[owners[4].id])
        self.assertEqual(Deci("27.77777777777777777777777778"), response[owners[5].id])

    def test_getScoringShare_nonAnnualOwner(self):
        ownersA, teamsA = getNDefaultOwnersAndTeams(6, randomNames=True)
        ownersB, teamsB = getNDefaultOwnersAndTeams(6, randomNames=True)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1.1, teamBScore=2.2
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3.3, teamBScore=4.4
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4.4, teamBScore=5.5
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
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        league = League(name="TEST", owners=ownersA + ownersB, years=[yearA, yearB])

        response = ScoringShareAllTimeCalculator.getScoringShare(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(12, len(response.keys()))
        self.assertEqual(Deci("100"), sum(response.values()))
        self.assertEqual(Deci("2.631578947368421052631578947"), response[ownersA[0].id])
        self.assertEqual(Deci("2.631578947368421052631578947"), response[ownersB[0].id])
        self.assertEqual(Deci("5.263157894736842105263157895"), response[ownersA[1].id])
        self.assertEqual(Deci("5.263157894736842105263157895"), response[ownersB[1].id])
        self.assertEqual(Deci("7.894736842105263157894736842"), response[ownersA[2].id])
        self.assertEqual(Deci("7.894736842105263157894736842"), response[ownersB[2].id])
        self.assertEqual(Deci("10.52631578947368421052631579"), response[ownersA[3].id])
        self.assertEqual(Deci("10.52631578947368421052631579"), response[ownersB[3].id])
        self.assertEqual(Deci("10.52631578947368421052631579"), response[ownersA[4].id])
        self.assertEqual(Deci("10.52631578947368421052631579"), response[ownersB[4].id])
        self.assertEqual(Deci("13.15789473684210526315789474"), response[ownersA[5].id])
        self.assertEqual(Deci("13.15789473684210526315789474"), response[ownersB[5].id])

    def test_getScoringShare_noneIfNoGamesPlayed(self):
        owners, teamsA = getNDefaultOwnersAndTeams(3)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1.1, teamBScore=2.2
        )
        matchup2_a = Matchup(
            teamAId=teamsA[1].id, teamBId=teamsA[2].id, teamAScore=3.3, teamBScore=4.4
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])

        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a])

        league = League(name="TEST", owners=owners, years=[yearA])

        response = ScoringShareAllTimeCalculator.getScoringShare(league, weekNumberEnd=1)

        self.assertIsInstance(response, dict)
        self.assertEqual(3, len(response.keys()))
        self.assertEqual(Deci("100"), sum(filter(None, response.values())))
        self.assertEqual(Deci("33.33333333333333333333333333"), response[owners[0].id])
        self.assertEqual(Deci("66.66666666666666666666666667"), response[owners[1].id])
        self.assertIsNone(response[owners[2].id])

    def test_getScoringShare_noPointsScoredInYears(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=0,
            teamBScore=0,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=0, teamBScore=0)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=0, teamBScore=0)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=0, teamBScore=0)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=0, teamBScore=0)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=0, teamBScore=0)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=0, teamBScore=0)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=0, teamBScore=0)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=0, teamBScore=0)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getScoringShare(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[owners[0].id])
        self.assertEqual(Deci("0"), response[owners[1].id])
        self.assertEqual(Deci("0"), response[owners[2].id])
        self.assertEqual(Deci("0"), response[owners[3].id])
        self.assertEqual(Deci("0"), response[owners[4].id])
        self.assertEqual(Deci("0"), response[owners[5].id])

    def test_getScoringShare_onlyPostSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3.3,
            teamBScore=4.4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4.4,
            teamBScore=5.5,
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
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3.3,
            teamBScore=4.4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4.4,
            teamBScore=5.5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getScoringShare(league, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("100"), sum(response.values()))
        self.assertEqual(Deci("2.857142857142857142857142857"), response[owners[0].id])
        self.assertEqual(Deci("5.714285714285714285714285714"), response[owners[1].id])
        self.assertEqual(Deci("17.14285714285714285714285714"), response[owners[2].id])
        self.assertEqual(Deci("22.85714285714285714285714286"), response[owners[3].id])
        self.assertEqual(Deci("22.85714285714285714285714286"), response[owners[4].id])
        self.assertEqual(Deci("28.57142857142857142857142857"), response[owners[5].id])

    def test_getScoringShare_onlyRegularSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3.3,
            teamBScore=4.4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4.4,
            teamBScore=5.5,
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
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3.3,
            teamBScore=4.4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4.4,
            teamBScore=5.5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getScoringShare(league, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        # due to rounding values, we assert that the values are very, very close
        self.assertTrue(math.isclose(Deci("100"), sum(response.values())))
        self.assertEqual(Deci("5.263157894736842105263157895"), response[owners[0].id])
        self.assertEqual(Deci("10.52631578947368421052631579"), response[owners[1].id])
        self.assertEqual(Deci("15.78947368421052631578947368"), response[owners[2].id])
        self.assertEqual(Deci("21.05263157894736842105263158"), response[owners[3].id])
        self.assertEqual(Deci("21.05263157894736842105263158"), response[owners[4].id])
        self.assertEqual(Deci("26.31578947368421052631578947"), response[owners[5].id])

    def test_getScoringShare_onlyChampionshipIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3.3,
            teamBScore=4.4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4.4,
            teamBScore=5.5,
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
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3.3,
            teamBScore=4.4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4.4,
            teamBScore=5.5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getScoringShare(league, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("100"), sum(filter(None, response.values())))
        self.assertIsNone(response[owners[0].id])
        self.assertIsNone(response[owners[1].id])
        self.assertIsNone(response[owners[2].id])
        self.assertIsNone(response[owners[3].id])
        self.assertEqual(Deci("44.44444444444444444444444444"), response[owners[4].id])
        self.assertEqual(Deci("55.55555555555555555555555556"), response[owners[5].id])

    def test_getScoringShare_yearNumberStartGivenWeekNumberStartGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3.3,
            teamBScore=4.4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4.4,
            teamBScore=5.5,
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
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3.3,
            teamBScore=4.4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4.4,
            teamBScore=5.5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getScoringShare(
            league, yearNumberStart=2001, weekNumberStart=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        # due to rounding values, we assert that the values are very, very close
        self.assertTrue(math.isclose(Deci("100"), sum(response.values())))
        self.assertEqual(Deci("5.263157894736842105263157895"), response[owners[0].id])
        self.assertEqual(Deci("10.52631578947368421052631579"), response[owners[1].id])
        self.assertEqual(Deci("15.78947368421052631578947368"), response[owners[2].id])
        self.assertEqual(Deci("21.05263157894736842105263158"), response[owners[3].id])
        self.assertEqual(Deci("21.05263157894736842105263158"), response[owners[4].id])
        self.assertEqual(Deci("26.31578947368421052631578947"), response[owners[5].id])

    def test_getScoringShare_yearNumberEndGivenWeekNumberEndGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3.3,
            teamBScore=4.4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4.4,
            teamBScore=5.5,
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
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3.3,
            teamBScore=4.4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4.4,
            teamBScore=5.5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getScoringShare(
            league, yearNumberEnd=2001, weekNumberEnd=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("100"), sum(response.values()))
        self.assertEqual(Deci("3.703703703703703703703703704"), response[owners[0].id])
        self.assertEqual(Deci("7.407407407407407407407407407"), response[owners[1].id])
        self.assertEqual(Deci("16.66666666666666666666666667"), response[owners[2].id])
        self.assertEqual(Deci("22.22222222222222222222222222"), response[owners[3].id])
        self.assertEqual(Deci("22.22222222222222222222222222"), response[owners[4].id])
        self.assertEqual(Deci("27.77777777777777777777777778"), response[owners[5].id])

    def test_getScoringShare_yearNumberStartGivenWeekNumberStartGivenAndYearNumberEndGivenWeekNumberEndGiven(
        self,
    ):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3.3,
            teamBScore=4.4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4.4,
            teamBScore=5.5,
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
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3.3,
            teamBScore=4.4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4.4,
            teamBScore=5.5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getScoringShare(
            league, yearNumberStart=2001, weekNumberStart=1, yearNumberEnd=2001, weekNumberEnd=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        # due to rounding values, we assert that the values are very, very close
        self.assertTrue(math.isclose(Deci("100"), sum(response.values())))
        self.assertEqual(Deci("5.263157894736842105263157895"), response[owners[0].id])
        self.assertEqual(Deci("10.52631578947368421052631579"), response[owners[1].id])
        self.assertEqual(Deci("15.78947368421052631578947368"), response[owners[2].id])
        self.assertEqual(Deci("21.05263157894736842105263158"), response[owners[3].id])
        self.assertEqual(Deci("21.05263157894736842105263158"), response[owners[4].id])
        self.assertEqual(Deci("26.31578947368421052631578947"), response[owners[5].id])

    def test_getOpponentScoringShare_happyPath(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3.3,
            teamBScore=4.4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4.4,
            teamBScore=5.5,
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
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3.3,
            teamBScore=4.4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4.4,
            teamBScore=5.5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getOpponentScoringShare(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("100"), sum(response.values()))
        self.assertEqual(Deci("7.407407407407407407407407407"), response[owners[0].id])
        self.assertEqual(Deci("3.703703703703703703703703704"), response[owners[1].id])
        self.assertEqual(Deci("22.22222222222222222222222222"), response[owners[2].id])
        self.assertEqual(Deci("16.66666666666666666666666667"), response[owners[3].id])
        self.assertEqual(Deci("27.77777777777777777777777778"), response[owners[4].id])
        self.assertEqual(Deci("22.22222222222222222222222222"), response[owners[5].id])

    def test_getOpponentScoringShare_nonAnnualOwner(self):
        ownersA, teamsA = getNDefaultOwnersAndTeams(6, randomNames=True)
        ownersB, teamsB = getNDefaultOwnersAndTeams(6, randomNames=True)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1.1, teamBScore=2.2
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3.3, teamBScore=4.4
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4.4, teamBScore=5.5
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
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        league = League(name="TEST", owners=ownersA + ownersB, years=[yearA, yearB])

        response = ScoringShareAllTimeCalculator.getOpponentScoringShare(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(12, len(response.keys()))
        self.assertEqual(Deci("100"), sum(response.values()))
        self.assertEqual(Deci("5.263157894736842105263157895"), response[ownersA[0].id])
        self.assertEqual(Deci("5.263157894736842105263157895"), response[ownersB[0].id])
        self.assertEqual(Deci("2.631578947368421052631578947"), response[ownersA[1].id])
        self.assertEqual(Deci("2.631578947368421052631578947"), response[ownersB[1].id])
        self.assertEqual(Deci("10.52631578947368421052631579"), response[ownersA[2].id])
        self.assertEqual(Deci("10.52631578947368421052631579"), response[ownersB[2].id])
        self.assertEqual(Deci("7.894736842105263157894736842"), response[ownersA[3].id])
        self.assertEqual(Deci("7.894736842105263157894736842"), response[ownersB[3].id])
        self.assertEqual(Deci("13.15789473684210526315789474"), response[ownersA[4].id])
        self.assertEqual(Deci("13.15789473684210526315789474"), response[ownersB[4].id])
        self.assertEqual(Deci("10.52631578947368421052631579"), response[ownersA[5].id])
        self.assertEqual(Deci("10.52631578947368421052631579"), response[ownersB[5].id])

    def test_getOpponentScoringShare_noneIfNoGamesPlayed(self):
        owners, teamsA = getNDefaultOwnersAndTeams(3)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1.1, teamBScore=2.2
        )
        matchup2_a = Matchup(
            teamAId=teamsA[1].id, teamBId=teamsA[2].id, teamAScore=3.3, teamBScore=4.4
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])

        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a])

        league = League(name="TEST", owners=owners, years=[yearA])

        response = ScoringShareAllTimeCalculator.getOpponentScoringShare(league, weekNumberEnd=1)

        self.assertIsInstance(response, dict)
        self.assertEqual(3, len(response.keys()))
        self.assertEqual(Deci("100"), sum(filter(None, response.values())))
        self.assertEqual(Deci("66.66666666666666666666666667"), response[owners[0].id])
        self.assertEqual(Deci("33.33333333333333333333333333"), response[owners[1].id])
        self.assertIsNone(response[owners[2].id])

    def test_getOpponentScoringShare_noPointsScoredInYears(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=0,
            teamBScore=0,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=0, teamBScore=0)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=0, teamBScore=0)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=0, teamBScore=0)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=0, teamBScore=0)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=0, teamBScore=0)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=0, teamBScore=0)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=0, teamBScore=0)
        matchup3_c = Matchup(
            teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=0, teamBScore=00
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getOpponentScoringShare(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[owners[0].id])
        self.assertEqual(Deci("0"), response[owners[1].id])
        self.assertEqual(Deci("0"), response[owners[2].id])
        self.assertEqual(Deci("0"), response[owners[3].id])
        self.assertEqual(Deci("0"), response[owners[4].id])
        self.assertEqual(Deci("0"), response[owners[5].id])

    def test_getOpponentScoringShare_onlyPostSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3.3,
            teamBScore=4.4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4.4,
            teamBScore=5.5,
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
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3.3,
            teamBScore=4.4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4.4,
            teamBScore=5.5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getOpponentScoringShare(
            league, onlyPostSeason=True
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("100"), sum(response.values()))
        self.assertEqual(Deci("5.714285714285714285714285714"), response[owners[0].id])
        self.assertEqual(Deci("2.857142857142857142857142857"), response[owners[1].id])
        self.assertEqual(Deci("22.85714285714285714285714286"), response[owners[2].id])
        self.assertEqual(Deci("17.14285714285714285714285714"), response[owners[3].id])
        self.assertEqual(Deci("28.57142857142857142857142857"), response[owners[4].id])
        self.assertEqual(Deci("22.85714285714285714285714286"), response[owners[5].id])

    def test_getOpponentScoringShare_onlyRegularSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3.3,
            teamBScore=4.4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4.4,
            teamBScore=5.5,
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
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3.3,
            teamBScore=4.4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4.4,
            teamBScore=5.5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getOpponentScoringShare(
            league, onlyRegularSeason=True
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        # due to rounding values, we assert that the values are very, very close
        self.assertTrue(math.isclose(Deci("100"), sum(response.values())))
        self.assertEqual(Deci("10.52631578947368421052631579"), response[owners[0].id])
        self.assertEqual(Deci("5.263157894736842105263157895"), response[owners[1].id])
        self.assertEqual(Deci("21.05263157894736842105263158"), response[owners[2].id])
        self.assertEqual(Deci("15.78947368421052631578947368"), response[owners[3].id])
        self.assertEqual(Deci("26.31578947368421052631578947"), response[owners[4].id])
        self.assertEqual(Deci("21.05263157894736842105263158"), response[owners[5].id])

    def test_getOpponentScoringShare_onlyChampionshipIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3.3,
            teamBScore=4.4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4.4,
            teamBScore=5.5,
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
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3.3,
            teamBScore=4.4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4.4,
            teamBScore=5.5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getOpponentScoringShare(
            league, onlyChampionship=True
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("100"), sum(filter(None, response.values())))
        self.assertIsNone(response[owners[0].id])
        self.assertIsNone(response[owners[1].id])
        self.assertIsNone(response[owners[2].id])
        self.assertIsNone(response[owners[3].id])
        self.assertEqual(Deci("55.55555555555555555555555556"), response[owners[4].id])
        self.assertEqual(Deci("44.44444444444444444444444444"), response[owners[5].id])

    def test_getOpponentScoringShare_yearNumberStartGivenWeekNumberStartGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3.3,
            teamBScore=4.4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4.4,
            teamBScore=5.5,
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
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3.3,
            teamBScore=4.4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4.4,
            teamBScore=5.5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getOpponentScoringShare(
            league, yearNumberStart=2001, weekNumberStart=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        # due to rounding values, we assert that the values are very, very close
        self.assertTrue(math.isclose(Deci("100"), sum(response.values())))
        self.assertEqual(Deci("10.52631578947368421052631579"), response[owners[0].id])
        self.assertEqual(Deci("5.263157894736842105263157895"), response[owners[1].id])
        self.assertEqual(Deci("21.05263157894736842105263158"), response[owners[2].id])
        self.assertEqual(Deci("15.78947368421052631578947368"), response[owners[3].id])
        self.assertEqual(Deci("26.31578947368421052631578947"), response[owners[4].id])
        self.assertEqual(Deci("21.05263157894736842105263158"), response[owners[5].id])

    def test_getOpponentScoringShare_yearNumberEndGivenWeekNumberEndGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3.3,
            teamBScore=4.4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4.4,
            teamBScore=5.5,
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
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3.3,
            teamBScore=4.4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4.4,
            teamBScore=5.5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getOpponentScoringShare(
            league, yearNumberEnd=2001, weekNumberEnd=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("100"), sum(response.values()))
        self.assertEqual(Deci("7.407407407407407407407407407"), response[owners[0].id])
        self.assertEqual(Deci("3.703703703703703703703703704"), response[owners[1].id])
        self.assertEqual(Deci("22.22222222222222222222222222"), response[owners[2].id])
        self.assertEqual(Deci("16.66666666666666666666666667"), response[owners[3].id])
        self.assertEqual(Deci("27.77777777777777777777777778"), response[owners[4].id])
        self.assertEqual(Deci("22.22222222222222222222222222"), response[owners[5].id])

    def test_getOpponentScoringShare_yearNumberStartGivenWeekNumberStartGivenAndYearNumberEndGivenWeekNumberEndGiven(
        self,
    ):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id,
            teamBId=teamsA[3].id,
            teamAScore=3.3,
            teamBScore=4.4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id,
            teamBId=teamsA[5].id,
            teamAScore=4.4,
            teamBScore=5.5,
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
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=3.3,
            teamBScore=4.4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4.4,
            teamBScore=5.5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getOpponentScoringShare(
            league, yearNumberStart=2001, weekNumberStart=1, yearNumberEnd=2001, weekNumberEnd=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        # due to rounding values, we assert that the values are very, very close
        self.assertTrue(math.isclose(Deci("100"), sum(response.values())))
        self.assertEqual(Deci("10.52631578947368421052631579"), response[owners[0].id])
        self.assertEqual(Deci("5.263157894736842105263157895"), response[owners[1].id])
        self.assertEqual(Deci("21.05263157894736842105263158"), response[owners[2].id])
        self.assertEqual(Deci("15.78947368421052631578947368"), response[owners[3].id])
        self.assertEqual(Deci("26.31578947368421052631578947"), response[owners[4].id])
        self.assertEqual(Deci("21.05263157894736842105263158"), response[owners[5].id])

    def test_getMaxScoringShare_happyPath(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=100,
            teamBScore=100,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=0, teamBScore=0)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=0, teamBScore=0)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=4, teamBScore=3)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=0)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=0, teamBScore=0)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=0,
            teamBScore=0,
            matchupType=MatchupType.PLAYOFF,
            teamAHasTiebreaker=True,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=0,
            teamBScore=3,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4,
            teamBScore=3,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getMaxScoringShare(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("40"), response[owners[0].id])
        self.assertEqual(Deci("30"), response[owners[1].id])
        self.assertEqual(Deci("30"), response[owners[2].id])
        self.assertEqual(Deci("30"), response[owners[3].id])
        self.assertEqual(Deci("40"), response[owners[4].id])
        self.assertEqual(Deci("30"), response[owners[5].id])

    def test_getMaxScoringShare_nonAnnualOwner(self):
        ownersA, teamsA_1 = getNDefaultOwnersAndTeams(6, randomNames=True)
        teamsA_2 = getTeamsFromOwners(ownersA)
        ownersB, teamsB_1 = getNDefaultOwnersAndTeams(6, randomNames=True)
        teamsB_2 = getTeamsFromOwners(ownersB)

        # years 1-2, has ownersA
        matchup1_a1 = Matchup(
            teamAId=teamsA_1[0].id, teamBId=teamsA_1[1].id, teamAScore=1.1, teamBScore=2.2
        )
        matchup2_a1 = Matchup(
            teamAId=teamsA_1[2].id, teamBId=teamsA_1[3].id, teamAScore=3.3, teamBScore=4.4
        )
        matchup3_a1 = Matchup(
            teamAId=teamsA_1[4].id, teamBId=teamsA_1[5].id, teamAScore=4.4, teamBScore=5.5
        )

        week1_a1 = Week(weekNumber=1, matchups=[matchup1_a1, matchup2_a1, matchup3_a1])
        yearA_1 = Year(yearNumber=2000, teams=teamsA_1, weeks=[week1_a1])

        matchup1_a2 = Matchup(
            teamAId=teamsA_2[0].id, teamBId=teamsA_2[1].id, teamAScore=1, teamBScore=0
        )
        matchup2_a2 = Matchup(
            teamAId=teamsA_2[2].id, teamBId=teamsA_2[3].id, teamAScore=1, teamBScore=0
        )
        matchup3_a2 = Matchup(
            teamAId=teamsA_2[4].id, teamBId=teamsA_2[5].id, teamAScore=1, teamBScore=0
        )

        week1_a2 = Week(weekNumber=1, matchups=[matchup1_a2, matchup2_a2, matchup3_a2])
        yearA_2 = Year(yearNumber=2001, teams=teamsA_2, weeks=[week1_a2])
        
        # years 3-4, has ownersB
        matchup1_b1 = Matchup(
            teamAId=teamsB_1[0].id, teamBId=teamsB_1[1].id, teamAScore=1.1, teamBScore=2.2
        )
        matchup2_b1 = Matchup(
            teamAId=teamsB_1[2].id, teamBId=teamsB_1[3].id, teamAScore=3.3, teamBScore=4.4
        )
        matchup3_b1 = Matchup(
            teamAId=teamsB_1[4].id, teamBId=teamsB_1[5].id, teamAScore=4.4, teamBScore=5.5
        )

        week1_b1 = Week(weekNumber=1, matchups=[matchup1_b1, matchup2_b1, matchup3_b1])
        yearB_1 = Year(yearNumber=2002, teams=teamsB_1, weeks=[week1_b1])

        matchup1_b2 = Matchup(
            teamAId=teamsB_2[0].id, teamBId=teamsB_2[1].id, teamAScore=1, teamBScore=0
        )
        matchup2_b2 = Matchup(
            teamAId=teamsB_2[2].id, teamBId=teamsB_2[3].id, teamAScore=1, teamBScore=0
        )
        matchup3_b2 = Matchup(
            teamAId=teamsB_2[4].id, teamBId=teamsB_2[5].id, teamAScore=1, teamBScore=0
        )

        week1_b2 = Week(weekNumber=1, matchups=[matchup1_b2, matchup2_b2, matchup3_b2])
        yearB_2 = Year(yearNumber=2003, teams=teamsB_2, weeks=[week1_b2])

        league = League(name="TEST", owners=ownersA + ownersB, years=[yearA_1, yearA_2, yearB_1, yearB_2])

        response = ScoringShareAllTimeCalculator.getMaxScoringShare(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(12, len(response.keys()))
        self.assertEqual(Deci("33.33333333333333333333333333"), response[ownersA[0].id])
        self.assertAlmostEqual(Deci("10.52631578947368320322336943"), response[ownersA[1].id], delta=Deci("0.00000000000001"))
        self.assertEqual(Deci("33.33333333333333333333333333"), response[ownersA[2].id])
        self.assertAlmostEqual(Deci("21.05263157894736640644673886"), response[ownersA[3].id], delta=Deci("0.00000000000001"))
        self.assertEqual(Deci("33.33333333333333333333333333"), response[ownersA[4].id])
        self.assertAlmostEqual(Deci("26.31578947368420800805842357"), response[ownersA[5].id], delta=Deci("0.00000000000001"))
        self.assertEqual(Deci("33.33333333333333333333333333"), response[ownersB[0].id])
        self.assertAlmostEqual(Deci("10.52631578947368320322336943"), response[ownersB[1].id], delta=Deci("0.00000000000001"))
        self.assertEqual(Deci("33.33333333333333333333333333"), response[ownersB[2].id])
        self.assertAlmostEqual(Deci("21.05263157894736640644673886"), response[ownersB[3].id], delta=Deci("0.00000000000001"))
        self.assertEqual(Deci("33.33333333333333333333333333"), response[ownersB[4].id])
        self.assertAlmostEqual(Deci("26.31578947368420800805842357"), response[ownersB[5].id], delta=Deci("0.00000000000001"))

    
    def test_getMaxScoringShare_noneIfNoGamesPlayed(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=100,
            teamBScore=100,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=4, teamBScore=3)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=3, teamBScore=0)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=4, teamBScore=3)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=0)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=0, teamBScore=0)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=0,
            teamBScore=0,
            matchupType=MatchupType.PLAYOFF,
            teamAHasTiebreaker=True,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=0,
            teamBScore=3,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4,
            teamBScore=3,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getMaxScoringShare(
            league, yearNumberEnd=2000, weekNumberEnd=1
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertIsNone(response[owners[0].id])
        self.assertIsNone(response[owners[1].id])
        self.assertEqual(Deci("40"), response[owners[2].id])
        self.assertEqual(Deci("30"), response[owners[3].id])
        self.assertEqual(Deci("30"), response[owners[4].id])
        self.assertEqual(Deci("0"), response[owners[5].id])

    def test_getMaxScoringShare_noPointsScoredInYears(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=0, teamBScore=0)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=0, teamBScore=0)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=0, teamBScore=0)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=0, teamBScore=0)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=0, teamBScore=0)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=0, teamBScore=0)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=0, teamBScore=0)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=0, teamBScore=0)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=0, teamBScore=0)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getMaxScoringShare(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[owners[0].id])
        self.assertEqual(Deci("0"), response[owners[1].id])
        self.assertEqual(Deci("0"), response[owners[2].id])
        self.assertEqual(Deci("0"), response[owners[3].id])
        self.assertEqual(Deci("0"), response[owners[4].id])
        self.assertEqual(Deci("0"), response[owners[5].id])

    def test_getMaxScoringShare_onlyPostSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=100, teamBScore=100
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=100, teamBScore=0
        )
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=0, teamBScore=0)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=0, teamBScore=0)
        matchup2_b = Matchup(
            teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=0, teamBScore=100
        )
        matchup3_b = Matchup(
            teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=100, teamBScore=100
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
            teamAHasTiebreaker=True,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=1,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
            teamAHasTiebreaker=True,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=1,
            teamBScore=1,
            matchupType=MatchupType.CHAMPIONSHIP,
            teamAHasTiebreaker=True,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getMaxScoringShare(league, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("16.66666666666666666666666667"), response[owners[0].id])
        self.assertEqual(Deci("16.66666666666666666666666667"), response[owners[1].id])
        self.assertEqual(Deci("16.66666666666666666666666667"), response[owners[2].id])
        self.assertEqual(Deci("16.66666666666666666666666667"), response[owners[3].id])
        self.assertEqual(Deci("16.66666666666666666666666667"), response[owners[4].id])
        self.assertEqual(Deci("16.66666666666666666666666667"), response[owners[5].id])

    def test_getMaxScoringShare_onlyRegularSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=1)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=1, teamBScore=1)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=1, teamBScore=1)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=0,
            teamBScore=0,
            matchupType=MatchupType.PLAYOFF,
            teamAHasTiebreaker=True,
        )
        matchup2_b = Matchup(
            teamAId=teamsB[2].id,
            teamBId=teamsB[3].id,
            teamAScore=0,
            teamBScore=100,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[4].id,
            teamBId=teamsB[5].id,
            teamAScore=100,
            teamBScore=100,
            matchupType=MatchupType.PLAYOFF,
            teamAHasTiebreaker=True,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=100,
            teamBScore=100,
            matchupType=MatchupType.PLAYOFF,
            teamAHasTiebreaker=True,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=100,
            teamBScore=0,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=0,
            teamBScore=0,
            matchupType=MatchupType.CHAMPIONSHIP,
            teamAHasTiebreaker=True,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getMaxScoringShare(league, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("16.66666666666666666666666667"), response[owners[0].id])
        self.assertEqual(Deci("16.66666666666666666666666667"), response[owners[1].id])
        self.assertEqual(Deci("16.66666666666666666666666667"), response[owners[2].id])
        self.assertEqual(Deci("16.66666666666666666666666667"), response[owners[3].id])
        self.assertEqual(Deci("16.66666666666666666666666667"), response[owners[4].id])
        self.assertEqual(Deci("16.66666666666666666666666667"), response[owners[5].id])

    def test_getMaxScoringShare_onlyChampionshipIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=100, teamBScore=100
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=100, teamBScore=0
        )
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=0, teamBScore=0)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=0, teamBScore=0)
        matchup2_b = Matchup(
            teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=0, teamBScore=100
        )
        matchup3_b = Matchup(
            teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=100, teamBScore=100
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
            teamAHasTiebreaker=True,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=1,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
            teamAHasTiebreaker=True,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=1,
            teamBScore=3,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getMaxScoringShare(league, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertIsNone(response[owners[0].id])
        self.assertIsNone(response[owners[1].id])
        self.assertIsNone(response[owners[2].id])
        self.assertIsNone(response[owners[3].id])
        self.assertEqual(Deci("25"), response[owners[4].id])
        self.assertEqual(Deci("75"), response[owners[5].id])

    def test_getMaxScoringShare_yearNumberStartGivenWeekNumberStartGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=100, teamBScore=0
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=100, teamBScore=0
        )
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=0, teamBScore=0)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=0, teamBScore=0)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=0, teamBScore=0)
        matchup3_b = Matchup(
            teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=100, teamBScore=100
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        matchup4_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=4, teamBScore=3)
        matchup5_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=0)
        matchup6_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=0, teamBScore=0)
        week2_b = Week(weekNumber=2, matchups=[matchup4_b, matchup5_b, matchup6_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=0,
            teamBScore=0,
            matchupType=MatchupType.PLAYOFF,
            teamAHasTiebreaker=True,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=0,
            teamBScore=3,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4,
            teamBScore=3,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getMaxScoringShare(
            league, yearNumberStart=2001, weekNumberStart=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("40"), response[owners[0].id])
        self.assertEqual(Deci("30"), response[owners[1].id])
        self.assertEqual(Deci("30"), response[owners[2].id])
        self.assertEqual(Deci("30"), response[owners[3].id])
        self.assertEqual(Deci("40"), response[owners[4].id])
        self.assertEqual(Deci("30"), response[owners[5].id])

    def test_getMaxScoringShare_yearNumberEndGivenWeekNumberEndGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=4, teamBScore=3)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3, teamBScore=0)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=0, teamBScore=0)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=0, teamBScore=0)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=0, teamBScore=3)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=3)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        matchup4_b = Matchup(
            teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=100, teamBScore=0
        )
        matchup5_b = Matchup(
            teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=100, teamBScore=0
        )
        matchup6_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=0, teamBScore=0)
        week2_b = Week(weekNumber=2, matchups=[matchup4_b, matchup5_b, matchup6_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=0, teamBScore=0)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=0, teamBScore=0)
        matchup3_c = Matchup(
            teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=100, teamBScore=100
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getMaxScoringShare(
            league, yearNumberEnd=2001, weekNumberEnd=1
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("40"), response[owners[0].id])
        self.assertEqual(Deci("30"), response[owners[1].id])
        self.assertEqual(Deci("30"), response[owners[2].id])
        self.assertEqual(Deci("30"), response[owners[3].id])
        self.assertEqual(Deci("40"), response[owners[4].id])
        self.assertEqual(Deci("30"), response[owners[5].id])

    def test_getMaxScoringShare_yearNumberStartGivenWeekNumberStartGivenAndYearNumberEndGivenWeekNumberEndGiven(
        self,
    ):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=100, teamBScore=0
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=100, teamBScore=0
        )
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=0, teamBScore=0)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(
            teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=0, teamBScore=100
        )
        matchup2_b = Matchup(
            teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=0, teamBScore=100
        )
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=0, teamBScore=0)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        matchup4_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=4, teamBScore=3)
        matchup5_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=0)
        matchup6_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=0, teamBScore=0)
        week2_b = Week(weekNumber=2, matchups=[matchup4_b, matchup5_b, matchup6_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=0, teamBScore=0)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=0, teamBScore=3)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4, teamBScore=3)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        matchup4_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=0, teamBScore=0)
        matchup5_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=0, teamBScore=0)
        matchup6_c = Matchup(
            teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=100, teamBScore=100
        )
        week2_c = Week(weekNumber=2, matchups=[matchup4_c, matchup5_c, matchup6_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getMaxScoringShare(
            league, yearNumberStart=2001, weekNumberStart=2, yearNumberEnd=2002, weekNumberEnd=1
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("40"), response[owners[0].id])
        self.assertEqual(Deci("30"), response[owners[1].id])
        self.assertEqual(Deci("30"), response[owners[2].id])
        self.assertEqual(Deci("30"), response[owners[3].id])
        self.assertEqual(Deci("40"), response[owners[4].id])
        self.assertEqual(Deci("30"), response[owners[5].id])

    def test_getMinScoringShare_happyPath(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=0, teamBScore=1)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=0, teamBScore=1)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=0, teamBScore=1)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=0)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=1, teamBScore=0)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=1, teamBScore=0)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3, teamBScore=4)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=5, teamBScore=6)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getMinScoringShare(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[owners[0].id])
        self.assertEqual(Deci("0"), response[owners[1].id])
        self.assertEqual(Deci("0"), response[owners[2].id])
        self.assertEqual(Deci("0"), response[owners[3].id])
        self.assertEqual(Deci("0"), response[owners[4].id])
        self.assertEqual(Deci("0"), response[owners[5].id])

    def test_getMinScoringShare_noneIfNoGamesPlayed(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=100,
            teamBScore=100,
            matchupType=MatchupType.IGNORE,
        )
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=4, teamBScore=3)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=3, teamBScore=0)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=4, teamBScore=3)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=0)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=0, teamBScore=0)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=0,
            teamBScore=0,
            matchupType=MatchupType.PLAYOFF,
            teamAHasTiebreaker=True,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=0,
            teamBScore=3,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=4,
            teamBScore=3,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getMinScoringShare(
            league, yearNumberEnd=2000, weekNumberEnd=1
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertIsNone(response[owners[0].id])
        self.assertIsNone(response[owners[1].id])
        self.assertEqual(Deci("40"), response[owners[2].id])
        self.assertEqual(Deci("30"), response[owners[3].id])
        self.assertEqual(Deci("30"), response[owners[4].id])
        self.assertEqual(Deci("0"), response[owners[5].id])

    def test_getMinScoringShare_noPointsScoredInYears(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=0, teamBScore=0)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=0, teamBScore=0)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=0, teamBScore=0)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=0, teamBScore=0)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=0, teamBScore=0)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=0, teamBScore=0)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=0, teamBScore=0)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=0, teamBScore=0)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=0, teamBScore=0)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getMinScoringShare(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[owners[0].id])
        self.assertEqual(Deci("0"), response[owners[1].id])
        self.assertEqual(Deci("0"), response[owners[2].id])
        self.assertEqual(Deci("0"), response[owners[3].id])
        self.assertEqual(Deci("0"), response[owners[4].id])
        self.assertEqual(Deci("0"), response[owners[5].id])

    def test_getMinScoringShare_onlyPostSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=100, teamBScore=100
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=100, teamBScore=0
        )
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=0, teamBScore=0)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=0, teamBScore=0)
        matchup2_b = Matchup(
            teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=0, teamBScore=100
        )
        matchup3_b = Matchup(
            teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=100, teamBScore=100
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
            teamAHasTiebreaker=True,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=1,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
            teamAHasTiebreaker=True,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=1,
            teamBScore=1,
            matchupType=MatchupType.CHAMPIONSHIP,
            teamAHasTiebreaker=True,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getMinScoringShare(league, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("16.66666666666666666666666667"), response[owners[0].id])
        self.assertEqual(Deci("16.66666666666666666666666667"), response[owners[1].id])
        self.assertEqual(Deci("16.66666666666666666666666667"), response[owners[2].id])
        self.assertEqual(Deci("16.66666666666666666666666667"), response[owners[3].id])
        self.assertEqual(Deci("16.66666666666666666666666667"), response[owners[4].id])
        self.assertEqual(Deci("16.66666666666666666666666667"), response[owners[5].id])

    def test_getMinScoringShare_onlyRegularSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=1)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=1, teamBScore=1)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=1, teamBScore=1)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=0,
            teamBScore=0,
            matchupType=MatchupType.PLAYOFF,
            teamAHasTiebreaker=True,
        )
        matchup2_b = Matchup(
            teamAId=teamsB[2].id,
            teamBId=teamsB[3].id,
            teamAScore=0,
            teamBScore=100,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[4].id,
            teamBId=teamsB[5].id,
            teamAScore=100,
            teamBScore=100,
            matchupType=MatchupType.PLAYOFF,
            teamAHasTiebreaker=True,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=100,
            teamBScore=100,
            matchupType=MatchupType.PLAYOFF,
            teamAHasTiebreaker=True,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=100,
            teamBScore=0,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=0,
            teamBScore=0,
            matchupType=MatchupType.CHAMPIONSHIP,
            teamAHasTiebreaker=True,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getMinScoringShare(league, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("16.66666666666666666666666667"), response[owners[0].id])
        self.assertEqual(Deci("16.66666666666666666666666667"), response[owners[1].id])
        self.assertEqual(Deci("16.66666666666666666666666667"), response[owners[2].id])
        self.assertEqual(Deci("16.66666666666666666666666667"), response[owners[3].id])
        self.assertEqual(Deci("16.66666666666666666666666667"), response[owners[4].id])
        self.assertEqual(Deci("16.66666666666666666666666667"), response[owners[5].id])

    def test_getMinScoringShare_onlyChampionshipIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=100, teamBScore=100
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=100, teamBScore=0
        )
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=0, teamBScore=0)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=0, teamBScore=0)
        matchup2_b = Matchup(
            teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=0, teamBScore=100
        )
        matchup3_b = Matchup(
            teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=100, teamBScore=100
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
            teamAHasTiebreaker=True,
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id,
            teamBId=teamsC[3].id,
            teamAScore=1,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
            teamAHasTiebreaker=True,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id,
            teamBId=teamsC[5].id,
            teamAScore=1,
            teamBScore=3,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getMinScoringShare(league, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertIsNone(response[owners[0].id])
        self.assertIsNone(response[owners[1].id])
        self.assertIsNone(response[owners[2].id])
        self.assertIsNone(response[owners[3].id])
        self.assertEqual(Deci("25"), response[owners[4].id])
        self.assertEqual(Deci("75"), response[owners[5].id])

    def test_getMinScoringShare_yearNumberStartGivenWeekNumberStartGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=100, teamBScore=0
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=100, teamBScore=0
        )
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=0, teamBScore=0)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=0, teamBScore=0)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=0, teamBScore=0)
        matchup3_b = Matchup(
            teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=100, teamBScore=100
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        matchup4_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=2, teamBScore=2)
        matchup5_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=2, teamBScore=2)
        matchup6_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=1, teamBScore=1)
        week2_b = Week(weekNumber=2, matchups=[matchup4_b, matchup5_b, matchup6_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=2, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=1, teamBScore=1)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=2, teamBScore=2)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getMinScoringShare(
            league, yearNumberStart=2001, weekNumberStart=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("20"), response[owners[0].id])
        self.assertEqual(Deci("20"), response[owners[1].id])
        self.assertEqual(Deci("10"), response[owners[2].id])
        self.assertEqual(Deci("10"), response[owners[3].id])
        self.assertEqual(Deci("10"), response[owners[4].id])
        self.assertEqual(Deci("10"), response[owners[5].id])

    def test_getMinScoringShare_yearNumberEndGivenWeekNumberEndGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=1)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=2, teamBScore=2)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=2, teamBScore=2)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=2, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=1, teamBScore=1)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=2, teamBScore=2)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        matchup4_b = Matchup(
            teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=100, teamBScore=0
        )
        matchup5_b = Matchup(
            teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=100, teamBScore=0
        )
        matchup6_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=0, teamBScore=0)
        week2_b = Week(weekNumber=2, matchups=[matchup4_b, matchup5_b, matchup6_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=0, teamBScore=0)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=0, teamBScore=0)
        matchup3_c = Matchup(
            teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=100, teamBScore=100
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getMinScoringShare(
            league, yearNumberEnd=2001, weekNumberEnd=1
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("10"), response[owners[0].id])
        self.assertEqual(Deci("10"), response[owners[1].id])
        self.assertEqual(Deci("10"), response[owners[2].id])
        self.assertEqual(Deci("10"), response[owners[3].id])
        self.assertEqual(Deci("20"), response[owners[4].id])
        self.assertEqual(Deci("20"), response[owners[5].id])

    def test_getMinScoringShare_yearNumberStartGivenWeekNumberStartGivenAndYearNumberEndGivenWeekNumberEndGiven(
        self,
    ):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=100, teamBScore=0
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=100, teamBScore=0
        )
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=0, teamBScore=0)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(
            teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=0, teamBScore=100
        )
        matchup2_b = Matchup(
            teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=0, teamBScore=100
        )
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=0, teamBScore=0)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        matchup4_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=1)
        matchup5_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=2, teamBScore=2)
        matchup6_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=2, teamBScore=2)
        week2_b = Week(weekNumber=2, matchups=[matchup4_b, matchup5_b, matchup6_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=2, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=1, teamBScore=1)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=2, teamBScore=2)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        matchup4_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=0, teamBScore=0)
        matchup5_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=0, teamBScore=0)
        matchup6_c = Matchup(
            teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=100, teamBScore=100
        )
        week2_c = Week(weekNumber=2, matchups=[matchup4_c, matchup5_c, matchup6_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getMinScoringShare(
            league, yearNumberStart=2001, weekNumberStart=2, yearNumberEnd=2002, weekNumberEnd=1
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("10"), response[owners[0].id])
        self.assertEqual(Deci("10"), response[owners[1].id])
        self.assertEqual(Deci("10"), response[owners[2].id])
        self.assertEqual(Deci("10"), response[owners[3].id])
        self.assertEqual(Deci("20"), response[owners[4].id])
        self.assertEqual(Deci("20"), response[owners[5].id])
