from leeger.exception.InvalidTeamFormatException import InvalidTeamFormatException
from leeger.model.league.Team import Team


def runAllChecks(team: Team) -> None:
    """
    Runs all checks on the given Team.
    """
    checkAllTypes(team)


def checkAllTypes(team: Team) -> None:
    """
    Checks all types that are within the Team object.
    """

    if not isinstance(team.ownerId, str):
        raise InvalidTeamFormatException("ownerId must be type 'str'.")
    if not isinstance(team.name, str):
        raise InvalidTeamFormatException("name must be type 'str'.")
    if not isinstance(team.divisionId, (str, type(None))):
        raise InvalidTeamFormatException("divisionId must be 'None' or type 'str'.")
