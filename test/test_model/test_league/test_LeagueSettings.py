import unittest

from leeger.model.league.LeagueSettings import LeagueSettings


class TestLeagueSettings(unittest.TestCase):
    def test_leagueSettings_init(self):
        leagueSettings = LeagueSettings(leagueMedianGames=True)

        self.assertTrue(leagueSettings.leagueMedianGames)

    def test_leagueSettings_eq_equal(self):
        # create LeagueSettings 1
        leagueSettings_1 = LeagueSettings(leagueMedianGames=True)

        # create LeagueSettings 2
        leagueSettings_2 = LeagueSettings(leagueMedianGames=True)

        self.assertEqual(leagueSettings_1, leagueSettings_2)

    def test_leagueSettings_eq_notEqual(self):
        # create LeagueSettings 1
        leagueSettings_1 = LeagueSettings(leagueMedianGames=True)

        # create LeagueSettings 2
        leagueSettings_2 = LeagueSettings(leagueMedianGames=False)

        self.assertNotEqual(leagueSettings_1, leagueSettings_2)

    def test_leagueSettings_toJson(self):
        leagueSettings = LeagueSettings(leagueMedianGames=True)
        leagueSettingsJson = leagueSettings.toJson()

        self.assertIsInstance(leagueSettingsJson, dict)
        self.assertTrue(leagueSettingsJson["leagueMedianGames"])
