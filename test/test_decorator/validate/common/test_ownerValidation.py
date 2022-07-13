import unittest

from leeger.decorator.validate.common import ownerValidation
from leeger.exception.InvalidOwnerFormatException import InvalidOwnerFormatException
from leeger.model.league.Owner import Owner


class TestOwnerValidation(unittest.TestCase):

    def test_checkAllTypes_ownerNameIsntTypeStr_raisesException(self):
        with self.assertRaises(InvalidOwnerFormatException) as context:
            ownerValidation.checkAllTypes(Owner(name=None))
        self.assertEqual("name must be type 'str'.", str(context.exception))
