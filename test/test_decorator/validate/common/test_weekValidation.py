import unittest

from src.leeger.decorator.validate.common import weekValidation
from src.leeger.exception.InvalidWeekFormatException import InvalidWeekFormatException
from src.leeger.model.Week import Week


class TestWeekValidation(unittest.TestCase):

    def test_checkWeekHasAtLeastOneMatchup_weekDoesntHaveAtLeastOneMatchup_raisesException(self):
        with self.assertRaises(InvalidWeekFormatException) as context:
            weekValidation.checkWeekHasAtLeastOneMatchup(
                Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list()))
        self.assertEqual("Week 1 must have at least 1 matchup.", str(context.exception))

    """
    TYPE CHECK TESTS
    """

    def test_checkAllTypes_weekNumberIsntTypeInt_raisesException(self):
        with self.assertRaises(InvalidWeekFormatException) as context:
            weekValidation.checkAllTypes(
                Week(weekNumber=None, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list()))
        self.assertEqual("Week number must be type 'int'.", str(context.exception))

    def test_checkAllTypes_weekisPlayoffWeekIsntTypeBool_raisesException(self):
        with self.assertRaises(InvalidWeekFormatException) as context:
            weekValidation.checkAllTypes(
                Week(weekNumber=1, isPlayoffWeek=None, isChampionshipWeek=False, matchups=list()))
        self.assertEqual("Week isPlayoffWeek must be type 'bool'.", str(context.exception))

    def test_checkAllTypes_weekisChampionshipWeekIsntTypeBool_raisesException(self):
        with self.assertRaises(InvalidWeekFormatException) as context:
            weekValidation.checkAllTypes(
                Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=None, matchups=list()))
        self.assertEqual("Week isChampionshipWeek must be type 'bool'.", str(context.exception))

    def test_checkAllTypes_weekMatchupsIsntTypeList_raisesException(self):
        with self.assertRaises(InvalidWeekFormatException) as context:
            weekValidation.checkAllTypes(
                Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=None))
        self.assertEqual("Week matchups must be type 'list'.", str(context.exception))
