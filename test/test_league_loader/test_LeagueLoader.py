import unittest
from leeger.exception.DoesNotExistException import DoesNotExistException
from leeger.exception.LeagueLoaderException import LeagueLoaderException

from leeger.league_loader.LeagueLoader import LeagueLoader
from leeger.model.league.League import League
from leeger.model.league.Owner import Owner
from leeger.model.league.Week import Week
from leeger.model.league.Year import Year


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

    def test__getLeagueName(self):
        # no league name given, takes most recent year name
        leagueLoader = LeagueLoader("leagueId", [2021])
        leagueLoader._leagueNameByYear = {2022: "foo", 2019: "baz", 2021: "bar"}
        leagueName = leagueLoader._getLeagueName()
        self.assertEqual("foo", leagueName)

        # league name given, league names by year set, takes league name given
        leagueLoader = LeagueLoader("leagueId", [2021], leagueName="bot")
        leagueLoader._leagueNameByYear = {2022: "foo", 2019: "baz", 2021: "bar"}
        leagueName = leagueLoader._getLeagueName()
        self.assertEqual("bot", leagueName)

        # league name given, no league names by year set, takes league name given
        leagueLoader = LeagueLoader("leagueId", [2021], leagueName="bot")
        leagueName = leagueLoader._getLeagueName()
        self.assertEqual("bot", leagueName)

        # no league name given, no league names by year set, raises exception
        leagueLoader = LeagueLoader("leagueId", [2021])

        with self.assertRaises(LeagueLoaderException) as context:
            leagueLoader._getLeagueName()
        self.assertEqual(
            "Tried to retrieve league name with no leagueName parameter given and no league names set.",
            str(context.exception),
        )

    def test__getValidYears(self):
        # no change -> returns same years
        dummyWeeks = [Week(weekNumber=1, matchups=list())]
        year2020 = Year(yearNumber=2020, teams=list(), weeks=dummyWeeks)
        year2021 = Year(yearNumber=2021, teams=list(), weeks=dummyWeeks)
        year2022 = Year(yearNumber=2022, teams=list(), weeks=dummyWeeks)
        leagueLoader = LeagueLoader("leagueId", [2020, 2021, 2022])
        response = leagueLoader._getValidYears([year2020, year2021, year2022])
        self.assertEqual([year2020, year2021, year2022], response)

        # year with no weeks -> removes year
        dummyWeeks = [Week(weekNumber=1, matchups=list())]
        year2020 = Year(yearNumber=2020, teams=list(), weeks=dummyWeeks)
        year2021 = Year(yearNumber=2021, teams=list(), weeks=list())
        year2022 = Year(yearNumber=2022, teams=list(), weeks=dummyWeeks)
        leagueLoader = LeagueLoader("leagueId", [2020, 2021, 2022])
        response = leagueLoader._getValidYears([year2020, year2021, year2022])
        self.assertEqual([year2020, year2022], response)

        # years not sorted correctly -> sorts years
        dummyWeeks = [Week(weekNumber=1, matchups=list())]
        year2020 = Year(yearNumber=2020, teams=list(), weeks=dummyWeeks)
        year2021 = Year(yearNumber=2021, teams=list(), weeks=dummyWeeks)
        year2022 = Year(yearNumber=2022, teams=list(), weeks=dummyWeeks)
        leagueLoader = LeagueLoader("leagueId", [2020, 2021, 2022])
        response = leagueLoader._getValidYears([year2021, year2022, year2020])
        self.assertEqual([year2020, year2021, year2022], response)

    def test__warnForUnusedOwnerNames(self):
        # ownerNamesAndAliases not given, nothing is logged
        owner1 = Owner(name="o1")
        owner2 = Owner(name="o2")
        league = League(name="league", owners=[owner1, owner2], years=list())
        leagueLoader = LeagueLoader("leagueId", [2020])

        try:
            with self.assertLogs() as _:
                leagueLoader._warnForUnusedOwnerNames(league)
        except AssertionError:
            pass
        else:
            self.fail("Logs were produced but weren't expected")

        # ownerNamesAndAliases given, all are used, nothing is logged
        leagueLoader = LeagueLoader(
            "leagueId", [2020], ownerNamesAndAliases={"o1": list(), "o2": list()}
        )
        try:
            with self.assertLogs() as _:
                leagueLoader._warnForUnusedOwnerNames(league)
        except AssertionError:
            pass
        else:
            self.fail("Logs were produced but weren't expected")

        # ownerNamesAndAliases given, some aren't used, logs each unused owner name
        leagueLoader = LeagueLoader(
            "leagueId",
            [2020],
            ownerNamesAndAliases={"o1": list(), "o2": list(), "o3": list(), "o4": list()},
        )

        with self.assertLogs() as captured:
            leagueLoader._warnForUnusedOwnerNames(league)
        self.assertEqual(
            "Some owner names were given but not assigned to the loaded League: ['o3', 'o4']",
            str(captured.records[0].getMessage()),
        )
