import unittest

from src.leeger.decorator.validate.validators import validateLeague
from src.leeger.exception.InvalidLeagueFormatException import InvalidLeagueFormatException
from src.leeger.model.League import League
from src.leeger.model.Matchup import Matchup
from src.leeger.model.Owner import Owner
from src.leeger.model.Team import Team
from src.leeger.model.Week import Week
from src.leeger.model.Year import Year


class TestLeagueValidation(unittest.TestCase):

    @validateLeague
    def dummyFunction(self, league: League, **kwargs):
        """
        This is used to represent any function that can be wrapped by @validateLeague.
        """
        ...

    def test_validateLeague_happyPath(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")

        a_team1 = Team(ownerId=owner1.id, name="1")
        a_team2 = Team(ownerId=owner2.id, name="2")

        a_matchup1 = Matchup(teamAId=a_team1.id, teamBId=a_team2.id, teamAScore=1, teamBScore=2)
        a_matchup2 = Matchup(teamAId=a_team1.id, teamBId=a_team2.id, teamAScore=1, teamBScore=2)
        a_matchup3 = Matchup(teamAId=a_team1.id, teamBId=a_team2.id, teamAScore=1, teamBScore=1,
                             teamAHasTiebreaker=True)
        a_matchup4 = Matchup(teamAId=a_team1.id, teamBId=a_team2.id, teamAScore=1, teamBScore=2)

        a_week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[a_matchup1])
        a_week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[a_matchup2])
        a_week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[a_matchup3])
        a_week4 = Week(weekNumber=4, isPlayoffWeek=True, isChampionshipWeek=True, matchups=[a_matchup4])

        a_year = Year(yearNumber=2000, teams=[a_team1, a_team2], weeks=[a_week1, a_week2, a_week3, a_week4])

        b_team1 = Team(ownerId=owner1.id, name="1")
        b_team2 = Team(ownerId=owner2.id, name="2")

        b_matchup1 = Matchup(teamAId=b_team1.id, teamBId=b_team2.id, teamAScore=1, teamBScore=2)
        b_matchup2 = Matchup(teamAId=b_team1.id, teamBId=b_team2.id, teamAScore=1, teamBScore=2)
        b_matchup3 = Matchup(teamAId=b_team1.id, teamBId=b_team2.id, teamAScore=1, teamBScore=1,
                             teamAHasTiebreaker=True)
        b_matchup4 = Matchup(teamAId=b_team1.id, teamBId=b_team2.id, teamAScore=1, teamBScore=2)

        b_week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[b_matchup1])
        b_week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[b_matchup2])
        b_week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[b_matchup3])
        b_week4 = Week(weekNumber=4, isPlayoffWeek=True, isChampionshipWeek=True, matchups=[b_matchup4])

        b_year = Year(yearNumber=2001, teams=[b_team1, b_team2], weeks=[b_week1, b_week2, b_week3, b_week4])

        self.dummyFunction(League(name="TEST", owners=[owner1, owner2], years=[a_year, b_year]))

    def test_validateLeague_yearsArentInCorrectOrder_raisesException(self):
        a_week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        a_team1 = Team(ownerId="1", name="1")
        a_team2 = Team(ownerId="2", name="2")
        a_year = Year(yearNumber=2000, teams=[a_team1, a_team2], weeks=[a_week1])

        b_week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        b_team1 = Team(ownerId="1", name="1")
        b_team2 = Team(ownerId="2", name="2")
        b_year = Year(yearNumber=2001, teams=[b_team1, b_team2], weeks=[b_week1])

        with self.assertRaises(InvalidLeagueFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[b_year, a_year]))
        self.assertEqual("Years are not in chronological order (oldest -> newest).", str(context.exception))

    def test_validateLeague_duplicateYearNumbers_raisesException(self):
        a_week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        a_team1 = Team(ownerId="1", name="1")
        a_team2 = Team(ownerId="2", name="2")
        a_year = Year(yearNumber=2000, teams=[a_team1, a_team2], weeks=[a_week1])

        b_week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        b_team1 = Team(ownerId="1", name="1")
        b_team2 = Team(ownerId="2", name="2")
        b_year = Year(yearNumber=2000, teams=[b_team1, b_team2], weeks=[b_week1])

        with self.assertRaises(InvalidLeagueFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[a_year, b_year]))
        self.assertEqual("Can only have 1 of each year number within a league.", str(context.exception))

    """
    TYPE CHECK TESTS
    """

    def test_validateLeague_leagueNameIsntTypeString_raisesException(self):
        with self.assertRaises(InvalidLeagueFormatException) as context:
            self.dummyFunction(League(name=None, owners=list(), years=list()))
        self.assertEqual("League name must be type 'str'.", str(context.exception))

    def test_validateLeague_leagueOwnersIsntTypeList_raisesException(self):
        with self.assertRaises(InvalidLeagueFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=None, years=list()))
        self.assertEqual("League owners must be type 'list'.", str(context.exception))

    def test_validateLeague_leagueYearsIsntTypeList_raisesException(self):
        with self.assertRaises(InvalidLeagueFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=None))
        self.assertEqual("League years must be type 'list'.", str(context.exception))
