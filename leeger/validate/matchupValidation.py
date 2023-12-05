from leeger.enum.MatchupType import MatchupType
from leeger.exception.InvalidMatchupFormatException import InvalidMatchupFormatException
from leeger.model.league.Matchup import Matchup


def runAllChecks(matchup: Matchup) -> None:
    """
    Runs all checks on the given Matchup.
    """
    checkAllTypes(matchup)
    checkForIllegalMatchupOutcomes(matchup)
    checkThatTeamIdsAreNotTheSame(matchup)


def checkAllTypes(matchup: Matchup) -> None:
    """
    Checks all types that are within the Matchup object.
    """
    if not isinstance(matchup.teamAId, str):
        raise InvalidMatchupFormatException("teamAId must be type 'str'.")
    if not isinstance(matchup.teamBId, str):
        raise InvalidMatchupFormatException("teamBId must be type 'str'.")
    if not isinstance(matchup.teamAScore, (float, int)):
        raise InvalidMatchupFormatException("teamAScore must be type 'float' or 'int'.")
    if not isinstance(matchup.teamBScore, (float, int)):
        raise InvalidMatchupFormatException("teamBScore must be type 'float' or 'int'.")
    if not isinstance(matchup.teamAHasTiebreaker, bool):
        raise InvalidMatchupFormatException("teamAHasTiebreaker must be type 'bool'.")
    if not isinstance(matchup.teamBHasTiebreaker, bool):
        raise InvalidMatchupFormatException("teamBHasTiebreaker must be type 'bool'.")
    if not isinstance(matchup.matchupType, MatchupType):
        raise InvalidMatchupFormatException("matchupType must be type 'MatchupType'.")
    if not isinstance(matchup.multiWeekMatchupId, (str, type(None))):
        raise InvalidMatchupFormatException("multiWeekMatchupId must be 'None' or type 'str'.")


def checkForIllegalMatchupOutcomes(matchup: Matchup) -> None:
    """
    Checks that no playoff/championship matchup ends in a tie.
    """
    from leeger.util.navigator.MatchupNavigator import MatchupNavigator

    if (
        matchup.matchupType in [MatchupType.PLAYOFF, MatchupType.CHAMPIONSHIP]
        and MatchupNavigator.getTeamIdOfMatchupWinner(matchup) is None
    ):
        raise InvalidMatchupFormatException(
            "Playoff and Championship matchups cannot end in a tie."
        )


def checkThatTeamIdsAreNotTheSame(matchup: Matchup) -> None:
    """
    Checks that team A and team B have different IDs
    """
    if matchup.teamAId == matchup.teamBId:
        raise InvalidMatchupFormatException("Team A and Team B cannot have the same ID.")
