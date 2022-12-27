from __future__ import annotations

import os
import random
from datetime import datetime
from typing import Any

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, Color, PatternFill, Alignment, Side, Border
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.dimensions import DimensionHolder, ColumnDimension
from openpyxl.worksheet.table import Table
from openpyxl.worksheet.worksheet import Worksheet

from leeger.model.filter import AllTimeFilters, YearFilters
from leeger.model.league import Year, League
from leeger.util.stat_sheet import yearStatSheet, leagueStatSheet, allTimeTeamsStatSheet


def leagueToExcel(league: League, filePath: str, **kwargs) -> None:
    """
    Saves the given League object to an Excel file.
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

    # get owner names
    # and
    # make sure we have the same color for owners and their teams across sheets
    ownerIdToSeedMap = dict()
    ownerIds = list()
    ownerNames = list()
    for owner in league.owners:
        ownerNames.append(owner.name)
        ownerIds.append(owner.id)
        ownerIdToSeedMap[owner.id] = f"{owner.id}{datetime.now().date()}"
    ownerIdToColorMap = dict()
    for ownerId, seed in ownerIdToSeedMap.items():
        ownerIdToColorMap[ownerId] = __getRandomColor(0.5, seed)

    # gather info for all time teams to be used later
    allTimeTeamIds: list[str] = list()
    allTimeTeamNames: list[str] = list()
    for year in league.years:
        # sort teams by owner ID
        allTeams = [team for team in year.teams]
        allTeams.sort(key=lambda x: x.ownerId)
        allTimeTeamIds += [team.id for team in allTeams]
        allTimeTeamNames += [team.name for team in allTeams]

        # add a sheet to the Excel document for this year
        yearToExcel(year, filePath, overwrite=False, **kwargs.copy())

    # add All-Time teams stats sheet
    workbook = load_workbook(filename=filePath)
    # figure out index to put this sheet into
    # we want the sheets to be ordered: oldest year -> newest year -> all time teams -> all time owners
    index = len(workbook.sheetnames)
    workbook.create_sheet("All Time Teams", index=index)
    worksheet = workbook["All Time Teams"]

    allTimeTeamsStatSheet_ = allTimeTeamsStatSheet(league, **kwargs.copy())

    allTimeFilters = AllTimeFilters.preferredOrderWithTitle(league, **kwargs.copy())
    __populateWorksheet(worksheet=worksheet,
                        displayName="AllTimeTeamStats",
                        titlesAndStatDicts=allTimeTeamsStatSheet_,
                        title="Team",
                        entityIds=allTimeTeamIds,
                        entityNames=allTimeTeamNames,
                        ownerIdToColorMap=ownerIdToColorMap,
                        ownerIds=ownerIds * len(league.years),
                        legendKeyValues=allTimeFilters,
                        freezePanes="D2")
    # save
    workbook.save(filePath)

    # add All-Time owner stats sheet
    workbook = load_workbook(filename=filePath)
    # figure out index to put this sheet into
    # we want the sheets to be ordered: oldest year -> newest year -> all time teams -> all time owners
    index = len(workbook.sheetnames)
    workbook.create_sheet("All Time Owners", index=index)
    worksheet = workbook["All Time Owners"]

    ownerIdToNameMap = dict()
    for owner in league.owners:
        ownerIdToNameMap[owner.id] = owner.name

    allTimeOwnerStatsWithTitles = leagueStatSheet(league, **kwargs.copy()).preferredOrderWithTitle()
    allTimeOwnerStatsWithTitles.insert(0, ("Owner", ownerIdToNameMap))

    __populateWorksheet(worksheet=worksheet,
                        displayName="AllTimeOwnerStats",
                        titlesAndStatDicts=allTimeOwnerStatsWithTitles,
                        title="Owner",
                        entityIds=ownerIds,
                        entityNames=ownerNames,
                        ownerIdToColorMap=ownerIdToColorMap,
                        ownerIds=ownerIds,
                        legendKeyValues=allTimeFilters,
                        freezePanes="B2")

    # save
    workbook.save(filePath)


def yearToExcel(year: Year, filePath: str, **kwargs) -> None:
    """
    Saves the given Year object to an Excel File.
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
            if year.yearNumber > int(sheetname[:5]):
                index += 1
        workbook.create_sheet(f"{year.yearNumber} Teams", index=index)
        workbook.create_sheet(f"{year.yearNumber} Matchups", index=index + 1)
    else:
        # overwrite Excel file OR create new Excel file
        try:
            os.remove(filePath)
        except FileNotFoundError:
            # we don't care if this doesn't exist
            pass
        # create workbook and sheet
        workbook = Workbook()
        workbook.create_sheet(f"{year.yearNumber} Teams", index=0)
        workbook.create_sheet(f"{year.yearNumber} Matchups", index=1)
        # remove default sheet
        del workbook["Sheet"]
    worksheet = workbook[f"{year.yearNumber} Teams"]

    # get team names
    # and
    # make sure we have the same color for owners and their teams across sheets
    ownerIdToSeedMap = dict()
    ownerIds = list()
    teamNames = list()
    teamIdToNameMap = dict()
    for team in year.teams:
        teamNames.append(team.name)
        ownerIds.append(team.ownerId)
        ownerIdToSeedMap[team.ownerId] = f"{team.ownerId}{datetime.now().date()}"
        teamIdToNameMap[team.id] = team.name
    ownerIdToColorMap = dict()
    for ownerId, seed in ownerIdToSeedMap.items():
        ownerIdToColorMap[ownerId] = __getRandomColor(0.5, seed)

    teamIds = [team.id for team in year.teams]
    yearFilters = YearFilters.preferredOrderWithTitle(year, **kwargs.copy())

    yearStatsWithTitles = yearStatSheet(year, **kwargs.copy()).preferredOrderWithTitle()
    yearStatsWithTitles.insert(0, ("Team", teamIdToNameMap))
    __populateWorksheet(worksheet=worksheet,
                        displayName=f"Teams{year.yearNumber}",
                        titlesAndStatDicts=yearStatsWithTitles,
                        title="Team",
                        entityIds=teamIds,
                        entityNames=teamNames,
                        ownerIdToColorMap=ownerIdToColorMap,
                        ownerIds=ownerIds,
                        legendKeyValues=yearFilters,
                        freezePanes="B2")
    # save
    workbook.save(filePath)


def __getRandomColor(tint: float = 0, seed: str = None) -> Color:
    """
    Used to get a random row color.
    """
    if seed:
        random.seed(seed)
    r = lambda: random.randint(0, 255)
    hexCode = "%02X%02X%02X" % (r(), r(), r())
    return Color(rgb=hexCode, tint=tint)


def __populateWorksheet(*,
                        worksheet: Worksheet,
                        displayName: str,
                        titlesAndStatDicts: list[tuple[str, dict]],
                        title: str,
                        entityIds: list[str],
                        entityNames: list[str],
                        ownerIdToColorMap: dict[str, Color],
                        ownerIds: list[str],
                        legendKeyValues: list[tuple[str, Any]],
                        freezePanes: str) -> None:
    ####################
    # Styles for table #
    ####################

    # fonts
    HEADER_COLUMN_FONT = Font(size=12, bold=True)
    ENTITY_NAME_FONT = Font(size=11, bold=True)

    # colors
    BLACK = Color(rgb="000000")
    LIGHT_GRAY = Color(rgb="B8B8B8")
    MEDIUM_GRAY = Color(rgb="828282")

    # fills
    HEADER_FILL = PatternFill(patternType="solid", fgColor=LIGHT_GRAY)

    #################
    # Fill in table #
    #################

    # # add title
    # worksheet["A1"] = title
    # worksheet["A1"].font = HEADER_COLUMN_FONT
    # worksheet["A1"].fill = HEADER_FILL
    # worksheet["A1"].alignment = Alignment(horizontal='center')
    # # add all entity names
    # for i, entityName in enumerate(entityNames):
    #     cell = f"A{i + 2}"
    #     worksheet[cell] = entityName
    #     worksheet[cell].font = ENTITY_NAME_FONT
    #     worksheet[cell].fill = PatternFill(patternType="solid", fgColor=ownerIdToColorMap[ownerIds[i]])

    # add all stats
    for i, entityId in enumerate(entityIds):
        rowFill = PatternFill(patternType="solid", fgColor=ownerIdToColorMap[ownerIds[i]])
        for col, (title, statDict) in enumerate(titlesAndStatDicts):
            char = get_column_letter(col + 1)
            if i == 1:
                # add stat header
                cell = f"{char}{i}"
                worksheet[cell] = title
                worksheet[cell].font = HEADER_COLUMN_FONT
                worksheet[cell].fill = HEADER_FILL
                worksheet[cell].alignment = Alignment(horizontal='center')
            # add stat value
            cell = f"{char}{i + 2}"
            if entityId in statDict:
                worksheet[cell] = statDict[entityId]
            else:
                worksheet[cell] = "N/A"
            worksheet[cell].fill = rowFill

    # put stats into table
    table = Table(displayName=displayName,
                  ref="A1:" + get_column_letter(worksheet.max_column) + str(len(entityIds) + 1))
    worksheet.add_table(table)
    # freeze owner name column and header row
    worksheet.freeze_panes = freezePanes

    # add legend for filters
    # define border to go around legend
    topSideSolid = Side(border_style="thick", color=BLACK)
    bottomSideSolid = Side(border_style="thick", color=BLACK)
    bottomSideThin = Side(border_style="thin", color=BLACK)
    leftSideSolid = Side(border_style="thick", color=BLACK)
    rightSideSolid = Side(border_style="thick", color=BLACK)
    # legend formatting
    legendCellAlignment = Alignment(horizontal='center')

    legendRowNumber = len(entityIds) + 4
    legendColLetter = "A"
    titleCell = f"A{legendRowNumber}"
    worksheet[titleCell] = "Filters Applied"
    worksheet[titleCell].fill = PatternFill(patternType="solid", fgColor=MEDIUM_GRAY)
    worksheet[titleCell].font = Font(bold=True)
    border = Border(left=leftSideSolid, right=rightSideSolid, top=topSideSolid, bottom=bottomSideThin)
    worksheet[titleCell].border = border
    worksheet[titleCell].alignment = legendCellAlignment

    for kwarg_title, kwarg_value in legendKeyValues:
        legendRowNumber += 1
        cell = f"{legendColLetter}{legendRowNumber}"
        worksheet[cell] = f"{kwarg_title}: {kwarg_value}"
        worksheet[cell].fill = PatternFill(patternType="solid", fgColor=MEDIUM_GRAY)
        worksheet[cell].alignment = legendCellAlignment
        border = Border(left=leftSideSolid, right=rightSideSolid)
        worksheet[cell].border = border

    # add border to last cell
    border = Border(left=leftSideSolid, right=rightSideSolid, bottom=bottomSideSolid)
    worksheet[f"{legendColLetter}{legendRowNumber}"].border = border

    # set column widths
    TITLE_MULTIPLIER = 1.2
    NAME_MULTIPLIER = 1.0
    DATA_MULTIPLIER = 0.5
    dim_holder = DimensionHolder(worksheet=worksheet)

    for col in range(worksheet.min_column, worksheet.max_column + 1):
        # figure out the width we want this column to be
        # first column has entity names, so use a different multiplier for them
        isNameColumn = col == 1
        maxWidth = 0
        for i, cell in enumerate(worksheet[get_column_letter(col)]):
            if cell.value:
                # count title/name cell characters as more than a data cell
                if i == 0:
                    multiplier = TITLE_MULTIPLIER
                elif isNameColumn:
                    multiplier = NAME_MULTIPLIER
                else:
                    multiplier = DATA_MULTIPLIER
                maxWidth = max((maxWidth, len(str(cell.value)) * multiplier))
        dim_holder[get_column_letter(col)] = ColumnDimension(worksheet, min=col, max=col, width=maxWidth + 7)

    worksheet.column_dimensions = dim_holder
