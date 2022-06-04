from typing import Callable

from src.leeger.decorator.validate.common import leagueValidation
from src.leeger.exception.InvalidMatchupFormatException import InvalidMatchupFormatException
from src.leeger.exception.InvalidWeekFormatException import InvalidWeekFormatException
from src.leeger.exception.InvalidYearFormatException import InvalidYearFormatException
from src.leeger.model.League import League


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
        __runAllChecks(league)
        return function(*args, **kwargs)

    return wrapFunction


def __runAllChecks(league) -> None:
    """
    Runs all checks on given League.
    The order in which these are called matters.
    """
    leagueValidation.checkAllTypes(league)
    leagueValidation.checkOnlyOneChampionshipWeekPerYear(league)
    leagueValidation.checkAtLeastOneWeekPerYear(league)
    leagueValidation.checkWeekNumberingInLeague(league)
    leagueValidation.checkPlayoffWeekOrderingInLeague(league)
    __checkAtLeastTwoTeamsPerYear(league)
    __checkAllYearsHaveValidYearNumbers(league)
    __checkYearsAreInCorrectOrder(league)
    __checkNoDuplicateYearNumbers(league)
    __checkTeamOwnerIds(league)
    __checkTeamNames(league)
    __checkWeekHasAtLeastOneMatchup(league)
    __checkMatchupTeamIdsMatchYearTeamIds(league)
    __checkPlayoffWeekWithTiedScoresHasATiebreakerDefined(league)


"""
Checker Functions

    - Will raise the appropriate exception if an incorrectly-formatted League is passed.
    - Will do nothing if a properly-formatted League is passed.

"""


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


def __checkYearsAreInCorrectOrder(league: League) -> None:
    """
    Checks that the years are in order from oldest -> most recent years.
    """
    if [year.yearNumber for year in league.years] != sorted([year.yearNumber for year in league.years]):
        raise InvalidYearFormatException(f"Years are not in chronological order (oldest -> newest).")


def __checkNoDuplicateYearNumbers(league: League) -> None:
    """
    Checks that all the years in the League have a unique year number.
    """
    if len(set([year.yearNumber for year in league.years])) != len([year.yearNumber for year in league.years]):
        raise InvalidYearFormatException(f"Can only have 1 of each year number within a league.")


def __checkTeamOwnerIds(league: League) -> None:
    """
    Checks that:
        - There are no duplicate owner IDs within the teams
        - Each team in a year has an owner ID that matches an Owner ID that is in the League's owners list as an ID
    """
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


def __checkTeamNames(league: League) -> None:
    """
    Checks that each team in a year has a unique name
    """
    for year in league.years:
        teamNames = list()
        for team in year.teams:
            teamNames.append(team.name)
        if len(set(teamNames)) != len(teamNames):
            raise InvalidYearFormatException(f"Year {year.yearNumber} has teams with duplicate names.")


def __checkWeekHasAtLeastOneMatchup(league: League) -> None:
    """
    Checks that each week has at least one matchup.
    """
    for year in league.years:
        for week in year.weeks:
            if len(week.matchups) == 0:
                raise InvalidWeekFormatException(f"Year {year.yearNumber} must have at least 1 matchup.")


def __checkMatchupTeamIdsMatchYearTeamIds(league: League) -> None:
    """
    Checks that each team ID in a matchup match that year's team IDs.
    """
    for year in league.years:
        teamIds = [team.id for team in year.teams]
        for week in year.weeks:
            for matchup in week.matchups:
                if matchup.teamAId not in teamIds or matchup.teamBId not in teamIds:
                    raise InvalidMatchupFormatException(
                        f"Year {year.yearNumber} Week {week.weekNumber} has a matchup with team IDs that do not match the Year's team IDs.")


def __checkPlayoffWeekWithTiedScoresHasATiebreakerDefined(league: League) -> None:
    """
    Checks that a playoff week that has a tied score has a tiebreaker defined.
    """
    for year in league.years:
        for week in year.weeks:
            if week.isPlayoffWeek:
                for matchup in week.matchups:
                    if matchup.teamAScore == matchup.teamBScore and not matchup.teamAHasTiebreaker and not matchup.teamBHasTiebreaker:
                        raise InvalidMatchupFormatException(
                            f"Week {week.weekNumber} is a tied playoff week without a tiebreaker chosen.")
