from leeger.enum.MatchupType import MatchupType
from leeger.exception.InvalidWeekFormatException import InvalidWeekFormatException
from leeger.model.league.Week import Week
from leeger.validate import matchupValidation


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
    checkWeekWithPlayoffOrChampionshipMatchupDoesNotHaveRegularSeasonMatchup(week)
    checkMultiWeekMatchupsWithSameIdAreOnlyInOneMatchupPerWeek(week)


def checkAllTypes(week: Week) -> None:
    """
    Checks all types that are within the Week object.
    """

    if not isinstance(week.matchups, list):
        raise InvalidWeekFormatException("matchups must be type 'list'.")
    if not isinstance(week.weekNumber, int):
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
        raise InvalidWeekFormatException(
            f"Week {week.weekNumber} has matchups with duplicate team IDs."
        )


def checkWeekDoesNotHaveMoreThanOneChampionshipMatchup(week: Week) -> None:
    """
    Checks that the given Week has no more than 1 championship matchup.
    """
    championshipMatchupCount = 0
    for matchup in week.matchups:
        if matchup.matchupType == MatchupType.CHAMPIONSHIP:
            championshipMatchupCount += 1
    if championshipMatchupCount > 1:
        raise InvalidWeekFormatException(
            f"Week {week.weekNumber} has {championshipMatchupCount} championship matchups. Maximum is 1."
        )


def checkWeekWithPlayoffOrChampionshipMatchupDoesNotHaveRegularSeasonMatchup(week: Week) -> None:
    """
    Checks that the given Week has no Regular Season Matchups IF it has a Playoff or Championship Matchup.
    """
    playoffOrChampionshipMatchupCount = 0
    regularSeasonMatchupCount = 0
    for matchup in week.matchups:
        if matchup.matchupType in (MatchupType.PLAYOFF, MatchupType.CHAMPIONSHIP):
            playoffOrChampionshipMatchupCount += 1
        elif matchup.matchupType == MatchupType.REGULAR_SEASON:
            regularSeasonMatchupCount += 1
    if regularSeasonMatchupCount > 0 and playoffOrChampionshipMatchupCount > 0:
        raise InvalidWeekFormatException(
            f"Week {week.weekNumber} has regular season matchups and playoff/championship matchups in the same week."
        )


def checkMultiWeekMatchupsWithSameIdAreOnlyInOneMatchupPerWeek(week: Week):
    """
    Checks that multi-week matchup IDs are only in 1 matchup per week.
    """
    multiWeekMatchupIds = list()
    for matchup in week.matchups:
        if matchup.multiWeekMatchupId is not None:
            if matchup.multiWeekMatchupId in multiWeekMatchupIds:
                raise InvalidWeekFormatException(
                    f"Week {week.weekNumber} has the multi-week matchup ID '{matchup.multiWeekMatchupId}' in multiple matchups."
                )
            multiWeekMatchupIds.append(matchup.multiWeekMatchupId)
