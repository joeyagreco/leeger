from leeger.exception.InvalidLeagueFormatException import InvalidLeagueFormatException
from leeger.model.league import LeagueSettings


def runAllChecks(leagueSettings: LeagueSettings) -> None:
    """
    Runs all checks on the given LeagueSettings.
    """
    checkAllTypes(leagueSettings)


def checkAllTypes(leagueSettings: LeagueSettings) -> None:
    """
    Checks all types that are within the LeagueSettings object.
    """
    if not isinstance(leagueSettings.leagueMedianGames, bool):
        raise InvalidLeagueFormatException("leagueMedianGames must be type 'bool'.")
