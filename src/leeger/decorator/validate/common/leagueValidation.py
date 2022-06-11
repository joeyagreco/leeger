from src.leeger.decorator.validate.common import ownerValidation, yearValidation
from src.leeger.exception.InvalidLeagueFormatException import InvalidLeagueFormatException
from src.leeger.model.League import League

"""
Checker Functions

    - Will raise the appropriate exception if an incorrectly-formatted League is passed.
    - Will do nothing if a properly-formatted League is passed.

"""


def runAllChecks(league: League) -> None:
    """
    Runs all checks on the given League.
    The order in which these are called matters.
    """
    checkAllOwners(league)
    checkAllYears(league)
    checkAllTypes(league)
    checkForDuplicateOwners(league)
    checkForDuplicateYears(league)
    checkYearsAreInCorrectOrder(league)
    checkNoDuplicateYearNumbers(league)
    checkNumberOfOwnersEqualsTheNumberOfTeams(league)


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
        raise InvalidLeagueFormatException("League name must be type 'str'.")
    if type(league.owners) != list:
        raise InvalidLeagueFormatException("League owners must be type 'list'.")
    if type(league.years) != list:
        raise InvalidLeagueFormatException("League years must be type 'list'.")


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


def checkNumberOfOwnersEqualsTheNumberOfTeams(league: League) -> None:
    """
    Checks that the number of Owners in a League matches the number of Teams.
    """
    for year in league.years:
        if len(year.teams) != len(league.owners):
            raise InvalidLeagueFormatException(
                f"Number of owners in a League must match the number of Teams in a year. (League has {len(league.owners)} owners, Year {year.yearNumber} has {len(year.teams)} team/s)")
