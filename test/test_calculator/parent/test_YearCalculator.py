import unittest

from src.leeger.calculator.parent.YearCalculator import YearCalculator
from src.leeger.enum.MatchupType import MatchupType
from src.leeger.exception.InvalidFilterException import InvalidFilterException
from src.leeger.model.Matchup import Matchup
from src.leeger.model.Owner import Owner
from src.leeger.model.Team import Team
from src.leeger.model.Week import Week
from src.leeger.model.Year import Year
from src.leeger.util.Deci import Deci
from test.helper.prototypes import getNDefaultOwnersAndTeams


class TestYearCalculator(unittest.TestCase):

    def test_getFilters_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2])

        yearFilters1 = YearCalculator.getFilters(year, onlyPostSeason=True)
        yearFilters2 = YearCalculator.getFilters(year, onlyRegularSeason=True)
        yearFilters3 = YearCalculator.getFilters(year, weekNumberStart=2)
        yearFilters4 = YearCalculator.getFilters(year, weekNumberEnd=1)

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
            YearCalculator.getFilters(year, onlyPostSeason=None)
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
            YearCalculator.getFilters(year, onlyRegularSeason=None)
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
            YearCalculator.getFilters(year, weekNumberStart=None)
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
            YearCalculator.getFilters(year, weekNumberEnd=None)
        self.assertEqual("'weekNumberEnd' must be type 'int'", str(context.exception))

    def test_getFilters_onlyPostSeasonAndOnlyRegularSeasonAreTrue_raisesException(self):
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
            YearCalculator.getFilters(year, onlyPostSeason=True, onlyRegularSeason=True)
        self.assertEqual("'onlyPostSeason' and 'onlyRegularSeason' cannot both be True.", str(context.exception))

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
            YearCalculator.getFilters(year, weekNumberStart=0)
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
            YearCalculator.getFilters(year, weekNumberEnd=3)
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
            YearCalculator.getFilters(year, weekNumberStart=2, weekNumberEnd=1)
        self.assertEqual("'weekNumberEnd' cannot be greater than 'weekNumberStart'.", str(context.exception))

    def test_getNumberOfGamesPlayed_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2])

        response = YearCalculator.getNumberOfGamesPlayed(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("2"), response[teams[0].id])
        self.assertEqual(Deci("2"), response[teams[1].id])

    def test_getNumberOfGamesPlayed_onlyPostSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = YearCalculator.getNumberOfGamesPlayed(year, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("2"), response[teams[0].id])
        self.assertEqual(Deci("2"), response[teams[1].id])

    def test_getNumberOfGamesPlayed_onlyRegularSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = YearCalculator.getNumberOfGamesPlayed(year, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("1"), response[teams[0].id])
        self.assertEqual(Deci("1"), response[teams[1].id])

    def test_getNumberOfGamesPlayed_weekNumberStartGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = YearCalculator.getNumberOfGamesPlayed(year, weekNumberStart=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("2"), response[teams[0].id])
        self.assertEqual(Deci("2"), response[teams[1].id])

    def test_getNumberOfGamesPlayed_weekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = YearCalculator.getNumberOfGamesPlayed(year, weekNumberEnd=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("2"), response[teams[0].id])
        self.assertEqual(Deci("2"), response[teams[1].id])

    def test_getNumberOfGamesPlayed_weekNumberStartGivenAndWeekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        matchup4 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])
        week4 = Week(weekNumber=4, matchups=[matchup4])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3, week4])

        response = YearCalculator.getNumberOfGamesPlayed(year, weekNumberStart=2, weekNumberEnd=3)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("2"), response[teams[0].id])
        self.assertEqual(Deci("2"), response[teams[1].id])
