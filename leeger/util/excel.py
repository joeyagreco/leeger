from __future__ import annotations

import os
import random

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, Color, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table

from leeger.model.league import Year, League
from leeger.util.stat_sheet import leagueStatSheet, yearStatSheet


def leagueToExcel(league: League, filePath: str, **kwargs) -> None:
    """
    If the given Excel file exists already, will raise an exception.
    """
    if league is None:
        raise ValueError("'league' has not been set.")
    if os.path.exists(filePath) and not kwargs.pop("overwrite", False):
        raise FileExistsError(f"Cannot create file at path: '{filePath}' because there is already a file there.")
    else:
        try:
            os.remove(filePath)
        except FileNotFoundError:
            # we don't care if this doesn't exist
            pass

    for year in league.years:
        yearToExcel(year, filePath, **kwargs)

    # add All-Time stats sheet
    workbook = load_workbook(filename=filePath)
    # figure out index to put this sheet into
    # we want the sheets to be ordered: oldest year -> newest year -> all time
    index = len(workbook.sheetnames)
    workbook.create_sheet("All Time", index=index)
    worksheet = workbook["All Time"]

    ####################
    # Styles for table #
    ####################

    # fonts
    headerColumnFont = Font(size=12, bold=True)
    teamNameFont = Font(size=11, bold=True)

    # colors
    GRAY = Color(rgb="B8B8B8")

    def getRandomColor(tint: float = 0) -> Color:
        r = lambda: random.randint(0, 255)
        hexCode = "%02X%02X%02X" % (r(), r(), r())
        return Color(rgb=hexCode, tint=tint)

    OWNER_ROW_COLORS = [getRandomColor(0.5) for _ in range(len(league.owners))]

    # fills
    headerFill = PatternFill(patternType="solid", fgColor=GRAY)

    #################
    # Fill in table #
    #################

    # add title
    worksheet["A1"] = "Owner Names"
    worksheet["A1"].font = headerColumnFont
    worksheet["A1"].fill = headerFill
    # add all team names
    for i, owner in enumerate(league.owners):
        col = "A"
        worksheet[f"{col}{i + 2}"] = owner.name
        worksheet[f"{col}{i + 2}"].font = teamNameFont
        worksheet[f"{col}{i + 2}"].fill = PatternFill(patternType="solid", fgColor=OWNER_ROW_COLORS[i])

    # add all stats
    statsWithTitles = leagueStatSheet(league, **kwargs).preferredOrderWithTitle()
    for row, ownerId in enumerate([owner.id for owner in league.owners]):
        rowFill = PatternFill(patternType="solid", fgColor=OWNER_ROW_COLORS[row])
        for col, statWithTitle in enumerate(statsWithTitles):
            char = get_column_letter(col + 2)
            if row == 1:
                # add stat header
                worksheet[f"{char}{row}"] = statWithTitle[0]
                worksheet[f"{char}{row}"].font = headerColumnFont
                worksheet[f"{char}{row}"].fill = headerFill
            # add stat value
            worksheet[f"{char}{row + 2}"] = statWithTitle[1][ownerId]
            worksheet[f"{char}{row + 2}"].fill = rowFill

    # put stats into table
    table = Table(displayName=f"AllTimeStats",
                  ref="A1:" + get_column_letter(worksheet.max_column) + str(worksheet.max_row))
    worksheet.add_table(table)

    # freeze owner name column
    worksheet.freeze_panes = "B1"

    # save
    workbook.save(filePath)


def yearToExcel(year: Year, filePath: str, **kwargs) -> None:
    """
    If the given Excel file exists already, add a worksheet to it with this year.
    If the given Excel file does not exist, create a new workbook and add a worksheet to it with this year.
    """

    if os.path.exists(filePath):
        workbook = load_workbook(filename=filePath)
        # figure out index to put this sheet into
        # we want the years as sheets in order from oldest -> newest year
        index = 0
        for i, sheetname in enumerate(workbook.sheetnames):
            if year.yearNumber > int(sheetname):
                index += 1
        workbook.create_sheet(str(year.yearNumber), index=index)
    else:
        # create workbook and sheet
        workbook = Workbook()
        workbook.create_sheet(str(year.yearNumber), index=0)
        # remove default sheet
        del workbook["Sheet"]
    worksheet = workbook[str(year.yearNumber)]

    ####################
    # Styles for table #
    ####################

    # fonts
    headerColumnFont = Font(size=12, bold=True)
    teamNameFont = Font(size=11, bold=True)

    # colors
    GRAY = Color(rgb="B8B8B8")

    def getRandomColor(tint: float = 0) -> Color:
        r = lambda: random.randint(0, 255)
        hexCode = "%02X%02X%02X" % (r(), r(), r())
        return Color(rgb=hexCode, tint=tint)

    TEAM_ROW_COLORS = [getRandomColor(0.5) for _ in range(len(year.teams))]

    # fills
    headerFill = PatternFill(patternType="solid", fgColor=GRAY)

    #################
    # Fill in table #
    #################

    # add title
    worksheet["A1"] = "Team Names"
    worksheet["A1"].font = headerColumnFont
    worksheet["A1"].fill = headerFill
    # add all team names
    for i, team in enumerate(year.teams):
        col = "A"
        worksheet[f"{col}{i + 2}"] = team.name
        worksheet[f"{col}{i + 2}"].font = teamNameFont
        worksheet[f"{col}{i + 2}"].fill = PatternFill(patternType="solid", fgColor=TEAM_ROW_COLORS[i])

    # add all stats
    statsWithTitles = yearStatSheet(year, **kwargs).preferredOrderWithTitle()
    for row, teamId in enumerate([team.id for team in year.teams]):
        rowFill = PatternFill(patternType="solid", fgColor=TEAM_ROW_COLORS[row])
        for col, statWithTitle in enumerate(statsWithTitles):
            char = get_column_letter(col + 2)
            if row == 1:
                # add stat header
                worksheet[f"{char}{row}"] = statWithTitle[0]
                worksheet[f"{char}{row}"].font = headerColumnFont
                worksheet[f"{char}{row}"].fill = headerFill
            # add stat value
            worksheet[f"{char}{row + 2}"] = statWithTitle[1][teamId]
            worksheet[f"{char}{row + 2}"].fill = rowFill

    # put stats into table
    table = Table(displayName=f"YearStats{year.yearNumber}",
                  ref="A1:" + get_column_letter(worksheet.max_column) + str(worksheet.max_row))
    worksheet.add_table(table)
    # freeze team name column
    worksheet.freeze_panes = "B1"

    # save
    workbook.save(filePath)
