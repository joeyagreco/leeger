import unittest

from leeger.calculator.year_calculator.SSLYearCalculator import SSLYearCalculator
from leeger.enum.MatchupType import MatchupType
from leeger.model.league.Matchup import Matchup
from leeger.model.league.Week import Week
from leeger.model.league.Year import Year
from leeger.util.Deci import Deci
from test.helper.prototypes import getNDefaultOwnersAndTeams


class TestSSLYearCalculator(unittest.TestCase):

    def test_getTeamScore_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=3)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=3,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.3, teamBScore=2.9,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = SSLYearCalculator.getTeamScore(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("57.72"), response[teams[0].id])
        self.assertEqual(Deci("242.695"), response[teams[1].id])

    def test_getTeamScore_noneIfNoGamesPlayed(self):
        owners, teams = getNDefaultOwnersAndTeams(3)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=3)
        matchup2 = Matchup(teamAId=teams[1].id, teamBId=teams[2].id, teamAScore=1.2, teamBScore=3)
        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2])

        response = SSLYearCalculator.getTeamScore(year, weekNumberEnd=1)

        self.assertIsInstance(response, dict)
        self.assertEqual(3, len(response.keys()))
        self.assertEqual(Deci("53.76853658536585365853658536"), response[teams[0].id])
        self.assertEqual(Deci("246.6414634146341463414634146"), response[teams[1].id])
        self.assertIsNone(response[teams[2].id])

    def test_getTeamScore_onlyPostSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=5, teamBScore=4)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=3,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.3, teamBScore=2.6,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = SSLYearCalculator.getTeamScore(year, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("61.85339506172839506172839506"), response[teams[0].id])
        self.assertEqual(Deci("238.5516049382716049382716049"), response[teams[1].id])

    def test_getTeamScore_onlyRegularSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=5)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=5, teamBScore=6,
                           matchupType=MatchupType.PLAYOFF)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = SSLYearCalculator.getTeamScore(year, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("47.53768041237113402061855670"), response[teams[0].id])
        self.assertEqual(Deci("252.9473195876288659793814433"), response[teams[1].id])

    def test_getTeamScore_onlyChampionshipIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=6, teamBScore=7,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=5, teamBScore=6,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1])

        response = SSLYearCalculator.getTeamScore(year, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertIsNone(response[teams[0].id])
        self.assertIsNone(response[teams[1].id])
        self.assertIsNone(response[teams[2].id])
        self.assertIsNone(response[teams[3].id])
        self.assertEqual(Deci("91.40909090909090909090909090"), response[teams[4].id])
        self.assertEqual(Deci("209.6909090909090909090909091"), response[teams[5].id])

    def test_getTeamScore_weekNumberStartGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=3, teamBScore=6)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=2.5)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.3, teamBScore=2.6,
                           matchupType=MatchupType.PLAYOFF)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = SSLYearCalculator.getTeamScore(year, weekNumberStart=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("65.91447368421052631578947368"), response[teams[0].id])
        self.assertEqual(Deci("234.4655263157894736842105263"), response[teams[1].id])

    def test_getTeamScore_weekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=2.5)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = SSLYearCalculator.getTeamScore(year, weekNumberEnd=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("64.00388888888888888888888888"), response[teams[0].id])
        self.assertEqual(Deci("236.3561111111111111111111111"), response[teams[1].id])

    def test_getTeamScore_weekNumberStartGivenAndWeekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=2.5)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.3, teamBScore=2.6,
                           matchupType=MatchupType.PLAYOFF)
        matchup4 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.4, teamBScore=2.7,
                           matchupType=MatchupType.PLAYOFF)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])
        week4 = Week(weekNumber=4, matchups=[matchup4])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3, week4])

        response = SSLYearCalculator.getTeamScore(year, weekNumberStart=2, weekNumberEnd=3)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("65.91447368421052631578947368"), response[teams[0].id])
        self.assertEqual(Deci("234.4655263157894736842105263"), response[teams[1].id])

    def test_getTeamSuccess_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=3)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=3,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.3, teamBScore=2.9,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = SSLYearCalculator.getTeamSuccess(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("57.72"), response[teams[0].id])
        self.assertEqual(Deci("242.695"), response[teams[1].id])

    def test_getTeamSuccess_noneIfNoGamesPlayed(self):
        owners, teams = getNDefaultOwnersAndTeams(3)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=3)
        matchup2 = Matchup(teamAId=teams[1].id, teamBId=teams[2].id, teamAScore=1.2, teamBScore=3)
        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2])

        response = SSLYearCalculator.getTeamSuccess(year, weekNumberEnd=1)

        self.assertIsInstance(response, dict)
        self.assertEqual(3, len(response.keys()))
        self.assertEqual(Deci("53.76853658536585365853658536"), response[teams[0].id])
        self.assertEqual(Deci("246.6414634146341463414634146"), response[teams[1].id])
        self.assertIsNone(response[teams[2].id])

    def test_getTeamSuccess_onlyPostSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=5, teamBScore=4)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=3,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.3, teamBScore=2.6,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = SSLYearCalculator.getTeamSuccess(year, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("61.85339506172839506172839506"), response[teams[0].id])
        self.assertEqual(Deci("238.5516049382716049382716049"), response[teams[1].id])

    def test_getTeamSuccess_onlyRegularSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=5)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=5, teamBScore=6,
                           matchupType=MatchupType.PLAYOFF)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = SSLYearCalculator.getTeamSuccess(year, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("47.53768041237113402061855670"), response[teams[0].id])
        self.assertEqual(Deci("252.9473195876288659793814433"), response[teams[1].id])

    def test_getTeamSuccess_onlyChampionshipIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=6, teamBScore=7,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=5, teamBScore=6,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1])

        response = SSLYearCalculator.getTeamSuccess(year, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertIsNone(response[teams[0].id])
        self.assertIsNone(response[teams[1].id])
        self.assertIsNone(response[teams[2].id])
        self.assertIsNone(response[teams[3].id])
        self.assertEqual(Deci("91.40909090909090909090909090"), response[teams[4].id])
        self.assertEqual(Deci("209.6909090909090909090909091"), response[teams[5].id])

    def test_getTeamSuccess_weekNumberStartGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=3, teamBScore=6)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=2.5)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.3, teamBScore=2.6,
                           matchupType=MatchupType.PLAYOFF)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = SSLYearCalculator.getTeamSuccess(year, weekNumberStart=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("65.91447368421052631578947368"), response[teams[0].id])
        self.assertEqual(Deci("234.4655263157894736842105263"), response[teams[1].id])

    def test_getTeamSuccess_weekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=2.5)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = SSLYearCalculator.getTeamSuccess(year, weekNumberEnd=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("64.00388888888888888888888888"), response[teams[0].id])
        self.assertEqual(Deci("236.3561111111111111111111111"), response[teams[1].id])

    def test_getTeamSuccess_weekNumberStartGivenAndWeekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=2.5)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.3, teamBScore=2.6,
                           matchupType=MatchupType.PLAYOFF)
        matchup4 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.4, teamBScore=2.7,
                           matchupType=MatchupType.PLAYOFF)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])
        week4 = Week(weekNumber=4, matchups=[matchup4])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3, week4])

        response = SSLYearCalculator.getTeamSuccess(year, weekNumberStart=2, weekNumberEnd=3)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("65.91447368421052631578947368"), response[teams[0].id])
        self.assertEqual(Deci("234.4655263157894736842105263"), response[teams[1].id])

    def test_getTeamLuck_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=3)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=3,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.3, teamBScore=2.9,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = SSLYearCalculator.getTeamLuck(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0"), response[teams[1].id])

    def test_getTeamLuck_noneIfNoGamesPlayed(self):
        owners, teams = getNDefaultOwnersAndTeams(3)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=3)
        matchup2 = Matchup(teamAId=teams[1].id, teamBId=teams[2].id, teamAScore=1.2, teamBScore=3)
        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2])

        response = SSLYearCalculator.getTeamLuck(year, weekNumberEnd=1)

        self.assertIsInstance(response, dict)
        self.assertEqual(3, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0"), response[teams[1].id])
        self.assertIsNone(response[teams[2].id])

    def test_getTeamLuck_sumOfLeagueEqualsZero(self):
        owners, teams = getNDefaultOwnersAndTeams(3)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=3)
        matchup2 = Matchup(teamAId=teams[1].id, teamBId=teams[2].id, teamAScore=1.2, teamBScore=3)
        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2])

        response = SSLYearCalculator.getTeamLuck(year, weekNumberEnd=1)

        self.assertEqual(0, sum([response[teams[0].id], response[teams[1].id]]))

    def test_getTeamLuck_onlyPostSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=5, teamBScore=4)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=3,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.3, teamBScore=2.6,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = SSLYearCalculator.getTeamLuck(year, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0"), response[teams[1].id])

    def test_getTeamLuck_onlyRegularSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=5)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=5, teamBScore=6,
                           matchupType=MatchupType.PLAYOFF)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = SSLYearCalculator.getTeamLuck(year, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0"), response[teams[1].id])

    def test_getTeamLuck_onlyChampionshipIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=6, teamBScore=7,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=5, teamBScore=6,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1])

        response = SSLYearCalculator.getTeamLuck(year, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertIsNone(response[teams[0].id])
        self.assertIsNone(response[teams[1].id])
        self.assertIsNone(response[teams[2].id])
        self.assertIsNone(response[teams[3].id])
        self.assertEqual(Deci("0"), response[teams[4].id])
        self.assertEqual(Deci("0"), response[teams[5].id])

    def test_getTeamLuck_weekNumberStartGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=3, teamBScore=6)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=2.5)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.3, teamBScore=2.6,
                           matchupType=MatchupType.PLAYOFF)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = SSLYearCalculator.getTeamLuck(year, weekNumberStart=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0"), response[teams[1].id])

    def test_getTeamLuck_weekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=2.5)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = SSLYearCalculator.getTeamLuck(year, weekNumberEnd=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0"), response[teams[1].id])

    def test_getTeamLuck_weekNumberStartGivenAndWeekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=2.5)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.3, teamBScore=2.6,
                           matchupType=MatchupType.PLAYOFF)
        matchup4 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.4, teamBScore=2.7,
                           matchupType=MatchupType.PLAYOFF)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])
        week4 = Week(weekNumber=4, matchups=[matchup4])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3, week4])

        response = SSLYearCalculator.getTeamLuck(year, weekNumberStart=2, weekNumberEnd=3)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0"), response[teams[1].id])
