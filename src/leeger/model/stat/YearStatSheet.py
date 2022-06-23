from dataclasses import dataclass

from src.leeger.util.Deci import Deci


@dataclass(kw_only=True, frozen=True)
class YearStatSheet:
    # Game Outcome
    wins: dict[str, int]
    losses: dict[str, int]
    ties: dict[str, int]
    winPercentage: dict[str, Deci]
    wal: dict[str, Deci]
    walPerGame: dict[str, Deci]

    # AWAL
    awal: dict[str, Deci]
    awalPerGame: dict[str, Deci]
    opponentAWAL: dict[str, Deci]
    opponentAWALPerGame: dict[str, Deci]

    # Smart Wins
    smartWins: dict[str, Deci]
    smartWinsPerGame: dict[str, Deci]
    opponentSmartWins: dict[str, Deci]
    opponentSmartWinsPerGame: dict[str, Deci]

    # Points Scored
    pointsScored: dict[str, Deci]
    pointsScoredPerGame: dict[str, Deci]
    opponentPointsScored: dict[str, Deci]
    opponentPointsScoredPerGame: dict[str, Deci]

    # Scoring Share
    scoringShare: dict[str, Deci]
    opponentScoringShare: dict[str, Deci]

    # Single Score
    maxScore: dict[str, float | int]
    minScore: dict[str, float | int]

    # Scoring Standard Deviation
    scoringStandardDeviation: dict[str, Deci]

    # Plus Minus
    plusMinus: dict[str, Deci]

    # SSL
    teamScore: dict[str, Deci]
    teamSuccess: dict[str, Deci]
    teamLuck: dict[str, Deci]

    # Year Outcome
    championshipCount: dict[str, Deci]
