import unittest

from src.leeger.decorator.validateLeague import validateLeague
from src.leeger.exception.InvalidLeagueFormatException import InvalidLeagueFormatException
from src.leeger.exception.InvalidMatchupFormatException import InvalidMatchupFormatException
from src.leeger.exception.InvalidOwnerFormatException import InvalidOwnerFormatException
from src.leeger.exception.InvalidTeamFormatException import InvalidTeamFormatException
from src.leeger.exception.InvalidWeekFormatException import InvalidWeekFormatException
from src.leeger.exception.InvalidYearFormatException import InvalidYearFormatException
from src.leeger.model.League import League
from src.leeger.model.Matchup import Matchup
from src.leeger.model.Owner import Owner
from src.leeger.model.Team import Team
from src.leeger.model.Week import Week
from src.leeger.model.Year import Year


class TestValidateLeague(unittest.TestCase):

    @validateLeague
    def dummyFunction(self, league: League):
        """
        This is used to represent any function that can be wrapped by @statCalculator.
        """
        ...

    def test_validateLeague_happyPath(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="2")

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup3 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])
        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[matchup2])
        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=True, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[team1, team2], weeks=[week1, week2, week3])

        self.dummyFunction(League(name="TEST", owners=[owner1, owner2], years=[year]))

    def test_validateLeague_twoChampionshipWeeksInYear_raisesException(self):
        week1 = Week(weekNumber=1, isPlayoffWeek=True, isChampionshipWeek=True, matchups=list())
        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=True, matchups=list())
        year = Year(yearNumber=2000, teams=list(), weeks=[week1, week2])

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[year]))
        self.assertEqual("Year 2000 has more than 1 championship week.", str(context.exception))

    def test_validateLeague_yearHasNoWeeks_raisesException(self):
        year = Year(yearNumber=2000, teams=list(), weeks=list())

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[year]))
        self.assertEqual("Year 2000 does not have at least 1 week.", str(context.exception))

    def test_validateLeague_yearDuplicateWeekNumbers_raisesException(self):
        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        week1duplicate = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        year = Year(yearNumber=2000, teams=list(), weeks=[week1, week1duplicate])

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[year]))
        self.assertEqual("Year 2000 has duplicate week numbers.", str(context.exception))

    def test_validateLeague_lowestWeekNumberIsNotOne_raisesException(self):
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        year = Year(yearNumber=2000, teams=list(), weeks=[week2])

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[year]))
        self.assertEqual("First week in year 2000 must be 1, not 2.", str(context.exception))

    def test_validateLeague_weekNumbersNotOneThroughN_raisesException(self):
        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        week3 = Week(weekNumber=3, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        week4 = Week(weekNumber=4, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        year = Year(yearNumber=2000, teams=list(), weeks=[week1, week2, week4])  # no week 3

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[year]))
        self.assertEqual("Year 2000 does not have week numbers in order (1-n).", str(context.exception))

        year = Year(yearNumber=2000, teams=list(), weeks=[week1, week2, week4, week3])  # weeks not in order
        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[year]))
        self.assertEqual("Year 2000 does not have week numbers in order (1-n).", str(context.exception))

    def test_validateLeague_nonPlayoffWeekAfterPlayoffWeek_raisesException(self):
        week1 = Week(weekNumber=1, isPlayoffWeek=True, isChampionshipWeek=False, matchups=list())
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        year = Year(yearNumber=2000, teams=list(), weeks=[week1, week2])

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[year]))
        self.assertEqual("Year 2000 has a non-playoff week after a playoff week.", str(context.exception))

    def test_validateLeague_nonChampionshipWeekAfterChampionshipWeek_raisesException(self):
        week1 = Week(weekNumber=1, isPlayoffWeek=True, isChampionshipWeek=True, matchups=list())
        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False, matchups=list())
        year = Year(yearNumber=2000, teams=list(), weeks=[week1, week2])

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[year]))
        self.assertEqual("Year 2000 has a non-championship week after a championship week.", str(context.exception))

    def test_validateLeague_yearHasLessThanTwoTeams_raisesException(self):
        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        team1 = Team(ownerId="1", name="1")
        year = Year(yearNumber=2000, teams=[team1], weeks=[week1, week2])

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[year]))
        self.assertEqual("Year 2000 needs at least 2 teams.", str(context.exception))

    def test_validateLeague_yearNumberIsntInValidRange_raisesException(self):
        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        team1 = Team(ownerId="1", name="1")
        team2 = Team(ownerId="2", name="2")
        year = Year(yearNumber=1919, teams=[team1, team2], weeks=[week1])

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[year]))
        self.assertEqual("Year 1919 is not in range 1920-2XXX.", str(context.exception))

        year = Year(yearNumber=3000, teams=[team1, team2], weeks=[week1])

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[year]))
        self.assertEqual("Year 3000 is not in range 1920-2XXX.", str(context.exception))

    def test_validateLeague_yearsArentInCorrectOrder_raisesException(self):
        a_week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        a_team1 = Team(ownerId="1", name="1")
        a_team2 = Team(ownerId="2", name="2")
        a_year = Year(yearNumber=2000, teams=[a_team1, a_team2], weeks=[a_week1])

        b_week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        b_team1 = Team(ownerId="1", name="1")
        b_team2 = Team(ownerId="2", name="2")
        b_year = Year(yearNumber=2001, teams=[b_team1, b_team2], weeks=[b_week1])

        with self.assertRaises(InvalidYearFormatException) as context:
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

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[a_year, b_year]))
        self.assertEqual("Can only have 1 of each year number within a league.", str(context.exception))

    def test_validateLeague_teamsHaveDuplicateOwnerIds_raisesException(self):
        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        team1 = Team(ownerId="1", name="1")
        team2 = Team(ownerId="1", name="2")
        year = Year(yearNumber=2000, teams=[team1, team2], weeks=[week1])

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[year]))
        self.assertEqual("Year 2000 has teams with the same owner IDs.", str(context.exception))

    def test_validateLeague_teamsHaveIdsThatDontMatchLeagueOwnerIds_raisesException(self):
        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        team1 = Team(ownerId="1", name="1")
        team2 = Team(ownerId="2", name="2")
        year = Year(yearNumber=2000, teams=[team1, team2], weeks=[week1])

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[year]))
        self.assertEqual("Year 2000 has teams with owner IDs that do not match the League's owner IDs: ['1', '2'].",
                         str(context.exception))

    def test_validateLeague_teamsInAYearHaveDuplicateNames_raisesException(self):
        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())

        owner1 = Owner(name="1")
        owner2 = Owner(name="2")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="1")
        year = Year(yearNumber=2000, teams=[team1, team2], weeks=[week1])

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=[owner1, owner2], years=[year]))
        self.assertEqual("Year 2000 has teams with duplicate names.", str(context.exception))

    def test_validateLeague_weekDoesntHaveAtLeastOneMatchup_raisesException(self):
        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())

        owner1 = Owner(name="1")
        owner2 = Owner(name="2")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="2")
        year = Year(yearNumber=2000, teams=[team1, team2], weeks=[week1])

        with self.assertRaises(InvalidWeekFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=[owner1, owner2], years=[year]))
        self.assertEqual("Year 2000 must have at least 1 matchup.", str(context.exception))

    def test_validateLeague_matchupDoesntHaveTeamIdsThatMatchYearTeamIds_raisesException(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="2")

        matchup1 = Matchup(teamAId="A", teamBId="B", teamAScore=1, teamBScore=2)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])

        year = Year(yearNumber=2000, teams=[team1, team2], weeks=[week1])

        with self.assertRaises(InvalidMatchupFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=[owner1, owner2], years=[year]))
        self.assertEqual("Year 2000 Week 1 has a matchup with team IDs that do not match the Year's team IDs.",
                         str(context.exception))

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

    def test_validateLeague_ownerNameIsntTypeStr_raisesException(self):
        owner = Owner(name=None)
        with self.assertRaises(InvalidOwnerFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=[owner], years=list()))
        self.assertEqual("Owner name must be type 'str'.", str(context.exception))

    def test_validateLeague_yearNumberIsntTypeInt_raisesException(self):
        owner = Owner(name="TEST")
        year = Year(yearNumber=None, teams=list(), weeks=list())
        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=[owner], years=[year]))
        self.assertEqual("Year number must be type 'int'.", str(context.exception))

    def test_validateLeague_yearTeamsIsntTypeList_raisesException(self):
        owner = Owner(name="TEST")
        year = Year(yearNumber=2000, teams=None, weeks=list())
        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=[owner], years=[year]))
        self.assertEqual("Year teams must be type 'list'.", str(context.exception))

    def test_validateLeague_yearWeeksIsntTypeList_raisesException(self):
        owner = Owner(name="TEST")
        year = Year(yearNumber=2000, teams=list(), weeks=None)
        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=[owner], years=[year]))
        self.assertEqual("Year weeks must be type 'list'.", str(context.exception))

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

    def test_validateLeague_weekNumberIsntTypeInt_raisesException(self):
        owner = Owner(name="TEST")
        team = Team(ownerId="id", name="name")
        week = Week(weekNumber=None, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        year = Year(yearNumber=2000, teams=[team], weeks=[week])
        with self.assertRaises(InvalidWeekFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=[owner], years=[year]))
        self.assertEqual("Week number must be type 'int'.", str(context.exception))

    def test_validateLeague_weekisPlayoffWeekIsntTypeBool_raisesException(self):
        owner = Owner(name="TEST")
        team = Team(ownerId="id", name="name")
        week = Week(weekNumber=1, isPlayoffWeek=None, isChampionshipWeek=False, matchups=list())
        year = Year(yearNumber=2000, teams=[team], weeks=[week])
        with self.assertRaises(InvalidWeekFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=[owner], years=[year]))
        self.assertEqual("Week isPlayoffWeek must be type 'bool'.", str(context.exception))

    def test_validateLeague_weekisChampionshipWeekIsntTypeBool_raisesException(self):
        owner = Owner(name="TEST")
        team = Team(ownerId="id", name="name")
        week = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=None, matchups=list())
        year = Year(yearNumber=2000, teams=[team], weeks=[week])
        with self.assertRaises(InvalidWeekFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=[owner], years=[year]))
        self.assertEqual("Week isChampionshipWeek must be type 'bool'.", str(context.exception))

    def test_validateLeague_weekMatchupsIsntTypeList_raisesException(self):
        owner = Owner(name="TEST")
        team = Team(ownerId="id", name="name")
        week = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=None)
        year = Year(yearNumber=2000, teams=[team], weeks=[week])
        with self.assertRaises(InvalidWeekFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=[owner], years=[year]))
        self.assertEqual("Week matchups must be type 'list'.", str(context.exception))

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
