import unittest

from src.leeger.decorator.validate.common import ownerValidation
from src.leeger.exception.InvalidOwnerFormatException import InvalidOwnerFormatException
from src.leeger.model.Owner import Owner


class TestOwnerValidation(unittest.TestCase):

    def test_validateLeague_ownerNameIsntTypeStr_raisesException(self):
        with self.assertRaises(InvalidOwnerFormatException) as context:
            ownerValidation.checkAllTypes(Owner(name=None))
        self.assertEqual("Owner name must be type 'str'.", str(context.exception))
