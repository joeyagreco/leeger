import unittest

from leeger.calculator.all_time_calculator.GameOutcomeAllTimeCalculator import (
    GameOutcomeAllTimeCalculator,
)
from leeger.enum.MatchupType import MatchupType
from leeger.model.league import YearSettings
from leeger.model.league.League import League
from leeger.model.league.Matchup import Matchup
from leeger.model.league.Week import Week
from leeger.model.league.Year import Year
from leeger.util.Deci import Deci
from test.helper.prototypes import getNDefaultOwnersAndTeams, getTeamsFromOwners


class TestGameOutcomeAllTimeCalculator(unittest.TestCase):
    def test_getWins_happyPath(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getWins(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(0, response[owners[0].id])
        self.assertEqual(9, response[owners[1].id])

    def test_getWins_nonAnnualOwner(self):
        ownersA, teamsA = getNDefaultOwnersAndTeams(2, randomNames=True)
        ownersB, teamsB = getNDefaultOwnersAndTeams(2, randomNames=True)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        league = League(name="TEST", owners=ownersA + ownersB, years=[yearA, yearB])

        response = GameOutcomeAllTimeCalculator.getWins(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(4, len(response.keys()))
        self.assertEqual(0, response[ownersA[0].id])
        self.assertEqual(3, response[ownersA[1].id])
        self.assertEqual(0, response[ownersB[0].id])
        self.assertEqual(3, response[ownersB[1].id])

    def test_getWins_multiWeekMatchups(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=3,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
            multiWeekMatchupId="1",
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=3,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
            multiWeekMatchupId="1",
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getWins(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(1, response[owners[0].id])
        self.assertEqual(7, response[owners[1].id])

    def test_getWins_noneIfNoGamesPlayed(self):
        owners, teamsA = getNDefaultOwnersAndTeams(3)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[1].id, teamBId=teamsA[2].id, teamAScore=1, teamBScore=2)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a])

        league = League(name="TEST", owners=owners, years=[yearA])

        response = GameOutcomeAllTimeCalculator.getWins(league, weekNumberEnd=1)

        self.assertIsInstance(response, dict)
        self.assertEqual(3, len(response.keys()))
        self.assertEqual(0, response[owners[0].id])
        self.assertEqual(1, response[owners[1].id])
        self.assertIsNone(response[owners[2].id])

    def test_getWins_onlyPostSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getWins(league, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(0, response[owners[0].id])
        self.assertEqual(6, response[owners[1].id])

    def test_getWins_onlyRegularSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getWins(league, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(0, response[owners[0].id])
        self.assertEqual(3, response[owners[1].id])

    def test_getWins_onlyChampionshipIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getWins(league, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(0, response[owners[0].id])
        self.assertEqual(3, response[owners[1].id])

    def test_getWins_yearNumberStartGivenWeekNumberStartGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getWins(
            league, yearNumberStart=2001, weekNumberStart=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(0, response[owners[0].id])
        self.assertEqual(5, response[owners[1].id])

    def test_getWins_yearNumberEndGivenWeekNumberEndGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getWins(league, yearNumberEnd=2001, weekNumberEnd=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(0, response[owners[0].id])
        self.assertEqual(5, response[owners[1].id])

    def test_getWins_yearNumberStartGivenWeekNumberStartGivenAndYearNumberEndGivenWeekNumberEndGiven(
        self,
    ):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)
        teamsD = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        matchup1_d = Matchup(teamAId=teamsD[0].id, teamBId=teamsD[1].id, teamAScore=1, teamBScore=2)
        matchup2_d = Matchup(
            teamAId=teamsD[0].id,
            teamBId=teamsD[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_d = Matchup(
            teamAId=teamsD[0].id,
            teamBId=teamsD[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_d = Week(weekNumber=1, matchups=[matchup1_d])
        week2_d = Week(weekNumber=2, matchups=[matchup2_d])
        week3_d = Week(weekNumber=3, matchups=[matchup3_d])
        yearD = Year(yearNumber=2003, teams=teamsD, weeks=[week1_d, week2_d, week3_d])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC, yearD])

        response = GameOutcomeAllTimeCalculator.getWins(
            league, yearNumberStart=2001, weekNumberStart=2, yearNumberEnd=2002, weekNumberEnd=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(0, response[owners[0].id])
        self.assertEqual(4, response[owners[1].id])

    def test_getLosses_happyPath(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getLosses(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(9, response[owners[0].id])
        self.assertEqual(0, response[owners[1].id])

    def test_getLosses_nonAnnualOwner(self):
        ownersA, teamsA = getNDefaultOwnersAndTeams(2, randomNames=True)
        ownersB, teamsB = getNDefaultOwnersAndTeams(2, randomNames=True)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        league = League(name="TEST", owners=ownersA + ownersB, years=[yearA, yearB])

        response = GameOutcomeAllTimeCalculator.getLosses(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(4, len(response.keys()))
        self.assertEqual(3, response[ownersA[0].id])
        self.assertEqual(0, response[ownersA[1].id])
        self.assertEqual(3, response[ownersB[0].id])
        self.assertEqual(0, response[ownersB[1].id])

    def test_getLosses_multiWeekMatchups(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=3,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
            multiWeekMatchupId="1",
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=3,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
            multiWeekMatchupId="1",
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getLosses(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(7, response[owners[0].id])
        self.assertEqual(1, response[owners[1].id])

    def test_getLosses_noneIfNoGamesPlayed(self):
        owners, teamsA = getNDefaultOwnersAndTeams(3)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[1].id, teamBId=teamsA[2].id, teamAScore=1, teamBScore=2)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a])

        league = League(name="TEST", owners=owners, years=[yearA])

        response = GameOutcomeAllTimeCalculator.getLosses(league, weekNumberEnd=1)

        self.assertIsInstance(response, dict)
        self.assertEqual(3, len(response.keys()))
        self.assertEqual(1, response[owners[0].id])
        self.assertEqual(0, response[owners[1].id])
        self.assertIsNone(response[owners[2].id])

    def test_getLosses_onlyPostSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getLosses(league, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(6, response[owners[0].id])
        self.assertEqual(0, response[owners[1].id])

    def test_getLosses_onlyRegularSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getLosses(league, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(3, response[owners[0].id])
        self.assertEqual(0, response[owners[1].id])

    def test_getLosses_onlyChampionshipIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getLosses(league, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(3, response[owners[0].id])
        self.assertEqual(0, response[owners[1].id])

    def test_getLosses_yearNumberStartGivenWeekNumberStartGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getLosses(
            league, yearNumberStart=2001, weekNumberStart=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(5, response[owners[0].id])
        self.assertEqual(0, response[owners[1].id])

    def test_getLosses_yearNumberEndGivenWeekNumberEndGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getLosses(
            league, yearNumberEnd=2001, weekNumberEnd=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(5, response[owners[0].id])
        self.assertEqual(0, response[owners[1].id])

    def test_getLosses_yearNumberStartGivenWeekNumberStartGivenAndYearNumberEndGivenWeekNumberEndGiven(
        self,
    ):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)
        teamsD = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        matchup1_d = Matchup(teamAId=teamsD[0].id, teamBId=teamsD[1].id, teamAScore=1, teamBScore=2)
        matchup2_d = Matchup(
            teamAId=teamsD[0].id,
            teamBId=teamsD[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_d = Matchup(
            teamAId=teamsD[0].id,
            teamBId=teamsD[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_d = Week(weekNumber=1, matchups=[matchup1_d])
        week2_d = Week(weekNumber=2, matchups=[matchup2_d])
        week3_d = Week(weekNumber=3, matchups=[matchup3_d])
        yearD = Year(yearNumber=2003, teams=teamsD, weeks=[week1_d, week2_d, week3_d])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC, yearD])

        response = GameOutcomeAllTimeCalculator.getLosses(
            league, yearNumberStart=2001, weekNumberStart=2, yearNumberEnd=2002, weekNumberEnd=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(4, response[owners[0].id])
        self.assertEqual(0, response[owners[1].id])

    def test_getTies_happyPath(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=1)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=1)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=1)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getTies(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(3, response[owners[0].id])
        self.assertEqual(3, response[owners[1].id])

    def test_getTies_nonAnnualOwner(self):
        ownersA, teamsA = getNDefaultOwnersAndTeams(2, randomNames=True)
        ownersB, teamsB = getNDefaultOwnersAndTeams(2, randomNames=True)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=1)
        matchup2_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=1)
        matchup3_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=1)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=1)
        matchup2_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=1)
        matchup3_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=1)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        league = League(name="TEST", owners=ownersA + ownersB, years=[yearA, yearB])

        response = GameOutcomeAllTimeCalculator.getTies(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(4, len(response.keys()))
        self.assertEqual(3, response[ownersA[0].id])
        self.assertEqual(3, response[ownersA[1].id])
        self.assertEqual(3, response[ownersB[0].id])
        self.assertEqual(3, response[ownersB[1].id])

    def test_getTies_multiWeekMatchups(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=1,
            multiWeekMatchupId="1",
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=1,
            multiWeekMatchupId="1",
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=1)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=1)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getTies(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(3, response[owners[0].id])
        self.assertEqual(3, response[owners[1].id])

    def test_getTies_noneIfNoGamesPlayed(self):
        owners, teamsA = getNDefaultOwnersAndTeams(3)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=1)
        matchup2_a = Matchup(teamAId=teamsA[1].id, teamBId=teamsA[2].id, teamAScore=1, teamBScore=1)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a])

        league = League(name="TEST", owners=owners, years=[yearA])

        response = GameOutcomeAllTimeCalculator.getTies(league, weekNumberEnd=1)

        self.assertIsInstance(response, dict)
        self.assertEqual(3, len(response.keys()))
        self.assertEqual(1, response[owners[0].id])
        self.assertEqual(1, response[owners[1].id])
        self.assertIsNone(response[owners[2].id])

    def test_getTies_onlyPostSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=1)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=1)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=1)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getTies(league, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(0, response[owners[0].id])
        self.assertEqual(0, response[owners[1].id])

    def test_getTies_onlyRegularSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=1)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=1)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=1)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getTies(league, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(3, response[owners[0].id])
        self.assertEqual(3, response[owners[1].id])

    def test_getTies_onlyChampionshipIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=1)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=1)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=1)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getTies(league, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(0, response[owners[0].id])
        self.assertEqual(0, response[owners[1].id])

    def test_getTies_yearNumberStartGivenWeekNumberStartGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=1)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=1)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=1)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getTies(
            league, yearNumberStart=2001, weekNumberStart=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(1, response[owners[0].id])
        self.assertEqual(1, response[owners[1].id])

    def test_getTies_yearNumberEndGivenWeekNumberEndGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=1)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=1)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=1)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getTies(league, yearNumberEnd=2001, weekNumberEnd=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(2, response[owners[0].id])
        self.assertEqual(2, response[owners[1].id])

    def test_getTies_yearNumberStartGivenWeekNumberStartGivenAndYearNumberEndGivenWeekNumberEndGiven(
        self,
    ):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)
        teamsD = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=1)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=1)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=1)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        matchup1_d = Matchup(teamAId=teamsD[0].id, teamBId=teamsD[1].id, teamAScore=1, teamBScore=2)
        matchup2_d = Matchup(
            teamAId=teamsD[0].id,
            teamBId=teamsD[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_d = Matchup(
            teamAId=teamsD[0].id,
            teamBId=teamsD[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_d = Week(weekNumber=1, matchups=[matchup1_d])
        week2_d = Week(weekNumber=2, matchups=[matchup2_d])
        week3_d = Week(weekNumber=3, matchups=[matchup3_d])
        yearD = Year(yearNumber=2003, teams=teamsD, weeks=[week1_d, week2_d, week3_d])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC, yearD])

        response = GameOutcomeAllTimeCalculator.getTies(
            league, yearNumberStart=2001, weekNumberStart=2, yearNumberEnd=2002, weekNumberEnd=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(1, response[owners[0].id])
        self.assertEqual(1, response[owners[1].id])

    def test_getWinPercentage_happyPath(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=2, teamBScore=1)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getWinPercentage(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.4444444444444444444444444444"), response[owners[0].id])
        self.assertEqual(Deci("0.5555555555555555555555555556"), response[owners[1].id])

    def test_getWinPercentage_nonAnnualOwner(self):
        ownersA, teamsA = getNDefaultOwnersAndTeams(2, randomNames=True)
        ownersB, teamsB = getNDefaultOwnersAndTeams(2, randomNames=True)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=2, teamBScore=1)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=2, teamBScore=1)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        league = League(name="TEST", owners=ownersA + ownersB, years=[yearA, yearB])

        response = GameOutcomeAllTimeCalculator.getWinPercentage(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(4, len(response.keys()))
        self.assertEqual(Deci("0.3333333333333333333333333333"), response[ownersA[0].id])
        self.assertEqual(Deci("0.6666666666666666666666666667"), response[ownersA[1].id])
        self.assertEqual(Deci("0.3333333333333333333333333333"), response[ownersB[0].id])
        self.assertEqual(Deci("0.6666666666666666666666666667"), response[ownersB[1].id])

    def test_getWinPercentage_leagueMedianGamesIsOn_happyPath(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)
        yearSettings = YearSettings(leagueMedianGames=True)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup3_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(
            yearNumber=2000,
            teams=teamsA,
            weeks=[week1_a, week2_a, week3_a],
            yearSettings=yearSettings,
        )

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=2, teamBScore=1)
        matchup2_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=2, teamBScore=1)
        matchup3_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=2, teamBScore=1)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(
            yearNumber=2001,
            teams=teamsB,
            weeks=[week1_b, week2_b, week3_b],
            yearSettings=yearSettings,
        )

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=2, teamBScore=1)
        matchup3_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(
            yearNumber=2002,
            teams=teamsC,
            weeks=[week1_c, week2_c, week3_c],
            yearSettings=yearSettings,
        )

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getWinPercentage(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.4444444444444444444444444444"), response[owners[0].id])
        self.assertEqual(Deci("0.5555555555555555555555555556"), response[owners[1].id])

    def test_getWinPercentage_multiWeekMatchups(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
            multiWeekMatchupId="1",
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
            multiWeekMatchupId="1",
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=1)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getWinPercentage(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.4375"), response[owners[0].id])
        self.assertEqual(Deci("0.5625"), response[owners[1].id])

    def test_getWinPercentage_noneIfNoGamesPlayed(self):
        owners, teamsA = getNDefaultOwnersAndTeams(3)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[1].id, teamBId=teamsA[2].id, teamAScore=1, teamBScore=2)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a])

        league = League(name="TEST", owners=owners, years=[yearA])

        response = GameOutcomeAllTimeCalculator.getWinPercentage(league, weekNumberEnd=1)

        self.assertIsInstance(response, dict)
        self.assertEqual(3, len(response.keys()))
        self.assertEqual(Deci("0"), response[owners[0].id])
        self.assertEqual(Deci("1"), response[owners[1].id])
        self.assertIsNone(response[owners[2].id])

    def test_getWinPercentage_onlyPostSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=2, teamBScore=1)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getWinPercentage(league, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.1666666666666666666666666667"), response[owners[0].id])
        self.assertEqual(Deci("0.8333333333333333333333333333"), response[owners[1].id])

    def test_getWinPercentage_onlyRegularSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=2, teamBScore=1)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getWinPercentage(league, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.3333333333333333333333333333"), response[owners[0].id])
        self.assertEqual(Deci("0.6666666666666666666666666667"), response[owners[1].id])

    def test_getWinPercentage_onlyChampionshipIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getWinPercentage(league, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.3333333333333333333333333333"), response[owners[0].id])
        self.assertEqual(Deci("0.6666666666666666666666666667"), response[owners[1].id])

    def test_getWinPercentage_yearNumberStartGivenWeekNumberStartGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=2, teamBScore=1)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getWinPercentage(
            league, yearNumberStart=2001, weekNumberStart=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("1"), response[owners[0].id])
        self.assertEqual(Deci("0"), response[owners[1].id])

    def test_getWinPercentage_yearNumberEndGivenWeekNumberEndGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=2, teamBScore=1)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=2, teamBScore=1)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getWinPercentage(
            league, yearNumberEnd=2001, weekNumberEnd=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("1"), response[owners[0].id])
        self.assertEqual(Deci("0"), response[owners[1].id])

    def test_getWinPercentage_yearNumberStartGivenWeekNumberStartGivenAndYearNumberEndGivenWeekNumberEndGiven(
        self,
    ):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)
        teamsD = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=2, teamBScore=1)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        matchup1_d = Matchup(teamAId=teamsD[0].id, teamBId=teamsD[1].id, teamAScore=1, teamBScore=2)
        matchup2_d = Matchup(
            teamAId=teamsD[0].id,
            teamBId=teamsD[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_d = Matchup(
            teamAId=teamsD[0].id,
            teamBId=teamsD[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_d = Week(weekNumber=1, matchups=[matchup1_d])
        week2_d = Week(weekNumber=2, matchups=[matchup2_d])
        week3_d = Week(weekNumber=3, matchups=[matchup3_d])
        yearD = Year(yearNumber=2003, teams=teamsD, weeks=[week1_d, week2_d, week3_d])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC, yearD])

        response = GameOutcomeAllTimeCalculator.getWinPercentage(
            league, yearNumberStart=2001, weekNumberStart=2, yearNumberEnd=2002, weekNumberEnd=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("1"), response[owners[0].id])
        self.assertEqual(Deci("0"), response[owners[1].id])

    def test_getWAL_happyPath(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=2, teamBScore=1)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=1)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getWAL(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("4.5"), response[owners[0].id])
        self.assertEqual(Deci("4.5"), response[owners[1].id])

    def test_getWAL_nonAnnualOwner(self):
        ownersA, teamsA = getNDefaultOwnersAndTeams(2, randomNames=True)
        ownersB, teamsB = getNDefaultOwnersAndTeams(2, randomNames=True)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=1)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=1)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        league = League(name="TEST", owners=ownersA + ownersB, years=[yearA, yearB])

        response = GameOutcomeAllTimeCalculator.getWAL(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(4, len(response.keys()))
        self.assertEqual(0.5, response[ownersA[0].id])
        self.assertEqual(2.5, response[ownersA[1].id])
        self.assertEqual(0.5, response[ownersB[0].id])
        self.assertEqual(2.5, response[ownersB[1].id])

    def test_getWAL_leagueMedianGamesIsTrue_happyPath(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)
        yearSettings = YearSettings(leagueMedianGames=True)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup3_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(
            yearNumber=2000,
            teams=teamsA,
            weeks=[week1_a, week2_a, week3_a],
            yearSettings=yearSettings,
        )

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=2, teamBScore=1)
        matchup2_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=2, teamBScore=1)
        matchup3_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=2, teamBScore=1)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(
            yearNumber=2001,
            teams=teamsB,
            weeks=[week1_b, week2_b, week3_b],
            yearSettings=yearSettings,
        )

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=1)
        matchup2_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=2, teamBScore=1)
        matchup3_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(
            yearNumber=2002,
            teams=teamsC,
            weeks=[week1_c, week2_c, week3_c],
            yearSettings=yearSettings,
        )

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getWAL(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("9"), response[owners[0].id])
        self.assertEqual(Deci("9"), response[owners[1].id])

    def test_getWAL_multiWeekMatchups(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
            multiWeekMatchupId="1",
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
            multiWeekMatchupId="1",
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=2, teamBScore=1)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=1)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getWAL(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("4.5"), response[owners[0].id])
        self.assertEqual(Deci("3.5"), response[owners[1].id])

    def test_getWAL_noneIfNoGamesPlayed(self):
        owners, teamsA = getNDefaultOwnersAndTeams(3)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[1].id, teamBId=teamsA[2].id, teamAScore=1, teamBScore=2)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a])

        league = League(name="TEST", owners=owners, years=[yearA])

        response = GameOutcomeAllTimeCalculator.getWAL(league, weekNumberEnd=1)

        self.assertIsInstance(response, dict)
        self.assertEqual(3, len(response.keys()))
        self.assertEqual(Deci("0"), response[owners[0].id])
        self.assertEqual(Deci("1"), response[owners[1].id])
        self.assertIsNone(response[owners[2].id])

    def test_getWAL_onlyPostSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=2, teamBScore=1)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getWAL(league, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("1"), response[owners[0].id])
        self.assertEqual(Deci("5"), response[owners[1].id])

    def test_getWAL_onlyRegularSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=1)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=2, teamBScore=1)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getWAL(league, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("1.5"), response[owners[0].id])
        self.assertEqual(Deci("1.5"), response[owners[1].id])

    def test_getWAL_onlyChampionshipIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getWAL(league, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("1"), response[owners[0].id])
        self.assertEqual(Deci("2"), response[owners[1].id])

    def test_getWAL_yearNumberStartGivenWeekNumberStartGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=1)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getWAL(
            league, yearNumberStart=2001, weekNumberStart=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("2.5"), response[owners[0].id])
        self.assertEqual(Deci("2.5"), response[owners[1].id])

    def test_getWAL_yearNumberEndGivenWeekNumberEndGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=1)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getWAL(league, yearNumberEnd=2001, weekNumberEnd=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("2.5"), response[owners[0].id])
        self.assertEqual(Deci("2.5"), response[owners[1].id])

    def test_getWAL_yearNumberStartGivenWeekNumberStartGivenAndYearNumberEndGivenWeekNumberEndGiven(
        self,
    ):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)
        teamsD = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=1)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        matchup1_d = Matchup(teamAId=teamsD[0].id, teamBId=teamsD[1].id, teamAScore=1, teamBScore=2)
        matchup2_d = Matchup(
            teamAId=teamsD[0].id,
            teamBId=teamsD[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_d = Matchup(
            teamAId=teamsD[0].id,
            teamBId=teamsD[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_d = Week(weekNumber=1, matchups=[matchup1_d])
        week2_d = Week(weekNumber=2, matchups=[matchup2_d])
        week3_d = Week(weekNumber=3, matchups=[matchup3_d])
        yearD = Year(yearNumber=2003, teams=teamsD, weeks=[week1_d, week2_d, week3_d])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC, yearD])

        response = GameOutcomeAllTimeCalculator.getWAL(
            league, yearNumberStart=2001, weekNumberStart=2, yearNumberEnd=2002, weekNumberEnd=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("2.5"), response[owners[0].id])
        self.assertEqual(Deci("1.5"), response[owners[1].id])

    def test_getWALPerGame_happyPath(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=2, teamBScore=1)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=1)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getWALPerGame(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.5"), response[owners[0].id])
        self.assertEqual(Deci("0.5"), response[owners[1].id])

    def test_getWALPerGame_nonAnnualOwner(self):
        ownersA, teamsA = getNDefaultOwnersAndTeams(2, randomNames=True)
        ownersB, teamsB = getNDefaultOwnersAndTeams(2, randomNames=True)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=1)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=1)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        league = League(name="TEST", owners=ownersA + ownersB, years=[yearA, yearB])

        response = GameOutcomeAllTimeCalculator.getWALPerGame(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(4, len(response.keys()))
        self.assertEqual(Deci("0.1666666666666666666666666667"), response[ownersA[0].id])
        self.assertEqual(Deci("0.8333333333333333333333333333"), response[ownersA[1].id])
        self.assertEqual(Deci("0.1666666666666666666666666667"), response[ownersB[0].id])
        self.assertEqual(Deci("0.8333333333333333333333333333"), response[ownersB[1].id])

    def test_getWALPerGame_leagueMedianGamesIsOn_happyPath(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)
        yearSettings = YearSettings(leagueMedianGames=True)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup3_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(
            yearNumber=2000,
            teams=teamsA,
            weeks=[week1_a, week2_a, week3_a],
            yearSettings=yearSettings,
        )

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=2, teamBScore=1)
        matchup2_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=2, teamBScore=1)
        matchup3_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=2, teamBScore=1)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(
            yearNumber=2001,
            teams=teamsB,
            weeks=[week1_b, week2_b, week3_b],
            yearSettings=yearSettings,
        )

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=1)
        matchup2_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=2, teamBScore=1)
        matchup3_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(
            yearNumber=2002,
            teams=teamsC,
            weeks=[week1_c, week2_c, week3_c],
            yearSettings=yearSettings,
        )

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getWALPerGame(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.5"), response[owners[0].id])
        self.assertEqual(Deci("0.5"), response[owners[1].id])

    def test_getWALPerGame_multiWeekMatchups(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
            multiWeekMatchupId="1",
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
            multiWeekMatchupId="1",
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=2, teamBScore=1)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=1)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getWALPerGame(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.5625"), response[owners[0].id])
        self.assertEqual(Deci("0.4375"), response[owners[1].id])

    def test_getWALPerGame_noneIfNoGamesPlayed(self):
        owners, teamsA = getNDefaultOwnersAndTeams(3)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[1].id, teamBId=teamsA[2].id, teamAScore=1, teamBScore=2)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a])

        league = League(name="TEST", owners=owners, years=[yearA])

        response = GameOutcomeAllTimeCalculator.getWALPerGame(league, weekNumberEnd=1)

        self.assertIsInstance(response, dict)
        self.assertEqual(3, len(response.keys()))
        self.assertEqual(Deci("0"), response[owners[0].id])
        self.assertEqual(Deci("1"), response[owners[1].id])
        self.assertIsNone(response[owners[2].id])

    def test_getWALPerGame_onlyPostSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=2, teamBScore=1)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getWALPerGame(league, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.1666666666666666666666666667"), response[owners[0].id])
        self.assertEqual(Deci("0.8333333333333333333333333333"), response[owners[1].id])

    def test_getWALPerGame_onlyRegularSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=1)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=2, teamBScore=1)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getWALPerGame(league, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.5"), response[owners[0].id])
        self.assertEqual(Deci("0.5"), response[owners[1].id])

    def test_getWALPerGame_onlyChampionshipIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getWALPerGame(league, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.3333333333333333333333333333"), response[owners[0].id])
        self.assertEqual(Deci("0.6666666666666666666666666667"), response[owners[1].id])

    def test_getWALPerGame_yearNumberStartGivenWeekNumberStartGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=1)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getWALPerGame(
            league, yearNumberStart=2001, weekNumberStart=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.5"), response[owners[0].id])
        self.assertEqual(Deci("0.5"), response[owners[1].id])

    def test_getWALPerGame_yearNumberEndGivenWeekNumberEndGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=1)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getWALPerGame(
            league, yearNumberEnd=2001, weekNumberEnd=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.5"), response[owners[0].id])
        self.assertEqual(Deci("0.5"), response[owners[1].id])

    def test_getWALPerGame_yearNumberStartGivenWeekNumberStartGivenAndYearNumberEndGivenWeekNumberEndGiven(
        self,
    ):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)
        teamsD = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=1)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        matchup1_d = Matchup(teamAId=teamsD[0].id, teamBId=teamsD[1].id, teamAScore=1, teamBScore=2)
        matchup2_d = Matchup(
            teamAId=teamsD[0].id,
            teamBId=teamsD[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_d = Matchup(
            teamAId=teamsD[0].id,
            teamBId=teamsD[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_d = Week(weekNumber=1, matchups=[matchup1_d])
        week2_d = Week(weekNumber=2, matchups=[matchup2_d])
        week3_d = Week(weekNumber=3, matchups=[matchup3_d])
        yearD = Year(yearNumber=2003, teams=teamsD, weeks=[week1_d, week2_d, week3_d])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC, yearD])

        response = GameOutcomeAllTimeCalculator.getWALPerGame(
            league, yearNumberStart=2001, weekNumberStart=2, yearNumberEnd=2002, weekNumberEnd=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.625"), response[owners[0].id])
        self.assertEqual(Deci("0.375"), response[owners[1].id])

    def test_getLeagueMedianWins_happyPath(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        yearSettings = YearSettings(leagueMedianGames=True)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup3_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(
            yearNumber=2000,
            teams=teamsA,
            weeks=[week1_a, week2_a, week3_a],
            yearSettings=yearSettings,
        )

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup3_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(
            yearNumber=2001,
            teams=teamsB,
            weeks=[week1_b, week2_b, week3_b],
            yearSettings=yearSettings,
        )

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup3_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(
            yearNumber=2002,
            teams=teamsC,
            weeks=[week1_c, week2_c, week3_c],
            yearSettings=yearSettings,
        )

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getLeagueMedianWins(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(0, response[owners[0].id])
        self.assertEqual(9, response[owners[1].id])

    def test_getLeagueMedianWins_yearsHaveLeagueMedianGamesOff_returnsZeroForEachTeam(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        yearSettings = YearSettings(leagueMedianGames=False)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup3_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(
            yearNumber=2000,
            teams=teamsA,
            weeks=[week1_a, week2_a, week3_a],
            yearSettings=yearSettings,
        )

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup3_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(
            yearNumber=2001,
            teams=teamsB,
            weeks=[week1_b, week2_b, week3_b],
            yearSettings=yearSettings,
        )

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup3_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(
            yearNumber=2002,
            teams=teamsC,
            weeks=[week1_c, week2_c, week3_c],
            yearSettings=yearSettings,
        )

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getLeagueMedianWins(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(0, response[owners[0].id])
        self.assertEqual(0, response[owners[1].id])

    def test_getLeagueMedianWins_tieForLeagueMedian_happyPath(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)
        yearSettings = YearSettings(leagueMedianGames=True)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=1)
        matchup2_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup3_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(
            yearNumber=2000,
            teams=teamsA,
            weeks=[week1_a, week2_a, week3_a],
            yearSettings=yearSettings,
        )

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=1)
        matchup2_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup3_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(
            yearNumber=2001,
            teams=teamsB,
            weeks=[week1_b, week2_b, week3_b],
            yearSettings=yearSettings,
        )

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=1)
        matchup2_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup3_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(
            yearNumber=2002,
            teams=teamsC,
            weeks=[week1_c, week2_c, week3_c],
            yearSettings=yearSettings,
        )

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getLeagueMedianWins(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("1.5"), response[owners[0].id])
        self.assertEqual(Deci("7.5"), response[owners[1].id])

    def test_getLeagueMedianWins_noneIfNoGamesPlayed(self):
        owners, teamsA = getNDefaultOwnersAndTeams(3)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[1].id, teamBId=teamsA[2].id, teamAScore=1, teamBScore=2)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        yearSettings = YearSettings(leagueMedianGames=True)
        yearA = Year(
            yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a], yearSettings=yearSettings
        )

        league = League(name="TEST", owners=owners, years=[yearA])

        response = GameOutcomeAllTimeCalculator.getLeagueMedianWins(league, weekNumberEnd=1)

        self.assertIsInstance(response, dict)
        self.assertEqual(3, len(response.keys()))
        self.assertEqual(0, response[owners[0].id])
        self.assertEqual(1, response[owners[1].id])
        self.assertIsNone(response[owners[2].id])

    def test_getLeagueMedianWins_onlyPostSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getLeagueMedianWins(league, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(0, response[owners[0].id])
        self.assertEqual(0, response[owners[1].id])

    def test_getLeagueMedianWins_onlyRegularSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)
        yearSettings = YearSettings(leagueMedianGames=True)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(
            yearNumber=2000,
            teams=teamsA,
            weeks=[week1_a, week2_a, week3_a],
            yearSettings=yearSettings,
        )

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(
            yearNumber=2001,
            teams=teamsB,
            weeks=[week1_b, week2_b, week3_b],
            yearSettings=yearSettings,
        )

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(
            yearNumber=2002,
            teams=teamsC,
            weeks=[week1_c, week2_c, week3_c],
            yearSettings=yearSettings,
        )

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getLeagueMedianWins(league, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(0, response[owners[0].id])
        self.assertEqual(3, response[owners[1].id])

    def test_getLeagueMedianWins_onlyChampionshipIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getLeagueMedianWins(league, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(0, response[owners[0].id])
        self.assertEqual(0, response[owners[1].id])

    def test_getLeagueMedianWins_yearNumberStartGivenWeekNumberStartGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup3_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearSettings = YearSettings(leagueMedianGames=True)

        yearA = Year(
            yearNumber=2000,
            teams=teamsA,
            weeks=[week1_a, week2_a, week3_a],
            yearSettings=yearSettings,
        )

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup3_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(
            yearNumber=2001,
            teams=teamsB,
            weeks=[week1_b, week2_b, week3_b],
            yearSettings=yearSettings,
        )

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup3_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(
            yearNumber=2002,
            teams=teamsC,
            weeks=[week1_c, week2_c, week3_c],
            yearSettings=yearSettings,
        )

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getLeagueMedianWins(
            league, yearNumberStart=2001, weekNumberStart=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(0, response[owners[0].id])
        self.assertEqual(5, response[owners[1].id])

    def test_getLeagueMedianWins_yearNumberEndGivenWeekNumberEndGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup3_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearSettings = YearSettings(leagueMedianGames=True)

        yearA = Year(
            yearNumber=2000,
            teams=teamsA,
            weeks=[week1_a, week2_a, week3_a],
            yearSettings=yearSettings,
        )

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup3_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(
            yearNumber=2001,
            teams=teamsB,
            weeks=[week1_b, week2_b, week3_b],
            yearSettings=yearSettings,
        )

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup3_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(
            yearNumber=2002,
            teams=teamsC,
            weeks=[week1_c, week2_c, week3_c],
            yearSettings=yearSettings,
        )

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getLeagueMedianWins(
            league, yearNumberEnd=2001, weekNumberEnd=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(0, response[owners[0].id])
        self.assertEqual(5, response[owners[1].id])

    def test_getLeagueMedianWins_yearNumberStartGivenWeekNumberStartGivenAndYearNumberEndGivenWeekNumberEndGiven(
        self,
    ):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)
        teamsD = getTeamsFromOwners(owners)
        yearSettings = YearSettings(leagueMedianGames=True)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup3_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(
            yearNumber=2000,
            teams=teamsA,
            weeks=[week1_a, week2_a, week3_a],
            yearSettings=yearSettings,
        )

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup3_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(
            yearNumber=2001,
            teams=teamsB,
            weeks=[week1_b, week2_b, week3_b],
            yearSettings=yearSettings,
        )

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup3_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(
            yearNumber=2002,
            teams=teamsC,
            weeks=[week1_c, week2_c, week3_c],
            yearSettings=yearSettings,
        )

        matchup1_d = Matchup(teamAId=teamsD[0].id, teamBId=teamsD[1].id, teamAScore=1, teamBScore=2)
        matchup2_d = Matchup(teamAId=teamsD[0].id, teamBId=teamsD[1].id, teamAScore=1, teamBScore=2)
        matchup3_d = Matchup(teamAId=teamsD[0].id, teamBId=teamsD[1].id, teamAScore=1, teamBScore=2)
        week1_d = Week(weekNumber=1, matchups=[matchup1_d])
        week2_d = Week(weekNumber=2, matchups=[matchup2_d])
        week3_d = Week(weekNumber=3, matchups=[matchup3_d])
        yearD = Year(yearNumber=2003, teams=teamsD, weeks=[week1_d, week2_d, week3_d])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC, yearD])

        response = GameOutcomeAllTimeCalculator.getLeagueMedianWins(
            league, yearNumberStart=2001, weekNumberStart=2, yearNumberEnd=2002, weekNumberEnd=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(0, response[owners[0].id])
        self.assertEqual(4, response[owners[1].id])

    def test_getOpponentLeagueMedianWins_happyPath(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        yearSettings = YearSettings(leagueMedianGames=True)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup3_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(
            yearNumber=2000,
            teams=teamsA,
            weeks=[week1_a, week2_a, week3_a],
            yearSettings=yearSettings,
        )

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup3_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(
            yearNumber=2001,
            teams=teamsB,
            weeks=[week1_b, week2_b, week3_b],
            yearSettings=yearSettings,
        )

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup3_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(
            yearNumber=2002,
            teams=teamsC,
            weeks=[week1_c, week2_c, week3_c],
            yearSettings=yearSettings,
        )

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getOpponentLeagueMedianWins(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(9, response[owners[0].id])
        self.assertEqual(0, response[owners[1].id])

    def test_getOpponentLeagueMedianWins_yearsHaveLeagueMedianGamesOff_returnsZeroForEachTeam(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        yearSettings = YearSettings(leagueMedianGames=False)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup3_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(
            yearNumber=2000,
            teams=teamsA,
            weeks=[week1_a, week2_a, week3_a],
            yearSettings=yearSettings,
        )

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup3_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(
            yearNumber=2001,
            teams=teamsB,
            weeks=[week1_b, week2_b, week3_b],
            yearSettings=yearSettings,
        )

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup3_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(
            yearNumber=2002,
            teams=teamsC,
            weeks=[week1_c, week2_c, week3_c],
            yearSettings=yearSettings,
        )

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getOpponentLeagueMedianWins(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(0, response[owners[0].id])
        self.assertEqual(0, response[owners[1].id])

    def test_getOpponentLeagueMedianWins_tieForLeagueMedian_happyPath(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)
        yearSettings = YearSettings(leagueMedianGames=True)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=1)
        matchup2_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup3_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(
            yearNumber=2000,
            teams=teamsA,
            weeks=[week1_a, week2_a, week3_a],
            yearSettings=yearSettings,
        )

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=1)
        matchup2_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup3_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(
            yearNumber=2001,
            teams=teamsB,
            weeks=[week1_b, week2_b, week3_b],
            yearSettings=yearSettings,
        )

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=1)
        matchup2_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup3_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(
            yearNumber=2002,
            teams=teamsC,
            weeks=[week1_c, week2_c, week3_c],
            yearSettings=yearSettings,
        )

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getOpponentLeagueMedianWins(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("7.5"), response[owners[0].id])
        self.assertEqual(Deci("1.5"), response[owners[1].id])

    def test_getOpponentLeagueMedianWins_noneIfNoGamesPlayed(self):
        owners, teamsA = getNDefaultOwnersAndTeams(3)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[1].id, teamBId=teamsA[2].id, teamAScore=1, teamBScore=2)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        yearSettings = YearSettings(leagueMedianGames=True)
        yearA = Year(
            yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a], yearSettings=yearSettings
        )

        league = League(name="TEST", owners=owners, years=[yearA])

        response = GameOutcomeAllTimeCalculator.getOpponentLeagueMedianWins(league, weekNumberEnd=1)

        self.assertIsInstance(response, dict)
        self.assertEqual(3, len(response.keys()))
        self.assertEqual(1, response[owners[0].id])
        self.assertEqual(0, response[owners[1].id])
        self.assertIsNone(response[owners[2].id])

    def test_getOpponentLeagueMedianWins_onlyPostSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getOpponentLeagueMedianWins(
            league, onlyPostSeason=True
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(0, response[owners[0].id])
        self.assertEqual(0, response[owners[1].id])

    def test_getOpponentLeagueMedianWins_onlyRegularSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)
        yearSettings = YearSettings(leagueMedianGames=True)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(
            yearNumber=2000,
            teams=teamsA,
            weeks=[week1_a, week2_a, week3_a],
            yearSettings=yearSettings,
        )

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(
            yearNumber=2001,
            teams=teamsB,
            weeks=[week1_b, week2_b, week3_b],
            yearSettings=yearSettings,
        )

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(
            yearNumber=2002,
            teams=teamsC,
            weeks=[week1_c, week2_c, week3_c],
            yearSettings=yearSettings,
        )

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getOpponentLeagueMedianWins(
            league, onlyRegularSeason=True
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(3, response[owners[0].id])
        self.assertEqual(0, response[owners[1].id])

    def test_getOpponentLeagueMedianWins_onlyChampionshipIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_a = Matchup(
            teamAId=teamsA[0].id,
            teamBId=teamsA[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_b = Matchup(
            teamAId=teamsB[0].id,
            teamBId=teamsB[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3_c = Matchup(
            teamAId=teamsC[0].id,
            teamBId=teamsC[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getOpponentLeagueMedianWins(
            league, onlyChampionship=True
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(0, response[owners[0].id])
        self.assertEqual(0, response[owners[1].id])

    def test_getOpponentLeagueMedianWins_yearNumberStartGivenWeekNumberStartGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup3_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearSettings = YearSettings(leagueMedianGames=True)

        yearA = Year(
            yearNumber=2000,
            teams=teamsA,
            weeks=[week1_a, week2_a, week3_a],
            yearSettings=yearSettings,
        )

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup3_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(
            yearNumber=2001,
            teams=teamsB,
            weeks=[week1_b, week2_b, week3_b],
            yearSettings=yearSettings,
        )

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup3_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(
            yearNumber=2002,
            teams=teamsC,
            weeks=[week1_c, week2_c, week3_c],
            yearSettings=yearSettings,
        )

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getOpponentLeagueMedianWins(
            league, yearNumberStart=2001, weekNumberStart=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(5, response[owners[0].id])
        self.assertEqual(0, response[owners[1].id])

    def test_getOpponentLeagueMedianWins_yearNumberEndGivenWeekNumberEndGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup3_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearSettings = YearSettings(leagueMedianGames=True)

        yearA = Year(
            yearNumber=2000,
            teams=teamsA,
            weeks=[week1_a, week2_a, week3_a],
            yearSettings=yearSettings,
        )

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup3_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(
            yearNumber=2001,
            teams=teamsB,
            weeks=[week1_b, week2_b, week3_b],
            yearSettings=yearSettings,
        )

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup3_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(
            yearNumber=2002,
            teams=teamsC,
            weeks=[week1_c, week2_c, week3_c],
            yearSettings=yearSettings,
        )

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = GameOutcomeAllTimeCalculator.getOpponentLeagueMedianWins(
            league, yearNumberEnd=2001, weekNumberEnd=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(5, response[owners[0].id])
        self.assertEqual(0, response[owners[1].id])

    def test_getOpponentLeagueMedianWins_yearNumberStartGivenWeekNumberStartGivenAndYearNumberEndGivenWeekNumberEndGiven(
        self,
    ):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)
        teamsD = getTeamsFromOwners(owners)
        yearSettings = YearSettings(leagueMedianGames=True)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup3_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(
            yearNumber=2000,
            teams=teamsA,
            weeks=[week1_a, week2_a, week3_a],
            yearSettings=yearSettings,
        )

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup3_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(
            yearNumber=2001,
            teams=teamsB,
            weeks=[week1_b, week2_b, week3_b],
            yearSettings=yearSettings,
        )

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup2_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup3_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(
            yearNumber=2002,
            teams=teamsC,
            weeks=[week1_c, week2_c, week3_c],
            yearSettings=yearSettings,
        )

        matchup1_d = Matchup(teamAId=teamsD[0].id, teamBId=teamsD[1].id, teamAScore=1, teamBScore=2)
        matchup2_d = Matchup(teamAId=teamsD[0].id, teamBId=teamsD[1].id, teamAScore=1, teamBScore=2)
        matchup3_d = Matchup(teamAId=teamsD[0].id, teamBId=teamsD[1].id, teamAScore=1, teamBScore=2)
        week1_d = Week(weekNumber=1, matchups=[matchup1_d])
        week2_d = Week(weekNumber=2, matchups=[matchup2_d])
        week3_d = Week(weekNumber=3, matchups=[matchup3_d])
        yearD = Year(yearNumber=2003, teams=teamsD, weeks=[week1_d, week2_d, week3_d])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC, yearD])

        response = GameOutcomeAllTimeCalculator.getOpponentLeagueMedianWins(
            league, yearNumberStart=2001, weekNumberStart=2, yearNumberEnd=2002, weekNumberEnd=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(4, response[owners[0].id])
        self.assertEqual(0, response[owners[1].id])
