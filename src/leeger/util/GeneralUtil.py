from typing import Any


class GeneralUtil:

    @classmethod
    def filter(cls, *, valueToFilterOut: Any, listToFilterFrom: list) -> list:
        return [value for value in listToFilterFrom if value is not valueToFilterOut]
