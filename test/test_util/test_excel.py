import math
import os
import tempfile
import unittest

from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

from leeger.model.league.League import League
from leeger.model.league.Matchup import Matchup
from leeger.model.league.Team import Team
from leeger.model.league.Week import Week
from leeger.model.league.Year import Year
from leeger.util.excel import leagueToExcel, yearToExcel
from leeger.util.stat_sheet import yearStatSheet
from test.helper.prototypes import getNDefaultOwnersAndTeams


class TestExcel(unittest.TestCase):
    def test_leagueToExcel_happyPath(self):
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
            leagueToExcel(league, fullPath)

            # open created Excel file to check that it was saved correctly
            workbook = load_workbook(filename=fullPath)

            # check sheets
            self.assertEqual(5, len(workbook.sheetnames))
            self.assertEqual("2000", workbook.sheetnames[0])
            self.assertEqual("2001", workbook.sheetnames[1])
            self.assertEqual("2002", workbook.sheetnames[2])
            self.assertEqual("All Time Teams", workbook.sheetnames[3])
            self.assertEqual("All Time Owners", workbook.sheetnames[4])

            # check sheet values
            worksheet2000Values = [
                ["a", 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 2, 2,
                 33.33333333333334, 66.66666666666667, 33.33333333333334, 33.33333333333334,
                 1, 1, 0, -1, 66.76666666666667, 66.76666666666667, 0],
                ["b", 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 2, 2, 1, 1,
                 66.66666666666667, 33.33333333333334, 66.66666666666667, 66.66666666666667,
                 2, 2, 0, 1, 233.5333333333333, 233.5333333333333, 0]]
            worksheet2001Values = [
                ["a2", 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 2, 2,
                 33.33333333333334, 66.66666666666667, 33.33333333333334, 33.33333333333334,
                 1, 1, 0, -1, 66.76666666666667, 66.76666666666667, 0],
                ["b2", 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 2, 2, 1, 1,
                 66.66666666666667, 33.33333333333334, 66.66666666666667, 66.66666666666667,
                 2, 2, 0, 1, 233.5333333333333, 233.5333333333333, 0]]
            worksheet2002Values = [
                ["a3", 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 2, 2,
                 33.33333333333334, 66.66666666666667, 33.33333333333334, 33.33333333333334,
                 1, 1, 0, -1, 66.76666666666667, 66.76666666666667, 0],
                ["b3", 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 2, 2, 1, 1,
                 66.66666666666667, 33.33333333333334, 66.66666666666667, 66.66666666666667,
                 2, 2, 0, 1, 233.5333333333333, 233.5333333333333, 0]]
            yearWorksheetsAndValues = [(workbook["2000"], worksheet2000Values),
                                       (workbook["2001"], worksheet2001Values),
                                       (workbook["2002"], worksheet2002Values)]
            # test year worksheet values
            for i, (currentWorksheet, allWorksheetValues) in enumerate(yearWorksheetsAndValues):
                for j, worksheetValues in enumerate(allWorksheetValues):
                    for k, worksheetValue in enumerate(worksheetValues):
                        row = j + 2
                        column = get_column_letter(k + 1)
                        self.assertEqual(worksheetValue, currentWorksheet[f"{column}{row}"].value)
                self.assertEqual("Team Names", currentWorksheet["A1"].value)
                self.assertEqual("Games Played", currentWorksheet["B1"].value)
                self.assertEqual("Wins", currentWorksheet["C1"].value)
                self.assertEqual("Losses", currentWorksheet["D1"].value)
                self.assertEqual("Ties", currentWorksheet["E1"].value)
                self.assertEqual("Win Percentage", currentWorksheet["F1"].value)
                self.assertEqual("WAL", currentWorksheet["G1"].value)
                self.assertEqual("WAL Per Game", currentWorksheet["H1"].value)
                self.assertEqual("AWAL", currentWorksheet["I1"].value)
                self.assertEqual("AWAL Per Game", currentWorksheet["J1"].value)
                self.assertEqual("Opponent AWAL", currentWorksheet["K1"].value)
                self.assertEqual("Opponent AWAL Per Game", currentWorksheet["L1"].value)
                self.assertEqual("Smart Wins", currentWorksheet["M1"].value)
                self.assertEqual("Smart Wins Per Game", currentWorksheet["N1"].value)
                self.assertEqual("Opponent Smart Wins", currentWorksheet["O1"].value)
                self.assertEqual("Opponent Smart Wins Per Game", currentWorksheet["P1"].value)
                self.assertEqual("Points Scored", currentWorksheet["Q1"].value)
                self.assertEqual("Points Scored Per Game", currentWorksheet["R1"].value)
                self.assertEqual("Opponent Points Scored", currentWorksheet["S1"].value)
                self.assertEqual("Opponent Points Scored Per Game", currentWorksheet["T1"].value)
                self.assertEqual("Scoring Share", currentWorksheet["U1"].value)
                self.assertEqual("Opponent Scoring Share", currentWorksheet["V1"].value)
                self.assertEqual("Max Scoring Share", currentWorksheet["W1"].value)
                self.assertEqual("Min Scoring Share", currentWorksheet["X1"].value)
                self.assertEqual("Max Score", currentWorksheet["Y1"].value)
                self.assertEqual("Min Score", currentWorksheet["Z1"].value)
                self.assertEqual("Scoring Standard Deviation", currentWorksheet["AA1"].value)
                self.assertEqual("Plus/Minus", currentWorksheet["AB1"].value)
                self.assertEqual("Team Score", currentWorksheet["AC1"].value)
                self.assertEqual("Team Success", currentWorksheet["AD1"].value)
                self.assertEqual("Team Luck", currentWorksheet["AE1"].value)

            allTimeTeamsWorksheet = workbook["All Time Teams"]
            self.assertEqual("Team Names", allTimeTeamsWorksheet["A1"].value)
            self.assertEqual("Owner Names", allTimeTeamsWorksheet["B1"].value)
            self.assertEqual("Year", allTimeTeamsWorksheet["C1"].value)
            self.assertEqual("Games Played", allTimeTeamsWorksheet["D1"].value)
            self.assertEqual("Wins", allTimeTeamsWorksheet["E1"].value)
            self.assertEqual("Losses", allTimeTeamsWorksheet["F1"].value)
            self.assertEqual("Ties", allTimeTeamsWorksheet["G1"].value)
            self.assertEqual("Win Percentage", allTimeTeamsWorksheet["H1"].value)
            self.assertEqual("WAL", allTimeTeamsWorksheet["I1"].value)
            self.assertEqual("WAL Per Game", allTimeTeamsWorksheet["J1"].value)
            self.assertEqual("AWAL", allTimeTeamsWorksheet["K1"].value)
            self.assertEqual("AWAL Per Game", allTimeTeamsWorksheet["L1"].value)
            self.assertEqual("Opponent AWAL", allTimeTeamsWorksheet["M1"].value)
            self.assertEqual("Opponent AWAL Per Game", allTimeTeamsWorksheet["N1"].value)
            self.assertEqual("Smart Wins", allTimeTeamsWorksheet["O1"].value)
            self.assertEqual("Smart Wins Per Game", allTimeTeamsWorksheet["P1"].value)
            self.assertEqual("Opponent Smart Wins", allTimeTeamsWorksheet["Q1"].value)
            self.assertEqual("Opponent Smart Wins Per Game", allTimeTeamsWorksheet["R1"].value)
            self.assertEqual("Points Scored", allTimeTeamsWorksheet["S1"].value)
            self.assertEqual("Points Scored Per Game", allTimeTeamsWorksheet["T1"].value)
            self.assertEqual("Opponent Points Scored", allTimeTeamsWorksheet["U1"].value)
            self.assertEqual("Opponent Points Scored Per Game", allTimeTeamsWorksheet["V1"].value)
            self.assertEqual("Scoring Share", allTimeTeamsWorksheet["W1"].value)
            self.assertEqual("Opponent Scoring Share", allTimeTeamsWorksheet["X1"].value)
            self.assertEqual("Max Scoring Share", allTimeTeamsWorksheet["Y1"].value)
            self.assertEqual("Min Scoring Share", allTimeTeamsWorksheet["Z1"].value)
            self.assertEqual("Max Score", allTimeTeamsWorksheet["AA1"].value)
            self.assertEqual("Min Score", allTimeTeamsWorksheet["AB1"].value)
            self.assertEqual("Scoring Standard Deviation", allTimeTeamsWorksheet["AC1"].value)
            self.assertEqual("Plus/Minus", allTimeTeamsWorksheet["AD1"].value)
            self.assertEqual("Team Score", allTimeTeamsWorksheet["AE1"].value)
            self.assertEqual("Team Success", allTimeTeamsWorksheet["AF1"].value)
            self.assertEqual("Team Luck", allTimeTeamsWorksheet["AG1"].value)

    def test_leagueToExcel_fileAlreadyExists_raisesException(self):
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
                leagueToExcel(league, fullPath)
        self.assertEqual(f"Cannot create file at path: '{fullPath}' because there is already a file there.",
                         str(context.exception))

    def test_yearToExcel_excelSheetDoesntAlreadyExist(self):
        owners, teams = getNDefaultOwnersAndTeams(2)
        teams[0].name = "a"
        teams[1].name = "b"
        matchup = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        week = Week(weekNumber=1, matchups=[matchup])
        year = Year(yearNumber=2000, teams=teams, weeks=[week])

        with tempfile.TemporaryDirectory() as tempDir:
            fullPath = os.path.join(tempDir, "tmp.xlsx")
            yearToExcel(year, fullPath)

            # open created Excel file to check that it was saved correctly
            workbook = load_workbook(filename=fullPath)
            worksheet = workbook.active

            self.assertEqual(1, len(workbook.sheetnames))
            self.assertEqual("2000", workbook.sheetnames[0])
            self.assertEqual("Team Names", worksheet["A1"].value)
            self.assertEqual("a", worksheet["A2"].value)
            self.assertEqual("b", worksheet["A3"].value)

            statsWithTitles = yearStatSheet(year).preferredOrderWithTitle()
            for row, teamId in enumerate([team.id for team in year.teams]):
                for col, statWithTitle in enumerate(statsWithTitles):
                    char = get_column_letter(col + 2)
                    if row == 1:
                        # check stat header
                        self.assertEqual(statWithTitle[0], worksheet[f"{char}{row}"].value)
                    # check stat value
                    # due to Excel rounding values, we assert that the values are very, very close
                    assert math.isclose(float(statWithTitle[1][teamId]), worksheet[f"{char}{row + 2}"].value,
                                        rel_tol=0.000000000000001)

    def test_yearToExcel_excelSheetAlreadyExists(self):
        owners, teams1 = getNDefaultOwnersAndTeams(2)
        teams1[0].name = "a1"
        teams1[1].name = "b1"
        matchup1 = Matchup(teamAId=teams1[0].id, teamBId=teams1[1].id, teamAScore=1, teamBScore=2)
        week1 = Week(weekNumber=1, matchups=[matchup1])
        year1 = Year(yearNumber=2000, teams=teams1, weeks=[week1])

        teams2 = [Team(ownerId=owners[0].id, name="a2"), Team(ownerId=owners[1].id, name="b2")]
        matchup2 = Matchup(teamAId=teams2[0].id, teamBId=teams2[1].id, teamAScore=1, teamBScore=2)
        week2 = Week(weekNumber=1, matchups=[matchup2])
        year2 = Year(yearNumber=2001, teams=teams2, weeks=[week2])

        with tempfile.TemporaryDirectory() as tempDir:
            fullPath = os.path.join(tempDir, "tmp.xlsx")
            yearToExcel(year1, fullPath)

            yearToExcel(year2, fullPath)

            # open created Excel file to check that it was saved correctly
            workbook = load_workbook(filename=fullPath)
            worksheet = workbook.worksheets[workbook.sheetnames.index("2001")]

            self.assertEqual(2, len(workbook.sheetnames))
            self.assertEqual("2000", workbook.sheetnames[0])
            self.assertEqual("2001", workbook.sheetnames[1])
            self.assertEqual("Team Names", worksheet["A1"].value)
            self.assertEqual("a2", worksheet["A2"].value)
            self.assertEqual("b2", worksheet["A3"].value)

            statsWithTitles = yearStatSheet(year2).preferredOrderWithTitle()
            for row, teamId in enumerate([team.id for team in year2.teams]):
                for col, statWithTitle in enumerate(statsWithTitles):
                    char = get_column_letter(col + 2)
                    if row == 1:
                        # check stat header
                        self.assertEqual(statWithTitle[0], worksheet[f"{char}{row}"].value)
                    # check stat value
                    # due to Excel rounding values, we assert that the values are very, very close
                    assert math.isclose(float(statWithTitle[1][teamId]), worksheet[f"{char}{row + 2}"].value,
                                        rel_tol=0.000000000000001)
