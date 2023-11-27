import math
import unittest
from test.helper.prototypes import getNDefaultOwnersAndTeams, getTeamsFromOwners

from leeger.calculator.all_time_calculator.ScoringStandardDeviationAllTimeCalculator import (
    ScoringStandardDeviationAllTimeCalculator,
)
from leeger.enum.MatchupType import MatchupType
from leeger.model.league.League import League
from leeger.model.league.Matchup import Matchup
from leeger.model.league.Week import Week
from leeger.model.league.Year import Year
from leeger.util.Deci import Deci


class TestScoringStandardDeviationAllTimeCalculator(unittest.TestCase):
    def test_getScoringStandardDeviation_happyPath(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1.1,
            teamBScore=2.1,
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
            teamBScore=5.1,
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
            teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.2, teamBScore=5.2
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
            teamBScore=5.3,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringStandardDeviationAllTimeCalculator.getScoringStandardDeviation(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.05"), response[owners[0].id])
        self.assertEqual(Deci("0.05"), response[owners[1].id])
        self.assertEqual(Deci("0.08164965809277260327324280249"), response[owners[2].id])
        self.assertEqual(Deci("0.08164965809277260327324280249"), response[owners[3].id])
        self.assertEqual(Deci("0.08164965809277260327324280249"), response[owners[4].id])
        self.assertEqual(Deci("0.08164965809277260327324280249"), response[owners[5].id])

    def test_getScoringStandardDeviation_multiWeekMatchups(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1.1,
            teamBScore=2.1,
            multiWeekMatchupId="1",
        )
        matchup2_a = Matchup(
            teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3.1, teamBScore=4.1
        )
        matchup3_a = Matchup(
            teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4.1, teamBScore=5.1
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1.2,
            teamBScore=2.2,
            multiWeekMatchupId="1",
        )
        matchup2_b = Matchup(
            teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.2, teamBScore=4.2
        )
        matchup3_b = Matchup(
            teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.2, teamBScore=5.2
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1.3, teamBScore=2.3
        )
        matchup2_c = Matchup(
            teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3.3, teamBScore=4.3
        )
        matchup3_c = Matchup(
            teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4.3, teamBScore=5.3
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringStandardDeviationAllTimeCalculator.getScoringStandardDeviation(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.5"), response[owners[0].id])
        self.assertTrue(math.isclose(Deci("1"), response[owners[1].id]))
        self.assertEqual(Deci("0.08164965809277260327324280249"), response[owners[2].id])
        self.assertEqual(Deci("0.08164965809277260327324280249"), response[owners[3].id])
        self.assertEqual(Deci("0.08164965809277260327324280249"), response[owners[4].id])
        self.assertEqual(Deci("0.08164965809277260327324280249"), response[owners[5].id])

    def test_getScoringStandardDeviation_noneIfNoGamesPlayed(self):
        owners, teamsA = getNDefaultOwnersAndTeams(3)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1.1, teamBScore=2.1
        )
        matchup2_a = Matchup(
            teamAId=teamsA[1].id, teamBId=teamsA[2].id, teamAScore=3.1, teamBScore=4.1
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])

        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a])

        league = League(name="TEST", owners=owners, years=[yearA])

        response = ScoringStandardDeviationAllTimeCalculator.getScoringStandardDeviation(
            league, weekNumberEnd=1
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(3, len(response.keys()))
        self.assertEqual(Deci("0"), response[owners[0].id])
        self.assertEqual(Deci("0"), response[owners[1].id])
        self.assertIsNone(response[owners[2].id])

    def test_getScoringStandardDeviation_onlyPostSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1.1,
            teamBScore=2.1,
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
            teamBScore=5.1,
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
            teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.2, teamBScore=5.2
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
            teamBScore=5.3,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringStandardDeviationAllTimeCalculator.getScoringStandardDeviation(
            league, onlyPostSeason=True
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[owners[0].id])
        self.assertEqual(Deci("0"), response[owners[1].id])
        self.assertEqual(Deci("0.1"), response[owners[2].id])
        self.assertEqual(Deci("0.1"), response[owners[3].id])
        self.assertEqual(Deci("0.1"), response[owners[4].id])
        self.assertEqual(Deci("0.1"), response[owners[5].id])

    def test_getScoringStandardDeviation_onlyRegularSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1.1,
            teamBScore=2.1,
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
            teamBScore=5.1,
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
            teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.2, teamBScore=5.2
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
            teamBScore=5.3,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringStandardDeviationAllTimeCalculator.getScoringStandardDeviation(
            league, onlyRegularSeason=True
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[owners[0].id])
        self.assertEqual(Deci("0"), response[owners[1].id])
        self.assertEqual(Deci("0"), response[owners[2].id])
        self.assertEqual(Deci("0"), response[owners[3].id])
        self.assertEqual(Deci("0"), response[owners[4].id])
        self.assertEqual(Deci("0"), response[owners[5].id])

    def test_getScoringStandardDeviation_onlyChampionshipIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1.1,
            teamBScore=2.1,
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
            teamBScore=5.1,
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
            teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.2, teamBScore=5.2
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
            teamBScore=5.3,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringStandardDeviationAllTimeCalculator.getScoringStandardDeviation(
            league, onlyChampionship=True
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertIsNone(response[owners[0].id])
        self.assertIsNone(response[owners[1].id])
        self.assertIsNone(response[owners[2].id])
        self.assertIsNone(response[owners[3].id])
        self.assertEqual(Deci("0.1"), response[owners[4].id])
        self.assertEqual(Deci("0.1"), response[owners[5].id])

    def test_getScoringStandardDeviation_yearNumberStartGivenWeekNumberStartGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1.1,
            teamBScore=2.1,
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
            teamBScore=5.1,
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
            teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.2, teamBScore=5.2
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        matchup4_b = Matchup(
            teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.2, teamBScore=2.2
        )
        matchup5_b = Matchup(
            teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.2, teamBScore=4.2
        )
        matchup6_b = Matchup(
            teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.2, teamBScore=5.2
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
            teamBScore=5.3,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringStandardDeviationAllTimeCalculator.getScoringStandardDeviation(
            league, yearNumberStart=2001, weekNumberStart=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.05"), response[owners[0].id])
        self.assertEqual(Deci("0.05"), response[owners[1].id])
        self.assertEqual(Deci("0.05"), response[owners[2].id])
        self.assertEqual(Deci("0.05"), response[owners[3].id])
        self.assertEqual(Deci("0.05"), response[owners[4].id])
        self.assertEqual(Deci("0.05"), response[owners[5].id])

    def test_getScoringStandardDeviation_yearNumberEndGivenWeekNumberEndGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1.1,
            teamBScore=2.1,
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
            teamBScore=5.1,
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
            teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.2, teamBScore=5.2
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        matchup4_b = Matchup(
            teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.2, teamBScore=2.2
        )
        matchup5_b = Matchup(
            teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.2, teamBScore=4.2
        )
        matchup6_b = Matchup(
            teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.2, teamBScore=5.2
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
            teamBScore=5.3,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringStandardDeviationAllTimeCalculator.getScoringStandardDeviation(
            league, yearNumberEnd=2001, weekNumberEnd=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[owners[0].id])
        self.assertEqual(Deci("0"), response[owners[1].id])
        self.assertEqual(Deci("0.04714045207910316829338962414"), response[owners[2].id])
        self.assertEqual(Deci("0.04714045207910316829338962414"), response[owners[3].id])
        self.assertEqual(Deci("0.04714045207910316829338962414"), response[owners[4].id])
        self.assertEqual(Deci("0.04714045207910316829338962414"), response[owners[5].id])

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
            teamBScore=2.1,
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
            teamBScore=5.1,
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
            teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.2, teamBScore=5.2
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        matchup4_b = Matchup(
            teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.2, teamBScore=2.2
        )
        matchup5_b = Matchup(
            teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.2, teamBScore=4.2
        )
        matchup6_b = Matchup(
            teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.2, teamBScore=5.2
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
            teamBScore=5.3,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = ScoringStandardDeviationAllTimeCalculator.getScoringStandardDeviation(
            league, yearNumberStart=2001, weekNumberStart=1, yearNumberEnd=2001, weekNumberEnd=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[owners[0].id])
        self.assertEqual(Deci("0"), response[owners[1].id])
        self.assertEqual(Deci("0"), response[owners[2].id])
        self.assertEqual(Deci("0"), response[owners[3].id])
        self.assertEqual(Deci("0"), response[owners[4].id])
        self.assertEqual(Deci("0"), response[owners[5].id])
