import statistics
from typing import Optional

from leeger.model.league.Matchup import Matchup


class MatchupNavigator:
    """
    Used to navigate the Matchup model.
    """

    @staticmethod
    def getTeamIdOfMatchupWinner(matchup: Matchup, **kwargs) -> Optional[str]:
        """
        Returns the team ID of the team that won the matchup or None if the matchup was a tie.
        """
        winningTeamId = None
        # team A won
        if (matchup.teamAScore > matchup.teamBScore) or (
            matchup.teamAScore == matchup.teamBScore and matchup.teamAHasTiebreaker
        ):
            winningTeamId = matchup.teamAId
        # team B won
        elif (matchup.teamBScore > matchup.teamAScore) or (
            matchup.teamAScore == matchup.teamBScore and matchup.teamBHasTiebreaker
        ):
            winningTeamId = matchup.teamBId
        return winningTeamId

    @staticmethod
    def simplifyMultiWeekMatchups(matchups: list[Matchup]) -> Matchup:
        """
        Takes a list of multi-week matchups and returns a single Matchup that is a combined representation of those matchups.
        This assumes the list of matchups given is validated.
        """
        if len(matchups) == 0:
            raise ValueError(f"matchups cannot be an empty list.")
        return Matchup(
            teamAId=matchups[0].teamAId,
            teamBId=matchups[0].teamBId,
            teamAScore=sum([matchup.teamAScore for matchup in matchups]),
            teamBScore=sum([matchup.teamBScore for matchup in matchups]),
            teamAHasTiebreaker=matchups[0].teamAHasTiebreaker,
            teamBHasTiebreaker=matchups[0].teamBHasTiebreaker,
            matchupType=matchups[0].matchupType,
        )

    @classmethod
    def getMedianScore(cls, matchups: list[Matchup]) -> float:
        """
        Returns the median score from the given matchups
        """
        scores = [m.teamAScore for m in matchups] + [m.teamBScore for m in matchups]
        return statistics.median(scores)
