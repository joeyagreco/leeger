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
        for year in self.years:
            year.toExcel(filePath, **kwargs)
