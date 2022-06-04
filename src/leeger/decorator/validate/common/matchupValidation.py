from src.leeger.exception.InvalidMatchupFormatException import InvalidMatchupFormatException
from src.leeger.model.Matchup import Matchup


def checkAllTypes(matchup: Matchup) -> None:
    """
    Checks all types that are within the Matchup object.
    """
    if type(matchup.teamAId) != str:
        raise InvalidMatchupFormatException("Matchup teamAId must be type 'str'.")
    if type(matchup.teamBId) != str:
        raise InvalidMatchupFormatException("Matchup teamBId must be type 'str'.")
    if type(matchup.teamAScore) != float and type(matchup.teamAScore) != int:
        raise InvalidMatchupFormatException("Matchup teamAScore must be type 'float' or 'int'.")
    if type(matchup.teamBScore) != float and type(matchup.teamBScore) != int:
        raise InvalidMatchupFormatException("Matchup teamBScore must be type 'float' or 'int'.")
    if type(matchup.teamAHasTiebreaker) != bool:
        raise InvalidMatchupFormatException("Matchup teamAHasTiebreaker must be type 'bool'.")
    if type(matchup.teamBHasTiebreaker) != bool:
        raise InvalidMatchupFormatException("Matchup teamBHasTiebreaker must be type 'bool'.")
