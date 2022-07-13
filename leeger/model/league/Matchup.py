from dataclasses import dataclass

from leeger.enum.MatchupType import MatchupType
from leeger.exception.InvalidMatchupFormatException import InvalidMatchupFormatException
from leeger.model.abstract.UniqueId import UniqueId


@dataclass(kw_only=True)
class Matchup(UniqueId):
    teamAId: str
    teamBId: str
    teamAScore: float | int
    teamBScore: float | int
    matchupType: MatchupType = MatchupType.REGULAR_SEASON
    teamAHasTiebreaker: bool = False
    teamBHasTiebreaker: bool = False
    
    def __post_init__(self):
        # Team A and Team B cannot both have the tiebreaker
        if self.teamAHasTiebreaker is True and self.teamBHasTiebreaker is True:
            raise InvalidMatchupFormatException("Team A and Team B cannot both have the tiebreaker.")
