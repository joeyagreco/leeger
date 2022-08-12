from __future__ import annotations

from dataclasses import dataclass

from leeger.model.abstract.UniqueId import UniqueId
from leeger.model.league.Team import Team
from leeger.model.league.Week import Week
from leeger.model.stat.YearStatSheet import YearStatSheet


@dataclass(kw_only=True, eq=False)
class Year(UniqueId):
    yearNumber: int
    teams: list[Team]
    weeks: list[Week]

    def __eq__(self, otherYear: Year) -> bool:
        """
        Checks if *this* Year is the same as the given Year.
        Does not check for equality of IDs, just values.
        """
        equal = self.yearNumber == otherYear.yearNumber
        equal = equal and self.teams == otherYear.teams
        equal = equal and self.weeks == otherYear.weeks
        return equal

    def statSheet(self, **kwargs) -> YearStatSheet:
        from leeger.calculator.year_calculator.AWALYearCalculator import AWALYearCalculator
        from leeger.calculator.year_calculator.GameOutcomeYearCalculator import GameOutcomeYearCalculator
        from leeger.calculator.year_calculator.PlusMinusYearCalculator import PlusMinusYearCalculator
        from leeger.calculator.year_calculator.PointsScoredYearCalculator import PointsScoredYearCalculator
        from leeger.calculator.year_calculator.ScoringShareYearCalculator import ScoringShareYearCalculator
        from leeger.calculator.year_calculator import \
            ScoringStandardDeviationYearCalculator
        from leeger.calculator.year_calculator import SingleScoreYearCalculator
        from leeger.calculator.year_calculator.SmartWinsYearCalculator import SmartWinsYearCalculator
        from leeger.calculator.year_calculator.SSLYearCalculator import SSLYearCalculator

        # Game Outcome
        wins = GameOutcomeYearCalculator.getWins(self, **kwargs)
        losses = GameOutcomeYearCalculator.getLosses(self, **kwargs)
        ties = GameOutcomeYearCalculator.getTies(self, **kwargs)
        winPercentage = GameOutcomeYearCalculator.getWinPercentage(self, **kwargs)
        wal = GameOutcomeYearCalculator.getWAL(self, **kwargs)
        walPerGame = GameOutcomeYearCalculator.getWALPerGame(self, **kwargs)

        # AWAL
        awal = AWALYearCalculator.getAWAL(self, **kwargs)
        awalPerGame = AWALYearCalculator.getAWALPerGame(self, **kwargs)
        opponentAWAL = AWALYearCalculator.getOpponentAWAL(self, **kwargs)
        opponentAWALPerGame = AWALYearCalculator.getOpponentAWALPerGame(self, **kwargs)

        # Smart Wins
        smartWins = SmartWinsYearCalculator.getSmartWins(self, **kwargs)
        smartWinsPerGame = SmartWinsYearCalculator.getSmartWinsPerGame(self, **kwargs)
        opponentSmartWins = SmartWinsYearCalculator.getOpponentSmartWins(self, **kwargs)
        opponentSmartWinsPerGame = SmartWinsYearCalculator.getOpponentSmartWinsPerGame(self, **kwargs)

        # Points Scored
        pointsScored = PointsScoredYearCalculator.getPointsScored(self, **kwargs)
        pointsScoredPerGame = PointsScoredYearCalculator.getPointsScoredPerGame(self, **kwargs)
        opponentPointsScored = PointsScoredYearCalculator.getOpponentPointsScored(self, **kwargs)
        opponentPointsScoredPerGame = PointsScoredYearCalculator.getOpponentPointsScoredPerGame(self, **kwargs)

        # Scoring Share
        scoringShare = ScoringShareYearCalculator.getScoringShare(self, **kwargs)
        opponentScoringShare = ScoringShareYearCalculator.getOpponentScoringShare(self, **kwargs)

        # Single Score
        maxScore = SingleScoreYearCalculator.getMaxScore(self, **kwargs)
        minScore = SingleScoreYearCalculator.getMinScore(self, **kwargs)

        # Scoring Standard Deviation
        scoringStandardDeviation = ScoringStandardDeviationYearCalculator.getScoringStandardDeviation(self, **kwargs)

        # Plus Minus
        plusMinus = PlusMinusYearCalculator.getPlusMinus(self, **kwargs)

        # SSL
        teamScore = SSLYearCalculator.getTeamScore(self, **kwargs)
        teamSuccess = SSLYearCalculator.getTeamSuccess(self, **kwargs)
        teamLuck = SSLYearCalculator.getTeamLuck(self, **kwargs)

        return YearStatSheet(wins=wins, losses=losses, ties=ties, winPercentage=winPercentage, wal=wal,
                             walPerGame=walPerGame, awal=awal, awalPerGame=awalPerGame, opponentAWAL=opponentAWAL,
                             opponentAWALPerGame=opponentAWALPerGame, smartWins=smartWins,
                             smartWinsPerGame=smartWinsPerGame, opponentSmartWins=opponentSmartWins,
                             opponentSmartWinsPerGame=opponentSmartWinsPerGame, pointsScored=pointsScored,
                             pointsScoredPerGame=pointsScoredPerGame, opponentPointsScored=opponentPointsScored,
                             opponentPointsScoredPerGame=opponentPointsScoredPerGame, scoringShare=scoringShare,
                             opponentScoringShare=opponentScoringShare, maxScore=maxScore, minScore=minScore,
                             scoringStandardDeviation=scoringStandardDeviation, plusMinus=plusMinus,
                             teamScore=teamScore, teamSuccess=teamSuccess, teamLuck=teamLuck)
