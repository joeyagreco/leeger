import unittest

from src.leeger.decorator.validate.validators import validateLeague
from src.leeger.exception.InvalidMatchupFormatException import InvalidMatchupFormatException
from src.leeger.model.League import League
from src.leeger.model.Matchup import Matchup
from src.leeger.model.Owner import Owner
from src.leeger.model.Team import Team
from src.leeger.model.Week import Week
from src.leeger.model.Year import Year


class TestMatchupValidation(unittest.TestCase):

    @validateLeague
    def dummyFunction(self, league: League, **kwargs):
        """
        This is used to represent any function that can be wrapped by @validateLeague.
        """
        ...

    def test_validateLeague_matchupTeamAIdIsntTypeStr_raisesException(self):
        owner = Owner(name="TEST")
        team = Team(ownerId="id", name="name")
        matchup = Matchup(teamAId=None, teamBId="bId", teamAScore=1, teamBScore=2)
        week = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup])
        year = Year(yearNumber=2000, teams=[team], weeks=[week])
        with self.assertRaises(InvalidMatchupFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=[owner], years=[year]))
        self.assertEqual("Matchup teamAId must be type 'str'.", str(context.exception))

    def test_validateLeague_matchupTeamBIdIsntTypeStr_raisesException(self):
        owner = Owner(name="TEST")
        team = Team(ownerId="id", name="name")
        matchup = Matchup(teamAId="aId", teamBId=None, teamAScore=1, teamBScore=2)
        week = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup])
        year = Year(yearNumber=2000, teams=[team], weeks=[week])
        with self.assertRaises(InvalidMatchupFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=[owner], years=[year]))
        self.assertEqual("Matchup teamBId must be type 'str'.", str(context.exception))

    def test_validateLeague_matchupTeamAScoreIsntTypeFloatOrInt_raisesException(self):
        owner = Owner(name="TEST")
        team = Team(ownerId="id", name="name")
        matchup = Matchup(teamAId="aId", teamBId="bId", teamAScore=None, teamBScore=2)
        week = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup])
        year = Year(yearNumber=2000, teams=[team], weeks=[week])
        with self.assertRaises(InvalidMatchupFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=[owner], years=[year]))
        self.assertEqual("Matchup teamAScore must be type 'float' or 'int'.", str(context.exception))

    def test_validateLeague_matchupTeamBScoreIsntTypeFloatOrInt_raisesException(self):
        owner = Owner(name="TEST")
        team = Team(ownerId="id", name="name")
        matchup = Matchup(teamAId="aId", teamBId="bId", teamAScore=1, teamBScore=None)
        week = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup])
        year = Year(yearNumber=2000, teams=[team], weeks=[week])
        with self.assertRaises(InvalidMatchupFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=[owner], years=[year]))
        self.assertEqual("Matchup teamBScore must be type 'float' or 'int'.", str(context.exception))

    def test_validateLeague_matchupTeamAHasTiebreakerIsntTypeBool_raisesException(self):
        owner = Owner(name="TEST")
        team = Team(ownerId="id", name="name")
        matchup = Matchup(teamAId="aId", teamBId="bId", teamAScore=1, teamBScore=2, teamAHasTiebreaker=None)
        week = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup])
        year = Year(yearNumber=2000, teams=[team], weeks=[week])
        with self.assertRaises(InvalidMatchupFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=[owner], years=[year]))
        self.assertEqual("Matchup teamAHasTiebreaker must be type 'bool'.", str(context.exception))

    def test_validateLeague_matchupTeamBHasTiebreakerIsntTypeBool_raisesException(self):
        owner = Owner(name="TEST")
        team = Team(ownerId="id", name="name")
        matchup = Matchup(teamAId="aId", teamBId="bId", teamAScore=1, teamBScore=2, teamBHasTiebreaker=None)
        week = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup])
        year = Year(yearNumber=2000, teams=[team], weeks=[week])
        with self.assertRaises(InvalidMatchupFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=[owner], years=[year]))
        self.assertEqual("Matchup teamBHasTiebreaker must be type 'bool'.", str(context.exception))
