from __future__ import annotations

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

    def __eq__(self, otherMatchup: Matchup) -> bool:
        """
        Checks if *this* Matchup is the same as the given Matchup.
        Does not check for equality of IDs, just values.
        """
        equal = self.teamAId == otherMatchup.teamAId
        equal = equal and self.teamBId == otherMatchup.teamBId
        equal = equal and self.teamAScore == otherMatchup.teamAScore
        equal = equal and self.teamBScore == otherMatchup.teamBScore
        equal = equal and self.matchupType == otherMatchup.matchupType
        equal = equal and self.teamAHasTiebreaker == otherMatchup.teamAHasTiebreaker
        equal = equal and self.teamBHasTiebreaker == otherMatchup.teamBHasTiebreaker
        return equal
