from __future__ import annotations

from enum import unique, Enum, auto


@unique
class MatchupType(Enum):
    """
    Used to hold the different types of matchup
    """
    CHAMPIONSHIP = auto()
    IGNORED = auto()
    PLAYOFF = auto()
    REGULAR_SEASON = auto()
