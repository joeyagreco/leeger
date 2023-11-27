import unittest
from test.helper.prototypes import getNDefaultOwnersAndTeams

from leeger.calculator.year_calculator import ScoringStandardDeviationYearCalculator
from leeger.enum.MatchupType import MatchupType
from leeger.model.league.Matchup import Matchup
from leeger.model.league.Week import Week
from leeger.model.league.Year import Year
from leeger.util.Deci import Deci


class TestScoringStandardDeviationYearCalculator(unittest.TestCase):
    def test_getScoringStandardDeviation_happyPath(self):
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
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = ScoringStandardDeviationYearCalculator.getScoringStandardDeviation(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.08164965809277260327324280249"), response[teams[0].id])
        self.assertEqual(Deci("1.202774570177914372863325978"), response[teams[1].id])

    def test_getScoringStandardDeviation_multiWeekMatchups(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1.1,
            teamBScore=2.4,
            multiWeekMatchupId="1",
        )
        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1.2,
            teamBScore=2.5,
            multiWeekMatchupId="1",
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1.3,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = ScoringStandardDeviationYearCalculator.getScoringStandardDeviation(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.5"), response[teams[0].id])
        self.assertEqual(Deci("0.05"), response[teams[1].id])

    def test_getScoringStandardDeviation_noneIfNoGamesPlayed(self):
        owners, teams = getNDefaultOwnersAndTeams(3)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4)
        matchup2 = Matchup(teamAId=teams[1].id, teamBId=teams[2].id, teamAScore=1.2, teamBScore=2.5)
        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2])

        response = ScoringStandardDeviationYearCalculator.getScoringStandardDeviation(
            year, weekNumberEnd=1
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(3, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0"), response[teams[1].id])
        self.assertIsNone(response[teams[2].id])

    def test_getScoringStandardDeviation_onlyPostSeasonIsTrue(self):
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
            teamBScore=3,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = ScoringStandardDeviationYearCalculator.getScoringStandardDeviation(
            year, onlyPostSeason=True
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.05"), response[teams[0].id])
        self.assertEqual(Deci("0.25"), response[teams[1].id])

    def test_getScoringStandardDeviation_onlyRegularSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=5, teamBScore=3)
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

        response = ScoringStandardDeviationYearCalculator.getScoringStandardDeviation(
            year, onlyRegularSeason=True
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("1.95"), response[teams[0].id])
        self.assertEqual(Deci("0.3"), response[teams[1].id])

    def test_getScoringStandardDeviation_onlyChampionshipIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.3, teamBScore=2.3)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3.3, teamBScore=4.3)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4.3, teamBScore=5.3)
        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup4 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1.3,
            teamBScore=2.3,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup5 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3.3,
            teamBScore=4.3,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup6 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4.3,
            teamBScore=5.3,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        week2 = Week(weekNumber=2, matchups=[matchup4, matchup5, matchup6])

        year = Year(yearNumber=2002, teams=teams, weeks=[week1, week2])

        response = ScoringStandardDeviationYearCalculator.getScoringStandardDeviation(
            year, onlyChampionship=True
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertIsNone(response[teams[0].id])
        self.assertIsNone(response[teams[1].id])
        self.assertIsNone(response[teams[2].id])
        self.assertIsNone(response[teams[3].id])
        self.assertEqual(Deci("0"), response[teams[4].id])
        self.assertEqual(Deci("0"), response[teams[5].id])

    def test_getScoringStandardDeviation_weekNumberStartGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=2.5)
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=5.5,
            teamBScore=2.6,
            matchupType=MatchupType.PLAYOFF,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3])

        response = ScoringStandardDeviationYearCalculator.getScoringStandardDeviation(
            year, weekNumberStart=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("2.15"), response[teams[0].id])
        self.assertEqual(Deci("0.05"), response[teams[1].id])

    def test_getScoringStandardDeviation_weekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.9, teamBScore=5)
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

        response = ScoringStandardDeviationYearCalculator.getScoringStandardDeviation(
            year, weekNumberEnd=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.4"), response[teams[0].id])
        self.assertEqual(Deci("1.3"), response[teams[1].id])

    def test_getScoringStandardDeviation_weekNumberStartGivenAndWeekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.4)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.2, teamBScore=2.5)
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1.3,
            teamBScore=12.6,
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

        response = ScoringStandardDeviationYearCalculator.getScoringStandardDeviation(
            year, weekNumberStart=2, weekNumberEnd=3
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.05"), response[teams[0].id])
        self.assertEqual(Deci("5.05"), response[teams[1].id])
