from functools import lru_cache

from leeger.exception.InvalidYearFormatException import InvalidYearFormatException
from leeger.model.league import Matchup, YearSettings
from leeger.model.league.Year import Year
from leeger.util.navigator import YearNavigator
from leeger.validate import (
    divisionValidation,
    teamValidation,
    weekValidation,
    yearSettingsValidation,
)


@lru_cache(maxsize=None)
def runAllChecks(year: Year) -> None:
    """
    Runs all checks on the given Year.
    The order in which these are called matters.
    """
    checkAllTypes(year)
    checkYearSettings(year)
    checkAllWeeks(year)
    checkAllTeams(year)
    checkAllDivisions(year)
    checkForDuplicateTeams(year)
    checkForDuplicateWeeks(year)
    checkForDuplicateDivisions(year)
    checkAtLeastOneWeekInYear(year)
    checkWeekNumberingInYear(year)
    checkPlayoffWeekOrderingInYear(year)
    checkAtLeastTwoTeamsInYear(year)
    checkGivenYearHasValidYearNumber(year)
    checkTeamNamesInYear(year)
    checkDivisionNamesInYear(year)
    checkTeamOwnerIdsInYear(year)
    checkEveryTeamInYearIsInAMatchup(year)
    checkMultiWeekMatchupsAreInConsecutiveWeeks(year)
    checkMultiWeekMatchupsAreInMoreThanOneWeekOrAreNotTheMostRecentWeek(year)
    checkMultiWeekMatchupsWithSameIdHaveSameMatchupType(year)
    checkMultiWeekMatchupsWithSameIdHaveSameTeamIds(year)
    checkMultiWeekMatchupsWithSameIdHaveSameTiebreakers(year)


def checkYearSettings(year: Year) -> None:
    """
    Runs all checks on the given Year's YearSettings.
    """
    yearSettingsValidation.runAllChecks(year.yearSettings)


def checkAllWeeks(year: Year) -> None:
    """
    Runs all checks on all Weeks.
    """
    for week in year.weeks:
        weekValidation.runAllChecks(week)


def checkAllTeams(year: Year) -> None:
    """
    Runs all checks on all Teams.
    """
    for team in year.teams:
        teamValidation.runAllChecks(team)


def checkAllDivisions(year: Year) -> None:
    """
    Runs all checks on all Divisions.
    """
    for division in year.divisions:
        divisionValidation.runAllChecks(division)


def checkAllTypes(year: Year) -> None:
    """
    Runs all checks on the given Year.
    """

    if not isinstance(year.yearNumber, int):
        raise InvalidYearFormatException("yearNumber must be type 'int'.")
    if not isinstance(year.teams, list):
        raise InvalidYearFormatException("teams must be type 'list'.")
    if not isinstance(year.weeks, list):
        raise InvalidYearFormatException("weeks must be type 'list'.")
    if not isinstance(year.divisions, list):
        raise InvalidYearFormatException("divisions must be type 'list'.")
    if not isinstance(year.yearSettings, YearSettings):
        raise InvalidYearFormatException("yearSettings must be type 'YearSettings'.")


def checkForDuplicateTeams(year: Year) -> None:
    """
    Checks that all Teams are unique instances.
    """
    teamInstanceIds = list()
    for team in year.teams:
        if id(team) in teamInstanceIds:
            raise InvalidYearFormatException("Teams must all be unique instances.")
        else:
            teamInstanceIds.append(id(team))


def checkForDuplicateWeeks(year: Year) -> None:
    """
    Checks that all Weeks are unique instances.
    """
    weekInstanceIds = list()
    for week in year.weeks:
        if id(week) in weekInstanceIds:
            raise InvalidYearFormatException("Weeks must all be unique instances.")
        else:
            weekInstanceIds.append(id(week))


def checkForDuplicateDivisions(year: Year) -> None:
    """
    Checks that all Weeks are unique instances.
    """
    divisionInstanceIds = list()
    for division in year.divisions:
        if id(division) in divisionInstanceIds:
            raise InvalidYearFormatException("Divisions must all be unique instances.")
        else:
            divisionInstanceIds.append(id(division))


def checkDivisionNamesInYear(year: Year) -> None:
    """
    Checks that each division in the given Year has a unique name
    Counts names as too similar if they are the same
        - when whitespace is removed
        - when case is uniform
    """
    if len(set([division.name for division in year.divisions])) != len(
        [division.name for division in year.divisions]
    ):
        raise InvalidYearFormatException(
            f"Year {year.yearNumber} has divisions with duplicate names."
        )
    if len(set([division.name.strip().upper() for division in year.divisions])) != len(
        [division.name for division in year.divisions]
    ):
        raise InvalidYearFormatException(
            f"Year {year.yearNumber} has divisions with very similar names."
        )


def checkAtLeastOneWeekInYear(year: Year) -> None:
    """
    Checks that there is a minimum of 1 week in the given Year.
    """
    if len(year.weeks) == 0:
        raise InvalidYearFormatException(f"Year {year.yearNumber} does not have at least 1 week.")


def checkWeekNumberingInYear(year: Year) -> None:
    """
    Checks that:
        - The given Year has no duplicate week numbers
        - First week number of the given Year is 1
        - The given Year has weeks numbered 1-n in order
    """
    weekNumbers = list()
    for week in year.weeks:
        weekNumbers.append(week.weekNumber)

    if len(set(weekNumbers)) != len(weekNumbers):
        raise InvalidYearFormatException(f"Year {year.yearNumber} has duplicate week numbers.")

    if weekNumbers[0] != 1:
        raise InvalidYearFormatException(
            f"First week in year {year.yearNumber} must be 1, not {weekNumbers[0]}."
        )

    if len(weekNumbers) != weekNumbers[-1]:
        raise InvalidYearFormatException(
            f"Year {year.yearNumber} does not have week numbers in order (1-n)."
        )


def checkPlayoffWeekOrderingInYear(year: Year) -> None:
    """
    Checks that:
        - There are no non-playoff weeks after a playoff week
        - There are no non-championship weeks after a championship week
    """

    haveHadPlayoffWeek = False
    haveHadChampionshipWeek = False
    for week in year.weeks:
        if week.isPlayoffWeek:
            haveHadPlayoffWeek = True
        else:
            if haveHadPlayoffWeek:
                raise InvalidYearFormatException(
                    f"Year {year.yearNumber} has a non-playoff week after a playoff week."
                )
        if week.isChampionshipWeek:
            haveHadChampionshipWeek = True
        else:
            if haveHadChampionshipWeek:
                raise InvalidYearFormatException(
                    f"Year {year.yearNumber} has a non-championship week after a championship week."
                )


def checkAtLeastTwoTeamsInYear(year: Year) -> None:
    """
    Checks that there is at least 2 teams in the given Year.
    """
    if len(year.teams) < 2:
        raise InvalidYearFormatException(f"Year {year.yearNumber} needs at least 2 teams.")


def checkGivenYearHasValidYearNumber(year: Year) -> None:
    """
    Checks that the given Year has a valid year number (1920-2XXX)
    1920 is the year the NFL was founded, so we'll assume nobody was playing fantasy football before then.
    """
    if year.yearNumber < 1920 or year.yearNumber > 2999:
        raise InvalidYearFormatException(f"Year {year.yearNumber} is not in range 1920-2XXX.")


def checkTeamNamesInYear(year: Year) -> None:
    """
    Checks that each team in the given Year has a unique name
    Counts names as too similar if they are the same
        - when whitespace is removed
        - when case is uniform
    """
    if len(set([team.name for team in year.teams])) != len([team.name for team in year.teams]):
        raise InvalidYearFormatException(f"Year {year.yearNumber} has teams with duplicate names.")
    if len(set([team.name.strip().upper() for team in year.teams])) != len(
        [team.name for team in year.teams]
    ):
        raise InvalidYearFormatException(
            f"Year {year.yearNumber} has teams with very similar names."
        )


def checkTeamOwnerIdsInYear(year: Year) -> None:
    """
    Checks that there are no duplicate owner IDs within the teams.
    """
    teamOwnerIds = [team.ownerId for team in year.teams]
    if len(set(teamOwnerIds)) != len(teamOwnerIds):
        raise InvalidYearFormatException(
            f"Year {year.yearNumber} has teams with the same owner IDs."
        )


def checkEveryTeamInYearIsInAMatchup(year: Year) -> None:
    """
    Checks that every Team in the year appears in at least 1 matchup.
    """
    from leeger.util.navigator.YearNavigator import YearNavigator

    teamIds = YearNavigator.getAllTeamIds(year)
    for week in year.weeks:
        for matchup in week.matchups:
            try:
                teamIds.remove(matchup.teamAId)
            except ValueError:
                pass
            try:
                teamIds.remove(matchup.teamBId)
            except ValueError:
                pass
    if len(teamIds) != 0:
        raise InvalidYearFormatException(
            f"Year {year.yearNumber} has teams that are not in any matchups. Team IDs not in matchups: {teamIds}"
        )


def checkMultiWeekMatchupsAreInConsecutiveWeeks(year: Year):
    """
    Checks that any multi-week matchups are in consecutive weeks.
    """
    weekNumberToMultiWeekMatchupIdListMap: dict[int, list[str]] = dict()
    completedMultiWeekMatchupIds = list()

    for i, week in enumerate(year.weeks):
        weekNumberToMultiWeekMatchupIdListMap[week.weekNumber] = list()
        for matchup in week.matchups:
            mwmid = matchup.multiWeekMatchupId
            if mwmid is not None:
                # multi-week matchup
                weekNumberToMultiWeekMatchupIdListMap[week.weekNumber].append(mwmid)

        # check if previous week has any multi-week matchup IDs that this one has
        # if not, the multi-week matchup is done, and any further usage of this ID is not allowed

        # skip first week since we can't end or invalidate any multi-week matchups after just 1 week
        if i != 0:
            previousWeekMWMIDs = weekNumberToMultiWeekMatchupIdListMap[week.weekNumber - 1]
            currentWeekMWMIDs = weekNumberToMultiWeekMatchupIdListMap[week.weekNumber]

            for mwmid in previousWeekMWMIDs:
                if mwmid not in currentWeekMWMIDs:
                    # this multi-week matchup is done, add to list of completed IDs
                    completedMultiWeekMatchupIds.append(mwmid)
            for mwmid in currentWeekMWMIDs:
                if mwmid in completedMultiWeekMatchupIds:
                    raise InvalidYearFormatException(
                        f"Year {year.yearNumber} has multi-week matchups with ID '{mwmid}' that are not in consecutive weeks."
                    )


def checkMultiWeekMatchupsAreInMoreThanOneWeekOrAreNotTheMostRecentWeek(year: Year):
    """
    Checks that any multi-week matchups in a year appear in more than 1 week.
    The exception is if the multi-week matchup is in the last (most recent) week of the year.
    That week is allowed to have the only occurrence of a multi-week matchup ID since there could be another week coming in the future with that ID.
    """
    multiWeekMatchupIdToCountAndMostRecentWeekMap: dict[str, list[int, bool]] = dict()
    # will hold an occurrence count and a boolean value of whether this ID was found in the most recent week of the year
    # will look something like:
    # {
    #   "someId": (1, False),
    #   "someOtherId": (3, True)
    # }

    for i, week in enumerate(year.weeks):
        isMostRecentWeekInYear = i == (len(year.weeks) - 1)
        for matchup in week.matchups:
            mwmid = matchup.multiWeekMatchupId
            if mwmid is not None:
                if mwmid in multiWeekMatchupIdToCountAndMostRecentWeekMap.keys():
                    multiWeekMatchupIdToCountAndMostRecentWeekMap[mwmid][0] += 1
                else:
                    multiWeekMatchupIdToCountAndMostRecentWeekMap[mwmid] = [
                        1,
                        isMostRecentWeekInYear,
                    ]

    for mwmid, countAndMostRecentWeek in multiWeekMatchupIdToCountAndMostRecentWeekMap.items():
        count, isMostRecentWeek = countAndMostRecentWeek
        if count == 1 and not isMostRecentWeek:
            raise InvalidYearFormatException(
                f"Year {year.yearNumber} has multi-week matchup with ID '{mwmid}' that only occurs once and is not the most recent week."
            )


def checkMultiWeekMatchupsWithSameIdHaveSameMatchupType(year: Year):
    """
    Checks that all multi-week matchups with the same ID have the same MatchupType.
    """
    multiWeekMatchupIdToMatchupListMap: dict[
        str, list[Matchup]
    ] = YearNavigator.getAllMultiWeekMatchups(year)

    for mwmid, matchupList in multiWeekMatchupIdToMatchupListMap.items():
        if len(matchupList) > 0:
            if not all(
                matchup.matchupType == matchupList[0].matchupType for matchup in matchupList
            ):
                raise InvalidYearFormatException(
                    f"Multi-week matchups with ID '{mwmid}' do not all have the same matchup type."
                )


def checkMultiWeekMatchupsWithSameIdHaveSameTeamIds(year: Year):
    """
    Checks that all multi-week matchups with the same ID have the same team A and team B
    """
    multiWeekMatchupIdToMatchupListMap: dict[
        str, list[Matchup]
    ] = YearNavigator.getAllMultiWeekMatchups(year)

    for mwmid, matchupList in multiWeekMatchupIdToMatchupListMap.items():
        if len(matchupList) > 0:
            if not all(
                matchup.teamAId == matchupList[0].teamAId
                and matchup.teamBId == matchupList[0].teamBId
                for matchup in matchupList
            ):
                raise InvalidYearFormatException(
                    f"Multi-week matchups with ID '{mwmid}' do not all have the same teamA and teamB."
                )


def checkMultiWeekMatchupsWithSameIdHaveSameTiebreakers(year: Year):
    """
    Checks that all multi-week matchups with the same ID have the same tiebreakers
    """
    multiWeekMatchupIdToMatchupListMap: dict[
        str, list[Matchup]
    ] = YearNavigator.getAllMultiWeekMatchups(year)

    for mwmid, matchupList in multiWeekMatchupIdToMatchupListMap.items():
        if len(matchupList) > 0:
            if not all(
                matchup.teamAHasTiebreaker == matchupList[0].teamAHasTiebreaker
                and matchup.teamBHasTiebreaker == matchupList[0].teamBHasTiebreaker
                for matchup in matchupList
            ):
                raise InvalidYearFormatException(
                    f"Multi-week matchups with ID '{mwmid}' do not all have the same tiebreakers."
                )

def checkIfAnyTeamIsInADivisionThatAllTeamsAreInADivision(year: Year):
    # TODO: test this
    """
    Checks that if at least 1 team is in a division, all teams are in a division.
    """
    allDivisionIds = [team.divisionId for team in year.teams]
    
    # Check if all teams have a division ID
    if not (all(isinstance(divisionId, str) for divisionId in allDivisionIds) or all(divisionId is None for divisionId in allDivisionIds)):
        raise InvalidYearFormatException(f"Only some teams in year f{year.yearNumber} have a divisionId.")
    
    
