import unittest

from src.leeger.calculator.AdvancedGameOutcome import AdvancedGameOutcome
from src.leeger.model.Matchup import Matchup
from src.leeger.model.Week import Week
from src.leeger.model.Year import Year
from src.leeger.util.Deci import Deci
from test.helper.prototypes import getNDefaultOwnersAndTeams


class TestAdvancedGameOutcome(unittest.TestCase):
    def test_getWAL_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])
        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[matchup2])
        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=True, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getWAL(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.5"), response[teams[0].id])
        self.assertEqual(Deci("2.5"), response[teams[1].id])

    def test_getWAL_onlyPostSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])
        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[matchup2])
        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=True, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getWAL(year, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("2"), response[teams[1].id])

    def test_getWAL_onlyRegularSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup2])
        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getWAL(year, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("2"), response[teams[1].id])

    def test_getWAL_weekNumberStartGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=2, teamBScore=1)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup2])
        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getWAL(year, weekNumberStart=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("1"), response[teams[0].id])
        self.assertEqual(Deci("1"), response[teams[1].id])

    def test_getWAL_weekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=2, teamBScore=1)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup2])
        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getWAL(year, weekNumberEnd=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("2"), response[teams[1].id])

    def test_getWAL_weekNumberStartGivenAndWeekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=2, teamBScore=1)
        matchup4 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=2, teamBScore=1)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup2])
        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[matchup3])
        week4 = Week(weekNumber=4, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[matchup4])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3, week4])

        response = AdvancedGameOutcome.getWAL(year, weekNumberStart=2, weekNumberEnd=3)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("1"), response[teams[0].id])
        self.assertEqual(Deci("1"), response[teams[1].id])

    def test_getAWAL_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getAWAL(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0.6"), response[teams[1].id])
        self.assertEqual(Deci("1.2"), response[teams[2].id])
        self.assertEqual(Deci("2.1"), response[teams[3].id])
        self.assertEqual(Deci("2.1"), response[teams[4].id])
        self.assertEqual(Deci("3"), response[teams[5].id])

    def test_getAWAL_onlyPostSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=True,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getAWAL(year, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0.4"), response[teams[1].id])
        self.assertEqual(Deci("0.8"), response[teams[2].id])
        self.assertEqual(Deci("1.4"), response[teams[3].id])
        self.assertEqual(Deci("1.4"), response[teams[4].id])
        self.assertEqual(Deci("2"), response[teams[5].id])

    def test_getAWAL_onlyRegularSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=True,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getAWAL(year, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0.2"), response[teams[1].id])
        self.assertEqual(Deci("0.4"), response[teams[2].id])
        self.assertEqual(Deci("0.7"), response[teams[3].id])
        self.assertEqual(Deci("0.7"), response[teams[4].id])
        self.assertEqual(Deci("1"), response[teams[5].id])

    def test_getAWAL_weekNumberStartGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=True,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getAWAL(year, weekNumberStart=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0.4"), response[teams[1].id])
        self.assertEqual(Deci("0.8"), response[teams[2].id])
        self.assertEqual(Deci("1.4"), response[teams[3].id])
        self.assertEqual(Deci("1.4"), response[teams[4].id])
        self.assertEqual(Deci("2"), response[teams[5].id])

    def test_getAWAL_weekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=True,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getAWAL(year, weekNumberEnd=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0.4"), response[teams[1].id])
        self.assertEqual(Deci("0.8"), response[teams[2].id])
        self.assertEqual(Deci("1.4"), response[teams[3].id])
        self.assertEqual(Deci("1.4"), response[teams[4].id])
        self.assertEqual(Deci("2"), response[teams[5].id])

    def test_getAWAL_weekNumberStartGivenAndWeekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=True,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getAWAL(year, weekNumberStart=2, weekNumberEnd=3)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0.4"), response[teams[1].id])
        self.assertEqual(Deci("0.8"), response[teams[2].id])
        self.assertEqual(Deci("1.4"), response[teams[3].id])
        self.assertEqual(Deci("1.4"), response[teams[4].id])
        self.assertEqual(Deci("2"), response[teams[5].id])

    def test_getAWAL_matchupEndsInTie(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=3)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]], weeks=[week1])

        response = AdvancedGameOutcome.getAWAL(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0.2"), response[teams[1].id])
        self.assertEqual(Deci("0.5"), response[teams[2].id])
        self.assertEqual(Deci("0.5"), response[teams[3].id])
        self.assertEqual(Deci("0.8"), response[teams[4].id])
        self.assertEqual(Deci("1"), response[teams[5].id])

    def test_getAWAL_multipleMatchupsEndInTie(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=3)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]], weeks=[week1])

        response = AdvancedGameOutcome.getAWAL(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.1"), response[teams[0].id])
        self.assertEqual(Deci("0.1"), response[teams[1].id])
        self.assertEqual(Deci("0.5"), response[teams[2].id])
        self.assertEqual(Deci("0.5"), response[teams[3].id])
        self.assertEqual(Deci("0.8"), response[teams[4].id])
        self.assertEqual(Deci("1"), response[teams[5].id])

    def test_getAWAL_allMatchupsEndInTie(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=2, teamBScore=2)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=3, teamBScore=3)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]], weeks=[week1])

        response = AdvancedGameOutcome.getAWAL(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.1"), response[teams[0].id])
        self.assertEqual(Deci("0.1"), response[teams[1].id])
        self.assertEqual(Deci("0.5"), response[teams[2].id])
        self.assertEqual(Deci("0.5"), response[teams[3].id])
        self.assertEqual(Deci("0.9"), response[teams[4].id])
        self.assertEqual(Deci("0.9"), response[teams[5].id])

    def test_getAWAL_allMatchupsEndInTieAndHaveSameScore(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=1, teamBScore=1)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=1, teamBScore=1)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]], weeks=[week1])

        response = AdvancedGameOutcome.getAWAL(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.5"), response[teams[0].id])
        self.assertEqual(Deci("0.5"), response[teams[1].id])
        self.assertEqual(Deci("0.5"), response[teams[2].id])
        self.assertEqual(Deci("0.5"), response[teams[3].id])
        self.assertEqual(Deci("0.5"), response[teams[4].id])
        self.assertEqual(Deci("0.5"), response[teams[5].id])

    def test_getAWAL_sixteenTeams(self):
        owners, teams = getNDefaultOwnersAndTeams(16)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=5, teamBScore=6)
        matchup4 = Matchup(teamAId=teams[6].id, teamBId=teams[7].id, teamAScore=7, teamBScore=8)
        matchup5 = Matchup(teamAId=teams[8].id, teamBId=teams[9].id, teamAScore=9, teamBScore=10)
        matchup6 = Matchup(teamAId=teams[10].id, teamBId=teams[11].id, teamAScore=11, teamBScore=12)
        matchup7 = Matchup(teamAId=teams[12].id, teamBId=teams[13].id, teamAScore=13, teamBScore=14)
        matchup8 = Matchup(teamAId=teams[14].id, teamBId=teams[15].id, teamAScore=15, teamBScore=16)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3, matchup4, matchup5, matchup6, matchup7, matchup8])

        year = Year(yearNumber=2000,
                    teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5], teams[6], teams[7], teams[8],
                           teams[9], teams[10], teams[11],
                           teams[12], teams[13], teams[14], teams[15]], weeks=[week1])

        response = AdvancedGameOutcome.getAWAL(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(16, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0.06666666666666666666666666667"), response[teams[1].id])
        self.assertEqual(Deci("0.1333333333333333333333333333"), response[teams[2].id])
        self.assertEqual(Deci("0.2"), response[teams[3].id])
        self.assertEqual(Deci("0.2666666666666666666666666667"), response[teams[4].id])
        self.assertEqual(Deci("0.3333333333333333333333333334"), response[teams[5].id])
        self.assertEqual(Deci("0.4"), response[teams[6].id])
        self.assertEqual(Deci("0.4666666666666666666666666667"), response[teams[7].id])
        self.assertEqual(Deci("0.5333333333333333333333333334"), response[teams[8].id])
        self.assertEqual(Deci("0.6"), response[teams[9].id])
        self.assertEqual(Deci("0.6666666666666666666666666667"), response[teams[10].id])
        self.assertEqual(Deci("0.7333333333333333333333333334"), response[teams[11].id])
        self.assertEqual(Deci("0.8"), response[teams[12].id])
        self.assertEqual(Deci("0.8666666666666666666666666667"), response[teams[13].id])
        self.assertEqual(Deci("0.9333333333333333333333333334"), response[teams[14].id])
        self.assertEqual(Deci("1"), response[teams[15].id])

    def test_getAWALPerGame_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getAWALPerGame(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0.2"), response[teams[1].id])
        self.assertEqual(Deci("0.4"), response[teams[2].id])
        self.assertEqual(Deci("0.7"), response[teams[3].id])
        self.assertEqual(Deci("0.7"), response[teams[4].id])
        self.assertEqual(Deci("1"), response[teams[5].id])

    def test_getAWALPerGame_onlyPostSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=True,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getAWALPerGame(year, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0.2"), response[teams[1].id])
        self.assertEqual(Deci("0.4"), response[teams[2].id])
        self.assertEqual(Deci("0.7"), response[teams[3].id])
        self.assertEqual(Deci("0.7"), response[teams[4].id])
        self.assertEqual(Deci("1"), response[teams[5].id])

    def test_getAWALPerGame_onlyRegularSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=True,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getAWALPerGame(year, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0.2"), response[teams[1].id])
        self.assertEqual(Deci("0.4"), response[teams[2].id])
        self.assertEqual(Deci("0.7"), response[teams[3].id])
        self.assertEqual(Deci("0.7"), response[teams[4].id])
        self.assertEqual(Deci("1"), response[teams[5].id])

    def test_getAWALPerGame_weekNumberStartGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=True,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getAWALPerGame(year, weekNumberStart=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0.2"), response[teams[1].id])
        self.assertEqual(Deci("0.4"), response[teams[2].id])
        self.assertEqual(Deci("0.7"), response[teams[3].id])
        self.assertEqual(Deci("0.7"), response[teams[4].id])
        self.assertEqual(Deci("1"), response[teams[5].id])

    def test_getAWALPerGame_weekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=True,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getAWALPerGame(year, weekNumberEnd=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0.2"), response[teams[1].id])
        self.assertEqual(Deci("0.4"), response[teams[2].id])
        self.assertEqual(Deci("0.7"), response[teams[3].id])
        self.assertEqual(Deci("0.7"), response[teams[4].id])
        self.assertEqual(Deci("1"), response[teams[5].id])

    def test_getAWALPerGame_weekNumberStartGivenAndWeekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week4 = Week(weekNumber=4, isPlayoffWeek=True, isChampionshipWeek=True,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3, week4])

        response = AdvancedGameOutcome.getAWALPerGame(year, weekNumberStart=2, weekNumberEnd=3)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0.2"), response[teams[1].id])
        self.assertEqual(Deci("0.4"), response[teams[2].id])
        self.assertEqual(Deci("0.7"), response[teams[3].id])
        self.assertEqual(Deci("0.7"), response[teams[4].id])
        self.assertEqual(Deci("1"), response[teams[5].id])

    def test_getAWALPerGame_teamsDontPlayEveryWeek(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[5].id, teamAScore=2, teamBScore=1)

        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=True,
                     matchups=[matchup1])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2])

        response = AdvancedGameOutcome.getAWALPerGame(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.5"), response[teams[0].id])
        self.assertEqual(Deci("0.2"), response[teams[1].id])
        self.assertEqual(Deci("0.4"), response[teams[2].id])
        self.assertEqual(Deci("0.7"), response[teams[3].id])
        self.assertEqual(Deci("0.7"), response[teams[4].id])
        self.assertEqual(Deci("0.5"), response[teams[5].id])

    def test_getOpponentAWAL_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getOpponentAWAL(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.6"), response[teams[0].id])
        self.assertEqual(Deci("0"), response[teams[1].id])
        self.assertEqual(Deci("2.1"), response[teams[2].id])
        self.assertEqual(Deci("1.2"), response[teams[3].id])
        self.assertEqual(Deci("3"), response[teams[4].id])
        self.assertEqual(Deci("2.1"), response[teams[5].id])

    def test_getOpponentAWAL_onlyPostSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=True,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getOpponentAWAL(year, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.4"), response[teams[0].id])
        self.assertEqual(Deci("0"), response[teams[1].id])
        self.assertEqual(Deci("1.4"), response[teams[2].id])
        self.assertEqual(Deci("0.8"), response[teams[3].id])
        self.assertEqual(Deci("2"), response[teams[4].id])
        self.assertEqual(Deci("1.4"), response[teams[5].id])

    def test_getOpponentAWAL_onlyRegularSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=True,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getOpponentAWAL(year, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.2"), response[teams[0].id])
        self.assertEqual(Deci("0"), response[teams[1].id])
        self.assertEqual(Deci("0.7"), response[teams[2].id])
        self.assertEqual(Deci("0.4"), response[teams[3].id])
        self.assertEqual(Deci("1"), response[teams[4].id])
        self.assertEqual(Deci("0.7"), response[teams[5].id])

    def test_getOpponentAWAL_weekNumberStartGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=True,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getOpponentAWAL(year, weekNumberStart=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.4"), response[teams[0].id])
        self.assertEqual(Deci("0"), response[teams[1].id])
        self.assertEqual(Deci("1.4"), response[teams[2].id])
        self.assertEqual(Deci("0.8"), response[teams[3].id])
        self.assertEqual(Deci("2"), response[teams[4].id])
        self.assertEqual(Deci("1.4"), response[teams[5].id])

    def test_getOpponentAWAL_weekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=True,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getOpponentAWAL(year, weekNumberEnd=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.4"), response[teams[0].id])
        self.assertEqual(Deci("0"), response[teams[1].id])
        self.assertEqual(Deci("1.4"), response[teams[2].id])
        self.assertEqual(Deci("0.8"), response[teams[3].id])
        self.assertEqual(Deci("2"), response[teams[4].id])
        self.assertEqual(Deci("1.4"), response[teams[5].id])

    def test_getOpponentAWAL_weekNumberStartGivenAndWeekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=True,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getOpponentAWAL(year, weekNumberStart=2, weekNumberEnd=3)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.4"), response[teams[0].id])
        self.assertEqual(Deci("0"), response[teams[1].id])
        self.assertEqual(Deci("1.4"), response[teams[2].id])
        self.assertEqual(Deci("0.8"), response[teams[3].id])
        self.assertEqual(Deci("2"), response[teams[4].id])
        self.assertEqual(Deci("1.4"), response[teams[5].id])

    def test_getOpponentAWAL_matchupEndsInTie(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=3)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]], weeks=[week1])

        response = AdvancedGameOutcome.getOpponentAWAL(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.2"), response[teams[0].id])
        self.assertEqual(Deci("0"), response[teams[1].id])
        self.assertEqual(Deci("0.5"), response[teams[2].id])
        self.assertEqual(Deci("0.5"), response[teams[3].id])
        self.assertEqual(Deci("1"), response[teams[4].id])
        self.assertEqual(Deci("0.8"), response[teams[5].id])

    def test_getOpponentAWAL_multipleMatchupsEndInTie(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=3)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]], weeks=[week1])

        response = AdvancedGameOutcome.getOpponentAWAL(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.1"), response[teams[0].id])
        self.assertEqual(Deci("0.1"), response[teams[1].id])
        self.assertEqual(Deci("0.5"), response[teams[2].id])
        self.assertEqual(Deci("0.5"), response[teams[3].id])
        self.assertEqual(Deci("1"), response[teams[4].id])
        self.assertEqual(Deci("0.8"), response[teams[5].id])

    def test_getOpponentAWAL_allMatchupsEndInTie(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=2, teamBScore=2)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=3, teamBScore=3)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]], weeks=[week1])

        response = AdvancedGameOutcome.getOpponentAWAL(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.1"), response[teams[0].id])
        self.assertEqual(Deci("0.1"), response[teams[1].id])
        self.assertEqual(Deci("0.5"), response[teams[2].id])
        self.assertEqual(Deci("0.5"), response[teams[3].id])
        self.assertEqual(Deci("0.9"), response[teams[4].id])
        self.assertEqual(Deci("0.9"), response[teams[5].id])

    def test_getOpponentAWAL_allMatchupsEndInTieAndHaveSameScore(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=1, teamBScore=1)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=1, teamBScore=1)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]], weeks=[week1])

        response = AdvancedGameOutcome.getOpponentAWAL(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.5"), response[teams[0].id])
        self.assertEqual(Deci("0.5"), response[teams[1].id])
        self.assertEqual(Deci("0.5"), response[teams[2].id])
        self.assertEqual(Deci("0.5"), response[teams[3].id])
        self.assertEqual(Deci("0.5"), response[teams[4].id])
        self.assertEqual(Deci("0.5"), response[teams[5].id])

    def test_getOpponentAWAL_sixteenTeams(self):
        owners, teams = getNDefaultOwnersAndTeams(16)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=5, teamBScore=6)
        matchup4 = Matchup(teamAId=teams[6].id, teamBId=teams[7].id, teamAScore=7, teamBScore=8)
        matchup5 = Matchup(teamAId=teams[8].id, teamBId=teams[9].id, teamAScore=9, teamBScore=10)
        matchup6 = Matchup(teamAId=teams[10].id, teamBId=teams[11].id, teamAScore=11, teamBScore=12)
        matchup7 = Matchup(teamAId=teams[12].id, teamBId=teams[13].id, teamAScore=13, teamBScore=14)
        matchup8 = Matchup(teamAId=teams[14].id, teamBId=teams[15].id, teamAScore=15, teamBScore=16)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3, matchup4, matchup5, matchup6, matchup7, matchup8])

        year = Year(yearNumber=2000,
                    teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5], teams[6], teams[7], teams[8],
                           teams[9], teams[10], teams[11],
                           teams[12], teams[13], teams[14], teams[15]], weeks=[week1])

        response = AdvancedGameOutcome.getOpponentAWAL(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(16, len(response.keys()))
        self.assertEqual(Deci("0.06666666666666666666666666667"), response[teams[0].id])
        self.assertEqual(Deci("0"), response[teams[1].id])
        self.assertEqual(Deci("0.2"), response[teams[2].id])
        self.assertEqual(Deci("0.1333333333333333333333333333"), response[teams[3].id])
        self.assertEqual(Deci("0.3333333333333333333333333334"), response[teams[4].id])
        self.assertEqual(Deci("0.2666666666666666666666666667"), response[teams[5].id])
        self.assertEqual(Deci("0.4666666666666666666666666667"), response[teams[6].id])
        self.assertEqual(Deci("0.4"), response[teams[7].id])
        self.assertEqual(Deci("0.6"), response[teams[8].id])
        self.assertEqual(Deci("0.5333333333333333333333333334"), response[teams[9].id])
        self.assertEqual(Deci("0.7333333333333333333333333334"), response[teams[10].id])
        self.assertEqual(Deci("0.6666666666666666666666666667"), response[teams[11].id])
        self.assertEqual(Deci("0.8666666666666666666666666667"), response[teams[12].id])
        self.assertEqual(Deci("0.8"), response[teams[13].id])
        self.assertEqual(Deci("1"), response[teams[14].id])
        self.assertEqual(Deci("0.9333333333333333333333333334"), response[teams[15].id])

    def test_getSmartWins_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getSmartWins(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.1764705882352941176470588236"), response[teams[0].id])
        self.assertEqual(Deci("0.7058823529411764705882352941"), response[teams[1].id])
        self.assertEqual(Deci("1.235294117647058823529411765"), response[teams[2].id])
        self.assertEqual(Deci("2.029411764705882352941176470"), response[teams[3].id])
        self.assertEqual(Deci("2.029411764705882352941176470"), response[teams[4].id])
        self.assertEqual(Deci("2.823529411764705882352941177"), response[teams[5].id])

    def test_getSmartWins_onlyPostSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=True,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getSmartWins(year, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.09090909090909090909090909090"), response[teams[0].id])
        self.assertEqual(Deci("0.4545454545454545454545454546"), response[teams[1].id])
        self.assertEqual(Deci("0.8181818181818181818181818182"), response[teams[2].id])
        self.assertEqual(Deci("1.363636363636363636363636364"), response[teams[3].id])
        self.assertEqual(Deci("1.363636363636363636363636364"), response[teams[4].id])
        self.assertEqual(Deci("1.909090909090909090909090909"), response[teams[5].id])

    def test_getSmartWins_onlyRegularSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=True,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getSmartWins(year, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0.2"), response[teams[1].id])
        self.assertEqual(Deci("0.4"), response[teams[2].id])
        self.assertEqual(Deci("0.7"), response[teams[3].id])
        self.assertEqual(Deci("0.7"), response[teams[4].id])
        self.assertEqual(Deci("1"), response[teams[5].id])

    def test_getSmartWins_weekNumberStartGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=True,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getSmartWins(year, weekNumberStart=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.09090909090909090909090909090"), response[teams[0].id])
        self.assertEqual(Deci("0.4545454545454545454545454546"), response[teams[1].id])
        self.assertEqual(Deci("0.8181818181818181818181818182"), response[teams[2].id])
        self.assertEqual(Deci("1.363636363636363636363636364"), response[teams[3].id])
        self.assertEqual(Deci("1.363636363636363636363636364"), response[teams[4].id])
        self.assertEqual(Deci("1.909090909090909090909090909"), response[teams[5].id])

    def test_getSmartWins_weekNumberStartGivenAndWeekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week4 = Week(weekNumber=4, isPlayoffWeek=True, isChampionshipWeek=True,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3, week4])

        response = AdvancedGameOutcome.getSmartWins(year, weekNumberStart=2, weekNumberEnd=3)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.09090909090909090909090909090"), response[teams[0].id])
        self.assertEqual(Deci("0.4545454545454545454545454546"), response[teams[1].id])
        self.assertEqual(Deci("0.8181818181818181818181818182"), response[teams[2].id])
        self.assertEqual(Deci("1.363636363636363636363636364"), response[teams[3].id])
        self.assertEqual(Deci("1.363636363636363636363636364"), response[teams[4].id])
        self.assertEqual(Deci("1.909090909090909090909090909"), response[teams[5].id])

    def test_getSmartWinsPerGame_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getSmartWinsPerGame(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.0588235294117647058823529412"), response[teams[0].id])
        self.assertEqual(Deci("0.2352941176470588235294117647"), response[teams[1].id])
        self.assertEqual(Deci("0.4117647058823529411764705883"), response[teams[2].id])
        self.assertEqual(Deci("0.6764705882352941176470588233"), response[teams[3].id])
        self.assertEqual(Deci("0.6764705882352941176470588233"), response[teams[4].id])
        self.assertEqual(Deci("0.941176470588235294117647059"), response[teams[5].id])

    def test_getSmartWinsPerGame_onlyPostSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=True,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getSmartWinsPerGame(year, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.04545454545454545454545454545"), response[teams[0].id])
        self.assertEqual(Deci("0.2272727272727272727272727273"), response[teams[1].id])
        self.assertEqual(Deci("0.4090909090909090909090909091"), response[teams[2].id])
        self.assertEqual(Deci("0.681818181818181818181818182"), response[teams[3].id])
        self.assertEqual(Deci("0.681818181818181818181818182"), response[teams[4].id])
        self.assertEqual(Deci("0.9545454545454545454545454545"), response[teams[5].id])

    def test_getSmartWinsPerGame_onlyRegularSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=True,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getSmartWinsPerGame(year, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0.2"), response[teams[1].id])
        self.assertEqual(Deci("0.4"), response[teams[2].id])
        self.assertEqual(Deci("0.7"), response[teams[3].id])
        self.assertEqual(Deci("0.7"), response[teams[4].id])
        self.assertEqual(Deci("1"), response[teams[5].id])

    def test_getSmartWinsPerGame_weekNumberStartGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=True,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getSmartWinsPerGame(year, weekNumberStart=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.04545454545454545454545454545"), response[teams[0].id])
        self.assertEqual(Deci("0.2272727272727272727272727273"), response[teams[1].id])
        self.assertEqual(Deci("0.4090909090909090909090909091"), response[teams[2].id])
        self.assertEqual(Deci("0.681818181818181818181818182"), response[teams[3].id])
        self.assertEqual(Deci("0.681818181818181818181818182"), response[teams[4].id])
        self.assertEqual(Deci("0.9545454545454545454545454545"), response[teams[5].id])

    def test_getSmartWinsPerGame_weekNumberStartGivenAndWeekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week4 = Week(weekNumber=4, isPlayoffWeek=True, isChampionshipWeek=True,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3, week4])

        response = AdvancedGameOutcome.getSmartWinsPerGame(year, weekNumberStart=2, weekNumberEnd=3)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.04545454545454545454545454545"), response[teams[0].id])
        self.assertEqual(Deci("0.2272727272727272727272727273"), response[teams[1].id])
        self.assertEqual(Deci("0.4090909090909090909090909091"), response[teams[2].id])
        self.assertEqual(Deci("0.681818181818181818181818182"), response[teams[3].id])
        self.assertEqual(Deci("0.681818181818181818181818182"), response[teams[4].id])
        self.assertEqual(Deci("0.9545454545454545454545454545"), response[teams[5].id])
