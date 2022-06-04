from src.leeger.exception.InvalidOwnerFormatException import InvalidOwnerFormatException
from src.leeger.model.Owner import Owner


def checkAllTypes(owner: Owner) -> None:
    """
    Checks all types that are within the Owner object.
    """
    if type(owner.name) != str:
        raise InvalidOwnerFormatException("Owner name must be type 'str'.")
