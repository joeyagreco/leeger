import unittest

from src.leeger.enum.MatchupType import MatchupType
from src.leeger.model.filter.YearFilters import YearFilters
from src.leeger.model.league.Matchup import Matchup
from src.leeger.model.league.Owner import Owner
from src.leeger.model.league.Team import Team
from src.leeger.model.league.Week import Week
from src.leeger.model.league.Year import Year
from src.leeger.util.Deci import Deci
from src.leeger.util.YearNavigator import YearNavigator
from test.helper.prototypes import getNDefaultOwnersAndTeams


class TestYearNavigator(unittest.TestCase):
    def test_getYearByYearNumber_happyPath(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")

        a_team1 = Team(ownerId=owner1.id, name="1")
        a_team2 = Team(ownerId=owner2.id, name="2")

        a_matchup1 = Matchup(teamAId=a_team1.id, teamBId=a_team2.id, teamAScore=1, teamBScore=2)
        a_matchup2 = Matchup(teamAId=a_team1.id, teamBId=a_team2.id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.PLAYOFF)
        a_matchup3 = Matchup(teamAId=a_team1.id, teamBId=a_team2.id, teamAScore=1, teamBScore=1,
                             teamAHasTiebreaker=True, matchupType=MatchupType.PLAYOFF)
        a_matchup4 = Matchup(teamAId=a_team1.id, teamBId=a_team2.id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.CHAMPIONSHIP)

        a_week1 = Week(weekNumber=1, matchups=[a_matchup1])
        a_week2 = Week(weekNumber=2, matchups=[a_matchup2])
        a_week3 = Week(weekNumber=3, matchups=[a_matchup3])
        a_week4 = Week(weekNumber=4, matchups=[a_matchup4])

        a_year = Year(yearNumber=2000, teams=[a_team1, a_team2], weeks=[a_week1, a_week2, a_week3, a_week4])

        response = YearNavigator.getAllTeamIds(a_year)

        self.assertIsInstance(response, list)
        self.assertEqual(2, len(response))
        self.assertEqual(a_team1.id, response[0])
        self.assertEqual(a_team2.id, response[1])

    def test_getNumberOfGamesPlayed_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2])

        yearFilters = YearFilters(weekNumberStart=1, weekNumberEnd=2,
                                  includeMatchupTypes=[MatchupType.REGULAR_SEASON, MatchupType.PLAYOFF,
                                                       MatchupType.CHAMPIONSHIP])
        response = YearNavigator.getNumberOfGamesPlayed(year, yearFilters)

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

        yearFilters = YearFilters(weekNumberStart=1, weekNumberEnd=3,
                                  includeMatchupTypes=[MatchupType.PLAYOFF, MatchupType.CHAMPIONSHIP])
        response = YearNavigator.getNumberOfGamesPlayed(year, yearFilters)

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

        yearFilters = YearFilters(weekNumberStart=1, weekNumberEnd=3, includeMatchupTypes=[MatchupType.REGULAR_SEASON])
        response = YearNavigator.getNumberOfGamesPlayed(year, yearFilters)

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

        yearFilters = YearFilters(weekNumberStart=2, weekNumberEnd=3,
                                  includeMatchupTypes=[MatchupType.REGULAR_SEASON, MatchupType.PLAYOFF,
                                                       MatchupType.CHAMPIONSHIP])
        response = YearNavigator.getNumberOfGamesPlayed(year, yearFilters)

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

        yearFilters = YearFilters(weekNumberStart=1, weekNumberEnd=2,
                                  includeMatchupTypes=[MatchupType.REGULAR_SEASON, MatchupType.PLAYOFF,
                                                       MatchupType.CHAMPIONSHIP])
        response = YearNavigator.getNumberOfGamesPlayed(year, yearFilters)

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

        yearFilters = YearFilters(weekNumberStart=2, weekNumberEnd=3,
                                  includeMatchupTypes=[MatchupType.REGULAR_SEASON, MatchupType.PLAYOFF,
                                                       MatchupType.CHAMPIONSHIP])
        response = YearNavigator.getNumberOfGamesPlayed(year, yearFilters)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Deci("2"), response[teams[0].id])
        self.assertEqual(Deci("2"), response[teams[1].id])
