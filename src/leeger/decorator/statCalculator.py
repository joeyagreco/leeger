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
        __checkOnlyTwoTeamsInChampionshipPerYear(league)
        return function(*args, **kwargs)

    return wrapFunction


# Checker functions

def __checkOnlyTwoTeamsInChampionshipPerYear(league: League) -> None:
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
