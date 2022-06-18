import unittest

from src.leeger.calculator.ScoringShareCalculator import ScoringShareCalculator
from src.leeger.model.Matchup import Matchup
from src.leeger.model.Week import Week
from src.leeger.model.Year import Year
from src.leeger.util.Deci import Deci
from test.helper.prototypes import getNDefaultOwnersAndTeams


class TestScoringShareCalculator(unittest.TestCase):

    def test_getScoringShare_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=2.5,
                           isPlayoffMatchup=True)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.3, teamBScore=2.6,
                           isChampionshipMatchup=True)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = ScoringShareCalculator.getScoringShare(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci(100), sum(response.values()))
        self.assertEqual(Deci("32.43243243243243243243243243"), response[teams[0].id])
        self.assertEqual(Deci("67.56756756756756756756756757"), response[teams[1].id])

    def test_getScoringShare_onlyPostSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=2.5,
                           isPlayoffMatchup=True)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.3, teamBScore=2.6,
                           isChampionshipMatchup=True)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = ScoringShareCalculator.getScoringShare(year, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci(100), sum(response.values()))
        self.assertEqual(Deci("32.89473684210526315789473684"), response[teams[0].id])
        self.assertEqual(Deci("67.10526315789473684210526316"), response[teams[1].id])

    def test_getScoringShare_onlyRegularSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=2.5)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.3, teamBScore=2.6,
                           isPlayoffMatchup=True)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = ScoringShareCalculator.getScoringShare(year, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci(100), sum(response.values()))
        self.assertEqual(Deci("31.94444444444444444444444444"), response[teams[0].id])
        self.assertEqual(Deci("68.05555555555555555555555556"), response[teams[1].id])

    def test_getScoringShare_weekNumberStartGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=2.5)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.3, teamBScore=2.6,
                           isPlayoffMatchup=True)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = ScoringShareCalculator.getScoringShare(year, weekNumberStart=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci(100), sum(response.values()))
        self.assertEqual(Deci("32.89473684210526315789473684"), response[teams[0].id])
        self.assertEqual(Deci("67.10526315789473684210526316"), response[teams[1].id])

    def test_getScoringShare_weekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=2.5)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.3, teamBScore=2.6,
                           isPlayoffMatchup=True)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = ScoringShareCalculator.getScoringShare(year, weekNumberEnd=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci(100), sum(response.values()))
        self.assertEqual(Deci("31.94444444444444444444444444"), response[teams[0].id])
        self.assertEqual(Deci("68.05555555555555555555555556"), response[teams[1].id])

    def test_getScoringShare_weekNumberStartGivenAndWeekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=2.5)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.3, teamBScore=2.6,
                           isPlayoffMatchup=True)
        matchup4 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.4, teamBScore=2.7,
                           isPlayoffMatchup=True)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])
        week4 = Week(weekNumber=4, matchups=[matchup4])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3, week4])

        response = ScoringShareCalculator.getScoringShare(year, weekNumberStart=2, weekNumberEnd=3)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci(100), sum(response.values()))
        self.assertEqual(Deci("32.89473684210526315789473684"), response[teams[0].id])
        self.assertEqual(Deci("67.10526315789473684210526316"), response[teams[1].id])

    def test_getOpponentScoringShare_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=2.5,
                           isPlayoffMatchup=True)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.3, teamBScore=2.6,
                           isChampionshipMatchup=True)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = ScoringShareCalculator.getOpponentScoringShare(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci(100), sum(response.values()))
        self.assertEqual(Deci("67.56756756756756756756756757"), response[teams[0].id])
        self.assertEqual(Deci("32.43243243243243243243243243"), response[teams[1].id])

    def test_getOpponentScoringShare_onlyPostSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=2.5,
                           isPlayoffMatchup=True)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.3, teamBScore=2.6,
                           isChampionshipMatchup=True)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = ScoringShareCalculator.getOpponentScoringShare(year, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci(100), sum(response.values()))
        self.assertEqual(Deci("67.10526315789473684210526316"), response[teams[0].id])
        self.assertEqual(Deci("32.89473684210526315789473684"), response[teams[1].id])

    def test_getOpponentScoringShare_onlyRegularSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=2.5)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.3, teamBScore=2.6,
                           isPlayoffMatchup=True)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = ScoringShareCalculator.getOpponentScoringShare(year, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci(100), sum(response.values()))
        self.assertEqual(Deci("68.05555555555555555555555556"), response[teams[0].id])
        self.assertEqual(Deci("31.94444444444444444444444444"), response[teams[1].id])

    def test_getOpponentScoringShare_weekNumberStartGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=2.5)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.3, teamBScore=2.6,
                           isPlayoffMatchup=True)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = ScoringShareCalculator.getOpponentScoringShare(year, weekNumberStart=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci(100), sum(response.values()))
        self.assertEqual(Deci("67.10526315789473684210526316"), response[teams[0].id])
        self.assertEqual(Deci("32.89473684210526315789473684"), response[teams[1].id])

    def test_getOpponentScoringShare_weekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=2.5)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.3, teamBScore=2.6,
                           isPlayoffMatchup=True)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = ScoringShareCalculator.getOpponentScoringShare(year, weekNumberEnd=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci(100), sum(response.values()))
        self.assertEqual(Deci("68.05555555555555555555555556"), response[teams[0].id])
        self.assertEqual(Deci("31.94444444444444444444444444"), response[teams[1].id])

    def test_getOpponentScoringShare_weekNumberStartGivenAndWeekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=2.5)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.3, teamBScore=2.6,
                           isPlayoffMatchup=True)
        matchup4 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.4, teamBScore=2.7,
                           isPlayoffMatchup=True)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])
        week4 = Week(weekNumber=4, matchups=[matchup4])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3, week4])

        response = ScoringShareCalculator.getOpponentScoringShare(year, weekNumberStart=2, weekNumberEnd=3)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci(100), sum(response.values()))
        self.assertEqual(Deci("67.10526315789473684210526316"), response[teams[0].id])
        self.assertEqual(Deci("32.89473684210526315789473684"), response[teams[1].id])
