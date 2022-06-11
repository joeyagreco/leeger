from decimal import Decimal


class Deci(Decimal):
    """
    The purpose of this class is to automatically cast the given value to a string before calling __new__ of Decimal.
    """

    def __new__(cls, value: int | float | str):
        return Decimal.__new__(cls, str(value))
