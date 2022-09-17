import unittest

from leeger.calculator.year_calculator.SmartWinsYearCalculator import SmartWinsYearCalculator
from leeger.enum.MatchupType import MatchupType
from leeger.model.league.Matchup import Matchup
from leeger.model.league.Week import Week
from leeger.model.league.Year import Year
from leeger.util.Deci import Deci
from test.helper.prototypes import getNDefaultOwnersAndTeams


class TestSmartWinsYearCalculator(unittest.TestCase):

    def test_getSmartWins_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.IGNORE)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = SmartWinsYearCalculator.getSmartWins(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.06666666666666666666666666666"), response[teams[0].id])
        self.assertEqual(Deci("0.3333333333333333333333333334"), response[teams[1].id])
        self.assertEqual(Deci("0.9999999999999999999999999999"), response[teams[2].id])
        self.assertEqual(Deci("1.9"), response[teams[3].id])
        self.assertEqual(Deci("1.9"), response[teams[4].id])
        self.assertEqual(Deci("2.8"), response[teams[5].id])

    def test_getSmartWins_multiWeekMatchups(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2, multiWeekMatchupId="1")
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup4 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2, multiWeekMatchupId="1")
        matchup5 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup6 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, matchups=[matchup4, matchup5, matchup6])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2])

        response = SmartWinsYearCalculator.getSmartWins(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0.5555555555555555555555555556"), response[teams[1].id])
        self.assertEqual(Deci("0.3333333333333333333333333334"), response[teams[2].id])
        self.assertEqual(Deci("1.111111111111111111111111111"), response[teams[3].id])
        self.assertEqual(Deci("1.111111111111111111111111111"), response[teams[4].id])
        self.assertEqual(Deci("1.888888888888888888888888889"), response[teams[5].id])

    def test_getSmartWins_noneIfNoGamesPlayed(self):
        owners, teams = getNDefaultOwnersAndTeams(3)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        week1 = Week(weekNumber=1, matchups=[matchup1])

        matchup2 = Matchup(teamAId=teams[1].id, teamBId=teams[2].id, teamAScore=3, teamBScore=4)
        week2 = Week(weekNumber=2, matchups=[matchup2])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2])

        response = SmartWinsYearCalculator.getSmartWins(year, weekNumberEnd=1)

        self.assertIsInstance(response, dict)
        self.assertEqual(3, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0.3333333333333333333333333333"), response[teams[1].id])
        self.assertIsNone(response[teams[2].id])

    def test_getSmartWins_onlyPostSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.IGNORE)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = SmartWinsYearCalculator.getSmartWins(year, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.03333333333333333333333333333"), response[teams[0].id])
        self.assertEqual(Deci("0.1666666666666666666666666667"), response[teams[1].id])
        self.assertEqual(Deci("0.3333333333333333333333333333"), response[teams[2].id])
        self.assertEqual(Deci("0.6333333333333333333333333333"), response[teams[3].id])
        self.assertEqual(Deci("0.6333333333333333333333333333"), response[teams[4].id])
        self.assertEqual(Deci("0.9333333333333333333333333333"), response[teams[5].id])

    def test_getSmartWins_onlyRegularSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.IGNORE)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = SmartWinsYearCalculator.getSmartWins(year, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.03333333333333333333333333333"), response[teams[0].id])
        self.assertEqual(Deci("0.1666666666666666666666666667"), response[teams[1].id])
        self.assertEqual(Deci("0.6666666666666666666666666666"), response[teams[2].id])
        self.assertEqual(Deci("1.266666666666666666666666667"), response[teams[3].id])
        self.assertEqual(Deci("1.266666666666666666666666667"), response[teams[4].id])
        self.assertEqual(Deci("1.866666666666666666666666667"), response[teams[5].id])

    def test_getSmartWins_onlyChampionshipIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.IGNORE)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = SmartWinsYearCalculator.getSmartWins(year, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertIsNone(response[teams[0].id])
        self.assertIsNone(response[teams[1].id])
        self.assertIsNone(response[teams[2].id])
        self.assertIsNone(response[teams[3].id])
        self.assertEqual(Deci("0.6333333333333333333333333333"), response[teams[4].id])
        self.assertEqual(Deci("0.9333333333333333333333333333"), response[teams[5].id])

    def test_getSmartWins_weekNumberStartGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.IGNORE)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = SmartWinsYearCalculator.getSmartWins(year, weekNumberStart=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.06666666666666666666666666666"), response[teams[0].id])
        self.assertEqual(Deci("0.3333333333333333333333333334"), response[teams[1].id])
        self.assertEqual(Deci("0.6666666666666666666666666666"), response[teams[2].id])
        self.assertEqual(Deci("1.266666666666666666666666667"), response[teams[3].id])
        self.assertEqual(Deci("1.266666666666666666666666667"), response[teams[4].id])
        self.assertEqual(Deci("1.866666666666666666666666667"), response[teams[5].id])

    def test_getSmartWins_weekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.IGNORE)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = SmartWinsYearCalculator.getSmartWins(year, weekNumberEnd=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.03333333333333333333333333333"), response[teams[0].id])
        self.assertEqual(Deci("0.1666666666666666666666666667"), response[teams[1].id])
        self.assertEqual(Deci("0.6666666666666666666666666666"), response[teams[2].id])
        self.assertEqual(Deci("1.266666666666666666666666667"), response[teams[3].id])
        self.assertEqual(Deci("1.266666666666666666666666667"), response[teams[4].id])
        self.assertEqual(Deci("1.866666666666666666666666667"), response[teams[5].id])

    def test_getSmartWins_weekNumberStartGivenWeekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.IGNORE)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week4 = Week(weekNumber=4, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = SmartWinsYearCalculator.getSmartWins(year, weekNumberStart=2, weekNumberEnd=3)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.06666666666666666666666666666"), response[teams[0].id])
        self.assertEqual(Deci("0.3333333333333333333333333334"), response[teams[1].id])
        self.assertEqual(Deci("0.6666666666666666666666666666"), response[teams[2].id])
        self.assertEqual(Deci("1.266666666666666666666666667"), response[teams[3].id])
        self.assertEqual(Deci("1.266666666666666666666666667"), response[teams[4].id])
        self.assertEqual(Deci("1.866666666666666666666666667"), response[teams[5].id])

    def test_getSmartWinsPerGame_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.IGNORE)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = SmartWinsYearCalculator.getSmartWinsPerGame(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.03333333333333333333333333333"), response[teams[0].id])
        self.assertEqual(Deci("0.1666666666666666666666666667"), response[teams[1].id])
        self.assertEqual(Deci("0.3333333333333333333333333333"), response[teams[2].id])
        self.assertEqual(Deci("0.6333333333333333333333333333"), response[teams[3].id])
        self.assertEqual(Deci("0.6333333333333333333333333333"), response[teams[4].id])
        self.assertEqual(Deci("0.9333333333333333333333333333"), response[teams[5].id])

    def test_getSmartWinsPerGame_multiWeekMatchups(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2, multiWeekMatchupId="1")
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup4 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2, multiWeekMatchupId="1")
        matchup5 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup6 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, matchups=[matchup4, matchup5, matchup6])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2])

        response = SmartWinsYearCalculator.getSmartWinsPerGame(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0.5555555555555555555555555556"), response[teams[1].id])
        self.assertEqual(Deci("0.1666666666666666666666666667"), response[teams[2].id])
        self.assertEqual(Deci("0.5555555555555555555555555555"), response[teams[3].id])
        self.assertEqual(Deci("0.5555555555555555555555555555"), response[teams[4].id])
        self.assertEqual(Deci("0.9444444444444444444444444445"), response[teams[5].id])

    def test_getSmartWinsPerGame_noneIfNoGamesPlayed(self):
        owners, teams = getNDefaultOwnersAndTeams(3)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        week1 = Week(weekNumber=1, matchups=[matchup1])

        matchup2 = Matchup(teamAId=teams[1].id, teamBId=teams[2].id, teamAScore=3, teamBScore=4)
        week2 = Week(weekNumber=2, matchups=[matchup2])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2])

        response = SmartWinsYearCalculator.getSmartWinsPerGame(year, weekNumberEnd=1)

        self.assertIsInstance(response, dict)
        self.assertEqual(3, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0.3333333333333333333333333333"), response[teams[1].id])
        self.assertIsNone(response[teams[2].id])

    def test_getSmartWinsPerGame_onlyPostSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.IGNORE)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = SmartWinsYearCalculator.getSmartWinsPerGame(year, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.03333333333333333333333333333"), response[teams[0].id])
        self.assertEqual(Deci("0.1666666666666666666666666667"), response[teams[1].id])
        self.assertEqual(Deci("0.3333333333333333333333333333"), response[teams[2].id])
        self.assertEqual(Deci("0.6333333333333333333333333333"), response[teams[3].id])
        self.assertEqual(Deci("0.6333333333333333333333333333"), response[teams[4].id])
        self.assertEqual(Deci("0.9333333333333333333333333333"), response[teams[5].id])

    def test_getSmartWinsPerGame_onlyRegularSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.IGNORE)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = SmartWinsYearCalculator.getSmartWinsPerGame(year, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.03333333333333333333333333333"), response[teams[0].id])
        self.assertEqual(Deci("0.1666666666666666666666666667"), response[teams[1].id])
        self.assertEqual(Deci("0.3333333333333333333333333333"), response[teams[2].id])
        self.assertEqual(Deci("0.6333333333333333333333333335"), response[teams[3].id])
        self.assertEqual(Deci("0.6333333333333333333333333335"), response[teams[4].id])
        self.assertEqual(Deci("0.9333333333333333333333333335"), response[teams[5].id])

    def test_getSmartWinsPerGame_onlyChampionshipIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.IGNORE)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = SmartWinsYearCalculator.getSmartWinsPerGame(year, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertIsNone(response[teams[0].id])
        self.assertIsNone(response[teams[1].id])
        self.assertIsNone(response[teams[2].id])
        self.assertIsNone(response[teams[3].id])
        self.assertEqual(Deci("0.6333333333333333333333333333"), response[teams[4].id])
        self.assertEqual(Deci("0.9333333333333333333333333333"), response[teams[5].id])

    def test_getSmartWinsPerGame_weekNumberStartGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.IGNORE)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = SmartWinsYearCalculator.getSmartWinsPerGame(year, weekNumberStart=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.03333333333333333333333333333"), response[teams[0].id])
        self.assertEqual(Deci("0.1666666666666666666666666667"), response[teams[1].id])
        self.assertEqual(Deci("0.3333333333333333333333333333"), response[teams[2].id])
        self.assertEqual(Deci("0.6333333333333333333333333335"), response[teams[3].id])
        self.assertEqual(Deci("0.6333333333333333333333333335"), response[teams[4].id])
        self.assertEqual(Deci("0.9333333333333333333333333335"), response[teams[5].id])

    def test_getSmartWinsPerGame_weekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.IGNORE)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = SmartWinsYearCalculator.getSmartWinsPerGame(year, weekNumberEnd=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.03333333333333333333333333333"), response[teams[0].id])
        self.assertEqual(Deci("0.1666666666666666666666666667"), response[teams[1].id])
        self.assertEqual(Deci("0.3333333333333333333333333333"), response[teams[2].id])
        self.assertEqual(Deci("0.6333333333333333333333333335"), response[teams[3].id])
        self.assertEqual(Deci("0.6333333333333333333333333335"), response[teams[4].id])
        self.assertEqual(Deci("0.9333333333333333333333333335"), response[teams[5].id])

    def test_getSmartWinsPerGame_weekNumberStartGivenWeekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.IGNORE)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week4 = Week(weekNumber=4, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = SmartWinsYearCalculator.getSmartWinsPerGame(year, weekNumberStart=2, weekNumberEnd=3)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.03333333333333333333333333333"), response[teams[0].id])
        self.assertEqual(Deci("0.1666666666666666666666666667"), response[teams[1].id])
        self.assertEqual(Deci("0.3333333333333333333333333333"), response[teams[2].id])
        self.assertEqual(Deci("0.6333333333333333333333333335"), response[teams[3].id])
        self.assertEqual(Deci("0.6333333333333333333333333335"), response[teams[4].id])
        self.assertEqual(Deci("0.9333333333333333333333333335"), response[teams[5].id])

    def test_getOpponentSmartWins_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.IGNORE)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = SmartWinsYearCalculator.getOpponentSmartWins(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.3333333333333333333333333334"), response[teams[0].id])
        self.assertEqual(Deci("0.06666666666666666666666666666"), response[teams[1].id])
        self.assertEqual(Deci("1.9"), response[teams[2].id])
        self.assertEqual(Deci("0.9999999999999999999999999999"), response[teams[3].id])
        self.assertEqual(Deci("2.8"), response[teams[4].id])
        self.assertEqual(Deci("1.9"), response[teams[5].id])

    def test_getOpponentSmartWins_multiWeekMatchups(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2, multiWeekMatchupId="1")
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup4 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2, multiWeekMatchupId="1")
        matchup5 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup6 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, matchups=[matchup4, matchup5, matchup6])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2])

        response = SmartWinsYearCalculator.getOpponentSmartWins(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.5555555555555555555555555556"), response[teams[0].id])
        self.assertEqual(Deci("0"), response[teams[1].id])
        self.assertEqual(Deci("1.111111111111111111111111111"), response[teams[2].id])
        self.assertEqual(Deci("0.3333333333333333333333333334"), response[teams[3].id])
        self.assertEqual(Deci("1.888888888888888888888888889"), response[teams[4].id])
        self.assertEqual(Deci("1.111111111111111111111111111"), response[teams[5].id])

    def test_getOpponentSmartWins_noneIfNoGamesPlayed(self):
        owners, teams = getNDefaultOwnersAndTeams(3)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        week1 = Week(weekNumber=1, matchups=[matchup1])

        matchup2 = Matchup(teamAId=teams[1].id, teamBId=teams[2].id, teamAScore=3, teamBScore=4)
        week2 = Week(weekNumber=2, matchups=[matchup2])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2])

        response = SmartWinsYearCalculator.getOpponentSmartWins(year, weekNumberEnd=1)

        self.assertIsInstance(response, dict)
        self.assertEqual(3, len(response.keys()))
        self.assertEqual(Deci("0.3333333333333333333333333333"), response[teams[0].id])
        self.assertEqual(Deci("0"), response[teams[1].id])
        self.assertIsNone(response[teams[2].id])

    def test_getOpponentSmartWins_onlyPostSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.IGNORE)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = SmartWinsYearCalculator.getOpponentSmartWins(year, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.1666666666666666666666666667"), response[teams[0].id])
        self.assertEqual(Deci("0.03333333333333333333333333333"), response[teams[1].id])
        self.assertEqual(Deci("0.6333333333333333333333333333"), response[teams[2].id])
        self.assertEqual(Deci("0.3333333333333333333333333333"), response[teams[3].id])
        self.assertEqual(Deci("0.9333333333333333333333333333"), response[teams[4].id])
        self.assertEqual(Deci("0.6333333333333333333333333333"), response[teams[5].id])

    def test_getOpponentSmartWins_onlyRegularSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.IGNORE)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = SmartWinsYearCalculator.getOpponentSmartWins(year, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.1666666666666666666666666667"), response[teams[0].id])
        self.assertEqual(Deci("0.03333333333333333333333333333"), response[teams[1].id])
        self.assertEqual(Deci("1.266666666666666666666666667"), response[teams[2].id])
        self.assertEqual(Deci("0.6666666666666666666666666666"), response[teams[3].id])
        self.assertEqual(Deci("1.866666666666666666666666667"), response[teams[4].id])
        self.assertEqual(Deci("1.266666666666666666666666667"), response[teams[5].id])

    def test_getOpponentSmartWins_onlyChampionshipIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.IGNORE)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = SmartWinsYearCalculator.getOpponentSmartWins(year, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertIsNone(response[teams[0].id])
        self.assertIsNone(response[teams[1].id])
        self.assertIsNone(response[teams[2].id])
        self.assertIsNone(response[teams[3].id])
        self.assertEqual(Deci("0.9333333333333333333333333333"), response[teams[4].id])
        self.assertEqual(Deci("0.6333333333333333333333333333"), response[teams[5].id])

    def test_getOpponentSmartWins_weekNumberStartGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.IGNORE)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = SmartWinsYearCalculator.getOpponentSmartWins(year, weekNumberStart=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.3333333333333333333333333334"), response[teams[0].id])
        self.assertEqual(Deci("0.06666666666666666666666666666"), response[teams[1].id])
        self.assertEqual(Deci("1.266666666666666666666666667"), response[teams[2].id])
        self.assertEqual(Deci("0.6666666666666666666666666666"), response[teams[3].id])
        self.assertEqual(Deci("1.866666666666666666666666667"), response[teams[4].id])
        self.assertEqual(Deci("1.266666666666666666666666667"), response[teams[5].id])

    def test_getOpponentSmartWins_weekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.IGNORE)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = SmartWinsYearCalculator.getOpponentSmartWins(year, weekNumberEnd=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.1666666666666666666666666667"), response[teams[0].id])
        self.assertEqual(Deci("0.03333333333333333333333333333"), response[teams[1].id])
        self.assertEqual(Deci("1.266666666666666666666666667"), response[teams[2].id])
        self.assertEqual(Deci("0.6666666666666666666666666666"), response[teams[3].id])
        self.assertEqual(Deci("1.866666666666666666666666667"), response[teams[4].id])
        self.assertEqual(Deci("1.266666666666666666666666667"), response[teams[5].id])

    def test_getOpponentSmartWins_weekNumberStartGivenWeekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.IGNORE)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week4 = Week(weekNumber=4, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = SmartWinsYearCalculator.getOpponentSmartWins(year, weekNumberStart=2, weekNumberEnd=3)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.3333333333333333333333333334"), response[teams[0].id])
        self.assertEqual(Deci("0.06666666666666666666666666666"), response[teams[1].id])
        self.assertEqual(Deci("1.266666666666666666666666667"), response[teams[2].id])
        self.assertEqual(Deci("0.6666666666666666666666666666"), response[teams[3].id])
        self.assertEqual(Deci("1.866666666666666666666666667"), response[teams[4].id])
        self.assertEqual(Deci("1.266666666666666666666666667"), response[teams[5].id])

    def test_getOpponentSmartWinsPerGame_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.IGNORE)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = SmartWinsYearCalculator.getOpponentSmartWinsPerGame(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.1666666666666666666666666667"), response[teams[0].id])
        self.assertEqual(Deci("0.03333333333333333333333333333"), response[teams[1].id])
        self.assertEqual(Deci("0.6333333333333333333333333333"), response[teams[2].id])
        self.assertEqual(Deci("0.3333333333333333333333333333"), response[teams[3].id])
        self.assertEqual(Deci("0.9333333333333333333333333333"), response[teams[4].id])
        self.assertEqual(Deci("0.6333333333333333333333333333"), response[teams[5].id])

    def test_getOpponentSmartWinsPerGame_noneIfNoGamesPlayed(self):
        owners, teams = getNDefaultOwnersAndTeams(3)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        week1 = Week(weekNumber=1, matchups=[matchup1])

        matchup2 = Matchup(teamAId=teams[1].id, teamBId=teams[2].id, teamAScore=3, teamBScore=4)
        week2 = Week(weekNumber=2, matchups=[matchup2])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2])

        response = SmartWinsYearCalculator.getOpponentSmartWinsPerGame(year, weekNumberEnd=1)

        self.assertIsInstance(response, dict)
        self.assertEqual(3, len(response.keys()))
        self.assertEqual(Deci("0.3333333333333333333333333333"), response[teams[0].id])
        self.assertEqual(Deci("0"), response[teams[1].id])
        self.assertIsNone(response[teams[2].id])

    def test_getOpponentSmartWinsPerGame_onlyPostSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.IGNORE)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = SmartWinsYearCalculator.getOpponentSmartWinsPerGame(year, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.1666666666666666666666666667"), response[teams[0].id])
        self.assertEqual(Deci("0.03333333333333333333333333333"), response[teams[1].id])
        self.assertEqual(Deci("0.6333333333333333333333333333"), response[teams[2].id])
        self.assertEqual(Deci("0.3333333333333333333333333333"), response[teams[3].id])
        self.assertEqual(Deci("0.9333333333333333333333333333"), response[teams[4].id])
        self.assertEqual(Deci("0.6333333333333333333333333333"), response[teams[5].id])

    def test_getOpponentSmartWinsPerGame_onlyRegularSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.IGNORE)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = SmartWinsYearCalculator.getOpponentSmartWinsPerGame(year, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.1666666666666666666666666667"), response[teams[0].id])
        self.assertEqual(Deci("0.03333333333333333333333333333"), response[teams[1].id])
        self.assertEqual(Deci("0.6333333333333333333333333335"), response[teams[2].id])
        self.assertEqual(Deci("0.3333333333333333333333333333"), response[teams[3].id])
        self.assertEqual(Deci("0.9333333333333333333333333335"), response[teams[4].id])
        self.assertEqual(Deci("0.6333333333333333333333333335"), response[teams[5].id])

    def test_getOpponentSmartWinsPerGame_onlyChampionshipIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.IGNORE)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = SmartWinsYearCalculator.getOpponentSmartWinsPerGame(year, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertIsNone(response[teams[0].id])
        self.assertIsNone(response[teams[1].id])
        self.assertIsNone(response[teams[2].id])
        self.assertIsNone(response[teams[3].id])
        self.assertEqual(Deci("0.9333333333333333333333333333"), response[teams[4].id])
        self.assertEqual(Deci("0.6333333333333333333333333333"), response[teams[5].id])

    def test_getOpponentSmartWinsPerGame_weekNumberStartGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.IGNORE)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = SmartWinsYearCalculator.getOpponentSmartWinsPerGame(year, weekNumberStart=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.1666666666666666666666666667"), response[teams[0].id])
        self.assertEqual(Deci("0.03333333333333333333333333333"), response[teams[1].id])
        self.assertEqual(Deci("0.6333333333333333333333333335"), response[teams[2].id])
        self.assertEqual(Deci("0.3333333333333333333333333333"), response[teams[3].id])
        self.assertEqual(Deci("0.9333333333333333333333333335"), response[teams[4].id])
        self.assertEqual(Deci("0.6333333333333333333333333335"), response[teams[5].id])

    def test_getOpponentSmartWinsPerGame_weekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.IGNORE)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = SmartWinsYearCalculator.getOpponentSmartWinsPerGame(year, weekNumberEnd=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.1666666666666666666666666667"), response[teams[0].id])
        self.assertEqual(Deci("0.03333333333333333333333333333"), response[teams[1].id])
        self.assertEqual(Deci("0.6333333333333333333333333335"), response[teams[2].id])
        self.assertEqual(Deci("0.3333333333333333333333333333"), response[teams[3].id])
        self.assertEqual(Deci("0.9333333333333333333333333335"), response[teams[4].id])
        self.assertEqual(Deci("0.6333333333333333333333333335"), response[teams[5].id])

    def test_getOpponentSmartWinsPerGame_weekNumberStartGivenWeekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.IGNORE)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week4 = Week(weekNumber=4, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = SmartWinsYearCalculator.getOpponentSmartWinsPerGame(year, weekNumberStart=2, weekNumberEnd=3)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.1666666666666666666666666667"), response[teams[0].id])
        self.assertEqual(Deci("0.03333333333333333333333333333"), response[teams[1].id])
        self.assertEqual(Deci("0.6333333333333333333333333335"), response[teams[2].id])
        self.assertEqual(Deci("0.3333333333333333333333333333"), response[teams[3].id])
        self.assertEqual(Deci("0.9333333333333333333333333335"), response[teams[4].id])
        self.assertEqual(Deci("0.6333333333333333333333333335"), response[teams[5].id])
