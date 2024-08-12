import unittest

from leeger.enum.MatchupType import MatchupType
from leeger.model.filter.AllTimeFilters import AllTimeFilters


class TestAllTimeFilters(unittest.TestCase):
    def test_includeMatchupTypes_default(self):
        allTimeFilters = AllTimeFilters(
            yearNumberStart=2000,
            yearNumberEnd=2001,
            weekNumberStart=1,
            weekNumberEnd=2,
            onlyChampionship=False,
            onlyPostSeason=False,
            onlyRegularSeason=False,
        )

        self.assertEqual(
            [MatchupType.REGULAR_SEASON, MatchupType.PLAYOFF, MatchupType.CHAMPIONSHIP],
            allTimeFilters.includeMatchupTypes,
        )

    def test_includeMatchupTypes_onlyChampionshipIsTrue(self):
        allTimeFilters = AllTimeFilters(
            yearNumberStart=2000,
            yearNumberEnd=2001,
            weekNumberStart=1,
            weekNumberEnd=2,
            onlyChampionship=True,
            onlyPostSeason=False,
            onlyRegularSeason=False,
        )

        self.assertEqual([MatchupType.CHAMPIONSHIP], allTimeFilters.includeMatchupTypes)

    def test_includeMatchupTypes_onlyPostSeasonIsTrue(self):
        allTimeFilters = AllTimeFilters(
            yearNumberStart=2000,
            yearNumberEnd=2001,
            weekNumberStart=1,
            weekNumberEnd=2,
            onlyChampionship=False,
            onlyPostSeason=True,
            onlyRegularSeason=False,
        )

        self.assertEqual(
            [MatchupType.PLAYOFF, MatchupType.CHAMPIONSHIP],
            allTimeFilters.includeMatchupTypes,
        )

    def test_includeMatchupTypes_onlyRegularSeasonIsTrue(self):
        allTimeFilters = AllTimeFilters(
            yearNumberStart=2000,
            yearNumberEnd=2001,
            weekNumberStart=1,
            weekNumberEnd=2,
            onlyChampionship=False,
            onlyPostSeason=False,
            onlyRegularSeason=True,
        )

        self.assertEqual(
            [MatchupType.REGULAR_SEASON], allTimeFilters.includeMatchupTypes
        )
