import unittest

from src.leeger.calculator.parent.YearCalculator import YearCalculator
from src.leeger.exception.InvalidFilterException import InvalidFilterException
from src.leeger.model.Matchup import Matchup
from src.leeger.model.Owner import Owner
from src.leeger.model.Team import Team
from src.leeger.model.Week import Week
from src.leeger.model.Year import Year


class TestYearCalculator(unittest.TestCase):

    def test_loadFilters_onlyPostSeasonWrongType_raisesException(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="2")

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup2])

        year = Year(yearNumber=2000, teams=[team1, team2], weeks=[week1, week2])

        with self.assertRaises(InvalidFilterException) as context:
            YearCalculator.loadFilters(year, onlyPostSeason=None)
        self.assertEqual("'onlyPostSeason' must be type 'bool'", str(context.exception))

    def test_loadFilters_onlyRegularSeasonWrongType_raisesException(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="2")

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup2])

        year = Year(yearNumber=2000, teams=[team1, team2], weeks=[week1, week2])

        with self.assertRaises(InvalidFilterException) as context:
            YearCalculator.loadFilters(year, onlyRegularSeason=None)
        self.assertEqual("'onlyRegularSeason' must be type 'bool'", str(context.exception))

    def test_loadFilters_weekNumberStartWrongType_raisesException(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="2")

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup2])

        year = Year(yearNumber=2000, teams=[team1, team2], weeks=[week1, week2])

        with self.assertRaises(InvalidFilterException) as context:
            YearCalculator.loadFilters(year, weekNumberStart=None)
        self.assertEqual("'weekNumberStart' must be type 'int'", str(context.exception))

    def test_loadFilters_weekNumberEndWrongType_raisesException(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="2")

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup2])

        year = Year(yearNumber=2000, teams=[team1, team2], weeks=[week1, week2])

        with self.assertRaises(InvalidFilterException) as context:
            YearCalculator.loadFilters(year, weekNumberEnd=None)
        self.assertEqual("'weekNumberEnd' must be type 'int'", str(context.exception))

    def test_loadFilters_onlyPostSeasonAndOnlyRegularSeasonAreTrue_raisesException(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="2")

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup2])

        year = Year(yearNumber=2000, teams=[team1, team2], weeks=[week1, week2])

        with self.assertRaises(InvalidFilterException) as context:
            YearCalculator.loadFilters(year, onlyPostSeason=True, onlyRegularSeason=True)
        self.assertEqual("'onlyPostSeason' and 'onlyRegularSeason' cannot both be True.", str(context.exception))

    def test_loadFilters_weekNumberStartLessThanOne_raisesException(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="2")

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup2])

        year = Year(yearNumber=2000, teams=[team1, team2], weeks=[week1, week2])

        with self.assertRaises(InvalidFilterException) as context:
            YearCalculator.loadFilters(year, weekNumberStart=0)
        self.assertEqual("'weekNumberStart' cannot be less than 1.", str(context.exception))

    def test_loadFilters_weekNumberEndGreaterThanNumberOfWeeks_raisesException(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="2")

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup2])

        year = Year(yearNumber=2000, teams=[team1, team2], weeks=[week1, week2])

        with self.assertRaises(InvalidFilterException) as context:
            YearCalculator.loadFilters(year, weekNumberEnd=3)
        self.assertEqual("'weekNumberEnd' cannot be greater than the number of weeks in the year.",
                         str(context.exception))

    def test_loadFilters_weekNumberStartGreaterThanWeekNumberEnd_raisesException(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="2")

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup2])

        year = Year(yearNumber=2000, teams=[team1, team2], weeks=[week1, week2])

        with self.assertRaises(InvalidFilterException) as context:
            YearCalculator.loadFilters(year, weekNumberStart=2, weekNumberEnd=1)
        self.assertEqual("'weekNumberEnd' cannot be greater than 'weekNumberStart'.", str(context.exception))
