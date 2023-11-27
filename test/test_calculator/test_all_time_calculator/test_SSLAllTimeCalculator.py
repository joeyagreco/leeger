import unittest
from test.helper.prototypes import getNDefaultOwnersAndTeams, getTeamsFromOwners

from leeger.calculator.all_time_calculator.SSLAllTimeCalculator import SSLAllTimeCalculator
from leeger.enum.MatchupType import MatchupType
from leeger.model.league.League import League
from leeger.model.league.Matchup import Matchup
from leeger.model.league.Week import Week
from leeger.model.league.Year import Year
from leeger.util.Deci import Deci


class TestSSLAllTimeCalculator(unittest.TestCase):
    def test_getAdjustedTeamScore_happyPath(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        matchup2_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a])

        matchup1_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=10,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        league = League(name="TEST", owners=owners, years=[yearA, yearB])

        response = SSLAllTimeCalculator.getAdjustedTeamScore(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("133.7333333333333199600000000"), response[owners[0].id])
        self.assertEqual(Deci("166.8666666666666499800000000"), response[owners[1].id])

    def test_getAdjustedTeamScore_noneIfNoGamesPlayed(self):
        owners, teamsA = getNDefaultOwnersAndTeams(3)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        matchup2_a = Matchup(teamAId=teamsA[1].id, teamBId=teamsA[2].id, teamAScore=1, teamBScore=2)
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a])

        league = League(name="TEST", owners=owners, years=[yearA])
        response = SSLAllTimeCalculator.getAdjustedTeamScore(league, weekNumberEnd=1)

        self.assertIsInstance(response, dict)
        self.assertEqual(3, len(response.keys()))
        self.assertEqual(Deci("66.76666666666666666666666666"), response[owners[0].id])
        self.assertEqual(Deci("233.5333333333333333333333333"), response[owners[1].id])
        self.assertIsNone(response[owners[2].id])

    def test_getAdjustedTeamScore_onlyPostSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=10,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        league = League(name="TEST", owners=owners, years=[yearA, yearB])

        response = SSLAllTimeCalculator.getAdjustedTeamScore(league, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("133.7333333333333199600000000"), response[owners[0].id])
        self.assertEqual(Deci("166.8666666666666499800000000"), response[owners[1].id])

    def test_getAdjustedTeamScore_onlyRegularSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        matchup2_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(
            teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=10, teamBScore=2
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        league = League(name="TEST", owners=owners, years=[yearA, yearB])

        response = SSLAllTimeCalculator.getAdjustedTeamScore(league, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("133.7333333333333199600000000"), response[owners[0].id])
        self.assertEqual(Deci("166.8666666666666499800000000"), response[owners[1].id])

    def test_getAdjustedTeamScore_onlyChampionshipIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        matchup2_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=10,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        league = League(name="TEST", owners=owners, years=[yearA, yearB])

        response = SSLAllTimeCalculator.getAdjustedTeamScore(league, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("167.2166666666666666666666667"), response[owners[0].id])
        self.assertEqual(Deci("133.5333333333333333333333333"), response[owners[1].id])

    def test_getAdjustedTeamScore_yearNumberStartGivenWeekNumberStartGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=10,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        yearA = Year(yearNumber=1999, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        matchup2_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2000, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=10,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        yearC = Year(yearNumber=2001, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SSLAllTimeCalculator.getAdjustedTeamScore(
            league, yearNumberStart=2000, weekNumberStart=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("133.7333333333333199600000000"), response[owners[0].id])
        self.assertEqual(Deci("166.8666666666666499800000000"), response[owners[1].id])

    def test_getAdjustedTeamScore_yearNumberEndGivenWeekNumberEndGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=10,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        yearA = Year(yearNumber=1999, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        matchup2_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2000, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=10,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        yearC = Year(yearNumber=2001, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SSLAllTimeCalculator.getAdjustedTeamScore(
            league, yearNumberEnd=2000, weekNumberEnd=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("133.7333333333333199600000000"), response[owners[0].id])
        self.assertEqual(Deci("166.8666666666666499800000000"), response[owners[1].id])

    def test_getAdjustedTeamScore_yearNumberStartGivenWeekNumberStartGivenAndYearNumberEndGivenWeekNumberEndGiven(
        self,
    ):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=10,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        yearA = Year(yearNumber=1999, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        matchup2_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2000, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=10,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=10,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        yearC = Year(yearNumber=2001, teams=teamsC, weeks=[week1_c, week2_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SSLAllTimeCalculator.getAdjustedTeamScore(
            league, yearNumberStart=2000, weekNumberStart=2, yearNumberEnd=2001, weekNumberEnd=1
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("133.7333333333333199600000000"), response[owners[0].id])
        self.assertEqual(Deci("166.8666666666666499800000000"), response[owners[1].id])

    def test_getAdjustedTeamSuccess_happyPath(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        matchup2_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a])

        matchup1_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=10,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        league = League(name="TEST", owners=owners, years=[yearA, yearB])

        response = SSLAllTimeCalculator.getAdjustedTeamSuccess(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("133.7333333333333199600000000"), response[owners[0].id])
        self.assertEqual(Deci("166.8666666666666499800000000"), response[owners[1].id])

    def test_getAdjustedTeamSuccess_noneIfNoGamesPlayed(self):
        owners, teamsA = getNDefaultOwnersAndTeams(3)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        matchup2_a = Matchup(teamAId=teamsA[1].id, teamBId=teamsA[2].id, teamAScore=1, teamBScore=2)
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a])

        league = League(name="TEST", owners=owners, years=[yearA])
        response = SSLAllTimeCalculator.getAdjustedTeamSuccess(league, weekNumberEnd=1)

        self.assertIsInstance(response, dict)
        self.assertEqual(3, len(response.keys()))
        self.assertEqual(Deci("66.76666666666666666666666666"), response[owners[0].id])
        self.assertEqual(Deci("233.5333333333333333333333333"), response[owners[1].id])
        self.assertIsNone(response[owners[2].id])

    def test_getAdjustedTeamSuccess_onlyPostSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=10,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        league = League(name="TEST", owners=owners, years=[yearA, yearB])

        response = SSLAllTimeCalculator.getAdjustedTeamSuccess(league, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("133.7333333333333199600000000"), response[owners[0].id])
        self.assertEqual(Deci("166.8666666666666499800000000"), response[owners[1].id])

    def test_getAdjustedTeamSuccess_onlyRegularSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        matchup2_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(
            teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=10, teamBScore=2
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        league = League(name="TEST", owners=owners, years=[yearA, yearB])

        response = SSLAllTimeCalculator.getAdjustedTeamSuccess(league, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("133.7333333333333199600000000"), response[owners[0].id])
        self.assertEqual(Deci("166.8666666666666499800000000"), response[owners[1].id])

    def test_getAdjustedTeamSuccess_onlyChampionshipIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        matchup2_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=10,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        league = League(name="TEST", owners=owners, years=[yearA, yearB])

        response = SSLAllTimeCalculator.getAdjustedTeamSuccess(league, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("167.2166666666666666666666667"), response[owners[0].id])
        self.assertEqual(Deci("133.5333333333333333333333333"), response[owners[1].id])

    def test_getAdjustedTeamSuccess_yearNumberStartGivenWeekNumberStartGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=10,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        yearA = Year(yearNumber=1999, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        matchup2_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2000, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=10,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        yearC = Year(yearNumber=2001, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SSLAllTimeCalculator.getAdjustedTeamSuccess(
            league, yearNumberStart=2000, weekNumberStart=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("133.7333333333333199600000000"), response[owners[0].id])
        self.assertEqual(Deci("166.8666666666666499800000000"), response[owners[1].id])

    def test_getAdjustedTeamSuccess_yearNumberEndGivenWeekNumberEndGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=10,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        yearA = Year(yearNumber=1999, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        matchup2_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2000, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=10,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        yearC = Year(yearNumber=2001, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SSLAllTimeCalculator.getAdjustedTeamSuccess(
            league, yearNumberEnd=2000, weekNumberEnd=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("133.7333333333333199600000000"), response[owners[0].id])
        self.assertEqual(Deci("166.8666666666666499800000000"), response[owners[1].id])

    def test_getAdjustedTeamSuccess_yearNumberStartGivenWeekNumberStartGivenAndYearNumberEndGivenWeekNumberEndGiven(
        self,
    ):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=10,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        yearA = Year(yearNumber=1999, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        matchup2_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2000, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=10,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=10,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        yearC = Year(yearNumber=2001, teams=teamsC, weeks=[week1_c, week2_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SSLAllTimeCalculator.getAdjustedTeamSuccess(
            league, yearNumberStart=2000, weekNumberStart=2, yearNumberEnd=2001, weekNumberEnd=1
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("133.7333333333333199600000000"), response[owners[0].id])
        self.assertEqual(Deci("166.8666666666666499800000000"), response[owners[1].id])

    def test_getAdjustedTeamLuck_happyPath(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        matchup2_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a])

        matchup1_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=10,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        league = League(name="TEST", owners=owners, years=[yearA, yearB])

        response = SSLAllTimeCalculator.getAdjustedTeamLuck(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0"), response[owners[0].id])
        self.assertEqual(Deci("0"), response[owners[1].id])

    def test_getAdjustedTeamLuck_noneIfNoGamesPlayed(self):
        owners, teamsA = getNDefaultOwnersAndTeams(3)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        matchup2_a = Matchup(teamAId=teamsA[1].id, teamBId=teamsA[2].id, teamAScore=1, teamBScore=2)
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a])

        league = League(name="TEST", owners=owners, years=[yearA])
        response = SSLAllTimeCalculator.getAdjustedTeamLuck(league, weekNumberEnd=1)

        self.assertIsInstance(response, dict)
        self.assertEqual(3, len(response.keys()))
        self.assertEqual(Deci("0"), response[owners[0].id])
        self.assertEqual(Deci("0"), response[owners[1].id])
        self.assertIsNone(response[owners[2].id])

    def test_getAdjustedTeamLuck_onlyPostSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=10,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        league = League(name="TEST", owners=owners, years=[yearA, yearB])

        response = SSLAllTimeCalculator.getAdjustedTeamLuck(league, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0"), response[owners[0].id])
        self.assertEqual(Deci("0"), response[owners[1].id])

    def test_getAdjustedTeamLuck_onlyRegularSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        matchup2_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(
            teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=10, teamBScore=2
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        league = League(name="TEST", owners=owners, years=[yearA, yearB])

        response = SSLAllTimeCalculator.getAdjustedTeamLuck(league, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0"), response[owners[0].id])
        self.assertEqual(Deci("0"), response[owners[1].id])

    def test_getAdjustedTeamLuck_onlyChampionshipIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        matchup2_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=10,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        league = League(name="TEST", owners=owners, years=[yearA, yearB])

        response = SSLAllTimeCalculator.getAdjustedTeamLuck(league, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0"), response[owners[0].id])
        self.assertEqual(Deci("0"), response[owners[1].id])

    def test_getAdjustedTeamLuck_yearNumberStartGivenWeekNumberStartGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=10,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        yearA = Year(yearNumber=1999, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        matchup2_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2000, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=10,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        yearC = Year(yearNumber=2001, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SSLAllTimeCalculator.getAdjustedTeamLuck(
            league, yearNumberStart=2000, weekNumberStart=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0"), response[owners[0].id])
        self.assertEqual(Deci("0"), response[owners[1].id])

    def test_getAdjustedTeamLuck_yearNumberEndGivenWeekNumberEndGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=10,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        yearA = Year(yearNumber=1999, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        matchup2_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2000, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=10,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        yearC = Year(yearNumber=2001, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SSLAllTimeCalculator.getAdjustedTeamLuck(
            league, yearNumberEnd=2000, weekNumberEnd=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0"), response[owners[0].id])
        self.assertEqual(Deci("0"), response[owners[1].id])

    def test_getAdjustedTeamLuck_yearNumberStartGivenWeekNumberStartGivenAndYearNumberEndGivenWeekNumberEndGiven(
        self,
    ):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=10,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        yearA = Year(yearNumber=1999, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        matchup2_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2000, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=10,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=10,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        yearC = Year(yearNumber=2001, teams=teamsC, weeks=[week1_c, week2_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SSLAllTimeCalculator.getAdjustedTeamLuck(
            league, yearNumberStart=2000, weekNumberStart=2, yearNumberEnd=2001, weekNumberEnd=1
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0"), response[owners[0].id])
        self.assertEqual(Deci("0"), response[owners[1].id])
