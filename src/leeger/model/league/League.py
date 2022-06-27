import os
from dataclasses import dataclass

from src.leeger.model.abstract.UniqueId import UniqueId
from src.leeger.model.league.Owner import Owner
from src.leeger.model.league.Year import Year


@dataclass(kw_only=True)
class League(UniqueId):
    name: str
    owners: list[Owner]
    years: list[Year]

    def yearsToExcel(self, filePath: str, **kwargs) -> None:
        if os.path.exists(filePath):
            raise FileExistsError(f"Cannot create file at path: '{filePath}' because there is already a file there.")
        for year in self.years:
            year.toExcel(filePath, **kwargs)
