import unittest

from src.leeger.decorator.validate.validators import validateLeague
from src.leeger.exception.InvalidWeekFormatException import InvalidWeekFormatException
from src.leeger.model.League import League
from src.leeger.model.Owner import Owner
from src.leeger.model.Team import Team
from src.leeger.model.Week import Week
from src.leeger.model.Year import Year


class TestWeekValidation(unittest.TestCase):

    @validateLeague
    def dummyFunction(self, league: League, **kwargs):
        """
        This is used to represent any function that can be wrapped by @validateLeague.
        """
        ...

    def test_validateLeague_weekNumberIsntTypeInt_raisesException(self):
        owner = Owner(name="TEST")
        team = Team(ownerId="id", name="name")
        week = Week(weekNumber=None, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        year = Year(yearNumber=2000, teams=[team], weeks=[week])
        with self.assertRaises(InvalidWeekFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=[owner], years=[year]))
        self.assertEqual("Week number must be type 'int'.", str(context.exception))

    def test_validateLeague_weekisPlayoffWeekIsntTypeBool_raisesException(self):
        owner = Owner(name="TEST")
        team = Team(ownerId="id", name="name")
        week = Week(weekNumber=1, isPlayoffWeek=None, isChampionshipWeek=False, matchups=list())
        year = Year(yearNumber=2000, teams=[team], weeks=[week])
        with self.assertRaises(InvalidWeekFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=[owner], years=[year]))
        self.assertEqual("Week isPlayoffWeek must be type 'bool'.", str(context.exception))

    def test_validateLeague_weekisChampionshipWeekIsntTypeBool_raisesException(self):
        owner = Owner(name="TEST")
        team = Team(ownerId="id", name="name")
        week = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=None, matchups=list())
        year = Year(yearNumber=2000, teams=[team], weeks=[week])
        with self.assertRaises(InvalidWeekFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=[owner], years=[year]))
        self.assertEqual("Week isChampionshipWeek must be type 'bool'.", str(context.exception))

    def test_validateLeague_weekMatchupsIsntTypeList_raisesException(self):
        owner = Owner(name="TEST")
        team = Team(ownerId="id", name="name")
        week = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=None)
        year = Year(yearNumber=2000, teams=[team], weeks=[week])
        with self.assertRaises(InvalidWeekFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=[owner], years=[year]))
        self.assertEqual("Week matchups must be type 'list'.", str(context.exception))
