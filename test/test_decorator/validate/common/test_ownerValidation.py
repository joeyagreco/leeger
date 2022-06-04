import unittest

from src.leeger.decorator.validate.validators import validateLeague
from src.leeger.exception.InvalidOwnerFormatException import InvalidOwnerFormatException
from src.leeger.model.League import League
from src.leeger.model.Owner import Owner


class TestOwnerValidation(unittest.TestCase):

    @validateLeague
    def dummyFunction(self, league: League, **kwargs):
        """
        This is used to represent any function that can be wrapped by @validateLeague.
        """
        ...

    def test_validateLeague_ownerNameIsntTypeStr_raisesException(self):
        owner = Owner(name=None)
        with self.assertRaises(InvalidOwnerFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=[owner], years=list()))
        self.assertEqual("Owner name must be type 'str'.", str(context.exception))
