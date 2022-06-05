from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class YearFilters:
    onlyPostSeason: bool  # only include post season wins
    onlyRegularSeason: bool  # only include regular season wins
    weekNumberStart: int  # week to start the calculations at (inclusive)
    weekNumberEnd: int  # week to end the calculations at (inclusive)
