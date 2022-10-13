import unittest

from leeger.exception import InvalidYearSettingsFormatException
from leeger.model.league import YearSettings
from leeger.validate import yearSettingsValidation


class TestYearSettingsValidation(unittest.TestCase):
    """
    TYPE CHECK TESTS
    """

    def test_checkAllTypes_leagueMedianGamesIsntTypeBool_raisesException(self):
        with self.assertRaises(InvalidYearSettingsFormatException) as context:
            yearSettings = YearSettings(leagueMedianGames=None)
            yearSettingsValidation.checkAllTypes(yearSettings)
        self.assertEqual("leagueMedianGames must be type 'bool'.", str(context.exception))
