from leeger.exception.InvalidOwnerFormatException import InvalidOwnerFormatException
from leeger.model.league.Owner import Owner


def runAllChecks(owner: Owner) -> None:
    """
    Runs all checks on the given Owner.
    """
    checkAllTypes(owner)


def checkAllTypes(owner: Owner) -> None:
    """
    Checks all types that are within the Owner object.
    """
    if not isinstance(owner.name, str):
        raise InvalidOwnerFormatException("name must be type 'str'.")
