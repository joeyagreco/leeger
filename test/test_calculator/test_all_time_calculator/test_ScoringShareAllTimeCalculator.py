import math
import unittest

from src.leeger.calculator.all_time_calculator.ScoringShareAllTimeCalculator import ScoringShareAllTimeCalculator
from src.leeger.enum.MatchupType import MatchupType
from src.leeger.model.league.League import League
from src.leeger.model.league.Matchup import Matchup
from src.leeger.model.league.Week import Week
from src.leeger.model.league.Year import Year
from src.leeger.util.Deci import Deci
from test.helper.prototypes import getNDefaultOwnersAndTeams, getTeamsFromOwners


class TestScoringShareAllTimeCalculator(unittest.TestCase):

    def test_getScoringShare_happyPath(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1.1, teamBScore=2.2,
                             matchupType=MatchupType.IGNORE)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3.3, teamBScore=4.4,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4.4, teamBScore=5.5,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.1, teamBScore=2.2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.3, teamBScore=4.4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.4, teamBScore=5.5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1.1, teamBScore=2.2,
                             matchupType=MatchupType.PLAYOFF)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3.3, teamBScore=4.4,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4.4, teamBScore=5.5,
                             matchupType=MatchupType.CHAMPIONSHIP)
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

    def test_getScoringShare_noPointsScoredInYears(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=0, teamBScore=0,
                             matchupType=MatchupType.IGNORE)
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

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1.1, teamBScore=2.2,
                             matchupType=MatchupType.IGNORE)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3.3, teamBScore=4.4,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4.4, teamBScore=5.5,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.1, teamBScore=2.2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.3, teamBScore=4.4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.4, teamBScore=5.5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1.1, teamBScore=2.2,
                             matchupType=MatchupType.PLAYOFF)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3.3, teamBScore=4.4,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4.4, teamBScore=5.5,
                             matchupType=MatchupType.CHAMPIONSHIP)
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

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1.1, teamBScore=2.2,
                             matchupType=MatchupType.IGNORE)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3.3, teamBScore=4.4,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4.4, teamBScore=5.5,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.1, teamBScore=2.2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.3, teamBScore=4.4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.4, teamBScore=5.5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1.1, teamBScore=2.2,
                             matchupType=MatchupType.PLAYOFF)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3.3, teamBScore=4.4,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4.4, teamBScore=5.5,
                             matchupType=MatchupType.CHAMPIONSHIP)
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

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1.1, teamBScore=2.2,
                             matchupType=MatchupType.IGNORE)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3.3, teamBScore=4.4,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4.4, teamBScore=5.5,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.1, teamBScore=2.2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.3, teamBScore=4.4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.4, teamBScore=5.5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1.1, teamBScore=2.2,
                             matchupType=MatchupType.PLAYOFF)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3.3, teamBScore=4.4,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4.4, teamBScore=5.5,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getScoringShare(league, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("100"), sum(response.values()))
        self.assertEqual(Deci("0"), response[owners[0].id])
        self.assertEqual(Deci("0"), response[owners[1].id])
        self.assertEqual(Deci("0"), response[owners[2].id])
        self.assertEqual(Deci("0"), response[owners[3].id])
        self.assertEqual(Deci("44.44444444444444444444444444"), response[owners[4].id])
        self.assertEqual(Deci("55.55555555555555555555555556"), response[owners[5].id])

    def test_getScoringShare_yearNumberStartGivenWeekNumberStartGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1.1, teamBScore=2.2,
                             matchupType=MatchupType.IGNORE)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3.3, teamBScore=4.4,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4.4, teamBScore=5.5,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.1, teamBScore=2.2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.3, teamBScore=4.4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.4, teamBScore=5.5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        matchup4_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.1, teamBScore=2.2)
        matchup5_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.3, teamBScore=4.4)
        matchup6_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.4, teamBScore=5.5)
        week2_b = Week(weekNumber=2, matchups=[matchup4_b, matchup5_b, matchup6_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1.1, teamBScore=2.2,
                             matchupType=MatchupType.PLAYOFF)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3.3, teamBScore=4.4,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4.4, teamBScore=5.5,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getScoringShare(league, yearNumberStart=2001, weekNumberStart=2)

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

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1.1, teamBScore=2.2,
                             matchupType=MatchupType.IGNORE)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3.3, teamBScore=4.4,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4.4, teamBScore=5.5,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.1, teamBScore=2.2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.3, teamBScore=4.4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.4, teamBScore=5.5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        matchup4_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.1, teamBScore=2.2)
        matchup5_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.3, teamBScore=4.4)
        matchup6_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.4, teamBScore=5.5)
        week2_b = Week(weekNumber=2, matchups=[matchup4_b, matchup5_b, matchup6_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1.1, teamBScore=2.2,
                             matchupType=MatchupType.PLAYOFF)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3.3, teamBScore=4.4,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4.4, teamBScore=5.5,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getScoringShare(league, yearNumberEnd=2001, weekNumberEnd=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("100"), sum(response.values()))
        self.assertEqual(Deci("3.703703703703703703703703704"), response[owners[0].id])
        self.assertEqual(Deci("7.407407407407407407407407407"), response[owners[1].id])
        self.assertEqual(Deci("16.66666666666666666666666667"), response[owners[2].id])
        self.assertEqual(Deci("22.22222222222222222222222222"), response[owners[3].id])
        self.assertEqual(Deci("22.22222222222222222222222222"), response[owners[4].id])
        self.assertEqual(Deci("27.77777777777777777777777778"), response[owners[5].id])

    def test_getScoringShare_yearNumberStartGivenWeekNumberStartGivenAndYearNumberEndGivenWeekNumberEndGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1.1, teamBScore=2.2,
                             matchupType=MatchupType.IGNORE)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3.3, teamBScore=4.4,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4.4, teamBScore=5.5,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.1, teamBScore=2.2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.3, teamBScore=4.4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.4, teamBScore=5.5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        matchup4_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.1, teamBScore=2.2)
        matchup5_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.3, teamBScore=4.4)
        matchup6_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.4, teamBScore=5.5)
        week2_b = Week(weekNumber=2, matchups=[matchup4_b, matchup5_b, matchup6_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1.1, teamBScore=2.2,
                             matchupType=MatchupType.PLAYOFF)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3.3, teamBScore=4.4,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4.4, teamBScore=5.5,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getScoringShare(league, yearNumberStart=2001, weekNumberStart=1,
                                                                 yearNumberEnd=2001, weekNumberEnd=2)

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

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1.1, teamBScore=2.2,
                             matchupType=MatchupType.IGNORE)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3.3, teamBScore=4.4,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4.4, teamBScore=5.5,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.1, teamBScore=2.2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.3, teamBScore=4.4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.4, teamBScore=5.5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1.1, teamBScore=2.2,
                             matchupType=MatchupType.PLAYOFF)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3.3, teamBScore=4.4,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4.4, teamBScore=5.5,
                             matchupType=MatchupType.CHAMPIONSHIP)
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

    def test_getOpponentScoringShare_noPointsScoredInYears(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=0, teamBScore=0,
                             matchupType=MatchupType.IGNORE)
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
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=0, teamBScore=00)
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

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1.1, teamBScore=2.2,
                             matchupType=MatchupType.IGNORE)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3.3, teamBScore=4.4,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4.4, teamBScore=5.5,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.1, teamBScore=2.2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.3, teamBScore=4.4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.4, teamBScore=5.5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1.1, teamBScore=2.2,
                             matchupType=MatchupType.PLAYOFF)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3.3, teamBScore=4.4,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4.4, teamBScore=5.5,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getOpponentScoringShare(league, onlyPostSeason=True)

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

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1.1, teamBScore=2.2,
                             matchupType=MatchupType.IGNORE)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3.3, teamBScore=4.4,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4.4, teamBScore=5.5,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.1, teamBScore=2.2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.3, teamBScore=4.4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.4, teamBScore=5.5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1.1, teamBScore=2.2,
                             matchupType=MatchupType.PLAYOFF)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3.3, teamBScore=4.4,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4.4, teamBScore=5.5,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getOpponentScoringShare(league, onlyRegularSeason=True)

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

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1.1, teamBScore=2.2,
                             matchupType=MatchupType.IGNORE)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3.3, teamBScore=4.4,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4.4, teamBScore=5.5,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.1, teamBScore=2.2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.3, teamBScore=4.4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.4, teamBScore=5.5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1.1, teamBScore=2.2,
                             matchupType=MatchupType.PLAYOFF)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3.3, teamBScore=4.4,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4.4, teamBScore=5.5,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getOpponentScoringShare(league, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("100"), sum(response.values()))
        self.assertEqual(Deci("0"), response[owners[0].id])
        self.assertEqual(Deci("0"), response[owners[1].id])
        self.assertEqual(Deci("0"), response[owners[2].id])
        self.assertEqual(Deci("0"), response[owners[3].id])
        self.assertEqual(Deci("55.55555555555555555555555556"), response[owners[4].id])
        self.assertEqual(Deci("44.44444444444444444444444444"), response[owners[5].id])

    def test_getOpponentScoringShare_yearNumberStartGivenWeekNumberStartGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1.1, teamBScore=2.2,
                             matchupType=MatchupType.IGNORE)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3.3, teamBScore=4.4,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4.4, teamBScore=5.5,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.1, teamBScore=2.2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.3, teamBScore=4.4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.4, teamBScore=5.5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        matchup4_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.1, teamBScore=2.2)
        matchup5_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.3, teamBScore=4.4)
        matchup6_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.4, teamBScore=5.5)
        week2_b = Week(weekNumber=2, matchups=[matchup4_b, matchup5_b, matchup6_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1.1, teamBScore=2.2,
                             matchupType=MatchupType.PLAYOFF)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3.3, teamBScore=4.4,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4.4, teamBScore=5.5,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getOpponentScoringShare(league, yearNumberStart=2001,
                                                                         weekNumberStart=2)

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

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1.1, teamBScore=2.2,
                             matchupType=MatchupType.IGNORE)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3.3, teamBScore=4.4,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4.4, teamBScore=5.5,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.1, teamBScore=2.2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.3, teamBScore=4.4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.4, teamBScore=5.5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        matchup4_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.1, teamBScore=2.2)
        matchup5_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.3, teamBScore=4.4)
        matchup6_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.4, teamBScore=5.5)
        week2_b = Week(weekNumber=2, matchups=[matchup4_b, matchup5_b, matchup6_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1.1, teamBScore=2.2,
                             matchupType=MatchupType.PLAYOFF)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3.3, teamBScore=4.4,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4.4, teamBScore=5.5,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getOpponentScoringShare(league, yearNumberEnd=2001, weekNumberEnd=2)

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
            self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1.1, teamBScore=2.2,
                             matchupType=MatchupType.IGNORE)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3.3, teamBScore=4.4,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4.4, teamBScore=5.5,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.1, teamBScore=2.2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.3, teamBScore=4.4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.4, teamBScore=5.5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        matchup4_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.1, teamBScore=2.2)
        matchup5_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.3, teamBScore=4.4)
        matchup6_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.4, teamBScore=5.5)
        week2_b = Week(weekNumber=2, matchups=[matchup4_b, matchup5_b, matchup6_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1.1, teamBScore=2.2,
                             matchupType=MatchupType.PLAYOFF)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3.3, teamBScore=4.4,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4.4, teamBScore=5.5,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringShareAllTimeCalculator.getOpponentScoringShare(league, yearNumberStart=2001,
                                                                         weekNumberStart=1,
                                                                         yearNumberEnd=2001, weekNumberEnd=2)

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
