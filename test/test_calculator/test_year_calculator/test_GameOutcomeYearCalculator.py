import unittest

from leeger.calculator.year_calculator.GameOutcomeYearCalculator import (
    GameOutcomeYearCalculator,
)
from leeger.enum.MatchupType import MatchupType
from leeger.model.league import YearSettings
from leeger.model.league.Matchup import Matchup
from leeger.model.league.Week import Week
from leeger.model.league.Year import Year
from leeger.util.Deci import Deci
from test.helper.prototypes import getNDefaultOwnersAndTeams


class TestGameOutcomeYearCalculator(unittest.TestCase):
    def test_getWins_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1])

        response = GameOutcomeYearCalculator.getWins(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(0, response[teams[0].id])
        self.assertEqual(1, response[teams[1].id])

    def test_getWins_multiWeekMatchups(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            multiWeekMatchupId="1",
        )
        week1 = Week(weekNumber=1, matchups=[matchup1])

        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            multiWeekMatchupId="1",
        )
        week2 = Week(weekNumber=2, matchups=[matchup2])

        matchup3 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = GameOutcomeYearCalculator.getWins(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(0, response[teams[0].id])
        self.assertEqual(2, response[teams[1].id])

    def test_getWins_noneIfNoGamesPlayed(self):
        owners, teams = getNDefaultOwnersAndTeams(3)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[1].id, teamBId=teams[2].id, teamAScore=1, teamBScore=2
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2])

        response = GameOutcomeYearCalculator.getWins(year, weekNumberEnd=1)

        self.assertIsInstance(response, dict)
        self.assertEqual(3, len(response.keys()))
        self.assertEqual(0, response[teams[0].id])
        self.assertEqual(1, response[teams[1].id])
        self.assertIsNone(response[teams[2].id])

    def test_getWins_onlyPostSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(
            yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3]
        )

        response = GameOutcomeYearCalculator.getWins(year, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(0, response[teams[0].id])
        self.assertEqual(2, response[teams[1].id])

    def test_getWins_onlyRegularSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(
            yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3]
        )

        response = GameOutcomeYearCalculator.getWins(year, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(0, response[teams[0].id])
        self.assertEqual(2, response[teams[1].id])

    def test_getWins_onlyChampionshipIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(
            yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3]
        )

        response = GameOutcomeYearCalculator.getWins(year, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(0, response[teams[0].id])
        self.assertEqual(1, response[teams[1].id])

    def test_getWins_weekNumberStartGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(
            yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3]
        )

        response = GameOutcomeYearCalculator.getWins(year, weekNumberStart=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(1, response[teams[0].id])
        self.assertEqual(1, response[teams[1].id])

    def test_getWins_weekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(
            yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3]
        )

        response = GameOutcomeYearCalculator.getWins(year, weekNumberEnd=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(0, response[teams[0].id])
        self.assertEqual(2, response[teams[1].id])

    def test_getWins_weekNumberStartGivenAndWeekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup4 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])
        week4 = Week(weekNumber=4, matchups=[matchup4])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1]],
            weeks=[week1, week2, week3, week4],
        )

        response = GameOutcomeYearCalculator.getWins(
            year, weekNumberStart=2, weekNumberEnd=3
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(1, response[teams[0].id])
        self.assertEqual(1, response[teams[1].id])

    def test_getLosses_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1])

        response = GameOutcomeYearCalculator.getLosses(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(1, response[teams[0].id])
        self.assertEqual(0, response[teams[1].id])

    def test_getLosses_multiWeekMatchups(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            multiWeekMatchupId="1",
        )
        week1 = Week(weekNumber=1, matchups=[matchup1])

        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            multiWeekMatchupId="1",
        )
        week2 = Week(weekNumber=2, matchups=[matchup2])

        matchup3 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = GameOutcomeYearCalculator.getLosses(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(2, response[teams[0].id])
        self.assertEqual(0, response[teams[1].id])

    def test_getLosses_noneIfNoGamesPlayed(self):
        owners, teams = getNDefaultOwnersAndTeams(3)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[1].id, teamBId=teams[2].id, teamAScore=1, teamBScore=2
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2])

        response = GameOutcomeYearCalculator.getLosses(year, weekNumberEnd=1)

        self.assertIsInstance(response, dict)
        self.assertEqual(3, len(response.keys()))
        self.assertEqual(1, response[teams[0].id])
        self.assertEqual(0, response[teams[1].id])
        self.assertIsNone(response[teams[2].id])

    def test_getLosses_onlyPostSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(
            yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3]
        )

        response = GameOutcomeYearCalculator.getLosses(year, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(2, response[teams[0].id])
        self.assertEqual(0, response[teams[1].id])

    def test_getLosses_onlyRegularSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(
            yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3]
        )

        response = GameOutcomeYearCalculator.getLosses(year, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(2, response[teams[0].id])
        self.assertEqual(0, response[teams[1].id])

    def test_getLosses_onlyChampionshipIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(
            yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3]
        )

        response = GameOutcomeYearCalculator.getLosses(year, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(1, response[teams[0].id])
        self.assertEqual(0, response[teams[1].id])

    def test_getLosses_weekNumberStartGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(
            yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3]
        )

        response = GameOutcomeYearCalculator.getLosses(year, weekNumberStart=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(1, response[teams[0].id])
        self.assertEqual(1, response[teams[1].id])

    def test_getLosses_weekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(
            yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3]
        )

        response = GameOutcomeYearCalculator.getLosses(year, weekNumberEnd=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(2, response[teams[0].id])
        self.assertEqual(0, response[teams[1].id])

    def test_getLosses_weekNumberStartGivenAndWeekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup4 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])
        week4 = Week(weekNumber=4, matchups=[matchup4])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1]],
            weeks=[week1, week2, week3, week4],
        )

        response = GameOutcomeYearCalculator.getLosses(
            year, weekNumberStart=2, weekNumberEnd=3
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(1, response[teams[0].id])
        self.assertEqual(1, response[teams[1].id])

    def test_getTies_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])

        year = Year(yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1])

        response = GameOutcomeYearCalculator.getTies(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(1, response[teams[0].id])
        self.assertEqual(1, response[teams[1].id])

    def test_getTies_multiWeekMatchups(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=1,
            multiWeekMatchupId="1",
        )
        week1 = Week(weekNumber=1, matchups=[matchup1])

        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=1,
            multiWeekMatchupId="1",
        )
        week2 = Week(weekNumber=2, matchups=[matchup2])

        matchup3 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1
        )
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = GameOutcomeYearCalculator.getTies(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(2, response[teams[0].id])
        self.assertEqual(2, response[teams[1].id])

    def test_getTies_noneIfNoGamesPlayed(self):
        owners, teams = getNDefaultOwnersAndTeams(3)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1
        )
        matchup2 = Matchup(
            teamAId=teams[1].id, teamBId=teams[2].id, teamAScore=1, teamBScore=1
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2])

        response = GameOutcomeYearCalculator.getTies(year, weekNumberEnd=1)

        self.assertIsInstance(response, dict)
        self.assertEqual(3, len(response.keys()))
        self.assertEqual(1, response[teams[0].id])
        self.assertEqual(1, response[teams[1].id])
        self.assertIsNone(response[teams[2].id])

    def test_getTies_onlyPostSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1
        )
        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(
            yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3]
        )

        response = GameOutcomeYearCalculator.getTies(year, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(0, response[teams[0].id])
        self.assertEqual(0, response[teams[1].id])

    def test_getTies_onlyRegularSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1
        )
        matchup2 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(
            yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3]
        )

        response = GameOutcomeYearCalculator.getTies(year, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(2, response[teams[0].id])
        self.assertEqual(2, response[teams[1].id])

    def test_getTies_onlyChampionshipIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1
        )
        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=0,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=0,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(
            yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3]
        )

        response = GameOutcomeYearCalculator.getTies(year, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(0, response[teams[0].id])
        self.assertEqual(0, response[teams[1].id])

    def test_getTies_weekNumberStartGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1
        )
        matchup2 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1
        )
        matchup3 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(
            yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3]
        )

        response = GameOutcomeYearCalculator.getTies(year, weekNumberStart=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(2, response[teams[0].id])
        self.assertEqual(2, response[teams[1].id])

    def test_getTies_weekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1
        )
        matchup2 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1
        )
        matchup3 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(
            yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3]
        )

        response = GameOutcomeYearCalculator.getTies(year, weekNumberEnd=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(2, response[teams[0].id])
        self.assertEqual(2, response[teams[1].id])

    def test_getTies_weekNumberStartGivenAndWeekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1
        )
        matchup2 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=2, teamBScore=1
        )
        matchup3 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1
        )
        matchup4 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])
        week4 = Week(weekNumber=4, matchups=[matchup4])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1]],
            weeks=[week1, week2, week3, week4],
        )

        response = GameOutcomeYearCalculator.getTies(
            year, weekNumberStart=2, weekNumberEnd=3
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(1, response[teams[0].id])
        self.assertEqual(1, response[teams[1].id])

    def test_getWinPercentage_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=2, teamBScore=1
        )
        matchup2 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup3 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup4 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])
        week4 = Week(weekNumber=4, matchups=[matchup4])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1]],
            weeks=[week1, week2, week3, week4],
        )

        response = GameOutcomeYearCalculator.getWinPercentage(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.375"), response[teams[0].id])
        self.assertEqual(Deci("0.625"), response[teams[1].id])

    def test_getWinPercentage_leagueMedianGamesIsOn_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=2, teamBScore=1
        )
        matchup2 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup3 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup4 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])
        week4 = Week(weekNumber=4, matchups=[matchup4])

        yearSettings = YearSettings(leagueMedianGames=True)
        year = Year(
            yearNumber=2000,
            teams=teams,
            weeks=[week1, week2, week3, week4],
            yearSettings=yearSettings,
        )

        response = GameOutcomeYearCalculator.getWinPercentage(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.375"), response[teams[0].id])
        self.assertEqual(Deci("0.625"), response[teams[1].id])

    def test_getWinPercentage_multiWeekMatchups(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            multiWeekMatchupId="1",
        )
        week1 = Week(weekNumber=1, matchups=[matchup1])

        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=3,
            teamBScore=4,
            multiWeekMatchupId="1",
        )
        week2 = Week(weekNumber=2, matchups=[matchup2])

        matchup3 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=2, teamBScore=1
        )
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = GameOutcomeYearCalculator.getWinPercentage(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.5"), response[teams[0].id])
        self.assertEqual(Deci("0.5"), response[teams[1].id])

    def test_getWinPercentage_noneIfNoGamesPlayed(self):
        owners, teams = getNDefaultOwnersAndTeams(3)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[1].id, teamBId=teams[2].id, teamAScore=1, teamBScore=2
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2])

        response = GameOutcomeYearCalculator.getWinPercentage(year, weekNumberEnd=1)

        self.assertIsInstance(response, dict)
        self.assertEqual(3, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("1"), response[teams[1].id])
        self.assertIsNone(response[teams[2].id])

    def test_getWinPercentage_onlyPostSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(
            yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3]
        )

        response = GameOutcomeYearCalculator.getWinPercentage(year, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.5"), response[teams[0].id])
        self.assertEqual(Deci("0.5"), response[teams[1].id])

    def test_getWinPercentage_onlyRegularSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(
            yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3]
        )

        response = GameOutcomeYearCalculator.getWinPercentage(
            year, onlyRegularSeason=True
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.0"), response[teams[0].id])
        self.assertEqual(Deci("1.0"), response[teams[1].id])

    def test_getWinPercentage_onlyChampionshipIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(
            yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3]
        )

        response = GameOutcomeYearCalculator.getWinPercentage(
            year, onlyChampionship=True
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.0"), response[teams[0].id])
        self.assertEqual(Deci("1.0"), response[teams[1].id])

    def test_getWinPercentage_weekNumberStartGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(
            yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3]
        )

        response = GameOutcomeYearCalculator.getWinPercentage(year, weekNumberStart=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.5"), response[teams[0].id])
        self.assertEqual(Deci("0.5"), response[teams[1].id])

    def test_getWinPercentage_weekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(
            yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3]
        )

        response = GameOutcomeYearCalculator.getWinPercentage(year, weekNumberEnd=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.0"), response[teams[0].id])
        self.assertEqual(Deci("1.0"), response[teams[1].id])

    def test_getWinPercentage_weekNumberStartGivenAndWeekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup4 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])
        week4 = Week(weekNumber=4, matchups=[matchup4])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1]],
            weeks=[week1, week2, week3, week4],
        )

        response = GameOutcomeYearCalculator.getWinPercentage(
            year, weekNumberStart=2, weekNumberEnd=3
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.5"), response[teams[0].id])
        self.assertEqual(Deci("0.5"), response[teams[1].id])

    def test_getWAL_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1
        )
        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(
            yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3]
        )

        response = GameOutcomeYearCalculator.getWAL(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.5"), response[teams[0].id])
        self.assertEqual(Deci("2.5"), response[teams[1].id])

    def test_getWAL_leagueMedianGamesIsTrue_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1
        )
        matchup2 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup3 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        yearSettings = YearSettings(leagueMedianGames=True)
        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1]],
            weeks=[week1, week2, week3],
            yearSettings=yearSettings,
        )

        response = GameOutcomeYearCalculator.getWAL(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("1"), response[teams[0].id])
        self.assertEqual(Deci("5"), response[teams[1].id])

    def test_getWAL_multiWeekMatchups(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            multiWeekMatchupId="1",
        )
        week1 = Week(weekNumber=1, matchups=[matchup1])

        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=3,
            teamBScore=4,
            multiWeekMatchupId="1",
        )
        week2 = Week(weekNumber=2, matchups=[matchup2])

        matchup3 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = GameOutcomeYearCalculator.getWAL(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("2"), response[teams[1].id])

    def test_getWAL_noneIfNoGamesPlayed(self):
        owners, teams = getNDefaultOwnersAndTeams(3)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[1].id, teamBId=teams[2].id, teamAScore=1, teamBScore=2
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2])

        response = GameOutcomeYearCalculator.getWAL(year, weekNumberEnd=1)

        self.assertIsInstance(response, dict)
        self.assertEqual(3, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("1"), response[teams[1].id])
        self.assertIsNone(response[teams[2].id])

    def test_getWAL_onlyPostSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(
            yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3]
        )

        response = GameOutcomeYearCalculator.getWAL(year, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("2"), response[teams[1].id])

    def test_getWAL_onlyRegularSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(
            yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3]
        )

        response = GameOutcomeYearCalculator.getWAL(year, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("2"), response[teams[1].id])

    def test_getWAL_onlyChampionshipIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(
            yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3]
        )

        response = GameOutcomeYearCalculator.getWAL(year, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("1"), response[teams[1].id])

    def test_getWAL_weekNumberStartGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(
            yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3]
        )

        response = GameOutcomeYearCalculator.getWAL(year, weekNumberStart=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("1"), response[teams[0].id])
        self.assertEqual(Deci("1"), response[teams[1].id])

    def test_getWAL_weekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(
            yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3]
        )

        response = GameOutcomeYearCalculator.getWAL(year, weekNumberEnd=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("2"), response[teams[1].id])

    def test_getWAL_weekNumberStartGivenAndWeekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup4 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])
        week4 = Week(weekNumber=4, matchups=[matchup4])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1]],
            weeks=[week1, week2, week3, week4],
        )

        response = GameOutcomeYearCalculator.getWAL(
            year, weekNumberStart=2, weekNumberEnd=3
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("1"), response[teams[0].id])
        self.assertEqual(Deci("1"), response[teams[1].id])

    def test_getWALPerGame_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1
        )
        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(
            yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3]
        )

        response = GameOutcomeYearCalculator.getWALPerGame(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.1666666666666666666666666667"), response[teams[0].id])
        self.assertEqual(Deci("0.8333333333333333333333333333"), response[teams[1].id])

    def test_getWALPerGame_leagueMedianGamesIsOn_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1
        )
        matchup2 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup3 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        yearSettings = YearSettings(leagueMedianGames=True)
        year = Year(
            yearNumber=2000,
            teams=teams,
            weeks=[week1, week2, week3],
            yearSettings=yearSettings,
        )

        response = GameOutcomeYearCalculator.getWALPerGame(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.1666666666666666666666666667"), response[teams[0].id])
        self.assertEqual(Deci("0.8333333333333333333333333333"), response[teams[1].id])

    def test_getWALPerGame_multiWeekMatchups(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            multiWeekMatchupId="1",
        )
        week1 = Week(weekNumber=1, matchups=[matchup1])

        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=3,
            teamBScore=4,
            multiWeekMatchupId="1",
        )
        week2 = Week(weekNumber=2, matchups=[matchup2])

        matchup3 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = GameOutcomeYearCalculator.getWALPerGame(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("1"), response[teams[1].id])

    def test_getWALPerGame_noneIfNoGamesPlayed(self):
        owners, teams = getNDefaultOwnersAndTeams(3)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[1].id, teamBId=teams[2].id, teamAScore=1, teamBScore=2
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2])

        response = GameOutcomeYearCalculator.getWALPerGame(year, weekNumberEnd=1)

        self.assertIsInstance(response, dict)
        self.assertEqual(3, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("1"), response[teams[1].id])
        self.assertIsNone(response[teams[2].id])

    def test_getWALPerGame_onlyPostSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(
            yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3]
        )

        response = GameOutcomeYearCalculator.getWALPerGame(year, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("1"), response[teams[1].id])

    def test_getWALPerGame_onlyRegularSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(
            yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3]
        )

        response = GameOutcomeYearCalculator.getWALPerGame(year, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("1"), response[teams[1].id])

    def test_getWALPerGame_onlyChampionshipIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(
            yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3]
        )

        response = GameOutcomeYearCalculator.getWALPerGame(year, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("1"), response[teams[1].id])

    def test_getWALPerGame_weekNumberStartGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(
            yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3]
        )

        response = GameOutcomeYearCalculator.getWALPerGame(year, weekNumberStart=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.5"), response[teams[0].id])
        self.assertEqual(Deci("0.5"), response[teams[1].id])

    def test_getWALPerGame_weekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(
            yearNumber=2000, teams=[teams[0], teams[1]], weeks=[week1, week2, week3]
        )

        response = GameOutcomeYearCalculator.getWALPerGame(year, weekNumberEnd=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("1"), response[teams[1].id])

    def test_getWALPerGame_weekNumberStartGivenAndWeekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup4 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.PLAYOFF,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])
        week4 = Week(weekNumber=4, matchups=[matchup4])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1]],
            weeks=[week1, week2, week3, week4],
        )

        response = GameOutcomeYearCalculator.getWALPerGame(
            year, weekNumberStart=2, weekNumberEnd=3
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("0.5"), response[teams[0].id])
        self.assertEqual(Deci("0.5"), response[teams[1].id])

    def test_getLeagueMedianWins_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(4)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4
        )

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2])

        yearSettings = YearSettings(leagueMedianGames=True)
        year = Year(
            yearNumber=2000, teams=teams, weeks=[week1], yearSettings=yearSettings
        )

        response = GameOutcomeYearCalculator.getLeagueMedianWins(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(4, len(response.keys()))
        self.assertEqual(0, response[teams[0].id])
        self.assertEqual(0, response[teams[1].id])
        self.assertEqual(1, response[teams[2].id])
        self.assertEqual(1, response[teams[3].id])

    def test_getLeagueMedianWins_yearHasLeagueMedianGamesOff_returnsZeroForEachTeam(
        self,
    ):
        owners, teams = getNDefaultOwnersAndTeams(4)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4
        )

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2])

        yearSettings = YearSettings(leagueMedianGames=False)
        year = Year(
            yearNumber=2000, teams=teams, weeks=[week1], yearSettings=yearSettings
        )

        response = GameOutcomeYearCalculator.getLeagueMedianWins(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(4, len(response.keys()))
        self.assertEqual(0, response[teams[0].id])
        self.assertEqual(0, response[teams[1].id])
        self.assertEqual(0, response[teams[2].id])
        self.assertEqual(0, response[teams[3].id])

    def test_getLeagueMedianWinsTieForLeagueMedian_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(4)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=2, teamBScore=4
        )

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2])

        yearSettings = YearSettings(leagueMedianGames=True)
        year = Year(
            yearNumber=2000, teams=teams, weeks=[week1], yearSettings=yearSettings
        )

        response = GameOutcomeYearCalculator.getLeagueMedianWins(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(4, len(response.keys()))
        self.assertEqual(0, response[teams[0].id])
        self.assertEqual(Deci("0.5"), response[teams[1].id])
        self.assertEqual(Deci("0.5"), response[teams[2].id])
        self.assertEqual(1, response[teams[3].id])

    def test_getLeagueMedianWins_noneIfNoGamesPlayed(self):
        owners, teams = getNDefaultOwnersAndTeams(3)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[1].id, teamBId=teams[2].id, teamAScore=1, teamBScore=2
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])

        yearSettings = YearSettings(leagueMedianGames=True)
        year = Year(
            yearNumber=2000,
            teams=teams,
            weeks=[week1, week2],
            yearSettings=yearSettings,
        )

        response = GameOutcomeYearCalculator.getLeagueMedianWins(year, weekNumberEnd=1)

        self.assertIsInstance(response, dict)
        self.assertEqual(3, len(response.keys()))
        self.assertEqual(0, response[teams[0].id])
        self.assertEqual(1, response[teams[1].id])
        self.assertIsNone(response[teams[2].id])

    def test_getLeagueMedianWins_onlyPostSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = GameOutcomeYearCalculator.getLeagueMedianWins(
            year, onlyPostSeason=True
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(0, response[teams[0].id])
        self.assertEqual(0, response[teams[1].id])

    def test_getLeagueMedianWins_onlyRegularSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        yearSettings = YearSettings(leagueMedianGames=True)
        year = Year(
            yearNumber=2000,
            teams=teams,
            weeks=[week1, week2, week3],
            yearSettings=yearSettings,
        )

        response = GameOutcomeYearCalculator.getLeagueMedianWins(
            year, onlyRegularSeason=True
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(0, response[teams[0].id])
        self.assertEqual(2, response[teams[1].id])

    def test_getLeagueMedianWins_onlyChampionshipIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = GameOutcomeYearCalculator.getLeagueMedianWins(
            year, onlyChampionship=True
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(0, response[teams[0].id])
        self.assertEqual(0, response[teams[1].id])

    def test_getLeagueMedianWins_weekNumberStartGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup3 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=2, teamBScore=1
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        yearSettings = YearSettings(leagueMedianGames=True)
        year = Year(
            yearNumber=2000,
            teams=teams,
            weeks=[week1, week2, week3],
            yearSettings=yearSettings,
        )

        response = GameOutcomeYearCalculator.getLeagueMedianWins(
            year, weekNumberStart=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(1, response[teams[0].id])
        self.assertEqual(1, response[teams[1].id])

    def test_getLeagueMedianWins_weekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup3 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=2, teamBScore=1
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        yearSettings = YearSettings(leagueMedianGames=True)
        year = Year(
            yearNumber=2000,
            teams=teams,
            weeks=[week1, week2, week3],
            yearSettings=yearSettings,
        )

        response = GameOutcomeYearCalculator.getLeagueMedianWins(year, weekNumberEnd=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(0, response[teams[0].id])
        self.assertEqual(2, response[teams[1].id])

    def test_getLeagueMedianWins_weekNumberStartGivenAndWeekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup3 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=2, teamBScore=1
        )
        matchup4 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=2, teamBScore=1
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])
        week4 = Week(weekNumber=4, matchups=[matchup4])

        yearSettings = YearSettings(leagueMedianGames=True)
        year = Year(
            yearNumber=2000,
            teams=teams,
            weeks=[week1, week2, week3, week4],
            yearSettings=yearSettings,
        )

        response = GameOutcomeYearCalculator.getLeagueMedianWins(
            year, weekNumberStart=2, weekNumberEnd=3
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(1, response[teams[0].id])
        self.assertEqual(1, response[teams[1].id])

    def test_getOpponentLeagueMedianWins_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(4)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4
        )

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2])

        yearSettings = YearSettings(leagueMedianGames=True)
        year = Year(
            yearNumber=2000, teams=teams, weeks=[week1], yearSettings=yearSettings
        )

        response = GameOutcomeYearCalculator.getOpponentLeagueMedianWins(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(4, len(response.keys()))
        self.assertEqual(0, response[teams[0].id])
        self.assertEqual(0, response[teams[1].id])
        self.assertEqual(1, response[teams[2].id])
        self.assertEqual(1, response[teams[3].id])

    def test_getOpponentLeagueMedianWins_yearHasLeagueMedianGamesOff_returnsZeroForEachTeam(
        self,
    ):
        owners, teams = getNDefaultOwnersAndTeams(4)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4
        )

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2])

        yearSettings = YearSettings(leagueMedianGames=False)
        year = Year(
            yearNumber=2000, teams=teams, weeks=[week1], yearSettings=yearSettings
        )

        response = GameOutcomeYearCalculator.getOpponentLeagueMedianWins(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(4, len(response.keys()))
        self.assertEqual(0, response[teams[0].id])
        self.assertEqual(0, response[teams[1].id])
        self.assertEqual(0, response[teams[2].id])
        self.assertEqual(0, response[teams[3].id])

    def test_getOpponentLeagueMedianWinsTieForLeagueMedian_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(4)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=2, teamBScore=4
        )

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2])

        yearSettings = YearSettings(leagueMedianGames=True)
        year = Year(
            yearNumber=2000, teams=teams, weeks=[week1], yearSettings=yearSettings
        )

        response = GameOutcomeYearCalculator.getOpponentLeagueMedianWins(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(4, len(response.keys()))
        self.assertEqual(Deci("0.5"), response[teams[0].id])
        self.assertEqual(0, response[teams[1].id])
        self.assertEqual(1, response[teams[2].id])
        self.assertEqual(Deci("0.5"), response[teams[3].id])

    def test_getOpponentLeagueMedianWins_noneIfNoGamesPlayed(self):
        owners, teams = getNDefaultOwnersAndTeams(3)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[1].id, teamBId=teams[2].id, teamAScore=1, teamBScore=2
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])

        yearSettings = YearSettings(leagueMedianGames=True)
        year = Year(
            yearNumber=2000,
            teams=teams,
            weeks=[week1, week2],
            yearSettings=yearSettings,
        )

        response = GameOutcomeYearCalculator.getOpponentLeagueMedianWins(
            year, weekNumberEnd=1
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(3, len(response.keys()))
        self.assertEqual(1, response[teams[0].id])
        self.assertEqual(0, response[teams[1].id])
        self.assertIsNone(response[teams[2].id])

    def test_getOpponentLeagueMedianWins_onlyPostSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = GameOutcomeYearCalculator.getOpponentLeagueMedianWins(
            year, onlyPostSeason=True
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(0, response[teams[0].id])
        self.assertEqual(0, response[teams[1].id])

    def test_getOpponentLeagueMedianWins_onlyRegularSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        yearSettings = YearSettings(leagueMedianGames=True)
        year = Year(
            yearNumber=2000,
            teams=teams,
            weeks=[week1, week2, week3],
            yearSettings=yearSettings,
        )

        response = GameOutcomeYearCalculator.getOpponentLeagueMedianWins(
            year, onlyRegularSeason=True
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(2, response[teams[0].id])
        self.assertEqual(0, response[teams[1].id])

    def test_getOpponentLeagueMedianWins_onlyChampionshipIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = GameOutcomeYearCalculator.getOpponentLeagueMedianWins(
            year, onlyChampionship=True
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(0, response[teams[0].id])
        self.assertEqual(0, response[teams[1].id])

    def test_getOpponentLeagueMedianWins_weekNumberStartGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup3 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=2, teamBScore=1
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        yearSettings = YearSettings(leagueMedianGames=True)
        year = Year(
            yearNumber=2000,
            teams=teams,
            weeks=[week1, week2, week3],
            yearSettings=yearSettings,
        )

        response = GameOutcomeYearCalculator.getOpponentLeagueMedianWins(
            year, weekNumberStart=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(1, response[teams[0].id])
        self.assertEqual(1, response[teams[1].id])

    def test_getOpponentLeagueMedianWins_weekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup3 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=2, teamBScore=1
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        yearSettings = YearSettings(leagueMedianGames=True)
        year = Year(
            yearNumber=2000,
            teams=teams,
            weeks=[week1, week2, week3],
            yearSettings=yearSettings,
        )

        response = GameOutcomeYearCalculator.getOpponentLeagueMedianWins(
            year, weekNumberEnd=2
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(2, response[teams[0].id])
        self.assertEqual(0, response[teams[1].id])

    def test_getOpponentLeagueMedianWins_weekNumberStartGivenAndWeekNumberEndGiven(
        self,
    ):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup2 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2
        )
        matchup3 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=2, teamBScore=1
        )
        matchup4 = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=2, teamBScore=1
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])
        week4 = Week(weekNumber=4, matchups=[matchup4])

        yearSettings = YearSettings(leagueMedianGames=True)
        year = Year(
            yearNumber=2000,
            teams=teams,
            weeks=[week1, week2, week3, week4],
            yearSettings=yearSettings,
        )

        response = GameOutcomeYearCalculator.getOpponentLeagueMedianWins(
            year, weekNumberStart=2, weekNumberEnd=3
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(1, response[teams[0].id])
        self.assertEqual(1, response[teams[1].id])
