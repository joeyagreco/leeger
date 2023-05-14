import unittest
from leeger.exception.DoesNotExistException import DoesNotExistException
from leeger.exception.LeagueLoaderException import LeagueLoaderException

from leeger.league_loader import SleeperLeagueLoader
from leeger.league_loader.LeagueLoader import LeagueLoader
from leeger.model.league.Owner import Owner


class TestLeagueLoader(unittest.TestCase):
    def test_noYearsGiven(self):
        with self.assertRaises(ValueError) as context:
            LeagueLoader("0", [])
        self.assertEqual("No years given to load league with ID '0'.", str(context.exception))

    def test_yearsGivenThatArentInts(self):
        with self.assertRaises(ValueError) as context:
            LeagueLoader("0", ["a"])
        self.assertEqual("All given years must be ints.", str(context.exception))

        with self.assertRaises(ValueError) as context:
            LeagueLoader("0", ["1"])
        self.assertEqual("All given years must be ints.", str(context.exception))

        with self.assertRaises(ValueError) as context:
            LeagueLoader("0", [1, "1"])
        self.assertEqual("All given years must be ints.", str(context.exception))

        with self.assertRaises(ValueError) as context:
            LeagueLoader("0", ["1", 1])
        self.assertEqual("All given years must be ints.", str(context.exception))

        # test for no error
        LeagueLoader("0", [1])

    def test__getGeneralOwnerNameFromGivenOwnerName(self):
        leagueLoader = LeagueLoader(
            "leagueId",
            [2021],
            ownerNamesAndAliases={
                "John Smith": ["John", "Smith"],
                "Jane Doe": ["Jane", "Doe"],
                "Tom Hanks": ["Tom"],
            },
        )

        # alias that belongs to a single owner
        self.assertEqual("John Smith", leagueLoader._getGeneralOwnerNameFromGivenOwnerName("John"))

        # alias that belongs to multiple owners
        self.assertEqual("John Smith", leagueLoader._getGeneralOwnerNameFromGivenOwnerName("Smith"))

        # alias that does not belong to any owner
        self.assertIsNone(leagueLoader._getGeneralOwnerNameFromGivenOwnerName("Foo"))

        # owner name that is also an owner name but NOT an alias
        self.assertIsNone(leagueLoader._getGeneralOwnerNameFromGivenOwnerName("John Smith"))

        # owner name that is not in the aliases list
        self.assertIsNone(leagueLoader._getGeneralOwnerNameFromGivenOwnerName("Foo"))

    def test__getOwnerByName(self):
        owners = [Owner(name="John Smith"), Owner(name="Jane Doe"), Owner(name="Tom Hanks")]
        leagueLoader = LeagueLoader(
            "leagueId",
            [2021],
            ownerNamesAndAliases={
                "John Smith": ["John", "Smith"],
                "Jane Doe": ["Jane", "Doe"],
                "Tom Hanks": ["Tom"],
            },
        )
        leagueLoader._owners = owners

        # exact owner name match
        self.assertEqual(owners[0], leagueLoader._getOwnerByName("John Smith"))

        # aliased owner name match
        self.assertEqual(owners[0], leagueLoader._getOwnerByName("John"))

        # alias that belongs to a single owner
        self.assertEqual(owners[0], leagueLoader._getOwnerByName("Smith"))

        # alias that does not exist
        with self.assertRaises(DoesNotExistException):
            leagueLoader._getOwnerByName("Foo")

    def test__validateRetrievedLeagues(self):
        # test for no error
        leagueLoader = LeagueLoader("leagueId", [2021])
        leagueLoader._validateRetrievedLeagues([{}])

        # test for error
        with self.assertRaises(LeagueLoaderException) as context:
            leagueLoader._validateRetrievedLeagues([{}, {}])
        self.assertEqual("Expected to retrieve 1 league/s, got 2 league/s.", str(context.exception))
