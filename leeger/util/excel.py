from __future__ import annotations

import os
import random

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, Color, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table
from openpyxl.worksheet.worksheet import Worksheet

from leeger.model.league import Year, League
from leeger.util.stat_sheet import yearStatSheet, leagueStatSheet


def leagueToExcel(league: League, filePath: str, **kwargs) -> None:
    """
    If the given Excel file exists already, will raise an exception.
    """
    overwrite = kwargs.pop("overwrite", False)

    if league is None:
        raise ValueError("'league' has not been set.")
    if os.path.exists(filePath) and not overwrite:
        raise FileExistsError(f"Cannot create file at path: '{filePath}' because there is already a file there.")
    else:
        try:
            os.remove(filePath)
        except FileNotFoundError:
            # we don't care if this doesn't exist
            pass

    for year in league.years:
        yearToExcel(year, filePath, overwrite=False, **kwargs)

    # add All-Time stats sheet
    workbook = load_workbook(filename=filePath)
    # figure out index to put this sheet into
    # we want the sheets to be ordered: oldest year -> newest year -> all time
    index = len(workbook.sheetnames)
    workbook.create_sheet("All Time", index=index)
    worksheet = workbook["All Time"]

    __populateWorksheet(worksheet,
                        leagueStatSheet(league, **kwargs).preferredOrderWithTitle(),
                        "Owner Names",
                        [owner.id for owner in league.owners],
                        [owner.name for owner in league.owners])

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
    overwrite = kwargs.pop("overwrite", False)

    if os.path.exists(filePath) and not overwrite:
        workbook = load_workbook(filename=filePath)
        # figure out index to put this sheet into
        # we want the years as sheets in order from oldest -> newest year
        index = 0
        for i, sheetname in enumerate(workbook.sheetnames):
            if year.yearNumber > int(sheetname):
                index += 1
        workbook.create_sheet(str(year.yearNumber), index=index)
    else:
        # overwrite Excel file OR create new Excel file
        try:
            os.remove(filePath)
        except FileNotFoundError:
            # we don't care if this doesn't exist
            pass
        # create workbook and sheet
        workbook = Workbook()
        workbook.create_sheet(str(year.yearNumber), index=0)
        # remove default sheet
        del workbook["Sheet"]
    worksheet = workbook[str(year.yearNumber)]

    __populateWorksheet(worksheet,
                        yearStatSheet(year, **kwargs).preferredOrderWithTitle(),
                        "Team Names",
                        [team.id for team in year.teams],
                        [team.name for team in year.teams])

    # put stats into table
    table = Table(displayName=f"YearStats{year.yearNumber}",
                  ref="A1:" + get_column_letter(worksheet.max_column) + str(worksheet.max_row))
    worksheet.add_table(table)
    # freeze team name column
    worksheet.freeze_panes = "B1"

    # save
    workbook.save(filePath)


def __getRandomColor(tint: float = 0) -> Color:
    """
    Used to get a random row color.
    """
    r = lambda: random.randint(0, 255)
    hexCode = "%02X%02X%02X" % (r(), r(), r())
    return Color(rgb=hexCode, tint=tint)


def __populateWorksheet(worksheet: Worksheet,
                        statsWithTitles: list[tuple[str, dict]],
                        title: str,
                        entityIds: list[str],
                        entityNames: list[str]) -> None:
    ####################
    # Styles for table #
    ####################

    # fonts
    HEADER_COLUMN_FONT = Font(size=12, bold=True)
    ENTITY_NAME_FONT = Font(size=11, bold=True)

    # colors
    GRAY = Color(rgb="B8B8B8")

    ENTITY_ROW_COLORS = [__getRandomColor(0.5) for _ in range(len(entityNames))]

    # fills
    HEADER_FILL = PatternFill(patternType="solid", fgColor=GRAY)

    #################
    # Fill in table #
    #################

    # add title
    worksheet["A1"] = title
    worksheet["A1"].font = HEADER_COLUMN_FONT
    worksheet["A1"].fill = HEADER_FILL
    # add all entity names
    for i, entityName in enumerate(entityNames):
        col = "A"
        worksheet[f"{col}{i + 2}"] = entityName
        worksheet[f"{col}{i + 2}"].font = ENTITY_NAME_FONT
        worksheet[f"{col}{i + 2}"].fill = PatternFill(patternType="solid", fgColor=ENTITY_ROW_COLORS[i])

    # add all stats
    for row, entityId in enumerate(entityIds):
        rowFill = PatternFill(patternType="solid", fgColor=ENTITY_ROW_COLORS[row])
        for col, statWithTitle in enumerate(statsWithTitles):
            char = get_column_letter(col + 2)
            if row == 1:
                # add stat header
                worksheet[f"{char}{row}"] = statWithTitle[0]
                worksheet[f"{char}{row}"].font = HEADER_COLUMN_FONT
                worksheet[f"{char}{row}"].fill = HEADER_FILL
            # add stat value
            worksheet[f"{char}{row + 2}"] = statWithTitle[1][entityId]
            worksheet[f"{char}{row + 2}"].fill = rowFill
