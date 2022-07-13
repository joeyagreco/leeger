from decimal import Decimal


class Deci(Decimal):
    """
    The purpose of this class is to automatically cast the given value to a string before calling __new__ of Decimal.
    The reason for this is IF a Decimal instance is created with a float that is NOT cast to a string first, you would have inaccuracies.
    i.e. Decimal(1.1) + Decimal(2.2) == Decimal("3.300000000000000266453525910")
    """

    def __new__(cls, value: int | float | str):
        return Decimal.__new__(cls, str(value))
