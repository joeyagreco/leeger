from dataclasses import dataclass

from leeger.util.Deci import Deci


@dataclass(kw_only=True, frozen=True)
class AllTimeStatSheet:
    # Team Summary
    gamesPlayed: dict[str, int]

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
    teamScorePerGame: dict[str, Deci]
    teamSuccessPerGame: dict[str, Deci]
    teamLuckPerGame: dict[str, Deci]

    def preferredOrderWithTitle(self) -> list[tuple[str, dict]]:
        """
        Returns all stats in the preferred order with the title for the stat.
        """
        return [
            ("Games Played", self.gamesPlayed),
            ("Wins", self.wins),
            ("Losses", self.losses),
            ("Ties", self.ties),
            ("Win Percentage", self.winPercentage),
            ("WAL", self.wal),
            ("WAL Per Game", self.walPerGame),
            ("AWAL", self.awal),
            ("AWAL Per Game", self.awalPerGame),
            ("Opponent AWAL", self.opponentAWAL),
            ("Opponent AWAL Per Game", self.opponentAWALPerGame),
            ("Smart Wins", self.smartWins),
            ("Smart Wins Per Game", self.smartWinsPerGame),
            ("Opponent Smart Wins", self.opponentSmartWins),
            ("Opponent Smart Wins Per Game", self.opponentSmartWinsPerGame),
            ("Points Scored", self.pointsScored),
            ("Points Scored Per Game", self.pointsScoredPerGame),
            ("Opponent Points Scored", self.opponentPointsScored),
            ("Opponent Points Scored Per Game", self.opponentPointsScoredPerGame),
            ("Scoring Share", self.scoringShare),
            ("Opponent Scoring Share", self.opponentScoringShare),
            ("Max Score", self.maxScore),
            ("Min Score", self.minScore),
            ("Scoring Standard Deviation", self.scoringStandardDeviation),
            ("Plus/Minus", self.plusMinus),
            ("Team Score", self.teamScore),
            ("Team Success", self.teamSuccess),
            ("Team Luck", self.teamLuck),
            ("Team Score Per Game", self.teamScorePerGame),
            ("Team Success Per Game", self.teamSuccessPerGame),
            ("Team Luck Per Game", self.teamLuckPerGame)
        ]
