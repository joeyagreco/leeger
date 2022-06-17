import unittest

from src.leeger.decorator.validate.common import matchupValidation
from src.leeger.exception.InvalidMatchupFormatException import InvalidMatchupFormatException
from src.leeger.model.Matchup import Matchup


class TestMatchupValidation(unittest.TestCase):

    def test_checkAllTypes_matchupTeamAIdIsntTypeStr_raisesException(self):
        with self.assertRaises(InvalidMatchupFormatException) as context:
            matchupValidation.checkAllTypes(Matchup(teamAId=None, teamBId="bId", teamAScore=1, teamBScore=2))
        self.assertEqual("teamAId must be type 'str'.", str(context.exception))

    def test_checkAllTypes_matchupTeamBIdIsntTypeStr_raisesException(self):
        with self.assertRaises(InvalidMatchupFormatException) as context:
            matchupValidation.checkAllTypes(Matchup(teamAId="aId", teamBId=None, teamAScore=1, teamBScore=2))
        self.assertEqual("teamBId must be type 'str'.", str(context.exception))

    def test_checkAllTypes_matchupTeamAScoreIsntTypeFloatOrInt_raisesException(self):
        with self.assertRaises(InvalidMatchupFormatException) as context:
            matchupValidation.checkAllTypes(Matchup(teamAId="aId", teamBId="bId", teamAScore=None, teamBScore=2))
        self.assertEqual("teamAScore must be type 'float' or 'int'.", str(context.exception))

    def test_checkAllTypes_matchupTeamBScoreIsntTypeFloatOrInt_raisesException(self):
        with self.assertRaises(InvalidMatchupFormatException) as context:
            matchupValidation.checkAllTypes(Matchup(teamAId="aId", teamBId="bId", teamAScore=1, teamBScore=None))
        self.assertEqual("teamBScore must be type 'float' or 'int'.", str(context.exception))

    def test_checkAllTypes_matchupTeamAHasTiebreakerIsntTypeBool_raisesException(self):
        with self.assertRaises(InvalidMatchupFormatException) as context:
            matchupValidation.checkAllTypes(
                Matchup(teamAId="aId", teamBId="bId", teamAScore=1, teamBScore=2, teamAHasTiebreaker=None))
        self.assertEqual("teamAHasTiebreaker must be type 'bool'.", str(context.exception))

    def test_checkAllTypes_matchupTeamBHasTiebreakerIsntTypeBool_raisesException(self):
        with self.assertRaises(InvalidMatchupFormatException) as context:
            matchupValidation.checkAllTypes(
                Matchup(teamAId="aId", teamBId="bId", teamAScore=1, teamBScore=2, teamBHasTiebreaker=None))
        self.assertEqual("teamBHasTiebreaker must be type 'bool'.", str(context.exception))
