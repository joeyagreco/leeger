import unittest

from leeger.exception.InvalidOwnerFormatException import \
    InvalidOwnerFormatException
from leeger.model.league.Owner import Owner
from leeger.validate import ownerValidation


class TestOwnerValidation(unittest.TestCase):
    def test_checkAllTypes_ownerNameIsntTypeStr_raisesException(self):
        with self.assertRaises(InvalidOwnerFormatException) as context:
            ownerValidation.checkAllTypes(Owner(name=None))
        self.assertEqual("name must be type 'str'.", str(context.exception))
