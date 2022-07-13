import os
import tempfile
import unittest

from openpyxl import load_workbook

from leeger.model.league.League import League
from leeger.model.league.Matchup import Matchup
from leeger.model.league.Owner import Owner
from leeger.model.league.Team import Team
from leeger.model.league.Week import Week
from leeger.model.league.Year import Year
from leeger.model.stat.AllTimeStatSheet import AllTimeStatSheet
from test.helper.prototypes import getNDefaultOwnersAndTeams


class TestLeague(unittest.TestCase):
    def test_league_init(self):
        year = Year(yearNumber=0, teams=[], weeks=[])
        owner = Owner(name="")
        league = League(name="leagueName", owners=[owner], years=[year])

        self.assertEqual("leagueName", league.name)
        self.assertEqual(1, len(league.owners))
        self.assertEqual(1, len(league.years))
        self.assertEqual(owner.id, league.owners[0].id)
        self.assertEqual(year.id, league.years[0].id)

    def test_league_statSheet(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        week = Week(weekNumber=1, matchups=[matchup])
        year = Year(yearNumber=2000, teams=teams, weeks=[week])

        league = League(name="TEST", owners=owners, years=[year])

        leagueStatSheet = league.statSheet()

        self.assertIsInstance(leagueStatSheet, AllTimeStatSheet)
        self.assertIsInstance(leagueStatSheet.wins, dict)
        self.assertIsInstance(leagueStatSheet.losses, dict)
        self.assertIsInstance(leagueStatSheet.ties, dict)
        self.assertIsInstance(leagueStatSheet.winPercentage, dict)
        self.assertIsInstance(leagueStatSheet.wal, dict)
        self.assertIsInstance(leagueStatSheet.walPerGame, dict)

        self.assertIsInstance(leagueStatSheet.awal, dict)
        self.assertIsInstance(leagueStatSheet.awalPerGame, dict)
        self.assertIsInstance(leagueStatSheet.opponentAWAL, dict)
        self.assertIsInstance(leagueStatSheet.opponentAWALPerGame, dict)

        self.assertIsInstance(leagueStatSheet.smartWins, dict)
        self.assertIsInstance(leagueStatSheet.smartWinsPerGame, dict)
        self.assertIsInstance(leagueStatSheet.opponentSmartWins, dict)
        self.assertIsInstance(leagueStatSheet.opponentSmartWinsPerGame, dict)

        self.assertIsInstance(leagueStatSheet.pointsScored, dict)
        self.assertIsInstance(leagueStatSheet.pointsScoredPerGame, dict)
        self.assertIsInstance(leagueStatSheet.opponentPointsScored, dict)
        self.assertIsInstance(leagueStatSheet.opponentPointsScoredPerGame, dict)

        self.assertIsInstance(leagueStatSheet.scoringShare, dict)
        self.assertIsInstance(leagueStatSheet.opponentScoringShare, dict)

        self.assertIsInstance(leagueStatSheet.maxScore, dict)
        self.assertIsInstance(leagueStatSheet.minScore, dict)

        self.assertIsInstance(leagueStatSheet.scoringStandardDeviation, dict)

        self.assertIsInstance(leagueStatSheet.plusMinus, dict)

        self.assertIsInstance(leagueStatSheet.teamScore, dict)
        self.assertIsInstance(leagueStatSheet.teamSuccess, dict)
        self.assertIsInstance(leagueStatSheet.teamLuck, dict)

    def test_league_toExcel_happyPath(self):
        owners, teams1 = getNDefaultOwnersAndTeams(2)
        teams1[0].name = "a"
        teams1[1].name = "b"
        matchup1 = Matchup(teamAId=teams1[0].id, teamBId=teams1[1].id, teamAScore=1, teamBScore=2)
        week1 = Week(weekNumber=1, matchups=[matchup1])
        year1 = Year(yearNumber=2000, teams=teams1, weeks=[week1])

        teams2 = [Team(ownerId=owners[0].id, name="a2"), Team(ownerId=owners[1].id, name="b2")]
        matchup2 = Matchup(teamAId=teams2[0].id, teamBId=teams2[1].id, teamAScore=1, teamBScore=2)
        week2 = Week(weekNumber=1, matchups=[matchup2])
        year2 = Year(yearNumber=2001, teams=teams2, weeks=[week2])

        teams3 = [Team(ownerId=owners[0].id, name="a3"), Team(ownerId=owners[1].id, name="b3")]
        matchup3 = Matchup(teamAId=teams3[0].id, teamBId=teams3[1].id, teamAScore=1, teamBScore=2)
        week3 = Week(weekNumber=1, matchups=[matchup3])
        year3 = Year(yearNumber=2002, teams=teams3, weeks=[week3])

        league = League(name="", owners=owners, years=[year1, year2, year3])

        with tempfile.TemporaryDirectory() as tempDir:
            fullPath = os.path.join(tempDir, "tmp.xlsx")
            league.toExcel(fullPath)

            # open created Excel file to check that it was saved correctly
            workbook = load_workbook(filename=fullPath)

            self.assertEqual(4, len(workbook.sheetnames))
            self.assertEqual("2000", workbook.sheetnames[0])
            self.assertEqual("2001", workbook.sheetnames[1])
            self.assertEqual("2002", workbook.sheetnames[2])
            self.assertEqual("All Time", workbook.sheetnames[3])

    def test_league_toExcel_fileAlreadyExists_raisesException(self):
        owners, teams1 = getNDefaultOwnersAndTeams(2)
        teams1[0].name = "a"
        teams1[1].name = "b"
        matchup1 = Matchup(teamAId=teams1[0].id, teamBId=teams1[1].id, teamAScore=1, teamBScore=2)
        week1 = Week(weekNumber=1, matchups=[matchup1])
        year1 = Year(yearNumber=2000, teams=teams1, weeks=[week1])

        teams2 = [Team(ownerId=owners[0].id, name="a2"), Team(ownerId=owners[1].id, name="b2")]
        matchup2 = Matchup(teamAId=teams2[0].id, teamBId=teams2[1].id, teamAScore=1, teamBScore=2)
        week2 = Week(weekNumber=1, matchups=[matchup2])
        year2 = Year(yearNumber=2001, teams=teams2, weeks=[week2])

        teams3 = [Team(ownerId=owners[0].id, name="a3"), Team(ownerId=owners[1].id, name="b3")]
        matchup3 = Matchup(teamAId=teams3[0].id, teamBId=teams3[1].id, teamAScore=1, teamBScore=2)
        week3 = Week(weekNumber=1, matchups=[matchup3])
        year3 = Year(yearNumber=1999, teams=teams3, weeks=[week3])

        league = League(name="", owners=owners, years=[year1, year2, year3])

        with self.assertRaises(FileExistsError) as context:
            with tempfile.TemporaryDirectory() as tempDir:
                fullPath = os.path.join(tempDir, "tmp.xlsx")
                # create a file with this same name/path first
                with open(fullPath, "w") as f:
                    ...
                league.toExcel(fullPath)
        self.assertEqual(f"Cannot create file at path: '{fullPath}' because there is already a file there.",
                         str(context.exception))
