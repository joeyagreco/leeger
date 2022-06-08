from src.leeger.exception.InvalidOwnerFormatException import InvalidOwnerFormatException
from src.leeger.model.Owner import Owner


def runAllChecks(owner: Owner) -> None:
    """
    Checks all types that are within the Owner object.
    """
    checkAllTypes(owner)


def checkAllTypes(owner: Owner) -> None:
    """
    Checks all types that are within the Owner object.
    """
    if type(owner.name) != str:
        raise InvalidOwnerFormatException("Owner name must be type 'str'.")
