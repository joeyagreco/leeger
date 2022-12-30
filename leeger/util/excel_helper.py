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
        for team in year.teams:
            ownerNames[team.id] = LeagueNavigator.getOwnerById(league, team.ownerId).name
            years[team.id] = year.yearNumber
            teamIdToNameMap[team.id] = team.name
        yearStatsWithTitles = yearStatSheet(year,
                                            ownerNames=ownerNames,
                                            years=years,
                                            **kwargs).preferredOrderWithTitle()

        yearStatsWithTitles.insert(0, ("Team", teamIdToNameMap))
        allTimeTeamsStatsWithTitles += yearStatsWithTitles

    # condense stats with titles so there's only 1 list value for each title
    condensedAllTimeTeamsStatsWithTitles: list[tuple[str, dict]] = list()
    for titleStr, statsDict in allTimeTeamsStatsWithTitles:
        allTitlesInCondensedList = list()
        if len(condensedAllTimeTeamsStatsWithTitles) > 0:
            allTitlesInCondensedList = [values[0] for values in condensedAllTimeTeamsStatsWithTitles]
        if titleStr in allTitlesInCondensedList:
            # add to stats dict for the existing title
            for i, (title_s, stats_d) in enumerate(condensedAllTimeTeamsStatsWithTitles):
                if title_s == titleStr:
                    condensedAllTimeTeamsStatsWithTitles[i] = (title_s, stats_d | statsDict)
        else:
            condensedAllTimeTeamsStatsWithTitles.append((titleStr, statsDict))
    return condensedAllTimeTeamsStatsWithTitles


def yearMatchupsStatSheet(year: Year, **kwargs) -> tuple[list[tuple[str, dict]], dict[str, str]]:
    yearFilters = YearFilters.getForYear(year, **kwargs)
    modifiedMatchupIdToOwnerIdMap: dict = dict()
    teamANames: dict[str, str] = dict()
    teamBNames: dict[str, str] = dict()
    teamAScores: dict[str, float | int] = dict()
    teamBScores: dict[str, float | int] = dict()
    matchupTypes: dict[str, str] = dict()
    weekNumbers: dict[str, int] = dict()

    for week in year.weeks:
        if yearFilters.weekNumberStart <= week.weekNumber <= yearFilters.weekNumberEnd:
            for matchup in week.matchups:
                if matchup.matchupType in yearFilters.includeMatchupTypes \
                        and (matchup.multiWeekMatchupId is None or yearFilters.includeMultiWeekMatchups is True):
                    teamA = YearNavigator.getTeamById(year, matchup.teamAId)
                    teamB = YearNavigator.getTeamById(year, matchup.teamBId)
                    # add matchup for both teams
                    # add for "A" team
                    modifiedMatchupId = f"{matchup.id}A"
                    modifiedMatchupIdToOwnerIdMap[modifiedMatchupId] = teamA.ownerId
                    teamANames[modifiedMatchupId] = teamA.name
                    teamBNames[modifiedMatchupId] = teamB.name
                    teamAScores[modifiedMatchupId] = matchup.teamAScore
                    teamBScores[modifiedMatchupId] = matchup.teamBScore
                    matchupTypes[modifiedMatchupId] = matchup.matchupType.name
                    weekNumbers[modifiedMatchupId] = week.weekNumber
                    # add for "B" team
                    modifiedMatchupId = f"{matchup.id}B"
                    modifiedMatchupIdToOwnerIdMap[modifiedMatchupId] = teamB.ownerId
                    teamANames[modifiedMatchupId] = teamB.name
                    teamBNames[modifiedMatchupId] = teamA.name
                    teamAScores[modifiedMatchupId] = matchup.teamBScore
                    teamBScores[modifiedMatchupId] = matchup.teamAScore
                    matchupTypes[modifiedMatchupId] = matchup.matchupType.name
                    weekNumbers[modifiedMatchupId] = week.weekNumber

    return [
        ("Team For", teamANames),
        ("Team Against", teamBNames),
        ("Week Number", weekNumbers),
        ("Matchup Type", matchupTypes),
        ("Points For", teamAScores),
        ("Points Against", teamBScores)
    ], modifiedMatchupIdToOwnerIdMap


def allTimeMatchupsStatSheet(league: League, **kwargs) -> tuple[list[tuple[str, dict]], dict[str, str]]:
    allTimeFilters = AllTimeFilters.getForLeague(league, **kwargs.copy())

    allYearMatchupStatSheets: list = list()
    allModifiedMatchupIdToOwnerIdMaps: list = list()
    teamANames: dict[str, str] = dict()
    teamBNames: dict[str, str] = dict()
    teamAScores: dict[str, float | int] = dict()
    teamBScores: dict[str, float | int] = dict()
    matchupTypes: dict[str, str] = dict()
    weekNumbers: dict[str, int] = dict()

    for year in league.years:
        if allTimeFilters.yearNumberStart <= year.yearNumber <= allTimeFilters.yearNumberEnd:
            currentYearMatchupStatSheet, currentModifiedMatchupIdToOwnerIdMap = yearMatchupsStatSheet(year,
                                                                                                      **kwargs.copy())
            allYearMatchupStatSheets.append(currentYearMatchupStatSheet)
            allModifiedMatchupIdToOwnerIdMaps.append(currentModifiedMatchupIdToOwnerIdMap)

    # combine responses into 1 response
    for yearMatchupStatSheet in allYearMatchupStatSheets:
        for title, statDict in yearMatchupStatSheet:
            if title == "Team For":
                teamANames.update(statDict)
            elif title == "Team Against":
                teamBNames.update(statDict)
            elif title == "Week Number":
                weekNumbers.update(statDict)
            elif title == "Matchup Type":
                matchupTypes.update(statDict)
            elif title == "Points For":
                teamAScores.update(statDict)
            elif title == "Points Against":
                teamBScores.update(statDict)
            else:
                raise ValueError(f"Title '{title}' is not valid.")

    combinedModifiedMatchupIdToOwnerIdMap: dict = dict()
    for modifiedMatchupIdToOwnerIdMap in allModifiedMatchupIdToOwnerIdMaps:
        combinedModifiedMatchupIdToOwnerIdMap.update(modifiedMatchupIdToOwnerIdMap)

    return [("Team For", teamANames),
            ("Team Against", teamBNames),
            ("Week Number", weekNumbers),
            ("Matchup Type", matchupTypes),
            ("Points For", teamAScores),
            ("Points Against", teamBScores)], combinedModifiedMatchupIdToOwnerIdMap
