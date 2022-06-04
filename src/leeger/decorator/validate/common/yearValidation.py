from src.leeger.decorator.validate.common import teamValidation, weekValidation
from src.leeger.exception.InvalidYearFormatException import InvalidYearFormatException
from src.leeger.model.Year import Year


def checkAllTypes(year: Year) -> None:
    """
    Checks all types that are within the Year object.
    """

    if type(year.yearNumber) != int:
        raise InvalidYearFormatException("Year number must be type 'int'.")
    if type(year.teams) != list:
        raise InvalidYearFormatException("Year teams must be type 'list'.")
    if type(year.weeks) != list:
        raise InvalidYearFormatException("Year weeks must be type 'list'.")

    for team in year.teams:
        teamValidation.checkAllTypes(team)

    for week in year.weeks:
        weekValidation.checkAllTypes(week)


def checkOnlyOneChampionshipWeekInYear(year: Year) -> None:
    """
    Checks that there is a maximum of 1 championship week in the given Year.
    """
    championshipWeekCount = 0
    for week in year.weeks:
        if week.isChampionshipWeek:
            championshipWeekCount += 1
        if championshipWeekCount > 1:
            raise InvalidYearFormatException(f"Year {year.yearNumber} has more than 1 championship week.")


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


def checkWeeksInYearHaveAtLeastOneMatchup(year: Year) -> None:
    """
    Checks that each Week in the given Year have at least one matchup.
    """
    for week in year.weeks:
        weekValidation.checkWeekHasAtLeastOneMatchup(week)


def checkTeamOwnerIdsInYear(year: Year) -> None:
    """
    Checks that there are no duplicate owner IDs within the teams.
    """
    teamOwnerIds = [team.ownerId for team in year.teams]
    if len(set(teamOwnerIds)) != len(teamOwnerIds):
        raise InvalidYearFormatException(
            f"Year {year.yearNumber} has teams with the same owner IDs.")
