import unittest

from src.leeger.decorator.validate.common import weekValidation
from src.leeger.exception.InvalidWeekFormatException import InvalidWeekFormatException
from src.leeger.model.Matchup import Matchup
from src.leeger.model.Week import Week


class TestWeekValidation(unittest.TestCase):

    def test_checkWeekHasAtLeastOneMatchup_weekDoesntHaveAtLeastOneMatchup_raisesException(self):
        with self.assertRaises(InvalidWeekFormatException) as context:
            weekValidation.checkWeekHasAtLeastOneMatchup(
                Week(weekNumber=1, isPlayoffWeek=False, matchups=list()))
        self.assertEqual("Week 1 must have at least 1 matchup.", str(context.exception))

    def test_checkForDuplicateMatchups_duplicateMatchupInstances_raisesException(self):
        matchup = Matchup(teamAId="a", teamBId="b", teamAScore=1, teamBScore=2)
        with self.assertRaises(InvalidWeekFormatException) as context:
            weekValidation.checkForDuplicateMatchups(
                Week(weekNumber=1, isPlayoffWeek=False, matchups=[matchup, matchup]))
        self.assertEqual("Matchups must all be unique instances.", str(context.exception))

    """
    TYPE CHECK TESTS
    """

    def test_checkAllTypes_weekNumberIsntTypeInt_raisesException(self):
        with self.assertRaises(InvalidWeekFormatException) as context:
            weekValidation.checkAllTypes(
                Week(weekNumber=None, isPlayoffWeek=False, matchups=list()))
        self.assertEqual("weekNumber must be type 'int'.", str(context.exception))

    def test_checkAllTypes_weekisPlayoffWeekIsntTypeBool_raisesException(self):
        with self.assertRaises(InvalidWeekFormatException) as context:
            weekValidation.checkAllTypes(
                Week(weekNumber=1, isPlayoffWeek=None, matchups=list()))
        self.assertEqual("isPlayoffWeek must be type 'bool'.", str(context.exception))

    def test_checkAllTypes_weekMatchupsIsntTypeList_raisesException(self):
        with self.assertRaises(InvalidWeekFormatException) as context:
            weekValidation.checkAllTypes(
                Week(weekNumber=1, isPlayoffWeek=False, matchups=None))
        self.assertEqual("matchups must be type 'list'.", str(context.exception))
