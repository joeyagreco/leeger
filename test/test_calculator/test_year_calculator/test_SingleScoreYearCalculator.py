import unittest

from src.leeger.calculator.year_calculator.SingleScoreYearCalculator import SingleScoreYearCalculator
from src.leeger.enum.MatchupType import MatchupType
from src.leeger.model.league.Matchup import Matchup
from src.leeger.model.league.Week import Week
from src.leeger.model.league.Year import Year
from test.helper.prototypes import getNDefaultOwnersAndTeams


class TestSingleScoreYearCalculator(unittest.TestCase):

    def test_getMaxScore_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.1,
                           matchupType=MatchupType.IGNORE)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3.1, teamBScore=4.1)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4.1, teamBScore=5)
        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup4 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=2.2)
        matchup5 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3.2, teamBScore=4.2)
        matchup6 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4.2, teamBScore=6)
        week2 = Week(weekNumber=2, matchups=[matchup4, matchup5, matchup6])

        matchup7 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.3, teamBScore=2.3,
                           matchupType=MatchupType.PLAYOFF)
        matchup8 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3.3, teamBScore=4.3,
                           matchupType=MatchupType.PLAYOFF)
        matchup9 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4.3, teamBScore=7,
                           matchupType=MatchupType.CHAMPIONSHIP)
        week3 = Week(weekNumber=3, matchups=[matchup7, matchup8, matchup9])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = SingleScoreYearCalculator.getMaxScore(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(1.3, response[teams[0].id])
        self.assertEqual(2.3, response[teams[1].id])
        self.assertEqual(3.3, response[teams[2].id])
        self.assertEqual(4.3, response[teams[3].id])
        self.assertEqual(4.3, response[teams[4].id])
        self.assertEqual(7, response[teams[5].id])

    def test_getMaxScore_onlyPostSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.1,
                           matchupType=MatchupType.IGNORE)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3.1, teamBScore=4.1)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4.1, teamBScore=5)
        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup4 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=10.2, teamBScore=20.2)
        matchup5 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=30.2, teamBScore=40.2)
        matchup6 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=40.2, teamBScore=60)
        week2 = Week(weekNumber=2, matchups=[matchup4, matchup5, matchup6])

        matchup7 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.3, teamBScore=2.3,
                           matchupType=MatchupType.PLAYOFF)
        matchup8 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3.3, teamBScore=4.3,
                           matchupType=MatchupType.PLAYOFF)
        matchup9 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4.3, teamBScore=7,
                           matchupType=MatchupType.CHAMPIONSHIP)
        week3 = Week(weekNumber=3, matchups=[matchup7, matchup8, matchup9])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = SingleScoreYearCalculator.getMaxScore(year, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(1.3, response[teams[0].id])
        self.assertEqual(2.3, response[teams[1].id])
        self.assertEqual(3.3, response[teams[2].id])
        self.assertEqual(4.3, response[teams[3].id])
        self.assertEqual(4.3, response[teams[4].id])
        self.assertEqual(7, response[teams[5].id])

    def test_getMaxScore_onlyRegularSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.1,
                           matchupType=MatchupType.IGNORE)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3.1, teamBScore=4.1)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4.1, teamBScore=5)
        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup4 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=2.2)
        matchup5 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3.2, teamBScore=4.2)
        matchup6 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4.2, teamBScore=6)
        week2 = Week(weekNumber=2, matchups=[matchup4, matchup5, matchup6])

        matchup7 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.3, teamBScore=2.3,
                           matchupType=MatchupType.PLAYOFF)
        matchup8 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3.3, teamBScore=4.3,
                           matchupType=MatchupType.PLAYOFF)
        matchup9 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4.3, teamBScore=7,
                           matchupType=MatchupType.CHAMPIONSHIP)
        week3 = Week(weekNumber=3, matchups=[matchup7, matchup8, matchup9])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = SingleScoreYearCalculator.getMaxScore(year, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(1.2, response[teams[0].id])
        self.assertEqual(2.2, response[teams[1].id])
        self.assertEqual(3.2, response[teams[2].id])
        self.assertEqual(4.2, response[teams[3].id])
        self.assertEqual(4.2, response[teams[4].id])
        self.assertEqual(6, response[teams[5].id])

    def test_getMaxScore_onlyChampionshipIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.1,
                           matchupType=MatchupType.IGNORE)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3.1, teamBScore=4.1)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4.1, teamBScore=5)
        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup4 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=2.2)
        matchup5 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3.2, teamBScore=4.2)
        matchup6 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4.2, teamBScore=6)
        week2 = Week(weekNumber=2, matchups=[matchup4, matchup5, matchup6])

        matchup7 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.3, teamBScore=2.3,
                           matchupType=MatchupType.PLAYOFF)
        matchup8 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3.3, teamBScore=4.3,
                           matchupType=MatchupType.PLAYOFF)
        matchup9 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4.3, teamBScore=7,
                           matchupType=MatchupType.CHAMPIONSHIP)
        week3 = Week(weekNumber=3, matchups=[matchup7, matchup8, matchup9])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = SingleScoreYearCalculator.getMaxScore(year, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertIsNone(response[teams[0].id])
        self.assertIsNone(response[teams[1].id])
        self.assertIsNone(response[teams[2].id])
        self.assertIsNone(response[teams[3].id])
        self.assertEqual(4.3, response[teams[4].id])
        self.assertEqual(7, response[teams[5].id])

    def test_getMaxScore_weekNumberStartGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=10.1, teamBScore=20.1,
                           matchupType=MatchupType.IGNORE)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=30.1, teamBScore=40.1)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=40.1, teamBScore=50)
        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup4 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=2.2)
        matchup5 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3.2, teamBScore=4.2)
        matchup6 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4.2, teamBScore=6)
        week2 = Week(weekNumber=2, matchups=[matchup4, matchup5, matchup6])

        matchup7 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.3, teamBScore=2.3,
                           matchupType=MatchupType.PLAYOFF)
        matchup8 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3.3, teamBScore=4.3,
                           matchupType=MatchupType.PLAYOFF)
        matchup9 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4.3, teamBScore=7,
                           matchupType=MatchupType.CHAMPIONSHIP)
        week3 = Week(weekNumber=3, matchups=[matchup7, matchup8, matchup9])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = SingleScoreYearCalculator.getMaxScore(year, weekNumberStart=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(1.3, response[teams[0].id])
        self.assertEqual(2.3, response[teams[1].id])
        self.assertEqual(3.3, response[teams[2].id])
        self.assertEqual(4.3, response[teams[3].id])
        self.assertEqual(4.3, response[teams[4].id])
        self.assertEqual(7, response[teams[5].id])

    def test_getMaxScore_weekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.1,
                           matchupType=MatchupType.IGNORE)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3.1, teamBScore=4.1)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4.1, teamBScore=5)
        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup4 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=2.2)
        matchup5 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3.2, teamBScore=4.2)
        matchup6 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4.2, teamBScore=6)
        week2 = Week(weekNumber=2, matchups=[matchup4, matchup5, matchup6])

        matchup7 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.3, teamBScore=2.3,
                           matchupType=MatchupType.PLAYOFF)
        matchup8 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3.3, teamBScore=4.3,
                           matchupType=MatchupType.PLAYOFF)
        matchup9 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4.3, teamBScore=7,
                           matchupType=MatchupType.CHAMPIONSHIP)
        week3 = Week(weekNumber=3, matchups=[matchup7, matchup8, matchup9])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = SingleScoreYearCalculator.getMaxScore(year, weekNumberEnd=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(1.2, response[teams[0].id])
        self.assertEqual(2.2, response[teams[1].id])
        self.assertEqual(3.2, response[teams[2].id])
        self.assertEqual(4.2, response[teams[3].id])
        self.assertEqual(4.2, response[teams[4].id])
        self.assertEqual(6, response[teams[5].id])

    def test_getMaxScore_weekNumberStartGivenAndWeekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.1,
                           matchupType=MatchupType.IGNORE)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3.1, teamBScore=4.1)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4.1, teamBScore=5)
        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup4 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=2.2)
        matchup5 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3.2, teamBScore=4.2)
        matchup6 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4.2, teamBScore=6)
        week2 = Week(weekNumber=2, matchups=[matchup4, matchup5, matchup6])

        matchup7 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.3, teamBScore=2.3)
        matchup8 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3.3, teamBScore=4.3)
        matchup9 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4.3, teamBScore=7)
        week3 = Week(weekNumber=3, matchups=[matchup7, matchup8, matchup9])

        matchup10 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=10.3, teamBScore=20.3,
                            matchupType=MatchupType.PLAYOFF)
        matchup11 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=30.3, teamBScore=40.3,
                            matchupType=MatchupType.PLAYOFF)
        matchup12 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=40.3, teamBScore=70,
                            matchupType=MatchupType.CHAMPIONSHIP)
        week4 = Week(weekNumber=4, matchups=[matchup10, matchup11, matchup12])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = SingleScoreYearCalculator.getMaxScore(year, weekNumberStart=2, weekNumberEnd=3)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(1.3, response[teams[0].id])
        self.assertEqual(2.3, response[teams[1].id])
        self.assertEqual(3.3, response[teams[2].id])
        self.assertEqual(4.3, response[teams[3].id])
        self.assertEqual(4.3, response[teams[4].id])
        self.assertEqual(7, response[teams[5].id])

    def test_getMinScore_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=1)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=3,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.3, teamBScore=2.9,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = SingleScoreYearCalculator.getMinScore(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(1.1, response[teams[0].id])
        self.assertEqual(1, response[teams[1].id])

    def test_getMinScore_onlyPostSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.3, teamBScore=2.6,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = SingleScoreYearCalculator.getMinScore(year, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(1.2, response[teams[0].id])
        self.assertEqual(2, response[teams[1].id])

    def test_getMinScore_onlyRegularSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=2)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = SingleScoreYearCalculator.getMinScore(year, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(1.1, response[teams[0].id])
        self.assertEqual(2, response[teams[1].id])

    def test_getMinScore_onlyChampionshipIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = SingleScoreYearCalculator.getMinScore(year, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(3, response[teams[0].id])
        self.assertEqual(4, response[teams[1].id])

    def test_getMinScore_weekNumberStartGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=2.5)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.3, teamBScore=2.6,
                           matchupType=MatchupType.PLAYOFF)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = SingleScoreYearCalculator.getMinScore(year, weekNumberStart=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(1.2, response[teams[0].id])
        self.assertEqual(2.5, response[teams[1].id])

    def test_getMinScore_weekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=2.5)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = SingleScoreYearCalculator.getMinScore(year, weekNumberEnd=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(1.1, response[teams[0].id])
        self.assertEqual(2.4, response[teams[1].id])

    def test_getMinScore_weekNumberStartGivenAndWeekNumberEndGiven(self):
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

        response = SingleScoreYearCalculator.getMinScore(year, weekNumberStart=2, weekNumberEnd=3)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(1.2, response[teams[0].id])
        self.assertEqual(2.5, response[teams[1].id])
