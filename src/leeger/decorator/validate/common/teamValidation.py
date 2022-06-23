from src.leeger.exception.InvalidTeamFormatException import InvalidTeamFormatException
from src.leeger.model.league.Team import Team


def runAllChecks(team: Team) -> None:
    """
    Runs all checks on the given Team.
    """
    checkAllTypes(team)


def checkAllTypes(team: Team) -> None:
    """
    Checks all types that are within the Team object.
    """

    if type(team.ownerId) != str:
        raise InvalidTeamFormatException("ownerId must be type 'str'.")
    if type(team.name) != str:
        raise InvalidTeamFormatException("name must be type 'str'.")
