import unittest

from src.leeger.decorator.validate.validators import validateLeague
from src.leeger.exception.InvalidTeamFormatException import InvalidTeamFormatException
from src.leeger.model.League import League
from src.leeger.model.Owner import Owner
from src.leeger.model.Team import Team
from src.leeger.model.Year import Year


class TestYearValidation(unittest.TestCase):

    @validateLeague
    def dummyFunction(self, league: League, **kwargs):
        """
        This is used to represent any function that can be wrapped by @validateLeague.
        """
        ...

    def test_validateLeague_teamOwnerIdIsntTypeStr_raisesException(self):
        owner = Owner(name="TEST")
        team = Team(ownerId=None, name="team")
        year = Year(yearNumber=2000, teams=[team], weeks=list())
        with self.assertRaises(InvalidTeamFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=[owner], years=[year]))
        self.assertEqual("Team owner ID must be type 'str'.", str(context.exception))

    def test_validateLeague_teamNameIsntTypeStr_raisesException(self):
        owner = Owner(name="TEST")
        team = Team(ownerId="id", name=None)
        year = Year(yearNumber=2000, teams=[team], weeks=list())
        with self.assertRaises(InvalidTeamFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=[owner], years=[year]))
        self.assertEqual("Team name must be type 'str'.", str(context.exception))
