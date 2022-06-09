from typing import Callable

from src.leeger.decorator.validate.common import leagueValidation, yearValidation, weekValidation
from src.leeger.model.League import League
from src.leeger.model.Week import Week
from src.leeger.model.Year import Year


def validateLeague(function: Callable) -> Callable:
    """
    It is expected that any function decorated with this will follow these rules:
        - Have a League object as a parameter
    This decorator will take the first League parameter found and use it for all validation
    If a function that is decorated with this has the kwarg "validateLeague" set to False, this validation will not be run.

    The purpose of this decorator is to do some initial checks on the League object to validate that it is correctly formatted.
    """

    def wrapFunction(*args, **kwargs):
        # check if we should run this method
        if "validateLeague" in kwargs and not kwargs["validateLeague"]:
            return function(*args, **kwargs)
        league = None
        for arg in args:
            if type(arg) == League:
                league = arg
                break
        if league is None:
            raise ValueError("No valid League argument given to validate.")
        leagueValidation.runAllChecks(league)
        return function(*args, **kwargs)

    return wrapFunction


def validateYear(function: Callable) -> Callable:
    """
    It is expected that any function decorated with this will follow these rules:
        - Have a Year object as a parameter
    This decorator will take the first Year parameter found and use it for all validation
    If a function that is decorated with this has the kwarg "validateYear" set to False, this validation will not be run.

    The purpose of this decorator is to do some initial checks on the Year object to validate that it is correctly formatted.
    """

    def wrapFunction(*args, **kwargs):
        # check if we should run this method
        if "validateYear" in kwargs and not kwargs["validateYear"]:
            return function(*args, **kwargs)
        year = None
        for arg in args:
            if type(arg) == Year:
                year = arg
                break
        if year is None:
            raise ValueError("No valid Year argument given to validate.")
        yearValidation.runAllChecks(year)
        return function(*args, **kwargs)

    return wrapFunction


def validateWeek(function: Callable) -> Callable:
    """
    It is expected that any function decorated with this will follow these rules:
        - Have a Week object as a parameter
    This decorator will take the first Week parameter found and use it for all validation
    If a function that is decorated with this has the kwarg "validateWeek" set to False, this validation will not be run.

    The purpose of this decorator is to do some initial checks on the Week object to validate that it is correctly formatted.
    """

    def wrapFunction(*args, **kwargs):
        # check if we should run this method
        if "validateWeek" in kwargs and not kwargs["validateWeek"]:
            return function(*args, **kwargs)
        week = None
        for arg in args:
            if type(arg) == Week:
                week = arg
                break
        if week is None:
            raise ValueError("No valid Week argument given to validate.")
        weekValidation.runAllChecks(week)
        return function(*args, **kwargs)

    return wrapFunction
