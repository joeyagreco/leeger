import unittest

from src.leeger.decorator.validate.validators import validateLeague, validateYear, validateWeek, validateMatchup
from src.leeger.model.League import League
from src.leeger.model.Week import Week
from src.leeger.model.Year import Year


class TestValidators(unittest.TestCase):

    @validateLeague
    def dummyLeagueFunction(self, league: League, **kwargs):
        """
        This is used to represent any function that can be wrapped by @validateLeague.
        """
        ...

    @validateYear
    def dummyYearFunction(self, year: Year, **kwargs):
        """
        This is used to represent any function that can be wrapped by @validateYear.
        """
        ...

    @validateWeek
    def dummyWeekFunction(self, week: Week, **kwargs):
        """
        This is used to represent any function that can be wrapped by @validateWeek.
        """
        ...

    @validateMatchup
    def dummyMatchupFunction(self, week: Week, **kwargs):
        """
        This is used to represent any function that can be wrapped by @validateMatchup.
        """
        ...

    # Validate League

    def test_validateLeague_noLeagueParameterGiven_raisesException(self):
        with self.assertRaises(ValueError) as context:
            self.dummyLeagueFunction(None)
        self.assertEqual("No valid League argument given to validate.", str(context.exception))

    def test_validateLeague_validateLeagueKwargIsFalse_doesntRunValidation(self):
        self.dummyLeagueFunction(None, validateLeague=False)

    # Validate Year

    def test_validateYear_noYearParameterGiven_raisesException(self):
        with self.assertRaises(ValueError) as context:
            self.dummyYearFunction(None)
        self.assertEqual("No valid Year argument given to validate.", str(context.exception))

    def test_validateYear_validateYearKwargIsFalse_doesntRunValidation(self):
        self.dummyYearFunction(None, validateYear=False)

    # Validate Week

    def test_validateWeek_noWeekParameterGiven_raisesException(self):
        with self.assertRaises(ValueError) as context:
            self.dummyWeekFunction(None)
        self.assertEqual("No valid Week argument given to validate.", str(context.exception))

    def test_validateWeek_validateWeekKwargIsFalse_doesntRunValidation(self):
        self.dummyWeekFunction(None, validateWeek=False)

    # Validate Matchup

    def test_validateMatchup_noMatchupParameterGiven_raisesException(self):
        with self.assertRaises(ValueError) as context:
            self.dummyMatchupFunction(None)
        self.assertEqual("No valid Matchup argument given to validate.", str(context.exception))

    def test_validateMatchup_validateMatchupKwargIsFalse_doesntRunValidation(self):
        self.dummyWeekFunction(None, validateWeek=False)
