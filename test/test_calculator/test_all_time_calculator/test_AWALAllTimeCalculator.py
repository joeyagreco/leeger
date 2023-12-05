import unittest
from test.helper.prototypes import (getNDefaultOwnersAndTeams,
                                    getTeamsFromOwners)

from leeger.calculator.all_time_calculator import AWALAllTimeCalculator
from leeger.enum.MatchupType import MatchupType
from leeger.model.league import YearSettings
from leeger.model.league.League import League
from leeger.model.league.Matchup import Matchup
from leeger.model.league.Week import Week
from leeger.model.league.Year import Year
from leeger.util.Deci import Deci


class TestAWALAllTimeCalculator(unittest.TestCase):
    def test_getAWAL_happyPath(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
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

        response = AWALAllTimeCalculator.getAWAL(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[owners[0].id])
        self.assertEqual(Deci("0.6"), response[owners[1].id])
        self.assertEqual(Deci("1.2"), response[owners[2].id])
        self.assertEqual(Deci("2.1"), response[owners[3].id])
        self.assertEqual(Deci("2.1"), response[owners[4].id])
        self.assertEqual(Deci("3"), response[owners[5].id])

    def test_getAWAL_leagueMedianGamesIsOn_addsLeagueMedianWinsToAWAL(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)
        yearSettings = YearSettings(leagueMedianGames=True)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3, teamBScore=4)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4, teamBScore=5)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a], yearSettings=yearSettings)

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b], yearSettings=yearSettings)

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3, teamBScore=4)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4, teamBScore=5)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c], yearSettings=yearSettings)

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = AWALAllTimeCalculator.getAWAL(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[owners[0].id])
        self.assertEqual(Deci("0.6"), response[owners[1].id])
        self.assertEqual(Deci("1.2"), response[owners[2].id])
        self.assertEqual(Deci("5.1"), response[owners[3].id])
        self.assertEqual(Deci("5.1"), response[owners[4].id])
        self.assertEqual(Deci("6"), response[owners[5].id])

    def test_getAWAL_noneIfNoGamesPlayed(self):
        owners, teamsA = getNDefaultOwnersAndTeams(3)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[1].id, teamBId=teamsA[2].id, teamAScore=3, teamBScore=4)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a])

        league = League(name="TEST", owners=owners, years=[yearA])

        response = AWALAllTimeCalculator.getAWAL(league, weekNumberEnd=1)

        self.assertIsInstance(response, dict)
        self.assertEqual(3, len(response.keys()))
        self.assertEqual(Deci("0"), response[owners[0].id])
        self.assertEqual(Deci("1"), response[owners[1].id])
        self.assertIsNone(response[owners[2].id])

    def test_getAWAL_onlyPostSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3, teamBScore=4)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4, teamBScore=5)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_b = Matchup(
            teamAId=teamsB[2].id,
            teamBId=teamsB[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[4].id,
            teamBId=teamsB[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.PLAYOFF,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3, teamBScore=4)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4, teamBScore=5)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = AWALAllTimeCalculator.getAWAL(league, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[owners[0].id])
        self.assertEqual(Deci("0.2"), response[owners[1].id])
        self.assertEqual(Deci("0.4"), response[owners[2].id])
        self.assertEqual(Deci("0.7"), response[owners[3].id])
        self.assertEqual(Deci("0.7"), response[owners[4].id])
        self.assertEqual(Deci("1"), response[owners[5].id])

    def test_getAWAL_onlyRegularSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3, teamBScore=4)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4, teamBScore=5)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_b = Matchup(
            teamAId=teamsB[2].id,
            teamBId=teamsB[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[4].id,
            teamBId=teamsB[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.PLAYOFF,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3, teamBScore=4)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4, teamBScore=5)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = AWALAllTimeCalculator.getAWAL(league, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[owners[0].id])
        self.assertEqual(Deci("0.4"), response[owners[1].id])
        self.assertEqual(Deci("0.8"), response[owners[2].id])
        self.assertEqual(Deci("1.4"), response[owners[3].id])
        self.assertEqual(Deci("1.4"), response[owners[4].id])
        self.assertEqual(Deci("2"), response[owners[5].id])

    def test_getAWAL_onlyChampionshipIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3, teamBScore=4)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4, teamBScore=5)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_b = Matchup(
            teamAId=teamsB[2].id,
            teamBId=teamsB[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[4].id,
            teamBId=teamsB[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3, teamBScore=4)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4, teamBScore=5)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = AWALAllTimeCalculator.getAWAL(league, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertIsNone(response[owners[0].id])
        self.assertIsNone(response[owners[1].id])
        self.assertIsNone(response[owners[2].id])
        self.assertIsNone(response[owners[3].id])
        self.assertEqual(Deci("0"), response[owners[4].id])
        self.assertEqual(Deci("1"), response[owners[5].id])

    def test_getAWAL_yearNumberStartGivenWeekNumberStartGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3, teamBScore=4)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4, teamBScore=5)
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

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3, teamBScore=4)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4, teamBScore=5)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = AWALAllTimeCalculator.getAWAL(league, yearNumberStart=2001, weekNumberStart=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[owners[0].id])
        self.assertEqual(Deci("0.4"), response[owners[1].id])
        self.assertEqual(Deci("0.8"), response[owners[2].id])
        self.assertEqual(Deci("1.4"), response[owners[3].id])
        self.assertEqual(Deci("1.4"), response[owners[4].id])
        self.assertEqual(Deci("2"), response[owners[5].id])

    def test_getAWAL_yearNumberEndGivenWeekNumberEndGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3, teamBScore=4)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4, teamBScore=5)
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

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3, teamBScore=4)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4, teamBScore=5)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = AWALAllTimeCalculator.getAWAL(league, yearNumberEnd=2001, weekNumberEnd=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[owners[0].id])
        self.assertEqual(Deci("0.6"), response[owners[1].id])
        self.assertEqual(Deci("1.2"), response[owners[2].id])
        self.assertEqual(Deci("2.1"), response[owners[3].id])
        self.assertEqual(Deci("2.1"), response[owners[4].id])
        self.assertEqual(Deci("3"), response[owners[5].id])

    def test_getAWAL_yearNumberStartGivenWeekNumberStartGivenAndYearNumberEndGivenWeekNumberEndGiven(
        self,
    ):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3, teamBScore=4)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4, teamBScore=5)
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

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3, teamBScore=4)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4, teamBScore=5)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = AWALAllTimeCalculator.getAWAL(
            league, yearNumberStart=2001, weekNumberStart=1, yearNumberEnd=2001, weekNumberEnd=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[owners[0].id])
        self.assertEqual(Deci("0.4"), response[owners[1].id])
        self.assertEqual(Deci("0.8"), response[owners[2].id])
        self.assertEqual(Deci("1.4"), response[owners[3].id])
        self.assertEqual(Deci("1.4"), response[owners[4].id])
        self.assertEqual(Deci("2"), response[owners[5].id])

    def test_getAWALPerGame_happyPath(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
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

        response = AWALAllTimeCalculator.getAWALPerGame(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[owners[0].id])
        self.assertEqual(Deci("0.2"), response[owners[1].id])
        self.assertEqual(Deci("0.4"), response[owners[2].id])
        self.assertEqual(Deci("0.7"), response[owners[3].id])
        self.assertEqual(Deci("0.7"), response[owners[4].id])
        self.assertEqual(Deci("1"), response[owners[5].id])

    def test_getAWALPerGame_leagueMedianGamesIsOn(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)
        yearSettings = YearSettings(leagueMedianGames=True)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3, teamBScore=4)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4, teamBScore=5)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a], yearSettings=yearSettings)

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b], yearSettings=yearSettings)

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3, teamBScore=4)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4, teamBScore=5)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c], yearSettings=yearSettings)

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = AWALAllTimeCalculator.getAWALPerGame(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[owners[0].id])
        self.assertEqual(Deci("0.1"), response[owners[1].id])
        self.assertEqual(Deci("0.2"), response[owners[2].id])
        self.assertEqual(Deci("0.85"), response[owners[3].id])
        self.assertEqual(Deci("0.85"), response[owners[4].id])
        self.assertEqual(Deci("1"), response[owners[5].id])

    def test_getAWALPerGame_noneIfNoGamesPlayed(self):
        owners, teamsA = getNDefaultOwnersAndTeams(3)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[1].id, teamBId=teamsA[2].id, teamAScore=3, teamBScore=4)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a])

        league = League(name="TEST", owners=owners, years=[yearA])

        response = AWALAllTimeCalculator.getAWALPerGame(league, weekNumberEnd=1)

        self.assertIsInstance(response, dict)
        self.assertEqual(3, len(response.keys()))
        self.assertEqual(Deci("0"), response[owners[0].id])
        self.assertEqual(Deci("1"), response[owners[1].id])
        self.assertIsNone(response[owners[2].id])

    def test_getAWALPerGame_onlyPostSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3, teamBScore=4)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4, teamBScore=5)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_b = Matchup(
            teamAId=teamsB[2].id,
            teamBId=teamsB[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[4].id,
            teamBId=teamsB[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.PLAYOFF,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3, teamBScore=4)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4, teamBScore=5)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = AWALAllTimeCalculator.getAWALPerGame(league, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[owners[0].id])
        self.assertEqual(Deci("0.2"), response[owners[1].id])
        self.assertEqual(Deci("0.4"), response[owners[2].id])
        self.assertEqual(Deci("0.7"), response[owners[3].id])
        self.assertEqual(Deci("0.7"), response[owners[4].id])
        self.assertEqual(Deci("1"), response[owners[5].id])

    def test_getAWALPerGame_onlyRegularSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3, teamBScore=4)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4, teamBScore=5)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_b = Matchup(
            teamAId=teamsB[2].id,
            teamBId=teamsB[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[4].id,
            teamBId=teamsB[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.PLAYOFF,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3, teamBScore=4)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4, teamBScore=5)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = AWALAllTimeCalculator.getAWALPerGame(league, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[owners[0].id])
        self.assertEqual(Deci("0.2"), response[owners[1].id])
        self.assertEqual(Deci("0.4"), response[owners[2].id])
        self.assertEqual(Deci("0.7"), response[owners[3].id])
        self.assertEqual(Deci("0.7"), response[owners[4].id])
        self.assertEqual(Deci("1"), response[owners[5].id])

    def test_getAWALPerGame_onlyChampionshipIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3, teamBScore=4)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4, teamBScore=5)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_b = Matchup(
            teamAId=teamsB[2].id,
            teamBId=teamsB[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[4].id,
            teamBId=teamsB[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3, teamBScore=4)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4, teamBScore=5)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = AWALAllTimeCalculator.getAWALPerGame(league, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertIsNone(response[owners[0].id])
        self.assertIsNone(response[owners[1].id])
        self.assertIsNone(response[owners[2].id])
        self.assertIsNone(response[owners[3].id])
        self.assertEqual(Deci("0"), response[owners[4].id])
        self.assertEqual(Deci("1"), response[owners[5].id])

    def test_getAWALPerGame_yearNumberStartGivenWeekNumberStartGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3, teamBScore=4)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4, teamBScore=5)
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

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3, teamBScore=4)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4, teamBScore=5)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = AWALAllTimeCalculator.getAWALPerGame(
            league, yearNumberStart=2001, weekNumberStart=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[owners[0].id])
        self.assertEqual(Deci("0.2"), response[owners[1].id])
        self.assertEqual(Deci("0.4"), response[owners[2].id])
        self.assertEqual(Deci("0.7"), response[owners[3].id])
        self.assertEqual(Deci("0.7"), response[owners[4].id])
        self.assertEqual(Deci("1"), response[owners[5].id])

    def test_getAWALPerGame_yearNumberEndGivenWeekNumberEndGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3, teamBScore=4)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4, teamBScore=5)
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

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3, teamBScore=4)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4, teamBScore=5)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = AWALAllTimeCalculator.getAWALPerGame(league, yearNumberEnd=2001, weekNumberEnd=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[owners[0].id])
        self.assertEqual(Deci("0.2"), response[owners[1].id])
        self.assertEqual(Deci("0.4"), response[owners[2].id])
        self.assertEqual(Deci("0.7"), response[owners[3].id])
        self.assertEqual(Deci("0.7"), response[owners[4].id])
        self.assertEqual(Deci("1"), response[owners[5].id])

    def test_getAWALPerGame_yearNumberStartGivenWeekNumberStartGivenAndYearNumberEndGivenWeekNumberEndGiven(
        self,
    ):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3, teamBScore=4)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4, teamBScore=5)
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

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3, teamBScore=4)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4, teamBScore=5)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = AWALAllTimeCalculator.getAWALPerGame(
            league, yearNumberStart=2001, weekNumberStart=1, yearNumberEnd=2001, weekNumberEnd=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[owners[0].id])
        self.assertEqual(Deci("0.2"), response[owners[1].id])
        self.assertEqual(Deci("0.4"), response[owners[2].id])
        self.assertEqual(Deci("0.7"), response[owners[3].id])
        self.assertEqual(Deci("0.7"), response[owners[4].id])
        self.assertEqual(Deci("1"), response[owners[5].id])

    def test_getOpponentAWAL_happyPath(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
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

        response = AWALAllTimeCalculator.getOpponentAWAL(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.6"), response[owners[0].id])
        self.assertEqual(Deci("0"), response[owners[1].id])
        self.assertEqual(Deci("2.1"), response[owners[2].id])
        self.assertEqual(Deci("1.2"), response[owners[3].id])
        self.assertEqual(Deci("3"), response[owners[4].id])
        self.assertEqual(Deci("2.1"), response[owners[5].id])

    def test_getOpponentAWAL_leagueMedianGamesIsOn_countsLeagueMedianGames(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)
        yearSettings = YearSettings(leagueMedianGames=True)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3, teamBScore=4)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4, teamBScore=5)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a], yearSettings=yearSettings)

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b], yearSettings=yearSettings)

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3, teamBScore=4)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4, teamBScore=5)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c], yearSettings=yearSettings)

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = AWALAllTimeCalculator.getOpponentAWAL(league)
        test = AWALAllTimeCalculator.getAWAL(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.6"), response[owners[0].id])
        self.assertEqual(Deci("0"), response[owners[1].id])
        self.assertEqual(Deci("5.1"), response[owners[2].id])
        self.assertEqual(Deci("1.2"), response[owners[3].id])
        self.assertEqual(Deci("6"), response[owners[4].id])
        self.assertEqual(Deci("5.1"), response[owners[5].id])

    def test_getOpponentAWAL_noneIfNoGamesPlayed(self):
        owners, teamsA = getNDefaultOwnersAndTeams(3)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[1].id, teamBId=teamsA[2].id, teamAScore=3, teamBScore=4)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a])

        league = League(name="TEST", owners=owners, years=[yearA])

        response = AWALAllTimeCalculator.getOpponentAWAL(league, weekNumberEnd=1)

        self.assertIsInstance(response, dict)
        self.assertEqual(3, len(response.keys()))
        self.assertEqual(Deci("1"), response[owners[0].id])
        self.assertEqual(Deci("0"), response[owners[1].id])
        self.assertIsNone(response[owners[2].id])

    def test_getOpponentAWAL_onlyPostSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3, teamBScore=4)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4, teamBScore=5)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_b = Matchup(
            teamAId=teamsB[2].id,
            teamBId=teamsB[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[4].id,
            teamBId=teamsB[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.PLAYOFF,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3, teamBScore=4)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4, teamBScore=5)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = AWALAllTimeCalculator.getOpponentAWAL(league, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.2"), response[owners[0].id])
        self.assertEqual(Deci("0"), response[owners[1].id])
        self.assertEqual(Deci("0.7"), response[owners[2].id])
        self.assertEqual(Deci("0.4"), response[owners[3].id])
        self.assertEqual(Deci("1"), response[owners[4].id])
        self.assertEqual(Deci("0.7"), response[owners[5].id])

    def test_getOpponentAWAL_onlyRegularSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3, teamBScore=4)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4, teamBScore=5)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_b = Matchup(
            teamAId=teamsB[2].id,
            teamBId=teamsB[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[4].id,
            teamBId=teamsB[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.PLAYOFF,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3, teamBScore=4)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4, teamBScore=5)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = AWALAllTimeCalculator.getOpponentAWAL(league, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.4"), response[owners[0].id])
        self.assertEqual(Deci("0"), response[owners[1].id])
        self.assertEqual(Deci("1.4"), response[owners[2].id])
        self.assertEqual(Deci("0.8"), response[owners[3].id])
        self.assertEqual(Deci("2"), response[owners[4].id])
        self.assertEqual(Deci("1.4"), response[owners[5].id])

    def test_getOpponentAWAL_onlyChampionshipIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3, teamBScore=4)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4, teamBScore=5)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_b = Matchup(
            teamAId=teamsB[2].id,
            teamBId=teamsB[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[4].id,
            teamBId=teamsB[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3, teamBScore=4)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4, teamBScore=5)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = AWALAllTimeCalculator.getOpponentAWAL(league, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertIsNone(response[owners[0].id])
        self.assertIsNone(response[owners[1].id])
        self.assertIsNone(response[owners[2].id])
        self.assertIsNone(response[owners[3].id])
        self.assertEqual(Deci("1"), response[owners[4].id])
        self.assertEqual(Deci("0"), response[owners[5].id])

    def test_getOpponentAWAL_yearNumberStartGivenWeekNumberStartGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3, teamBScore=4)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4, teamBScore=5)
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

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3, teamBScore=4)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4, teamBScore=5)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = AWALAllTimeCalculator.getOpponentAWAL(
            league, yearNumberStart=2001, weekNumberStart=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.4"), response[owners[0].id])
        self.assertEqual(Deci("0"), response[owners[1].id])
        self.assertEqual(Deci("1.4"), response[owners[2].id])
        self.assertEqual(Deci("0.8"), response[owners[3].id])
        self.assertEqual(Deci("2"), response[owners[4].id])
        self.assertEqual(Deci("1.4"), response[owners[5].id])

    def test_getOpponentAWAL_yearNumberEndGivenWeekNumberEndGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3, teamBScore=4)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4, teamBScore=5)
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

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3, teamBScore=4)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4, teamBScore=5)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = AWALAllTimeCalculator.getOpponentAWAL(
            league, yearNumberEnd=2001, weekNumberEnd=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.6"), response[owners[0].id])
        self.assertEqual(Deci("0"), response[owners[1].id])
        self.assertEqual(Deci("2.1"), response[owners[2].id])
        self.assertEqual(Deci("1.2"), response[owners[3].id])
        self.assertEqual(Deci("3"), response[owners[4].id])
        self.assertEqual(Deci("2.1"), response[owners[5].id])

    def test_getOpponentAWAL_yearNumberStartGivenWeekNumberStartGivenAndYearNumberEndGivenWeekNumberEndGiven(
        self,
    ):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3, teamBScore=4)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4, teamBScore=5)
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

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3, teamBScore=4)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4, teamBScore=5)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = AWALAllTimeCalculator.getOpponentAWAL(
            league, yearNumberStart=2001, weekNumberStart=1, yearNumberEnd=2001, weekNumberEnd=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.4"), response[owners[0].id])
        self.assertEqual(Deci("0"), response[owners[1].id])
        self.assertEqual(Deci("1.4"), response[owners[2].id])
        self.assertEqual(Deci("0.8"), response[owners[3].id])
        self.assertEqual(Deci("2"), response[owners[4].id])
        self.assertEqual(Deci("1.4"), response[owners[5].id])

    def test_getOpponentAWALPerGame_happyPath(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
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

        response = AWALAllTimeCalculator.getOpponentAWALPerGame(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.2"), response[owners[0].id])
        self.assertEqual(Deci("0"), response[owners[1].id])
        self.assertEqual(Deci("0.7"), response[owners[2].id])
        self.assertEqual(Deci("0.4"), response[owners[3].id])
        self.assertEqual(Deci("1"), response[owners[4].id])
        self.assertEqual(Deci("0.7"), response[owners[5].id])

    def test_getOpponentAWALPerGame_leagueMedianGamesIsOn(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)
        yearSettings = YearSettings(leagueMedianGames=True)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3, teamBScore=4)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4, teamBScore=5)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a], yearSettings=yearSettings)

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3, teamBScore=4)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4, teamBScore=5)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b], yearSettings=yearSettings)

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3, teamBScore=4)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4, teamBScore=5)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c], yearSettings=yearSettings)

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = AWALAllTimeCalculator.getOpponentAWALPerGame(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.1"), response[owners[0].id])
        self.assertEqual(Deci("0"), response[owners[1].id])
        self.assertEqual(Deci("0.85"), response[owners[2].id])
        self.assertEqual(Deci("0.2"), response[owners[3].id])
        self.assertEqual(Deci("1"), response[owners[4].id])
        self.assertEqual(Deci("0.85"), response[owners[5].id])

    def test_getOpponentAWALPerGame_noneIfNoGamesPlayed(self):
        owners, teamsA = getNDefaultOwnersAndTeams(3)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[1].id, teamBId=teamsA[2].id, teamAScore=3, teamBScore=4)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a])

        league = League(name="TEST", owners=owners, years=[yearA])

        response = AWALAllTimeCalculator.getOpponentAWALPerGame(league, weekNumberEnd=1)

        self.assertIsInstance(response, dict)
        self.assertEqual(3, len(response.keys()))
        self.assertEqual(Deci("1"), response[owners[0].id])
        self.assertEqual(Deci("0"), response[owners[1].id])
        self.assertIsNone(response[owners[2].id])

    def test_getOpponentAWALPerGame_onlyPostSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3, teamBScore=4)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4, teamBScore=5)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_b = Matchup(
            teamAId=teamsB[2].id,
            teamBId=teamsB[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[4].id,
            teamBId=teamsB[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.PLAYOFF,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3, teamBScore=4)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4, teamBScore=5)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = AWALAllTimeCalculator.getOpponentAWALPerGame(league, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.2"), response[owners[0].id])
        self.assertEqual(Deci("0"), response[owners[1].id])
        self.assertEqual(Deci("0.7"), response[owners[2].id])
        self.assertEqual(Deci("0.4"), response[owners[3].id])
        self.assertEqual(Deci("1"), response[owners[4].id])
        self.assertEqual(Deci("0.7"), response[owners[5].id])

    def test_getOpponentAWALPerGame_onlyRegularSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3, teamBScore=4)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4, teamBScore=5)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_b = Matchup(
            teamAId=teamsB[2].id,
            teamBId=teamsB[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[4].id,
            teamBId=teamsB[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.PLAYOFF,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3, teamBScore=4)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4, teamBScore=5)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = AWALAllTimeCalculator.getOpponentAWALPerGame(league, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.2"), response[owners[0].id])
        self.assertEqual(Deci("0"), response[owners[1].id])
        self.assertEqual(Deci("0.7"), response[owners[2].id])
        self.assertEqual(Deci("0.4"), response[owners[3].id])
        self.assertEqual(Deci("1"), response[owners[4].id])
        self.assertEqual(Deci("0.7"), response[owners[5].id])

    def test_getOpponentAWALPerGame_onlyChampionshipIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3, teamBScore=4)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4, teamBScore=5)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2_b = Matchup(
            teamAId=teamsB[2].id,
            teamBId=teamsB[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[4].id,
            teamBId=teamsB[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3, teamBScore=4)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4, teamBScore=5)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = AWALAllTimeCalculator.getOpponentAWALPerGame(league, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertIsNone(response[owners[0].id])
        self.assertIsNone(response[owners[1].id])
        self.assertIsNone(response[owners[2].id])
        self.assertIsNone(response[owners[3].id])
        self.assertEqual(Deci("1"), response[owners[4].id])
        self.assertEqual(Deci("0"), response[owners[5].id])

    def test_getOpponentAWALPerGame_yearNumberStartGivenWeekNumberStartGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3, teamBScore=4)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4, teamBScore=5)
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

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3, teamBScore=4)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4, teamBScore=5)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = AWALAllTimeCalculator.getOpponentAWALPerGame(
            league, yearNumberStart=2001, weekNumberStart=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.2"), response[owners[0].id])
        self.assertEqual(Deci("0"), response[owners[1].id])
        self.assertEqual(Deci("0.7"), response[owners[2].id])
        self.assertEqual(Deci("0.4"), response[owners[3].id])
        self.assertEqual(Deci("1"), response[owners[4].id])
        self.assertEqual(Deci("0.7"), response[owners[5].id])

    def test_getOpponentAWALPerGame_yearNumberEndGivenWeekNumberEndGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3, teamBScore=4)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4, teamBScore=5)
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

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3, teamBScore=4)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4, teamBScore=5)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = AWALAllTimeCalculator.getOpponentAWALPerGame(
            league, yearNumberEnd=2001, weekNumberEnd=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.2"), response[owners[0].id])
        self.assertEqual(Deci("0"), response[owners[1].id])
        self.assertEqual(Deci("0.7"), response[owners[2].id])
        self.assertEqual(Deci("0.4"), response[owners[3].id])
        self.assertEqual(Deci("1"), response[owners[4].id])
        self.assertEqual(Deci("0.7"), response[owners[5].id])

    def test_getOpponentAWALPerGame_yearNumberStartGivenWeekNumberStartGivenAndYearNumberEndGivenWeekNumberEndGiven(
        self,
    ):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3, teamBScore=4)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4, teamBScore=5)
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

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3, teamBScore=4)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4, teamBScore=5)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = AWALAllTimeCalculator.getOpponentAWALPerGame(
            league, yearNumberStart=2001, weekNumberStart=1, yearNumberEnd=2001, weekNumberEnd=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.2"), response[owners[0].id])
        self.assertEqual(Deci("0"), response[owners[1].id])
        self.assertEqual(Deci("0.7"), response[owners[2].id])
        self.assertEqual(Deci("0.4"), response[owners[3].id])
        self.assertEqual(Deci("1"), response[owners[4].id])
        self.assertEqual(Deci("0.7"), response[owners[5].id])
