import unittest

from src.leeger.decorator.validate.validators import validateLeague
from src.leeger.exception.InvalidYearFormatException import InvalidYearFormatException
from src.leeger.model.League import League
from src.leeger.model.Owner import Owner
from src.leeger.model.Year import Year


class TestYearValidation(unittest.TestCase):

    @validateLeague
    def dummyFunction(self, league: League, **kwargs):
        """
        This is used to represent any function that can be wrapped by @validateLeague.
        """
        ...

    def test_validateLeague_yearNumberIsntTypeInt_raisesException(self):
        owner = Owner(name="TEST")
        year = Year(yearNumber=None, teams=list(), weeks=list())
        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=[owner], years=[year]))
        self.assertEqual("Year number must be type 'int'.", str(context.exception))

    def test_validateLeague_yearTeamsIsntTypeList_raisesException(self):
        owner = Owner(name="TEST")
        year = Year(yearNumber=2000, teams=None, weeks=list())
        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=[owner], years=[year]))
        self.assertEqual("Year teams must be type 'list'.", str(context.exception))

    def test_validateLeague_yearWeeksIsntTypeList_raisesException(self):
        owner = Owner(name="TEST")
        year = Year(yearNumber=2000, teams=list(), weeks=None)
        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=[owner], years=[year]))
        self.assertEqual("Year weeks must be type 'list'.", str(context.exception))
