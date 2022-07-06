from typing import Any


class GeneralUtil:

    @classmethod
    def filter(cls, *, value: Any, list_: list) -> list:
        return [v for v in list_ if v is not value]
