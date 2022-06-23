from dataclasses import dataclass

from src.leeger.model.abstract.UniqueId import UniqueId
from src.leeger.model.league.Team import Team
from src.leeger.model.league.Week import Week
from src.leeger.model.stat.YearStatSheet import YearStatSheet


@dataclass(kw_only=True)
class Year(UniqueId):
    yearNumber: int
    teams: list[Team]
    weeks: list[Week]

    @property
    def statSheet(self) -> YearStatSheet:
        from src.leeger.calculator.year_calculator.AWALCalculator import AWALCalculator
        from src.leeger.calculator.year_calculator.GameOutcomeCalculator import GameOutcomeCalculator
        from src.leeger.calculator.year_calculator.PlusMinusCalculator import PlusMinusCalculator
        from src.leeger.calculator.year_calculator.PointsScoredCalculator import PointsScoredCalculator
        from src.leeger.calculator.year_calculator.ScoringShareCalculator import ScoringShareCalculator
        from src.leeger.calculator.year_calculator.ScoringStandardDeviationCalculator import \
            ScoringStandardDeviationCalculator
        from src.leeger.calculator.year_calculator.SingleScoreCalculator import SingleScoreCalculator
        from src.leeger.calculator.year_calculator.SmartWinsCalculator import SmartWinsCalculator
        from src.leeger.calculator.year_calculator.SSLCalculator import SSLCalculator
        from src.leeger.calculator.year_calculator.YearOutcomeCalculator import YearOutcomeCalculator

        # Game Outcome
        wins = GameOutcomeCalculator.getWins(self)
        losses = GameOutcomeCalculator.getLosses(self)
        ties = GameOutcomeCalculator.getTies(self)
        winPercentage = GameOutcomeCalculator.getWinPercentage(self)
        wal = GameOutcomeCalculator.getWAL(self)
        walPerGame = GameOutcomeCalculator.getWALPerGame(self)

        # AWAL
        awal = AWALCalculator.getAWAL(self)
        awalPerGame = AWALCalculator.getAWALPerGame(self)
        opponentAWAL = AWALCalculator.getOpponentAWAL(self)
        opponentAWALPerGame = AWALCalculator.getOpponentAWALPerGame(self)

        # Smart Wins
        smartWins = SmartWinsCalculator.getSmartWins(self)
        smartWinsPerGame = SmartWinsCalculator.getSmartWinsPerGame(self)
        opponentSmartWins = SmartWinsCalculator.getOpponentSmartWins(self)
        opponentSmartWinsPerGame = SmartWinsCalculator.getOpponentSmartWinsPerGame(self)

        # Points Scored
        pointsScored = PointsScoredCalculator.getPointsScored(self)
        pointsScoredPerGame = PointsScoredCalculator.getPointsScoredPerGame(self)
        opponentPointsScored = PointsScoredCalculator.getOpponentPointsScored(self)
        opponentPointsScoredPerGame = PointsScoredCalculator.getOpponentPointsScoredPerGame(self)

        # Scoring Share
        scoringShare = ScoringShareCalculator.getScoringShare(self)
        opponentScoringShare = ScoringShareCalculator.getOpponentScoringShare(self)

        # Single Score
        maxScore = SingleScoreCalculator.getMaxScore(self)
        minScore = SingleScoreCalculator.getMinScore(self)

        # Scoring Standard Deviation
        scoringStandardDeviation = ScoringStandardDeviationCalculator.getScoringStandardDeviation(self)

        # Plus Minus
        plusMinus = PlusMinusCalculator.getPlusMinus(self)

        # SSL
        teamScore = SSLCalculator.getTeamScore(self)
        teamSuccess = SSLCalculator.getTeamSuccess(self)
        teamLuck = SSLCalculator.getTeamLuck(self)

        # Year Outcome
        championshipCount = YearOutcomeCalculator.getChampionshipCount(self)

        return YearStatSheet(wins=wins, losses=losses, ties=ties, winPercentage=winPercentage, wal=wal,
                             walPerGame=walPerGame, awal=awal, awalPerGame=awalPerGame, opponentAWAL=opponentAWAL,
                             opponentAWALPerGame=opponentAWALPerGame, smartWins=smartWins,
                             smartWinsPerGame=smartWinsPerGame, opponentSmartWins=opponentSmartWins,
                             opponentSmartWinsPerGame=opponentSmartWinsPerGame, pointsScored=pointsScored,
                             pointsScoredPerGame=pointsScoredPerGame, opponentPointsScored=opponentPointsScored,
                             opponentPointsScoredPerGame=opponentPointsScoredPerGame, scoringShare=scoringShare,
                             opponentScoringShare=opponentScoringShare, maxScore=maxScore, minScore=minScore,
                             scoringStandardDeviation=scoringStandardDeviation, plusMinus=plusMinus,
                             teamScore=teamScore, teamSuccess=teamSuccess, teamLuck=teamLuck,
                             championshipCount=championshipCount)
