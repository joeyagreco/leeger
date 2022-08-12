from leeger.exception.InvalidLeagueFormatException import InvalidLeagueFormatException
from leeger.model.league.League import League
from leeger.validate import ownerValidation, yearValidation

"""
Checker Functions

    - Will raise the appropriate exception if an incorrectly-formatted League is passed.
    - Will do nothing if a properly-formatted League is passed.

"""


def runAllChecks(league: League) -> None:
    """
    Runs all checks on the given League.
    """
    checkAllTypes(league)
    checkAllOwners(league)
    checkAllYears(league)
    checkForDuplicateOwners(league)
    checkForDuplicateYears(league)
    checkForDuplicateTeams(league)
    checkYearsAreInCorrectOrder(league)
    checkNoDuplicateYearNumbers(league)
    checkNoDuplicateOwnerNames(league)
    checkLeagueHasAtLeastOneYear(league)


def checkAllOwners(league: League) -> None:
    """
    Runs all checks on all Owners.
    """
    for owner in league.owners:
        ownerValidation.runAllChecks(owner)


def checkAllYears(league: League) -> None:
    """
    Runs all checks on all Years.
    """
    for year in league.years:
        yearValidation.runAllChecks(year)


def checkAllTypes(league: League) -> None:
    """
    Checks all types that are within the League object.
    """
    if type(league.name) != str:
        raise InvalidLeagueFormatException("name must be type 'str'.")
    if type(league.owners) != list:
        raise InvalidLeagueFormatException("owners must be type 'list'.")
    if type(league.years) != list:
        raise InvalidLeagueFormatException("years must be type 'list'.")


def checkForDuplicateOwners(league: League) -> None:
    """
    Checks that all Owners are unique instances.
    """
    ownerInstanceIds = list()
    for owner in league.owners:
        if id(owner) in ownerInstanceIds:
            raise InvalidLeagueFormatException("Owners must all be unique instances.")
        else:
            ownerInstanceIds.append(id(owner))


def checkForDuplicateYears(league: League) -> None:
    """
    Checks that all Years are unique instances.
    """
    yearInstanceIds = list()
    for year in league.years:
        if id(year) in yearInstanceIds:
            raise InvalidLeagueFormatException("Years must all be unique instances.")
        else:
            yearInstanceIds.append(id(year))


def checkForDuplicateTeams(league: League) -> None:
    """
    Checks that all Teams within the given League are unique instances.
    """
    teamInstanceIds = list()
    for year in league.years:
        for team in year.teams:
            if id(team) in teamInstanceIds:
                raise InvalidLeagueFormatException("Teams must all be unique instances.")
            else:
                teamInstanceIds.append(id(team))


def checkYearsAreInCorrectOrder(league: League) -> None:
    """
    Checks that the Years are in order from oldest -> most recent years.
    """
    if [year.yearNumber for year in league.years] != sorted([year.yearNumber for year in league.years]):
        raise InvalidLeagueFormatException("Years are not in chronological order (oldest -> newest).")


def checkNoDuplicateYearNumbers(league: League) -> None:
    """
    Checks that all the years in the League have a unique year number.
    """
    if len(set([year.yearNumber for year in league.years])) != len([year.yearNumber for year in league.years]):
        raise InvalidLeagueFormatException("Can only have 1 of each year number within a league.")


def checkNoDuplicateOwnerNames(league: League) -> None:
    """
    Checks that all Owners in the League have a unique name.
    """
    if len(set([owner.name for owner in league.owners])) != len([owner.name for owner in league.owners]):
        raise InvalidLeagueFormatException("All owners must have a unique name.")


def checkLeagueHasAtLeastOneYear(league: League) -> None:
    """
    Checks that the given League has at least 1 Year.
    """
    if len(league.years) == 0:
        raise InvalidLeagueFormatException("League must have at least 1 year.")
