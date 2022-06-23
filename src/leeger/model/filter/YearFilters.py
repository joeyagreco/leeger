from dataclasses import dataclass

from src.leeger.enum.MatchupType import MatchupType


@dataclass(kw_only=True)
class YearFilters:
    """
    Used to house filters that will be applied to a Year when navigating through it.
    """
    weekNumberStart: int  # week to start at (inclusive)
    weekNumberEnd: int  # week to end at (inclusive)
    includeMatchupTypes: list[MatchupType]  # include matchups of these types
