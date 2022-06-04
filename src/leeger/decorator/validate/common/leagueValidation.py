from src.leeger.decorator.validate.common import ownerValidation, yearValidation
from src.leeger.exception.InvalidLeagueFormatException import InvalidLeagueFormatException
from src.leeger.exception.InvalidYearFormatException import InvalidYearFormatException
from src.leeger.model.League import League


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

    for owner in league.owners:
        ownerValidation.checkAllTypes(owner)

    for year in league.years:
        yearValidation.checkAllTypes(year)


def checkOnlyOneChampionshipWeekPerYear(league: League) -> None:
    """
    Checks that there is a maximum of 1 championship week per year.
    """
    for year in league.years:
        yearValidation.checkOnlyOneChampionshipWeekInYear(year)


def checkAtLeastOneWeekPerYear(league: League) -> None:
    """
    Checks that there is a minimum of 1 week per Year.
    """
    for year in league.years:
        yearValidation.checkAtLeastOneWeekInYear(year)


def checkWeekNumberingInLeague(league: League) -> None:
    """
    Checks that:
        - Each year has no duplicate week numbers
        - First week number of every Year is 1
        - Each Year has weeks numbered 1-n in order
    """
    for year in league.years:
        yearValidation.checkWeekNumberingInYear(year)


def checkPlayoffWeekOrderingInLeague(league: League) -> None:
    """
    Checks that:
        - There are no non-playoff weeks after a playoff week
        - There are no non-championship weeks after a championship week
    """
    for year in league.years:
        yearValidation.checkPlayoffWeekOrderingInYear(year)


def checkAtLeastTwoTeamsPerYear(league: League) -> None:
    """
    Checks that there is at least 2 teams per year.
    """
    for year in league.years:
        yearValidation.checkAtLeastTwoTeamsInYear(year)


def checkAllYearsHaveValidYearNumbers(league: League) -> None:
    """
    Checks that each year has a valid year number (1920-2XXX)
    1920 is the year the NFL was founded, so we'll assume nobody was playing fantasy football before then.
    """
    for year in league.years:
        yearValidation.checkGivenYearHasValidYearNumber(year)


def checkYearsAreInCorrectOrder(league: League) -> None:
    """
    Checks that the Years are in order from oldest -> most recent years.
    """
    if [year.yearNumber for year in league.years] != sorted([year.yearNumber for year in league.years]):
        raise InvalidLeagueFormatException(f"Years are not in chronological order (oldest -> newest).")


def checkNoDuplicateYearNumbers(league: League) -> None:
    """
    Checks that all the years in the League have a unique year number.
    """
    if len(set([year.yearNumber for year in league.years])) != len([year.yearNumber for year in league.years]):
        raise InvalidLeagueFormatException(f"Can only have 1 of each year number within a league.")


def checkTeamOwnerIds(league: League) -> None:
    """
    Checks that:
        - There are no duplicate owner IDs within the teams
        - Each team in a year has an owner ID that matches an Owner ID that is in the League's owners list as an ID
    """
    # TODO: this should be done at the year level as well, but the Year model does not have access to the owner IDs as that is on the League model level.
    for year in league.years:
        teamOwnerIds = list()
        for team in year.teams:
            teamOwnerIds.append(team.ownerId)
        if len(set(teamOwnerIds)) != len(teamOwnerIds):
            raise InvalidYearFormatException(f"Year {year.yearNumber} has teams with the same owner IDs.")
        for owner in league.owners:
            if owner.id in teamOwnerIds:
                teamOwnerIds.remove(owner.id)
        if len(teamOwnerIds) > 0:
            raise InvalidYearFormatException(
                f"Year {year.yearNumber} has teams with owner IDs that do not match the League's owner IDs: {teamOwnerIds}.")


def checkTeamNamesInLeague(league: League) -> None:
    """
    Checks that each team in each Year has a unique name
    """
    for year in league.years:
        yearValidation.checkTeamNamesInYear(year)
