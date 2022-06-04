import unittest

from src.leeger.decorator.statCalculator import statCalculator
from src.leeger.exception.InvalidMatchupFormatException import InvalidMatchupFormatException
from src.leeger.exception.InvalidWeekFormatException import InvalidWeekFormatException
from src.leeger.exception.InvalidYearFormatException import InvalidYearFormatException
from src.leeger.model.League import League
from src.leeger.model.Matchup import Matchup
from src.leeger.model.Owner import Owner
from src.leeger.model.Team import Team
from src.leeger.model.Week import Week
from src.leeger.model.Year import Year


class TestStatCalculator(unittest.TestCase):

    @statCalculator
    def dummyFunction(self, league: League):
        """
        This is used to represent any function that can be wrapped by @statCalculator.
        """
        ...

    def test_statCalculator_happyPath(self):
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

    def test_statCalculator_twoChampionshipWeeksInYear_raisesException(self):
        week1 = Week(weekNumber=1, isPlayoffWeek=True, isChampionshipWeek=True, matchups=list())
        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=True, matchups=list())
        year = Year(yearNumber=2000, teams=list(), weeks=[week1, week2])

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[year]))
        self.assertEqual("Year 2000 has more than 1 championship week.", str(context.exception))

    def test_statCalculator_yearHasNoWeeks_raisesException(self):
        year = Year(yearNumber=2000, teams=list(), weeks=list())

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[year]))
        self.assertEqual("Year 2000 does not have at least 1 week.", str(context.exception))

    def test_statCalculator_yearDuplicateWeekNumbers_raisesException(self):
        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        week1duplicate = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        year = Year(yearNumber=2000, teams=list(), weeks=[week1, week1duplicate])

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[year]))
        self.assertEqual("Year 2000 has duplicate week numbers.", str(context.exception))

    def test_statCalculator_lowestWeekNumberIsNotOne_raisesException(self):
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        year = Year(yearNumber=2000, teams=list(), weeks=[week2])

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[year]))
        self.assertEqual("First week in year 2000 must be 1, not 2.", str(context.exception))

    def test_statCalculator_weekNumbersNotOneThroughN_raisesException(self):
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

    def test_statCalculator_nonPlayoffWeekAfterPlayoffWeek_raisesException(self):
        week1 = Week(weekNumber=1, isPlayoffWeek=True, isChampionshipWeek=False, matchups=list())
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        year = Year(yearNumber=2000, teams=list(), weeks=[week1, week2])

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[year]))
        self.assertEqual("Year 2000 has a non-playoff week after a playoff week.", str(context.exception))

    def test_statCalculator_nonChampionshipWeekAfterChampionshipWeek_raisesException(self):
        week1 = Week(weekNumber=1, isPlayoffWeek=True, isChampionshipWeek=True, matchups=list())
        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False, matchups=list())
        year = Year(yearNumber=2000, teams=list(), weeks=[week1, week2])

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[year]))
        self.assertEqual("Year 2000 has a non-championship week after a championship week.", str(context.exception))

    def test_statCalculator_yearHasLessThanTwoTeams_raisesException(self):
        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        team1 = Team(ownerId="1", name="1")
        year = Year(yearNumber=2000, teams=[team1], weeks=[week1, week2])

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[year]))
        self.assertEqual("Year 2000 needs at least 2 teams.", str(context.exception))

    def test_statCalculator_yearNumberIsntInValidRange_raisesException(self):
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

    def test_statCalculator_teamsHaveDuplicateOwnerIds_raisesException(self):
        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        team1 = Team(ownerId="1", name="1")
        team2 = Team(ownerId="1", name="2")
        year = Year(yearNumber=2000, teams=[team1, team2], weeks=[week1])

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[year]))
        self.assertEqual("Year 2000 has teams with the same owner IDs.", str(context.exception))

    def test_statCalculator_teamsHaveIdsThatDontMatchLeagueOwnerIds_raisesException(self):
        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())
        team1 = Team(ownerId="1", name="1")
        team2 = Team(ownerId="2", name="2")
        year = Year(yearNumber=2000, teams=[team1, team2], weeks=[week1])

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=list(), years=[year]))
        self.assertEqual("Year 2000 has teams with owner IDs that do not match the League's owner IDs: ['1', '2'].",
                         str(context.exception))

    def test_statCalculator_teamsInAYearHaveDuplicateNames_raisesException(self):
        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())

        owner1 = Owner(name="1")
        owner2 = Owner(name="2")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="1")
        year = Year(yearNumber=2000, teams=[team1, team2], weeks=[week1])

        with self.assertRaises(InvalidYearFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=[owner1, owner2], years=[year]))
        self.assertEqual("Year 2000 has teams with duplicate names.", str(context.exception))

    def test_statCalculator_weekDoesntHaveAtLeastOneMatchup_raisesException(self):
        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=list())

        owner1 = Owner(name="1")
        owner2 = Owner(name="2")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="2")
        year = Year(yearNumber=2000, teams=[team1, team2], weeks=[week1])

        with self.assertRaises(InvalidWeekFormatException) as context:
            self.dummyFunction(League(name="TEST", owners=[owner1, owner2], years=[year]))
        self.assertEqual("Year 2000 must have at least 1 matchup.", str(context.exception))

    def test_statCalculator_matchupDoesntHaveTeamIdsThatMatchYearTeamIds_raisesException(self):
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
