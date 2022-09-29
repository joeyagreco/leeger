from enum import unique, Enum


@unique
class FantasySite(Enum):
    """
    Used to hold all fantasy sites this library supports.
    """
    ESPN = "ESPN"
    MY_FANTASY_LEAGUE = "MY_FANTASY_LEAGUE"
    SLEEPER = "SLEEPER"
    YAHOO = "YAHOO"
