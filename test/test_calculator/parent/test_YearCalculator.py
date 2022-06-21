import unittest

from src.leeger.calculator.parent.YearCalculator import YearCalculator
from src.leeger.enum.MatchupType import MatchupType
from src.leeger.exception.InvalidFilterException import InvalidFilterException
from src.leeger.model.Matchup import Matchup
from src.leeger.model.Owner import Owner
from src.leeger.model.Team import Team
from src.leeger.model.Week import Week
from src.leeger.model.Year import Year
from test.helper.prototypes import getNDefaultOwnersAndTeams


class TestYearCalculator(unittest.TestCase):

    def test_getFilters_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2])

        yearFilters1 = YearCalculator.getYearFilters(year, onlyPostSeason=True)
        yearFilters2 = YearCalculator.getYearFilters(year, onlyRegularSeason=True)
        yearFilters3 = YearCalculator.getYearFilters(year, weekNumberStart=2)
        yearFilters4 = YearCalculator.getYearFilters(year, weekNumberEnd=1)

        self.assertEqual([MatchupType.PLAYOFF, MatchupType.CHAMPIONSHIP], yearFilters1.includeMatchupTypes)
        self.assertEqual(1, yearFilters1.weekNumberStart)
        self.assertEqual(2, yearFilters1.weekNumberEnd)
        self.assertEqual([MatchupType.REGULAR_SEASON], yearFilters2.includeMatchupTypes)
        self.assertEqual(1, yearFilters2.weekNumberStart)
        self.assertEqual(2, yearFilters2.weekNumberEnd)
        self.assertEqual([MatchupType.REGULAR_SEASON, MatchupType.PLAYOFF, MatchupType.CHAMPIONSHIP],
                         yearFilters3.includeMatchupTypes)
        self.assertEqual(2, yearFilters3.weekNumberStart)
        self.assertEqual(2, yearFilters3.weekNumberEnd)
        self.assertEqual([MatchupType.REGULAR_SEASON, MatchupType.PLAYOFF, MatchupType.CHAMPIONSHIP],
                         yearFilters4.includeMatchupTypes)
        self.assertEqual(1, yearFilters4.weekNumberStart)
        self.assertEqual(1, yearFilters4.weekNumberEnd)

    def test_getFilters_onlyChampionshipWrongType_raisesException(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="2")

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])

        year = Year(yearNumber=2000, teams=[team1, team2], weeks=[week1, week2])

        with self.assertRaises(InvalidFilterException) as context:
            YearCalculator.getYearFilters(year, onlyChampionship=None)
        self.assertEqual("'onlyChampionship' must be type 'bool'", str(context.exception))

    def test_getFilters_onlyPostSeasonWrongType_raisesException(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="2")

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])

        year = Year(yearNumber=2000, teams=[team1, team2], weeks=[week1, week2])

        with self.assertRaises(InvalidFilterException) as context:
            YearCalculator.getYearFilters(year, onlyPostSeason=None)
        self.assertEqual("'onlyPostSeason' must be type 'bool'", str(context.exception))

    def test_getFilters_onlyRegularSeasonWrongType_raisesException(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="2")

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])

        year = Year(yearNumber=2000, teams=[team1, team2], weeks=[week1, week2])

        with self.assertRaises(InvalidFilterException) as context:
            YearCalculator.getYearFilters(year, onlyRegularSeason=None)
        self.assertEqual("'onlyRegularSeason' must be type 'bool'", str(context.exception))

    def test_getFilters_weekNumberStartWrongType_raisesException(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="2")

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])

        year = Year(yearNumber=2000, teams=[team1, team2], weeks=[week1, week2])

        with self.assertRaises(InvalidFilterException) as context:
            YearCalculator.getYearFilters(year, weekNumberStart=None)
        self.assertEqual("'weekNumberStart' must be type 'int'", str(context.exception))

    def test_getFilters_weekNumberEndWrongType_raisesException(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="2")

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])

        year = Year(yearNumber=2000, teams=[team1, team2], weeks=[week1, week2])

        with self.assertRaises(InvalidFilterException) as context:
            YearCalculator.getYearFilters(year, weekNumberEnd=None)
        self.assertEqual("'weekNumberEnd' must be type 'int'", str(context.exception))

    def test_getFilters_multipleOnlyParametersAreTrue_raisesException(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="2")

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])

        year = Year(yearNumber=2000, teams=[team1, team2], weeks=[week1, week2])

        with self.assertRaises(InvalidFilterException) as context:
            YearCalculator.getYearFilters(year, onlyPostSeason=True, onlyRegularSeason=True)
        self.assertEqual("Only one of 'onlyChampionship', 'onlyPostSeason', 'onlyRegularSeason' can be True",
                         str(context.exception))

        with self.assertRaises(InvalidFilterException) as context:
            YearCalculator.getYearFilters(year, onlyPostSeason=True, onlyChampionship=True)
        self.assertEqual("Only one of 'onlyChampionship', 'onlyPostSeason', 'onlyRegularSeason' can be True",
                         str(context.exception))

        with self.assertRaises(InvalidFilterException) as context:
            YearCalculator.getYearFilters(year, onlyRegularSeason=True, onlyChampionship=True)
        self.assertEqual("Only one of 'onlyChampionship', 'onlyPostSeason', 'onlyRegularSeason' can be True",
                         str(context.exception))

    def test_getFilters_weekNumberStartLessThanOne_raisesException(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="2")

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])

        year = Year(yearNumber=2000, teams=[team1, team2], weeks=[week1, week2])

        with self.assertRaises(InvalidFilterException) as context:
            YearCalculator.getYearFilters(year, weekNumberStart=0)
        self.assertEqual("'weekNumberStart' cannot be less than 1.", str(context.exception))

    def test_getFilters_weekNumberEndGreaterThanNumberOfWeeks_raisesException(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="2")

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])

        year = Year(yearNumber=2000, teams=[team1, team2], weeks=[week1, week2])

        with self.assertRaises(InvalidFilterException) as context:
            YearCalculator.getYearFilters(year, weekNumberEnd=3)
        self.assertEqual("'weekNumberEnd' cannot be greater than the number of weeks in the year.",
                         str(context.exception))

    def test_getFilters_weekNumberStartGreaterThanWeekNumberEnd_raisesException(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="2")

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])

        year = Year(yearNumber=2000, teams=[team1, team2], weeks=[week1, week2])

        with self.assertRaises(InvalidFilterException) as context:
            YearCalculator.getYearFilters(year, weekNumberStart=2, weekNumberEnd=1)
        self.assertEqual("'weekNumberEnd' cannot be greater than 'weekNumberStart'.", str(context.exception))

    def test_getNumberOfValidTeamsInWeek_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.IGNORE)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2])

        response1 = YearCalculator.getNumberOfValidTeamsInWeek(year, 1)
        response2 = YearCalculator.getNumberOfValidTeamsInWeek(year, 2)

        self.assertIsInstance(response1, int)
        self.assertEqual(2, response1)
        self.assertIsInstance(response2, int)
        self.assertEqual(0, response2)

    def test_getNumberOfValidTeamsInWeek_onlyPostSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(4)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1])

        response = YearCalculator.getNumberOfValidTeamsInWeek(year, 1, onlyPostSeason=True)

        self.assertIsInstance(response, int)
        self.assertEqual(4, response)

    def test_getNumberOfValidTeamsInWeek_onlyRegularSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(4)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.REGULAR_SEASON)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.REGULAR_SEASON)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1])

        response = YearCalculator.getNumberOfValidTeamsInWeek(year, 1, onlyRegularSeason=True)

        self.assertIsInstance(response, int)
        self.assertEqual(4, response)
