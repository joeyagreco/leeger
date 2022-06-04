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
    Order matters.
    """
    __checkOnlyOneChampionshipWeekPerYear(league)
    __checkAtLeastOneWeekPerYear(league)
    __checkWeekNumbering(league)


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
    Checks that each week is numbered 1-n.
    NOTE: This check assumes that there is at least 1 week in every year, as this is done by another check.
    """
    for year in league.years:
        weekNumbers = list()
        for week in year.weeks:
            weekNumbers.append(week.weekNumber)

        weekNumbers.sort()

        if len(set(weekNumbers)) != len(weekNumbers):
            raise InvalidYearFormatException(f"Year {year.yearNumber} has duplicate week numbers.")

        if weekNumbers[0] != 1:
            raise InvalidYearFormatException(f"First week in year {year.yearNumber} must be 1, not {weekNumbers[0]}.")

        if len(weekNumbers) != weekNumbers[-1]:
            raise InvalidYearFormatException(f"Year {year.yearNumber} does not have week numbers in order (1-n).")
