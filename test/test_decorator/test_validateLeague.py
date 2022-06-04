import unittest

from src.leeger.decorator.validate.validators import validateLeague
from src.leeger.model.League import League


class TestValidateLeague(unittest.TestCase):

    @validateLeague
    def dummyFunction(self, league: League, **kwargs):
        """
        This is used to represent any function that can be wrapped by @validateLeague.
        """
        ...

    def test_validateLeague_noLeagueParameterGiven_raisesException(self):
        with self.assertRaises(ValueError) as context:
            self.dummyFunction(None)
        self.assertEqual("No valid League argument given to validate.", str(context.exception))

    def test_validateLeague_validateLeagueKwargIsFalse_doesntRunValidation(self):
        self.dummyFunction(None, validateLeague=False)
