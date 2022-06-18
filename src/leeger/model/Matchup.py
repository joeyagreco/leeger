from dataclasses import dataclass

from src.leeger.exception.InvalidMatchupFormatException import InvalidMatchupFormatException
from src.leeger.model.abstract.UniqueId import UniqueId


@dataclass(kw_only=True)
class Matchup(UniqueId):
    teamAId: str
    teamBId: str
    teamAScore: float | int
    teamBScore: float | int
    teamAHasTiebreaker: bool = False
    teamBHasTiebreaker: bool = False
    isPlayoffMatchup: bool = False
    isChampionshipMatchup: bool = False
    
    def __post_init__(self):
        # Team A and Team B cannot both have the tiebreaker
        if self.teamAHasTiebreaker is True and self.teamBHasTiebreaker is True:
            raise InvalidMatchupFormatException("Team A and Team B cannot both have the tiebreaker.")
        # a championship matchup must be a playoff matchup
        self.isPlayoffMatchup = self.isPlayoffMatchup or self.isChampionshipMatchup
