import unittest

from leeger.enum.MatchupType import MatchupType
from leeger.exception.InvalidMatchupFormatException import \
    InvalidMatchupFormatException
from leeger.model.league.Matchup import Matchup
from leeger.validate import matchupValidation


class TestMatchupValidation(unittest.TestCase):
    def test_checkForIllegalMatchupOutcomes_playoffMatchupIsTie_raisesException(self):
        with self.assertRaises(InvalidMatchupFormatException) as context:
            matchupValidation.checkForIllegalMatchupOutcomes(
                Matchup(
                    teamAId="a",
                    teamBId="b",
                    teamAScore=1,
                    teamBScore=1,
                    matchupType=MatchupType.PLAYOFF,
                )
            )
        self.assertEqual(
            "Playoff and Championship matchups cannot end in a tie.", str(context.exception)
        )

    def test_checkForIllegalMatchupOutcomes_championshipMatchupIsTie_raisesException(self):
        with self.assertRaises(InvalidMatchupFormatException) as context:
            matchupValidation.checkForIllegalMatchupOutcomes(
                Matchup(
                    teamAId="a",
                    teamBId="b",
                    teamAScore=1,
                    teamBScore=1,
                    matchupType=MatchupType.CHAMPIONSHIP,
                )
            )
        self.assertEqual(
            "Playoff and Championship matchups cannot end in a tie.", str(context.exception)
        )

    def test_checkThatTeamIdsAreNotTheSame_teamAIdAndTeamBIdAreTheSame_raisesException(self):
        with self.assertRaises(InvalidMatchupFormatException) as context:
            matchupValidation.checkThatTeamIdsAreNotTheSame(
                Matchup(
                    teamAId="a",
                    teamBId="a",
                    teamAScore=1,
                    teamBScore=1,
                    matchupType=MatchupType.CHAMPIONSHIP,
                )
            )
        self.assertEqual("Team A and Team B cannot have the same ID.", str(context.exception))

    ####################
    # TYPE CHECK TESTS #
    ####################

    def test_checkAllTypes_teamAIdIsntTypeStr_raisesException(self):
        with self.assertRaises(InvalidMatchupFormatException) as context:
            matchupValidation.checkAllTypes(
                Matchup(teamAId=None, teamBId="bId", teamAScore=1, teamBScore=2)
            )
        self.assertEqual("teamAId must be type 'str'.", str(context.exception))

    def test_checkAllTypes_teamBIdIsntTypeStr_raisesException(self):
        with self.assertRaises(InvalidMatchupFormatException) as context:
            matchupValidation.checkAllTypes(
                Matchup(teamAId="aId", teamBId=None, teamAScore=1, teamBScore=2)
            )
        self.assertEqual("teamBId must be type 'str'.", str(context.exception))

    def test_checkAllTypes_teamAScoreIsntTypeFloatOrInt_raisesException(self):
        with self.assertRaises(InvalidMatchupFormatException) as context:
            matchupValidation.checkAllTypes(
                Matchup(teamAId="aId", teamBId="bId", teamAScore=None, teamBScore=2)
            )
        self.assertEqual("teamAScore must be type 'float' or 'int'.", str(context.exception))

    def test_checkAllTypes_teamBScoreIsntTypeFloatOrInt_raisesException(self):
        with self.assertRaises(InvalidMatchupFormatException) as context:
            matchupValidation.checkAllTypes(
                Matchup(teamAId="aId", teamBId="bId", teamAScore=1, teamBScore=None)
            )
        self.assertEqual("teamBScore must be type 'float' or 'int'.", str(context.exception))

    def test_checkAllTypes_matchupTypeIsntTypeMatchup_raisesException(self):
        with self.assertRaises(InvalidMatchupFormatException) as context:
            matchupValidation.checkAllTypes(
                Matchup(teamAId="aId", teamBId="bId", teamAScore=1, teamBScore=2, matchupType=None)
            )
        self.assertEqual("matchupType must be type 'MatchupType'.", str(context.exception))

    def test_checkAllTypes_multiWeekMatchupIsntNoneOrTypeStr_raisesException(self):
        with self.assertRaises(InvalidMatchupFormatException) as context:
            matchupValidation.checkAllTypes(
                Matchup(
                    teamAId="aId",
                    teamBId="bId",
                    teamAScore=1,
                    teamBScore=2,
                    matchupType=MatchupType.REGULAR_SEASON,
                    multiWeekMatchupId=1,
                )
            )
        self.assertEqual("multiWeekMatchupId must be 'None' or type 'str'.", str(context.exception))
