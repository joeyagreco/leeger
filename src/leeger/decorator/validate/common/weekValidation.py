from src.leeger.decorator.validate.common import matchupValidation
from src.leeger.exception.InvalidWeekFormatException import InvalidWeekFormatException
from src.leeger.model.Week import Week


def runAllChecks(week: Week) -> None:
    """
    Checks all types that are within the Week object.
    """
    checkAllMatchups(week)
    checkAllTypes(week)
    checkWeekHasAtLeastOneMatchup(week)
    checkWeekHasMatchupsWithNoDuplicateTeamIds(week)


def checkAllMatchups(week: Week) -> None:
    """
    Runs all checks on all Weeks.
    """
    for matchup in week.matchups:
        matchupValidation.runAllChecks(matchup)


def checkAllTypes(week: Week) -> None:
    """
    Checks all types that are within the Week object.
    """

    if type(week.weekNumber) != int:
        raise InvalidWeekFormatException("Week number must be type 'int'.")
    if type(week.isPlayoffWeek) != bool:
        raise InvalidWeekFormatException("Week isPlayoffWeek must be type 'bool'.")
    if type(week.isChampionshipWeek) != bool:
        raise InvalidWeekFormatException("Week isChampionshipWeek must be type 'bool'.")
    if type(week.matchups) != list:
        raise InvalidWeekFormatException("Week matchups must be type 'list'.")


def checkWeekHasAtLeastOneMatchup(week: Week) -> None:
    """
    Checks that the given Week has at least one Matchup.
    """
    if len(week.matchups) == 0:
        raise InvalidWeekFormatException(f"Week {week.weekNumber} must have at least 1 matchup.")


def checkWeekHasMatchupsWithNoDuplicateTeamIds(week: Week) -> None:
    """
    Checks that the given Week has Matchups with all unique team IDs.
    we expect to have n unique team IDs where n = the number of matchups in the week * 2
    i.e. A team cannot have 2 Matchups in the same week.
    """
    teamIdsInMatchups = list()
    for matchup in week.matchups:
        teamIdsInMatchups.append(matchup.teamAId)
        teamIdsInMatchups.append(matchup.teamBId)
    numberOfExpectedUniqueTeamIds = len(week.matchups) * 2
    if len(set(teamIdsInMatchups)) != numberOfExpectedUniqueTeamIds:
        raise InvalidWeekFormatException(f"Week {week.weekNumber} has matchups with duplicate team IDs.")
