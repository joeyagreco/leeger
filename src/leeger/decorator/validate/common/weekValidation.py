from src.leeger.decorator.validate.common import matchupValidation
from src.leeger.exception.InvalidWeekFormatException import InvalidWeekFormatException
from src.leeger.model.Week import Week


def runAllChecks(week: Week) -> None:
    """
    Runs all checks on the given Week.
    """
    checkAllTypes(week)
    checkForDuplicateMatchups(week)
    checkAllMatchups(week)
    checkWeekHasAtLeastOneMatchup(week)
    checkWeekHasMatchupsWithNoDuplicateTeamIds(week)
    checkWeekDoesNotHaveMoreThanOneChampionshipMatchup(week)


def checkAllTypes(week: Week) -> None:
    """
    Checks all types that are within the Week object.
    """

    if type(week.matchups) != list:
        raise InvalidWeekFormatException("matchups must be type 'list'.")
    if type(week.weekNumber) != int:
        raise InvalidWeekFormatException("weekNumber must be type 'int'.")


def checkForDuplicateMatchups(week: Week) -> None:
    """
    Checks that all Matchups are unique instances.
    """
    matchupInstanceIds = list()
    for matchup in week.matchups:
        if id(matchup) in matchupInstanceIds:
            raise InvalidWeekFormatException("Matchups must all be unique instances.")
        else:
            matchupInstanceIds.append(id(matchup))


def checkAllMatchups(week: Week) -> None:
    """
    Runs all checks on all Weeks.
    """
    for matchup in week.matchups:
        matchupValidation.runAllChecks(matchup)


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


def checkWeekDoesNotHaveMoreThanOneChampionshipMatchup(week: Week) -> None:
    """
    Checks that the given Week has no more than 1 championship matchup.
    """
    championshipMatchupCount = 0
    for matchup in week.matchups:
        if matchup.isChampionshipMatchup:
            championshipMatchupCount += 1
    if championshipMatchupCount > 1:
        raise InvalidWeekFormatException(
            f"Week {week.weekNumber} has {championshipMatchupCount} championship matchups. Maximum is 1.")
