import unittest

from leeger.model.league import YearSettings
from leeger.validate import yearSettingsValidation


class TestYearSettingsValidation(unittest.TestCase):
    """
    TYPE CHECK TESTS
    """

    def test_runAllChecks(self):
        yearSettings = YearSettings(leagueMedianGames=None)
        yearSettingsValidation.runAllChecks(yearSettings)
        yearSettings = YearSettings(leagueMedianGames=True)
        yearSettingsValidation.runAllChecks(yearSettings)
        yearSettings = YearSettings(leagueMedianGames=False)
        yearSettingsValidation.runAllChecks(yearSettings)
