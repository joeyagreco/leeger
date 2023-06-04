import unittest

from leeger.model.league.YearSettings import YearSettings


class TestYearSettings(unittest.TestCase):
    def test_yearSettings_init(self):
        yearSettings = YearSettings(leagueMedianGames=True)

        self.assertTrue(yearSettings.leagueMedianGames)

    def test_yearSettings_init_default_1(self):
        yearSettings = YearSettings()

        self.assertFalse(yearSettings.leagueMedianGames)

    def test_yearSettings_init_default_2(self):
        yearSettings = YearSettings(leagueMedianGames=None)

        self.assertFalse(yearSettings.leagueMedianGames)

    def test_yearSettings_eq_callsEqualsMethod(self):
        # create yearSettings 1
        yearSettings_1 = YearSettings(leagueMedianGames=True)

        # create yearSettings 2
        yearSettings_2 = YearSettings(leagueMedianGames=True)

        self.assertTrue(yearSettings_1 == yearSettings_2)

    def test_yearSettings_eq_equal(self):
        # create yearSettings 1
        yearSettings_1 = YearSettings(leagueMedianGames=True)

        # create yearSettings 2
        yearSettings_2 = YearSettings(leagueMedianGames=True)

        self.assertTrue(yearSettings_1.equals(yearSettings_2))

    def test_yearSettings_eq_notEqual(self):
        # create yearSettings 1
        yearSettings_1 = YearSettings(leagueMedianGames=True)

        # create yearSettings 2
        yearSettings_2 = YearSettings(leagueMedianGames=False)

        self.assertFalse(yearSettings_1.equals(yearSettings_2))

    def test_yearSettings_toJson(self):
        yearSettings = YearSettings(leagueMedianGames=True)
        yearSettingsJson = yearSettings.toJson()

        self.assertIsInstance(yearSettingsJson, dict)
        self.assertTrue(yearSettingsJson["leagueMedianGames"])
