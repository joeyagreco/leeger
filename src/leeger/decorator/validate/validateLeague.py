from typing import Callable

from src.leeger.decorator.validate.common import leagueValidation
from src.leeger.exception.InvalidMatchupFormatException import InvalidMatchupFormatException
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
    leagueValidation.checkAtLeastTwoTeamsPerYear(league)
    leagueValidation.checkAllYearsHaveValidYearNumbers(league)
    leagueValidation.checkYearsAreInCorrectOrder(league)
    leagueValidation.checkNoDuplicateYearNumbers(league)
    leagueValidation.checkTeamOwnerIds(league)
    leagueValidation.checkTeamNamesInLeague(league)
    leagueValidation.checkWeeksInYearsHaveAtLeastOneMatchup(league)
    __checkMatchupTeamIdsMatchYearTeamIds(league)
    __checkPlayoffWeekWithTiedScoresHasATiebreakerDefined(league)


"""
Checker Functions

    - Will raise the appropriate exception if an incorrectly-formatted League is passed.
    - Will do nothing if a properly-formatted League is passed.

"""


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
