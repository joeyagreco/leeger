from enum import unique, Enum, auto


@unique
class MatchupType(Enum):
    """
    Used to hold the different types of matchups.
    """
    CHAMPIONSHIP = auto()
    IGNORE = auto()
    PLAYOFF = auto()
    REGULAR_SEASON = auto()
