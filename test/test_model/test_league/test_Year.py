import unittest

from src.leeger.model.league.Matchup import Matchup
from src.leeger.model.league.Team import Team
from src.leeger.model.league.Week import Week
from src.leeger.model.league.Year import Year
from src.leeger.model.stat.YearStatSheet import YearStatSheet
from test.helper.prototypes import getNDefaultOwnersAndTeams


class TestYear(unittest.TestCase):
    def test_year_init(self):
        week = Week(weekNumber=1, matchups=[])
        team = Team(ownerId="", name="")
        year = Year(yearNumber=2000, teams=[team], weeks=[week])

        self.assertEqual(2000, year.yearNumber)
        self.assertEqual(1, len(year.teams))
        self.assertEqual(1, len(year.weeks))
        self.assertEqual(week.id, year.weeks[0].id)
        self.assertEqual(team.id, year.teams[0].id)

    def test_year_statSheet(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        week = Week(weekNumber=1, matchups=[matchup])
        year = Year(yearNumber=2000, teams=teams, weeks=[week])

        yearStatSheet = year.statSheet()

        self.assertIsInstance(yearStatSheet, YearStatSheet)
        self.assertIsInstance(yearStatSheet.wins, dict)
        self.assertIsInstance(yearStatSheet.losses, dict)
        self.assertIsInstance(yearStatSheet.ties, dict)
        self.assertIsInstance(yearStatSheet.winPercentage, dict)
        self.assertIsInstance(yearStatSheet.wal, dict)
        self.assertIsInstance(yearStatSheet.walPerGame, dict)

        self.assertIsInstance(yearStatSheet.awal, dict)
        self.assertIsInstance(yearStatSheet.awalPerGame, dict)
        self.assertIsInstance(yearStatSheet.opponentAWAL, dict)
        self.assertIsInstance(yearStatSheet.opponentAWALPerGame, dict)

        self.assertIsInstance(yearStatSheet.smartWins, dict)
        self.assertIsInstance(yearStatSheet.smartWinsPerGame, dict)
        self.assertIsInstance(yearStatSheet.opponentSmartWins, dict)
        self.assertIsInstance(yearStatSheet.opponentSmartWinsPerGame, dict)

        self.assertIsInstance(yearStatSheet.pointsScored, dict)
        self.assertIsInstance(yearStatSheet.pointsScoredPerGame, dict)
        self.assertIsInstance(yearStatSheet.opponentPointsScored, dict)
        self.assertIsInstance(yearStatSheet.opponentPointsScoredPerGame, dict)

        self.assertIsInstance(yearStatSheet.scoringShare, dict)
        self.assertIsInstance(yearStatSheet.opponentScoringShare, dict)

        self.assertIsInstance(yearStatSheet.maxScore, dict)
        self.assertIsInstance(yearStatSheet.minScore, dict)

        self.assertIsInstance(yearStatSheet.scoringStandardDeviation, dict)

        self.assertIsInstance(yearStatSheet.plusMinus, dict)

        self.assertIsInstance(yearStatSheet.teamScore, dict)
        self.assertIsInstance(yearStatSheet.teamSuccess, dict)
        self.assertIsInstance(yearStatSheet.teamLuck, dict)

        self.assertIsInstance(yearStatSheet.championshipCount, dict)
