from typing import Any, Optional

from leeger.util.CustomLogger import CustomLogger
from leeger.util.Deci import Deci


class GeneralUtil:

    @staticmethod
    def filter(*, value: Any, list_: list) -> list:
        """
        Filters out the given value from the given list.
        """
        return [v for v in list_ if v is not value]

    @staticmethod
    def warnForUnusedKwargs(kwargs: dict) -> None:
        """
        Logs a warning for each present kwarg in the given dict.
        """
        LOGGER = CustomLogger.getLogger()
        # this is a list of common kwargs that sometimes linger in kwargs to be used later.
        IGNORE_KWARGS = ["validate"]
        unused_kwargs = [kwarg for kwarg in kwargs.keys() if kwarg not in IGNORE_KWARGS]
        for kwarg in unused_kwargs:
            LOGGER.warning(f"Keyword argument '{kwarg}' unused.")

    @staticmethod
    def safeSum(*numbers) -> Optional[Deci | int | float]:
        """
        Safely adds numbers where None is ignored.
        Examples:
            * 1 + None = 1
            * None + 1 = 1
            * None + None = None
            * 1 + 1 = 2
        """
        safeSum = None
        for number in numbers:
            if None in (safeSum, number):
                safeSum = number if safeSum is None else safeSum
            else:
                safeSum += number

        return safeSum
