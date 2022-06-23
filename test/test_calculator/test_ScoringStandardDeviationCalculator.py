import unittest

from src.leeger.calculator.year_calculator.ScoringStandardDeviationCalculator import ScoringStandardDeviationCalculator
from src.leeger.enum.MatchupType import MatchupType
from src.leeger.model.league.Matchup import Matchup
from src.leeger.model.league.Week import Week
from src.leeger.model.league.Year import Year
from src.leeger.util.Deci import Deci
from test.helper.prototypes import getNDefaultOwnersAndTeams


class TestScoringStandardDeviationCalculator(unittest.TestCase):

    def test_getScoringStandardDeviation_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=2.5,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.3, teamBScore=5,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = ScoringStandardDeviationCalculator.getScoringStandardDeviation(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.08164965809277260327324280249"), response[teams[0].id])
        self.assertEqual(Deci("1.202774570177914372863325978"), response[teams[1].id])

    def test_getScoringStandardDeviation_onlyPostSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=2.5,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.3, teamBScore=3,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = ScoringStandardDeviationCalculator.getScoringStandardDeviation(year, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.05"), response[teams[0].id])
        self.assertEqual(Deci("0.25"), response[teams[1].id])

    def test_getScoringStandardDeviation_onlyRegularSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=5, teamBScore=3)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.3, teamBScore=2.6,
                           matchupType=MatchupType.PLAYOFF)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = ScoringStandardDeviationCalculator.getScoringStandardDeviation(year, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("1.95"), response[teams[0].id])
        self.assertEqual(Deci("0.3"), response[teams[1].id])

    def test_getScoringStandardDeviation_weekNumberStartGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=2.5)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=5.5, teamBScore=2.6,
                           matchupType=MatchupType.PLAYOFF)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = ScoringStandardDeviationCalculator.getScoringStandardDeviation(year, weekNumberStart=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("2.15"), response[teams[0].id])
        self.assertEqual(Deci("0.05"), response[teams[1].id])

    def test_getScoringStandardDeviation_weekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.9, teamBScore=5)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.3, teamBScore=2.6,
                           matchupType=MatchupType.PLAYOFF)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = ScoringStandardDeviationCalculator.getScoringStandardDeviation(year, weekNumberEnd=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.4"), response[teams[0].id])
        self.assertEqual(Deci("1.3"), response[teams[1].id])

    def test_getScoringStandardDeviation_weekNumberStartGivenAndWeekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=2.5)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.3, teamBScore=12.6,
                           matchupType=MatchupType.PLAYOFF)
        matchup4 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.4, teamBScore=2.7,
                           matchupType=MatchupType.PLAYOFF)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])
        week4 = Week(weekNumber=4, matchups=[matchup4])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3, week4])

        response = ScoringStandardDeviationCalculator.getScoringStandardDeviation(year, weekNumberStart=2,
                                                                                  weekNumberEnd=3)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.05"), response[teams[0].id])
        self.assertEqual(Deci("5.05"), response[teams[1].id])
