from src.leeger.decorator.validate.common import ownerValidation, yearValidation
from src.leeger.exception.InvalidLeagueFormatException import InvalidLeagueFormatException
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
