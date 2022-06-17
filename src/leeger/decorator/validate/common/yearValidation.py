from src.leeger.decorator.validate.common import teamValidation, weekValidation
from src.leeger.exception.InvalidYearFormatException import InvalidYearFormatException
from src.leeger.model.Year import Year

"""
Checker Functions

    - Will raise the appropriate exception if an incorrectly-formatted Year is passed.
    - Will do nothing if a properly-formatted Year is passed.

"""


def runAllChecks(year: Year) -> None:
    """
    Runs all checks on the given Year.
    The order in which these are called matters.
    """
    checkAllTypes(year)
    checkAllWeeks(year)
    checkAllTeams(year)
    checkForDuplicateTeams(year)
    checkForDuplicateWeeks(year)
    checkOnlyOneChampionshipWeekInYear(year)
    checkAtLeastOneWeekInYear(year)
    checkWeekNumberingInYear(year)
    checkPlayoffWeekOrderingInYear(year)
    checkAtLeastTwoTeamsInYear(year)
    checkGivenYearHasValidYearNumber(year)
    checkTeamNamesInYear(year)
    checkTeamOwnerIdsInYear(year)
    checkEveryTeamInYearIsInAMatchup(year)


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


def checkAllTypes(year: Year) -> None:
    """
    Runs all checks on the given Year.
    """

    if type(year.yearNumber) != int:
        raise InvalidYearFormatException("yearNumber must be type 'int'.")
    if type(year.teams) != list:
        raise InvalidYearFormatException("teams must be type 'list'.")
    if type(year.weeks) != list:
        raise InvalidYearFormatException("weeks must be type 'list'.")


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


def checkOnlyOneChampionshipWeekInYear(year: Year) -> None:
    """
    Checks that there is a maximum of 1 championship week in the given Year.
    """
    championshipWeekCount = 0
    for week in year.weeks:
        if week.isChampionshipWeek:
            championshipWeekCount += 1
        if championshipWeekCount > 1:
            raise InvalidYearFormatException(
                f"Year {year.yearNumber} has {championshipWeekCount} championship weeks. Maximum is 1.")


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
        raise InvalidYearFormatException(f"First week in year {year.yearNumber} must be 1, not {weekNumbers[0]}.")

    if len(weekNumbers) != weekNumbers[-1]:
        raise InvalidYearFormatException(f"Year {year.yearNumber} does not have week numbers in order (1-n).")


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
                    f"Year {year.yearNumber} has a non-playoff week after a playoff week.")
        if week.isChampionshipWeek:
            haveHadChampionshipWeek = True
        else:
            if haveHadChampionshipWeek:
                raise InvalidYearFormatException(
                    f"Year {year.yearNumber} has a non-championship week after a championship week.")


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
    """
    teamNames = list()
    for team in year.teams:
        teamNames.append(team.name)
    if len(set(teamNames)) != len(teamNames):
        raise InvalidYearFormatException(f"Year {year.yearNumber} has teams with duplicate names.")


def checkTeamOwnerIdsInYear(year: Year) -> None:
    """
    Checks that there are no duplicate owner IDs within the teams.
    """
    teamOwnerIds = [team.ownerId for team in year.teams]
    if len(set(teamOwnerIds)) != len(teamOwnerIds):
        raise InvalidYearFormatException(
            f"Year {year.yearNumber} has teams with the same owner IDs.")


def checkEveryTeamInYearIsInAMatchup(year: Year) -> None:
    """
    Checks that every Team in the year appears in at least 1 matchup.
    """
    teamIds = [team.id for team in year.teams]
    for week in year.weeks:
        for matchup in week.matchups:
            try:
                teamIds.remove(matchup.teamAId)
                teamIds.remove(matchup.teamBId)
            except ValueError:
                pass
    if len(teamIds) != 0:
        raise InvalidYearFormatException(
            f"Year {year.yearNumber} has teams that are not in any matchups. Team IDs not in matchups: {teamIds}")
