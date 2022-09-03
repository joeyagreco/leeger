from typing import Any

from leeger.util.CustomLogger import CustomLogger


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
