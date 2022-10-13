from leeger.exception import InvalidYearSettingsFormatException
from leeger.model.league import YearSettings


def runAllChecks(yearSettings: YearSettings) -> None:
    """
    Runs all checks on the given YearSettings.
    The order in which these are called matters.
    """
    checkAllTypes(yearSettings)


def checkAllTypes(yearSettings: YearSettings) -> None:
    """
    Runs all checks on the given YearSettings.
    """

    if not isinstance(yearSettings.leagueMedianGames, bool):
        raise InvalidYearSettingsFormatException("leagueMedianGames must be type 'bool'.")
