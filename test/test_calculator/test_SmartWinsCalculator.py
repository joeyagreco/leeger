import unittest

from src.leeger.calculator.SmartWinsCalculator import SmartWinsCalculator
from src.leeger.enum.MatchupType import MatchupType
from src.leeger.model.Matchup import Matchup
from src.leeger.model.Week import Week
from src.leeger.model.Year import Year
from src.leeger.util.Deci import Deci
from test.helper.prototypes import getNDefaultOwnersAndTeams


class TestSmartWinsCalculator(unittest.TestCase):

    def test_getSmartWins_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
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

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3])

        response = SmartWinsCalculator.getSmartWins(year)

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

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.PLAYOFF)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3])

        response = SmartWinsCalculator.getSmartWins(year, onlyPostSeason=True)

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

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.PLAYOFF)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3])

        response = SmartWinsCalculator.getSmartWins(year, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0.2"), response[teams[1].id])
        self.assertEqual(Deci("0.4"), response[teams[2].id])
        self.assertEqual(Deci("0.7"), response[teams[3].id])
        self.assertEqual(Deci("0.7"), response[teams[4].id])
        self.assertEqual(Deci("1"), response[teams[5].id])

    def test_getSmartWins_onlyChampionshipIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.PLAYOFF)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = SmartWinsCalculator.getSmartWins(year, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0"), response[teams[1].id])
        self.assertEqual(Deci("0"), response[teams[2].id])
        self.assertEqual(Deci("0"), response[teams[3].id])
        self.assertEqual(Deci("0"), response[teams[4].id])
        self.assertEqual(Deci("1"), response[teams[5].id])

    def test_getSmartWins_weekNumberStartGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.PLAYOFF)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3])

        response = SmartWinsCalculator.getSmartWins(year, weekNumberStart=2)

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

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.PLAYOFF)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.PLAYOFF)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week4 = Week(weekNumber=4, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3, week4])

        response = SmartWinsCalculator.getSmartWins(year, weekNumberStart=2, weekNumberEnd=3)

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

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3])

        response = SmartWinsCalculator.getSmartWinsPerGame(year)

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

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.PLAYOFF)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3])

        response = SmartWinsCalculator.getSmartWinsPerGame(year, onlyPostSeason=True)

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

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.PLAYOFF)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3])

        response = SmartWinsCalculator.getSmartWinsPerGame(year, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0.2"), response[teams[1].id])
        self.assertEqual(Deci("0.4"), response[teams[2].id])
        self.assertEqual(Deci("0.7"), response[teams[3].id])
        self.assertEqual(Deci("0.7"), response[teams[4].id])
        self.assertEqual(Deci("1"), response[teams[5].id])

    def test_getSmartWinsPerGame_onlyChampionshipIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.PLAYOFF)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = SmartWinsCalculator.getSmartWinsPerGame(year, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0"), response[teams[1].id])
        self.assertEqual(Deci("0"), response[teams[2].id])
        self.assertEqual(Deci("0"), response[teams[3].id])
        self.assertEqual(Deci("0"), response[teams[4].id])
        self.assertEqual(Deci("1"), response[teams[5].id])

    def test_getSmartWinsPerGame_weekNumberStartGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.PLAYOFF)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3])

        response = SmartWinsCalculator.getSmartWinsPerGame(year, weekNumberStart=2)

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

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.PLAYOFF)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.PLAYOFF)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week4 = Week(weekNumber=4, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3, week4])

        response = SmartWinsCalculator.getSmartWinsPerGame(year, weekNumberStart=2, weekNumberEnd=3)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.04545454545454545454545454545"), response[teams[0].id])
        self.assertEqual(Deci("0.2272727272727272727272727273"), response[teams[1].id])
        self.assertEqual(Deci("0.4090909090909090909090909091"), response[teams[2].id])
        self.assertEqual(Deci("0.681818181818181818181818182"), response[teams[3].id])
        self.assertEqual(Deci("0.681818181818181818181818182"), response[teams[4].id])
        self.assertEqual(Deci("0.9545454545454545454545454545"), response[teams[5].id])

    def test_getOpponentSmartWins_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
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

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3])

        response = SmartWinsCalculator.getOpponentSmartWins(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.7058823529411764705882352941"), response[teams[0].id])
        self.assertEqual(Deci("0.1764705882352941176470588236"), response[teams[1].id])
        self.assertEqual(Deci("2.029411764705882352941176470"), response[teams[2].id])
        self.assertEqual(Deci("1.235294117647058823529411765"), response[teams[3].id])
        self.assertEqual(Deci("2.823529411764705882352941177"), response[teams[4].id])
        self.assertEqual(Deci("2.029411764705882352941176470"), response[teams[5].id])

    def test_getOpponentSmartWins_onlyPostSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.PLAYOFF)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3])

        response = SmartWinsCalculator.getOpponentSmartWins(year, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.4545454545454545454545454546"), response[teams[0].id])
        self.assertEqual(Deci("0.09090909090909090909090909090"), response[teams[1].id])
        self.assertEqual(Deci("1.363636363636363636363636364"), response[teams[2].id])
        self.assertEqual(Deci("0.8181818181818181818181818182"), response[teams[3].id])
        self.assertEqual(Deci("1.909090909090909090909090909"), response[teams[4].id])
        self.assertEqual(Deci("1.363636363636363636363636364"), response[teams[5].id])

    def test_getOpponentSmartWins_onlyRegularSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.PLAYOFF)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3])

        response = SmartWinsCalculator.getOpponentSmartWins(year, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.2"), response[teams[0].id])
        self.assertEqual(Deci("0"), response[teams[1].id])
        self.assertEqual(Deci("0.7"), response[teams[2].id])
        self.assertEqual(Deci("0.4"), response[teams[3].id])
        self.assertEqual(Deci("1"), response[teams[4].id])
        self.assertEqual(Deci("0.7"), response[teams[5].id])

    def test_getOpponentSmartWins_onlyChampionshipIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.PLAYOFF)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = SmartWinsCalculator.getOpponentSmartWins(year, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0"), response[teams[1].id])
        self.assertEqual(Deci("0"), response[teams[2].id])
        self.assertEqual(Deci("0"), response[teams[3].id])
        self.assertEqual(Deci("1"), response[teams[4].id])
        self.assertEqual(Deci("0"), response[teams[5].id])

    def test_getOpponentSmartWins_weekNumberStartGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.PLAYOFF)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3])

        response = SmartWinsCalculator.getOpponentSmartWins(year, weekNumberStart=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.4545454545454545454545454546"), response[teams[0].id])
        self.assertEqual(Deci("0.09090909090909090909090909090"), response[teams[1].id])
        self.assertEqual(Deci("1.363636363636363636363636364"), response[teams[2].id])
        self.assertEqual(Deci("0.8181818181818181818181818182"), response[teams[3].id])
        self.assertEqual(Deci("1.909090909090909090909090909"), response[teams[4].id])
        self.assertEqual(Deci("1.363636363636363636363636364"), response[teams[5].id])

    def test_getOpponentSmartWins_weekNumberStartGivenAndWeekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.PLAYOFF)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.PLAYOFF)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week4 = Week(weekNumber=4, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3, week4])

        response = SmartWinsCalculator.getOpponentSmartWins(year, weekNumberStart=2, weekNumberEnd=3)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.4545454545454545454545454546"), response[teams[0].id])
        self.assertEqual(Deci("0.09090909090909090909090909090"), response[teams[1].id])
        self.assertEqual(Deci("1.363636363636363636363636364"), response[teams[2].id])
        self.assertEqual(Deci("0.8181818181818181818181818182"), response[teams[3].id])
        self.assertEqual(Deci("1.909090909090909090909090909"), response[teams[4].id])
        self.assertEqual(Deci("1.363636363636363636363636364"), response[teams[5].id])

    def test_getOpponentSmartWinsPerGame_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
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

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3])

        response = SmartWinsCalculator.getOpponentSmartWinsPerGame(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.2352941176470588235294117647"), response[teams[0].id])
        self.assertEqual(Deci("0.0588235294117647058823529412"), response[teams[1].id])
        self.assertEqual(Deci("0.6764705882352941176470588233"), response[teams[2].id])
        self.assertEqual(Deci("0.4117647058823529411764705883"), response[teams[3].id])
        self.assertEqual(Deci("0.941176470588235294117647059"), response[teams[4].id])
        self.assertEqual(Deci("0.6764705882352941176470588233"), response[teams[5].id])

    def test_getOpponentSmartWinsPerGame_onlyPostSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.PLAYOFF)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3])

        response = SmartWinsCalculator.getOpponentSmartWinsPerGame(year, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.2272727272727272727272727273"), response[teams[0].id])
        self.assertEqual(Deci("0.04545454545454545454545454545"), response[teams[1].id])
        self.assertEqual(Deci("0.681818181818181818181818182"), response[teams[2].id])
        self.assertEqual(Deci("0.4090909090909090909090909091"), response[teams[3].id])
        self.assertEqual(Deci("0.9545454545454545454545454545"), response[teams[4].id])
        self.assertEqual(Deci("0.681818181818181818181818182"), response[teams[5].id])

    def test_getOpponentSmartWinsPerGame_onlyRegularSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.PLAYOFF)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3])

        response = SmartWinsCalculator.getOpponentSmartWinsPerGame(year, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.2"), response[teams[0].id])
        self.assertEqual(Deci("0"), response[teams[1].id])
        self.assertEqual(Deci("0.7"), response[teams[2].id])
        self.assertEqual(Deci("0.4"), response[teams[3].id])
        self.assertEqual(Deci("1"), response[teams[4].id])
        self.assertEqual(Deci("0.7"), response[teams[5].id])

    def test_getOpponentSmartWinsPerGame_onlyChampionshipIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.PLAYOFF)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = SmartWinsCalculator.getOpponentSmartWinsPerGame(year, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0"), response[teams[1].id])
        self.assertEqual(Deci("0"), response[teams[2].id])
        self.assertEqual(Deci("0"), response[teams[3].id])
        self.assertEqual(Deci("1"), response[teams[4].id])
        self.assertEqual(Deci("0"), response[teams[5].id])

    def test_getOpponentSmartWinsPerGame_weekNumberStartGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.PLAYOFF)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3])

        response = SmartWinsCalculator.getOpponentSmartWinsPerGame(year, weekNumberStart=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.2272727272727272727272727273"), response[teams[0].id])
        self.assertEqual(Deci("0.04545454545454545454545454545"), response[teams[1].id])
        self.assertEqual(Deci("0.681818181818181818181818182"), response[teams[2].id])
        self.assertEqual(Deci("0.4090909090909090909090909091"), response[teams[3].id])
        self.assertEqual(Deci("0.9545454545454545454545454545"), response[teams[4].id])
        self.assertEqual(Deci("0.681818181818181818181818182"), response[teams[5].id])

    def test_getOpponentSmartWinsPerGame_weekNumberStartGivenAndWeekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.PLAYOFF)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.PLAYOFF)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week4 = Week(weekNumber=4, matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
                    weeks=[week1, week2, week3, week4])

        response = SmartWinsCalculator.getOpponentSmartWinsPerGame(year, weekNumberStart=2, weekNumberEnd=3)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.2272727272727272727272727273"), response[teams[0].id])
        self.assertEqual(Deci("0.04545454545454545454545454545"), response[teams[1].id])
        self.assertEqual(Deci("0.681818181818181818181818182"), response[teams[2].id])
        self.assertEqual(Deci("0.4090909090909090909090909091"), response[teams[3].id])
        self.assertEqual(Deci("0.9545454545454545454545454545"), response[teams[4].id])
        self.assertEqual(Deci("0.681818181818181818181818182"), response[teams[5].id])
