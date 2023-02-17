from __future__ import annotations

from enum import unique, Enum


@unique
class MatchupType(Enum):
    """
    Used to hold the different types of matchups.
    """
    CHAMPIONSHIP = "CHAMPIONSHIP"
    IGNORE = "IGNORE"
    PLAYOFF = "PLAYOFF"
    REGULAR_SEASON = "REGULAR_SEASON"

    @classmethod
    def fromStr(cls, s: str) -> MatchupType:
        s_upper = s.upper()
        if s_upper == "CHAMPIONSHIP":
            return MatchupType.CHAMPIONSHIP
        elif s_upper == "IGNORE":
            return MatchupType.IGNORE
        elif s_upper == "PLAYOFF":
            return MatchupType.PLAYOFF
        elif s_upper == "REGULAR_SEASON":
            return MatchupType.REGULAR_SEASON
        raise ValueError(f"'{s}' is not a valid MatchupType.")
