import unittest
from test.helper.prototypes import getNDefaultOwnersAndTeams

from leeger.calculator.year_calculator.PlusMinusYearCalculator import \
    PlusMinusYearCalculator
from leeger.enum.MatchupType import MatchupType
from leeger.model.league.Matchup import Matchup
from leeger.model.league.Week import Week
from leeger.model.league.Year import Year
from leeger.util.Deci import Deci


class TestPlusMinusYearCalculator(unittest.TestCase):
    def test_getPlusMinus_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4)
        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1.2,
            teamBScore=2.5,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1.3,
            teamBScore=2.6,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = PlusMinusYearCalculator.getPlusMinus(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("-3.9"), response[teams[0].id])
        self.assertEqual(Deci("3.9"), response[teams[1].id])

    def test_getPlusMinus_noneIfNoGamesPlayed(self):
        owners, teams = getNDefaultOwnersAndTeams(3)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4)
        matchup2 = Matchup(teamAId=teams[1].id, teamBId=teams[2].id, teamAScore=1.2, teamBScore=2.5)
        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2])

        response = PlusMinusYearCalculator.getPlusMinus(year, weekNumberEnd=1)

        self.assertIsInstance(response, dict)
        self.assertEqual(3, len(response.keys()))
        self.assertEqual(Deci("-1.3"), response[teams[0].id])
        self.assertEqual(Deci("1.3"), response[teams[1].id])
        self.assertIsNone(response[teams[2].id])

    def test_getPlusMinus_onlyPostSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4)
        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1.2,
            teamBScore=2.5,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1.3,
            teamBScore=2.6,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = PlusMinusYearCalculator.getPlusMinus(year, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("-2.6"), response[teams[0].id])
        self.assertEqual(Deci("2.6"), response[teams[1].id])

    def test_getPlusMinus_onlyRegularSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=2.5)
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1.3,
            teamBScore=2.6,
            matchupType=MatchupType.PLAYOFF,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = PlusMinusYearCalculator.getPlusMinus(year, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("-2.6"), response[teams[0].id])
        self.assertEqual(Deci("2.6"), response[teams[1].id])

    def test_getPlusMinus_onlyChampionshipIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4)
        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1.2,
            teamBScore=2.5,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1.3,
            teamBScore=2.6,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = PlusMinusYearCalculator.getPlusMinus(year, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("-1.3"), response[teams[0].id])
        self.assertEqual(Deci("1.3"), response[teams[1].id])

    def test_getPlusMinus_weekNumberStartGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=2.5)
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1.3,
            teamBScore=2.6,
            matchupType=MatchupType.PLAYOFF,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = PlusMinusYearCalculator.getPlusMinus(year, weekNumberStart=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("-2.6"), response[teams[0].id])
        self.assertEqual(Deci("2.6"), response[teams[1].id])

    def test_getPlusMinus_weekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=2.5)
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1.3,
            teamBScore=2.6,
            matchupType=MatchupType.PLAYOFF,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = PlusMinusYearCalculator.getPlusMinus(year, weekNumberEnd=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("-2.6"), response[teams[0].id])
        self.assertEqual(Deci("2.6"), response[teams[1].id])

    def test_getPlusMinus_weekNumberStartGivenAndWeekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=2.5)
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1.3,
            teamBScore=2.6,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup4 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1.4,
            teamBScore=2.7,
            matchupType=MatchupType.PLAYOFF,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])
        week4 = Week(weekNumber=4, matchups=[matchup4])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3, week4])

        response = PlusMinusYearCalculator.getPlusMinus(year, weekNumberStart=2, weekNumberEnd=3)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("-2.6"), response[teams[0].id])
        self.assertEqual(Deci("2.6"), response[teams[1].id])
