import unittest

from src.leeger.decorator.validate.validators import validateLeague
from src.leeger.exception.InvalidLeagueFormatException import InvalidLeagueFormatException
from src.leeger.model.League import League


class TestLeagueValidation(unittest.TestCase):

    @validateLeague
    def dummyFunction(self, league: League, **kwargs):
        """
        This is used to represent any function that can be wrapped by @validateLeague.
        """
        ...

    def test_validateLeague_leagueNameIsntTypeString_raisesException(self):
        with self.assertRaises(InvalidLeagueFormatException) as context:
            self.dummyFunction(League(name=None, owners=list(), years=list()))
        self.assertEqual("League name must be type 'str'.", str(context.exception))

    def test_validateLeague_leagueOwnersIsntTypeList_raisesException(self):
        with self.assertRaises(InvalidLeagueFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=None, years=list()))
        self.assertEqual("League owners must be type 'list'.", str(context.exception))

    def test_validateLeague_leagueYearsIsntTypeList_raisesException(self):
        with self.assertRaises(InvalidLeagueFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=None))
        self.assertEqual("League years must be type 'list'.", str(context.exception))
