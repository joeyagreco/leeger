from leeger.model.filter import YearFilters, AllTimeFilters
from leeger.model.league import League, Year
from leeger.util.navigator import LeagueNavigator, YearNavigator
from leeger.util.stat_sheet import yearStatSheet


def allTimeTeamsStatSheet(league: League, **kwargs) -> list[tuple[str, dict]]:
    allTimeTeamsStatsWithTitles: list[tuple[str, dict]] = list()
    for year in league.years:
        ownerNames: dict[str, str] = dict()
        years: dict[str, int] = dict()
        teamIdToNameMap = dict()
        teamIdToDivisionNameMap = dict()
        for team in year.teams:
            ownerNames[team.id] = LeagueNavigator.getOwnerById(league, team.ownerId).name
            years[team.id] = year.yearNumber
            teamIdToNameMap[team.id] = team.name
            if team.divisionId:
                teamIdToDivisionNameMap[team.id] = YearNavigator.getDivisionById(
                    year, team.divisionId
                ).name
        yearStatsWithTitles = yearStatSheet(
            year, ownerNames=ownerNames, years=years, **kwargs
        ).preferredOrderWithTitle()

        yearStatsWithTitles.insert(0, ("Team", teamIdToNameMap))
        # TODO: need logic here to insert "N/A" for division column if some years have divisions and some years don't
        if len(year.divisions) > 0:
            yearStatsWithTitles.insert(2, ("Division", teamIdToDivisionNameMap))

        allTimeTeamsStatsWithTitles += yearStatsWithTitles

    # condense stats with titles so there's only 1 list value for each title
    condensedAllTimeTeamsStatsWithTitles: list[tuple[str, dict]] = list()
    for titleStr, statsDict in allTimeTeamsStatsWithTitles:
        allTitlesInCondensedList = list()
        if len(condensedAllTimeTeamsStatsWithTitles) > 0:
            allTitlesInCondensedList = [
                values[0] for values in condensedAllTimeTeamsStatsWithTitles
            ]
        if titleStr in allTitlesInCondensedList:
            # add to stats dict for the existing title
            for i, (title_s, stats_d) in enumerate(condensedAllTimeTeamsStatsWithTitles):
                if title_s == titleStr:
                    condensedAllTimeTeamsStatsWithTitles[i] = (title_s, stats_d | statsDict)
        else:
            condensedAllTimeTeamsStatsWithTitles.append((titleStr, statsDict))
    return condensedAllTimeTeamsStatsWithTitles


def yearMatchupsStatSheet(
    year: Year, includeOwnerIds: bool = False, includeYears: bool = False, **kwargs
) -> tuple[list[tuple[str, dict]], dict[str, str]]:
    yearFilters = YearFilters.getForYear(year, **kwargs)
    modifiedMatchupIdToOwnerIdMap: dict = dict()
    teamForNames: dict[str, str] = dict()
    ownerForIds: dict[str, str] = dict()
    teamAgainstNames: dict[str, str] = dict()
    ownerAgainstIds: dict[str, str] = dict()
    teamForScores: dict[str, float | int] = dict()
    teamAgainstScores: dict[str, float | int] = dict()
    matchupTypes: dict[str, str] = dict()
    yearNumbers: dict[str, int] = dict()
    weekNumbers: dict[str, int] = dict()

    for week in year.weeks:
        if yearFilters.weekNumberStart <= week.weekNumber <= yearFilters.weekNumberEnd:
            for matchup in week.matchups:
                if matchup.matchupType in yearFilters.includeMatchupTypes and (
                    matchup.multiWeekMatchupId is None
                    or yearFilters.includeMultiWeekMatchups is True
                ):
                    teamA = YearNavigator.getTeamById(year, matchup.teamAId)
                    teamB = YearNavigator.getTeamById(year, matchup.teamBId)
                    # add matchup for both teams
                    # add for "A" team
                    modifiedMatchupId = f"{matchup.id}A"
                    modifiedMatchupIdToOwnerIdMap[modifiedMatchupId] = teamA.ownerId
                    teamForNames[modifiedMatchupId] = teamA.name
                    ownerForIds[modifiedMatchupId] = teamA.ownerId
                    teamAgainstNames[modifiedMatchupId] = teamB.name
                    ownerAgainstIds[modifiedMatchupId] = teamB.ownerId
                    teamForScores[modifiedMatchupId] = matchup.teamAScore
                    teamAgainstScores[modifiedMatchupId] = matchup.teamBScore
                    matchupTypes[modifiedMatchupId] = matchup.matchupType.name
                    yearNumbers[modifiedMatchupId] = year.yearNumber
                    weekNumbers[modifiedMatchupId] = week.weekNumber
                    # add for "B" team
                    modifiedMatchupId = f"{matchup.id}B"
                    modifiedMatchupIdToOwnerIdMap[modifiedMatchupId] = teamB.ownerId
                    teamForNames[modifiedMatchupId] = teamB.name
                    ownerForIds[modifiedMatchupId] = teamB.ownerId
                    teamAgainstNames[modifiedMatchupId] = teamA.name
                    ownerAgainstIds[modifiedMatchupId] = teamA.ownerId
                    teamForScores[modifiedMatchupId] = matchup.teamBScore
                    teamAgainstScores[modifiedMatchupId] = matchup.teamAScore
                    matchupTypes[modifiedMatchupId] = matchup.matchupType.name
                    yearNumbers[modifiedMatchupId] = year.yearNumber
                    weekNumbers[modifiedMatchupId] = week.weekNumber

    titlesAndStatDicts = [
        ("Team For", teamForNames),
        ("Team Against", teamAgainstNames),
        ("Week Number", weekNumbers),
        ("Matchup Type", matchupTypes),
        ("Points For", teamForScores),
        ("Points Against", teamAgainstScores),
    ]
    if includeYears:
        titlesAndStatDicts.insert(2, ("Year", yearNumbers))
    if includeOwnerIds:
        titlesAndStatDicts.insert(1, ("Owner ID For", ownerForIds))
        titlesAndStatDicts.insert(3, ("Owner ID Against", ownerAgainstIds))

    return titlesAndStatDicts, modifiedMatchupIdToOwnerIdMap


def allTimeMatchupsStatSheet(
    league: League, **kwargs
) -> tuple[list[tuple[str, dict]], dict[str, str]]:
    allTimeFilters = AllTimeFilters.getForLeague(league, **kwargs.copy())

    allYearMatchupStatSheets: list = list()
    allModifiedMatchupIdToOwnerIdMaps: list = list()
    teamForNames: dict[str, str] = dict()
    ownerForNames: dict[str, str] = dict()
    teamAgainstNames: dict[str, str] = dict()
    ownerAgainstNames: dict[str, str] = dict()
    teamForScores: dict[str, float | int] = dict()
    teamAgainstScores: dict[str, float | int] = dict()
    matchupTypes: dict[str, str] = dict()
    weekNumbers: dict[str, int] = dict()
    yearNumbers: dict[str, int] = dict()

    for year in league.years:
        if allTimeFilters.yearNumberStart <= year.yearNumber <= allTimeFilters.yearNumberEnd:
            (
                currentYearMatchupStatSheet,
                currentModifiedMatchupIdToOwnerIdMap,
            ) = yearMatchupsStatSheet(
                year, includeYears=True, includeOwnerIds=True, **kwargs.copy()
            )
            allYearMatchupStatSheets.append(currentYearMatchupStatSheet)
            allModifiedMatchupIdToOwnerIdMaps.append(currentModifiedMatchupIdToOwnerIdMap)

    # combine responses into 1 response
    for yearMatchupStatSheet in allYearMatchupStatSheets:
        for title, statDict in yearMatchupStatSheet:
            if title == "Team For":
                teamForNames.update(statDict)
            elif title == "Team Against":
                teamAgainstNames.update(statDict)
            elif title == "Week Number":
                weekNumbers.update(statDict)
            elif title == "Matchup Type":
                matchupTypes.update(statDict)
            elif title == "Points For":
                teamForScores.update(statDict)
            elif title == "Points Against":
                teamAgainstScores.update(statDict)
            elif title == "Year":
                yearNumbers.update(statDict)
            elif title == "Owner ID For":
                # turn owner IDs into owner names
                currentOwnerForNames: dict[str, str] = dict()
                for key, ownerId in statDict.items():
                    owner = LeagueNavigator.getOwnerById(league, ownerId)
                    currentOwnerForNames[key] = owner.name
                ownerForNames.update(currentOwnerForNames)
            elif title == "Owner ID Against":
                # turn owner IDs into owner names
                currentOwnerAgainstNames: dict[str, str] = dict()
                for key, ownerId in statDict.items():
                    owner = LeagueNavigator.getOwnerById(league, ownerId)
                    currentOwnerAgainstNames[key] = owner.name
                ownerAgainstNames.update(currentOwnerAgainstNames)

    combinedModifiedMatchupIdToOwnerIdMap: dict = dict()
    for modifiedMatchupIdToOwnerIdMap in allModifiedMatchupIdToOwnerIdMaps:
        combinedModifiedMatchupIdToOwnerIdMap.update(modifiedMatchupIdToOwnerIdMap)

    return [
        ("Team For", teamForNames),
        ("Owner For", ownerForNames),
        ("Team Against", teamAgainstNames),
        ("Owner Against", ownerAgainstNames),
        ("Year", yearNumbers),
        ("Week Number", weekNumbers),
        ("Matchup Type", matchupTypes),
        ("Points For", teamForScores),
        ("Points Against", teamAgainstScores),
    ], combinedModifiedMatchupIdToOwnerIdMap
