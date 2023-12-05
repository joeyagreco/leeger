import unittest

from leeger.exception.InvalidDivisionFormatException import InvalidDivisionFormatException
from leeger.model.league.Division import Division
from leeger.validate import divisionValidation


class TestDivisionValidation(unittest.TestCase):
    def test_checkAllTypes_divisionNameIsntTypeStr_raisesException(self):
        with self.assertRaises(InvalidDivisionFormatException) as context:
            divisionValidation.checkAllTypes(Division(name=None))
        self.assertEqual("name must be type 'str'.", str(context.exception))
