import unittest

from leeger.exception.InvalidTeamFormatException import InvalidTeamFormatException
from leeger.model.league.Team import Team
from leeger.validate import teamValidation


class TestYearValidation(unittest.TestCase):
    def test_checkAllTypes_teamOwnerIdIsntTypeStr_raisesException(self):
        with self.assertRaises(InvalidTeamFormatException) as context:
            teamValidation.checkAllTypes(Team(ownerId=None, name="team"))
        self.assertEqual("ownerId must be type 'str'.", str(context.exception))

    def test_checkAllTypes_teamNameIsntTypeStr_raisesException(self):
        with self.assertRaises(InvalidTeamFormatException) as context:
            teamValidation.checkAllTypes(Team(ownerId="id", name=None))
        self.assertEqual("name must be type 'str'.", str(context.exception))

    def test_checkAllTypes_divisionIdIsntTypeStrOrNone_raisesException(self):
        with self.assertRaises(InvalidTeamFormatException) as context:
            teamValidation.checkAllTypes(Team(ownerId="id", name="team", divisionId=1))
        self.assertEqual(
            "divisionId must be 'None' or type 'str'.", str(context.exception)
        )
