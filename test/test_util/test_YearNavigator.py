import unittest

from src.leeger.model.Matchup import Matchup
from src.leeger.model.Owner import Owner
from src.leeger.model.Team import Team
from src.leeger.model.Week import Week
from src.leeger.model.Year import Year
from src.leeger.util.YearNavigator import YearNavigator


class TestYearNavigator(unittest.TestCase):
    def test_getYearByYearNumber_happyPath(self):
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

        response = YearNavigator.getAllTeamIds(a_year)

        self.assertIsInstance(response, list)
        self.assertEqual(2, len(response))
        self.assertEqual(a_team1.id, response[0])
        self.assertEqual(a_team2.id, response[1])
