import unittest

from src.leeger.decorator.validate.common import matchupValidation
from src.leeger.enum.MatchupType import MatchupType
from src.leeger.exception.InvalidMatchupFormatException import InvalidMatchupFormatException
from src.leeger.model.Matchup import Matchup


class TestMatchupValidation(unittest.TestCase):

    def test_checkForIllegalMatchupOutcomes_playoffMatchupIsTie_raisesException(self):
        with self.assertRaises(InvalidMatchupFormatException) as context:
            matchupValidation.checkForIllegalMatchupOutcomes(
                Matchup(teamAId="", teamBId="", teamAScore=1, teamBScore=1, matchupType=MatchupType.PLAYOFF))
        self.assertEqual("Playoff and Championship matchups cannot end in a tie.", str(context.exception))

    def test_checkForIllegalMatchupOutcomes_championshipMatchupIsTie_raisesException(self):
        with self.assertRaises(InvalidMatchupFormatException) as context:
            matchupValidation.checkForIllegalMatchupOutcomes(
                Matchup(teamAId="", teamBId="", teamAScore=1, teamBScore=1, matchupType=MatchupType.CHAMPIONSHIP))
        self.assertEqual("Playoff and Championship matchups cannot end in a tie.", str(context.exception))

    ####################
    # TYPE CHECK TESTS #
    ####################

    def test_checkAllTypes_teamAIdIsntTypeStr_raisesException(self):
        with self.assertRaises(InvalidMatchupFormatException) as context:
            matchupValidation.checkAllTypes(Matchup(teamAId=None, teamBId="bId", teamAScore=1, teamBScore=2))
        self.assertEqual("teamAId must be type 'str'.", str(context.exception))

    def test_checkAllTypes_teamBIdIsntTypeStr_raisesException(self):
        with self.assertRaises(InvalidMatchupFormatException) as context:
            matchupValidation.checkAllTypes(Matchup(teamAId="aId", teamBId=None, teamAScore=1, teamBScore=2))
        self.assertEqual("teamBId must be type 'str'.", str(context.exception))

    def test_checkAllTypes_teamAScoreIsntTypeFloatOrInt_raisesException(self):
        with self.assertRaises(InvalidMatchupFormatException) as context:
            matchupValidation.checkAllTypes(Matchup(teamAId="aId", teamBId="bId", teamAScore=None, teamBScore=2))
        self.assertEqual("teamAScore must be type 'float' or 'int'.", str(context.exception))

    def test_checkAllTypes_teamBScoreIsntTypeFloatOrInt_raisesException(self):
        with self.assertRaises(InvalidMatchupFormatException) as context:
            matchupValidation.checkAllTypes(Matchup(teamAId="aId", teamBId="bId", teamAScore=1, teamBScore=None))
        self.assertEqual("teamBScore must be type 'float' or 'int'.", str(context.exception))

    def test_checkAllTypes_teamAHasTiebreakerIsntTypeBool_raisesException(self):
        with self.assertRaises(InvalidMatchupFormatException) as context:
            matchupValidation.checkAllTypes(
                Matchup(teamAId="aId", teamBId="bId", teamAScore=1, teamBScore=2, teamAHasTiebreaker=None))
        self.assertEqual("teamAHasTiebreaker must be type 'bool'.", str(context.exception))

    def test_checkAllTypes_teamBHasTiebreakerIsntTypeBool_raisesException(self):
        with self.assertRaises(InvalidMatchupFormatException) as context:
            matchupValidation.checkAllTypes(
                Matchup(teamAId="aId", teamBId="bId", teamAScore=1, teamBScore=2, teamBHasTiebreaker=None))
        self.assertEqual("teamBHasTiebreaker must be type 'bool'.", str(context.exception))

    def test_checkAllTypes_matchupTypeIsntTypeMatchup_raisesException(self):
        with self.assertRaises(InvalidMatchupFormatException) as context:
            matchupValidation.checkAllTypes(
                Matchup(teamAId="aId", teamBId="bId", teamAScore=1, teamBScore=2, matchupType=None))
        self.assertEqual("matchupType must be type 'MatchupType'.", str(context.exception))
