from dataclasses import dataclass


@dataclass(kw_only=True)
class Streak:
    number: int
    teamIdStart: str
    teamIdEnd: str
    weekNumberStart: int
    weekNumberEnd: int
    yearNumberStart: int
    yearNumberEnd: int
    isOngoing: bool
