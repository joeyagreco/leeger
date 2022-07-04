import unittest

from src.leeger.calculator.all_time_calculator.SSLAllTimeCalculator import SSLAllTimeCalculator
from src.leeger.enum.MatchupType import MatchupType
from src.leeger.model.league.League import League
from src.leeger.model.league.Matchup import Matchup
from src.leeger.model.league.Week import Week
from src.leeger.model.league.Year import Year
from src.leeger.util.Deci import Deci
from test.helper.prototypes import getNDefaultOwnersAndTeams, getTeamsFromOwners


class TestSSLAllTimeCalculator(unittest.TestCase):

    def test_getTeamScore_happyPath(self):
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

        response = SSLAllTimeCalculator.getTeamScore(league)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("21.27263157894736842105263158"), response[owners[0].id])
        self.assertEqual(Deci("82.54526315789473684210526316"), response[owners[1].id])
        self.assertEqual(Deci("181.6478947368421052631578948"), response[owners[2].id])
        self.assertEqual(Deci("325.5305263157894736842105264"), response[owners[3].id])
        self.assertEqual(Deci("325.5305263157894736842105264"), response[owners[4].id])
        self.assertEqual(Deci("469.4131578947368421052631578"), response[owners[5].id])

    def test_getTeamScore_onlyPostSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1.1, teamBScore=2.1,
                             matchupType=MatchupType.IGNORE)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3.1, teamBScore=4.1,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4.1, teamBScore=5.1,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.2, teamBScore=2.2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.2, teamBScore=4.2)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.2, teamBScore=5.2)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1.3, teamBScore=2.3,
                             matchupType=MatchupType.PLAYOFF)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3.3, teamBScore=4.3,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4.3, teamBScore=5.3,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SSLAllTimeCalculator.getTeamScore(league, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("12.63000"), response[owners[0].id])
        self.assertEqual(Deci("42.34538461538461538461538462"), response[owners[1].id])
        self.assertEqual(Deci("110.1756472795497185741088180"), response[owners[2].id])
        self.assertEqual(Deci("212.1861538461538461538461538"), response[owners[3].id])
        self.assertEqual(Deci("212.1861538461538461538461538"), response[owners[4].id])
        self.assertEqual(Deci("314.1966604127579737335834897"), response[owners[5].id])

    def test_getTeamScore_onlyRegularSeasonIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1.1, teamBScore=2.1,
                             matchupType=MatchupType.IGNORE)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3.1, teamBScore=4.1,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4.1, teamBScore=5.1,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.2, teamBScore=2.2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.2, teamBScore=4.2)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.2, teamBScore=5.2)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1.3, teamBScore=2.3,
                             matchupType=MatchupType.PLAYOFF)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3.3, teamBScore=4.3,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4.3, teamBScore=5.3,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SSLAllTimeCalculator.getTeamScore(league, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("12.00118811881188118811881188"), response[owners[0].id])
        self.assertEqual(Deci("42.00217821782178217821782178"), response[owners[1].id])
        self.assertEqual(Deci("72.00316831683168316831683168"), response[owners[2].id])
        self.assertEqual(Deci("112.0041584158415841584158416"), response[owners[3].id])
        self.assertEqual(Deci("112.0041584158415841584158416"), response[owners[4].id])
        self.assertEqual(Deci("152.0051485148514851485148515"), response[owners[5].id])

    def test_getTeamScore_onlyChampionshipIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1.1, teamBScore=2.1,
                             matchupType=MatchupType.IGNORE)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3.1, teamBScore=4.1,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4.1, teamBScore=5.1,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.2, teamBScore=2.2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.2, teamBScore=4.2)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.2, teamBScore=5.2)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1.3, teamBScore=2.3,
                             matchupType=MatchupType.PLAYOFF)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3.3, teamBScore=4.3,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4.3, teamBScore=5.3,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SSLAllTimeCalculator.getTeamScore(league, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertIsNone(response[owners[0].id])
        self.assertIsNone(response[owners[1].id])
        self.assertIsNone(response[owners[2].id])
        self.assertIsNone(response[owners[3].id])
        self.assertEqual(Deci("179.5537681159420289855072464"), response[owners[4].id])
        self.assertEqual(Deci("422.3262318840579710144927537"), response[owners[5].id])

    def test_getTeamScore_yearNumberStartGivenWeekNumberStartGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1.1, teamBScore=2.1,
                             matchupType=MatchupType.IGNORE)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3.1, teamBScore=4.1,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4.1, teamBScore=5.1,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.2, teamBScore=2.2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.2, teamBScore=4.2)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.2, teamBScore=5.2)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        matchup4_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.2, teamBScore=2.2)
        matchup5_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.2, teamBScore=4.2)
        matchup6_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.2, teamBScore=5.2)
        week2_b = Week(weekNumber=2, matchups=[matchup4_b, matchup5_b, matchup6_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1.3, teamBScore=2.3,
                             matchupType=MatchupType.PLAYOFF)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3.3, teamBScore=4.3,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4.3, teamBScore=5.3,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SSLAllTimeCalculator.getTeamScore(league, yearNumberStart=2001, weekNumberStart=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("24.63118811881188118811881188"), response[owners[0].id])
        self.assertEqual(Deci("84.34756283320639756283320640"), response[owners[1].id])
        self.assertEqual(Deci("144.0639375476009139375476009"), response[owners[2].id])
        self.assertEqual(Deci("223.7803122619954303122619954"), response[owners[3].id])
        self.assertEqual(Deci("223.7803122619954303122619954"), response[owners[4].id])
        self.assertEqual(Deci("303.4966869763899466869763900"), response[owners[5].id])

    def test_getTeamScore_yearNumberEndGivenWeekNumberEndGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1.1, teamBScore=2.1,
                             matchupType=MatchupType.IGNORE)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3.1, teamBScore=4.1,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4.1, teamBScore=5.1,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.2, teamBScore=2.2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.2, teamBScore=4.2)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.2, teamBScore=5.2)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        matchup4_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.2, teamBScore=2.2)
        matchup5_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.2, teamBScore=4.2)
        matchup6_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.2, teamBScore=5.2)
        week2_b = Week(weekNumber=2, matchups=[matchup4_b, matchup5_b, matchup6_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1.3, teamBScore=2.3,
                             matchupType=MatchupType.PLAYOFF)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3.3, teamBScore=4.3,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4.3, teamBScore=5.3,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SSLAllTimeCalculator.getTeamScore(league, yearNumberEnd=2001, weekNumberEnd=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("12.00118811881188118811881188"), response[owners[0].id])
        self.assertEqual(Deci("42.00217821782178217821782178"), response[owners[1].id])
        self.assertEqual(Deci("110.1180463656121709731948805"), response[owners[2].id])
        self.assertEqual(Deci("212.4141584158415841584158416"), response[owners[3].id])
        self.assertEqual(Deci("212.4141584158415841584158416"), response[owners[4].id])
        self.assertEqual(Deci("314.7102704660709973436368027"), response[owners[5].id])

    def test_getTeamScore_yearNumberStartGivenWeekNumberStartGivenAndYearNumberEndGivenWeekNumberEndGiven(self):
        owners, teamsA = getNDefaultOwnersAndTeams(6)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1.1, teamBScore=2.1,
                             matchupType=MatchupType.IGNORE)
        matchup2_a = Matchup(teamAId=teamsA[2].id, teamBId=teamsA[3].id, teamAScore=3.1, teamBScore=4.1,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_a = Matchup(teamAId=teamsA[4].id, teamBId=teamsA[5].id, teamAScore=4.1, teamBScore=5.1,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a, matchup2_a, matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.2, teamBScore=2.2)
        matchup2_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.2, teamBScore=4.2)
        matchup3_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.2, teamBScore=5.2)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b, matchup2_b, matchup3_b])
        matchup4_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1.2, teamBScore=2.2)
        matchup5_b = Matchup(teamAId=teamsB[2].id, teamBId=teamsB[3].id, teamAScore=3.2, teamBScore=4.2)
        matchup6_b = Matchup(teamAId=teamsB[4].id, teamBId=teamsB[5].id, teamAScore=4.2, teamBScore=5.2)
        week2_b = Week(weekNumber=2, matchups=[matchup4_b, matchup5_b, matchup6_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1.3, teamBScore=2.3,
                             matchupType=MatchupType.PLAYOFF)
        matchup2_c = Matchup(teamAId=teamsC[2].id, teamBId=teamsC[3].id, teamAScore=3.3, teamBScore=4.3,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_c = Matchup(teamAId=teamsC[4].id, teamBId=teamsC[5].id, teamAScore=4.3, teamBScore=5.3,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c, matchup2_c, matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC])

        response = SSLAllTimeCalculator.getTeamScore(league, yearNumberStart=2001, weekNumberStart=1,
                                                     yearNumberEnd=2001, weekNumberEnd=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("12.00118811881188118811881188"), response[owners[0].id])
        self.assertEqual(Deci("42.00217821782178217821782178"), response[owners[1].id])
        self.assertEqual(Deci("72.00316831683168316831683168"), response[owners[2].id])
        self.assertEqual(Deci("112.0041584158415841584158416"), response[owners[3].id])
        self.assertEqual(Deci("112.0041584158415841584158416"), response[owners[4].id])
        self.assertEqual(Deci("152.0051485148514851485148515"), response[owners[5].id])
