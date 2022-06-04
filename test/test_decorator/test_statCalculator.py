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

    def test_statCalculator_happyPath(self):
        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=False, matchups=list())
        week4 = Week(weekNumber=4, isPlayoffWeek=True, isChampionshipWeek=True, matchups=list())
        year = Year(yearNumber=2000, teams=list(), weeks=[week1, week2, week3, week4])
        self.dummyFunction(League(name="TEST", owners=list(), years=[year]))

    def test_statCalculator_twoChampionshipWeeksInYear_raisesException(self):
        week1 = Week(weekNumber=1, isPlayoffWeek=True, isChampionshipWeek=True, matchups=list())
        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=True, matchups=list())
        year = Year(yearNumber=2000, teams=list(), weeks=[week1, week2])

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[year]))
        self.assertEqual("Year 2000 has more than 1 championship week.", str(context.exception))

    def test_statCalculator_yearHasNoWeeks_raisesException(self):
        year = Year(yearNumber=2000, teams=list(), weeks=list())

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[year]))
        self.assertEqual("Year 2000 does not have at least 1 week.", str(context.exception))

    def test_statCalculator_yearDuplicateWeekNumbers_raisesException(self):
        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        week1duplicate = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        year = Year(yearNumber=2000, teams=list(), weeks=[week1, week1duplicate])

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[year]))
        self.assertEqual("Year 2000 has duplicate week numbers.", str(context.exception))

    def test_statCalculator_lowestWeekNumberIsNotOne_raisesException(self):
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        year = Year(yearNumber=2000, teams=list(), weeks=[week2])

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[year]))
        self.assertEqual("First week in year 2000 must be 1, not 2.", str(context.exception))

    def test_statCalculator_weekNumbersNotOneThroughN_raisesException(self):
        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        week3 = Week(weekNumber=3, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        week4 = Week(weekNumber=4, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        year = Year(yearNumber=2000, teams=list(), weeks=[week1, week2, week4])  # no week 3

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[year]))
        self.assertEqual("Year 2000 does not have week numbers in order (1-n).", str(context.exception))

        year = Year(yearNumber=2000, teams=list(), weeks=[week1, week2, week4, week3])  # weeks not in order
        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[year]))
        self.assertEqual("Year 2000 does not have week numbers in order (1-n).", str(context.exception))

    def test_statCalculator_nonPlayoffWeekAfterPlayoffWeek_raisesException(self):
        week1 = Week(weekNumber=1, isPlayoffWeek=True, isChampionshipWeek=False, matchups=list())
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        year = Year(yearNumber=2000, teams=list(), weeks=[week1, week2])

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[year]))
        self.assertEqual("Year 2000 has a non-playoff week after a playoff week.", str(context.exception))

    def test_statCalculator_nonChampionshipWeekAfterChampionshipWeek_raisesException(self):
        week1 = Week(weekNumber=1, isPlayoffWeek=True, isChampionshipWeek=True, matchups=list())
        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False, matchups=list())
        year = Year(yearNumber=2000, teams=list(), weeks=[week1, week2])

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[year]))
        self.assertEqual("Year 2000 has a non-championship week after a championship week.", str(context.exception))
