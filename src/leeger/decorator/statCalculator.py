from typing import Callable

from src.leeger.exception.InvalidYearFormatException import InvalidYearFormatException
from src.leeger.model.League import League


def statCalculator(function: Callable) -> Callable:
    """
    It is expected that any function decorated with this will follow these rules:
        - Be decorated as a @classmethod
        - Have a League object as the first parameter

    The purpose of this decorator is to do some initial checks on the League object BEFORE any stats are calculated.
    """

    def wrapFunction(*args, **kwargs):
        league = args[1]
        __runAllChecks(league)
        return function(*args, **kwargs)

    return wrapFunction


def __runAllChecks(league) -> None:
    """
    Runs all checks on given League.
    The order in which these are called matters.
    """
    __checkOnlyOneChampionshipWeekPerYear(league)
    __checkAtLeastOneWeekPerYear(league)
    __checkWeekNumbering(league)
    __checkPlayoffWeekOrdering(league)
    __checkAtLeastTwoTeamsPerYear(league)
    __checkAllYearsHaveValidYearNumbers(league)


"""
Checker Functions

    - Will raise the appropriate exception if an incorrectly-formatted League is passed.
    - Will do nothing if a properly-formatted League is passed.

"""


def __checkOnlyOneChampionshipWeekPerYear(league: League) -> None:
    """
    Checks that there is a maximum of 1 championship week per year.
    """
    for year in league.years:
        championshipWeekCount = 0
        for week in year.weeks:
            if week.isChampionshipWeek:
                championshipWeekCount += 1
            if championshipWeekCount > 1:
                raise InvalidYearFormatException(f"Year {year.yearNumber} has more than 1 championship week.")


def __checkAtLeastOneWeekPerYear(league: League) -> None:
    """
    Checks that there is a minimum of 1 week per year.
    """
    for year in league.years:
        if len(year.weeks) == 0:
            raise InvalidYearFormatException(f"Year {year.yearNumber} does not have at least 1 week.")


def __checkWeekNumbering(league: League) -> None:
    """
    Checks that:
        - Each year has no duplicate week numbers
        - First week number of every year is 1
        - Each year has weeks numbered 1-n in order
    """
    for year in league.years:
        weekNumbers = list()
        for week in year.weeks:
            weekNumbers.append(week.weekNumber)

        if len(set(weekNumbers)) != len(weekNumbers):
            raise InvalidYearFormatException(f"Year {year.yearNumber} has duplicate week numbers.")

        if weekNumbers[0] != 1:
            raise InvalidYearFormatException(f"First week in year {year.yearNumber} must be 1, not {weekNumbers[0]}.")

        if len(weekNumbers) != weekNumbers[-1]:
            raise InvalidYearFormatException(f"Year {year.yearNumber} does not have week numbers in order (1-n).")


def __checkPlayoffWeekOrdering(league: League) -> None:
    """
    Checks that:
        - There are no non-playoff weeks after a playoff week
        - There are no non-championship weeks after a championship week
    """
    for year in league.years:
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


def __checkAtLeastTwoTeamsPerYear(league: League) -> None:
    """
    Checks that there is at least 2 teams per year.
    """
    for year in league.years:
        if len(year.teams) < 2:
            raise InvalidYearFormatException(f"Year {year.yearNumber} needs at least 2 teams.")


def __checkAllYearsHaveValidYearNumbers(league: League) -> None:
    """
    Checks that each year has a valid year number (1920-2XXX)
    1920 is the year the NFL was founded, so we'll assume nobody was playing fantasy football before then.
    """
    for year in league.years:
        if year.yearNumber < 1920 or year.yearNumber > 2999:
            raise InvalidYearFormatException(f"Year {year.yearNumber} is not in range 1920-2XXX.")
