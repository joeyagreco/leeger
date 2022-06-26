from dataclasses import dataclass


@dataclass(kw_only=True)
class AllTimeFilters:
    """
    Used to house filters that will be used to calculate All-Time stats.
    """
    yearNumberStart: int  # year to start at (inclusive)
    weekNumberStart: int  # week to start at (inclusive)
    yearNumberEnd: int  # year to end at (inclusive)
    weekNumberEnd: int  # week to end at (inclusive)
    onlyChampionship: bool  # only include championship weeks
    onlyPostSeason: bool  # only include playoff weeks
    onlyRegularSeason: bool  # only include regular season weeks
