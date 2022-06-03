import unittest

from src.leeger.decorator.statCalculator import statCalculator
from src.leeger.exception.InvalidYearFormatException import InvalidYearFormatException
from src.leeger.model.League import League
from src.leeger.model.Week import Week
from src.leeger.model.Year import Year


class TestStatCalculator(unittest.TestCase):

    @statCalculator
    def dummyFunction(self, league: League):
        """
        This is used to represent any function that can be wrapped by @statCalculator.
        """
        ...

    def test_statCalculator_twoChampionshipWeeksInYear_raisesException(self):
        week1 = Week(weekNumber=1, isPlayoffWeek=True, isChampionshipWeek=True, matchups=list())
        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=True, matchups=list())
        year = Year(yearNumber=2000, teams=list(), weeks=[week1, week2])

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="PBL", owners=list(), years=[year]), a="a", b="b")
        self.assertEqual("Year 2000 has more than 1 championship week.", str(context.exception))
