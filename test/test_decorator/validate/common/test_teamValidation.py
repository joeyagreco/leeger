import unittest

from src.leeger.decorator.validate.common import teamValidation
from src.leeger.exception.InvalidTeamFormatException import InvalidTeamFormatException
from src.leeger.model.Team import Team


class TestYearValidation(unittest.TestCase):

    def test_validateLeague_teamOwnerIdIsntTypeStr_raisesException(self):
        with self.assertRaises(InvalidTeamFormatException) as context:
            teamValidation.checkAllTypes(Team(ownerId=None, name="team"))
        self.assertEqual("Team owner ID must be type 'str'.", str(context.exception))

    def test_validateLeague_teamNameIsntTypeStr_raisesException(self):
        with self.assertRaises(InvalidTeamFormatException) as context:
            teamValidation.checkAllTypes(Team(ownerId="id", name=None))
        self.assertEqual("Team name must be type 'str'.", str(context.exception))
