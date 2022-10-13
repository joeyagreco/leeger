import unittest

from leeger.exception.InvalidLeagueFormatException import InvalidLeagueFormatException
from leeger.model.league import LeagueSettings
from leeger.validate import leagueSettingsValidation


class TestLeagueSettingsValidation(unittest.TestCase):
    """
    TYPE CHECK TESTS
    """

    def test_checkAllTypes_leagueMedianGamesIsntTypeBool_raisesException(self):
        with self.assertRaises(InvalidLeagueFormatException) as context:
            leagueSettings = LeagueSettings()
            leagueSettings.leagueMedianGames = None
            leagueSettingsValidation.checkAllTypes(leagueSettings)
        self.assertEqual("leagueMedianGames must be type 'bool'.", str(context.exception))
