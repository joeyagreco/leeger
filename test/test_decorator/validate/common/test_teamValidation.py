import unittest

from leeger.decorator.validate.common import teamValidation
from leeger.exception.InvalidTeamFormatException import InvalidTeamFormatException
from leeger.model.league.Team import Team


class TestYearValidation(unittest.TestCase):

    def test_checkAllTypes_teamOwnerIdIsntTypeStr_raisesException(self):
        with self.assertRaises(InvalidTeamFormatException) as context:
            teamValidation.checkAllTypes(Team(ownerId=None, name="team"))
        self.assertEqual("ownerId must be type 'str'.", str(context.exception))

    def test_checkAllTypes_teamNameIsntTypeStr_raisesException(self):
        with self.assertRaises(InvalidTeamFormatException) as context:
            teamValidation.checkAllTypes(Team(ownerId="id", name=None))
        self.assertEqual("name must be type 'str'.", str(context.exception))
