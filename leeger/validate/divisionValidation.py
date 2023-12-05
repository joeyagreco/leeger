from leeger.exception.InvalidDivisionFormatException import \
    InvalidDivisionFormatException
from leeger.model.league.Division import Division


def runAllChecks(division: Division) -> None:
    """
    Runs all checks on the given Division.
    """
    checkAllTypes(division)


def checkAllTypes(division: Division) -> None:
    """
    Checks all types that are within the Owner object.
    """
    if not isinstance(division.name, str):
        raise InvalidDivisionFormatException("name must be type 'str'.")
