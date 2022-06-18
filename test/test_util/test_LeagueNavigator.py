import unittest

from src.leeger.enum.MatchupType import MatchupType
from src.leeger.exception.DoesNotExistException import DoesNotExistException
from src.leeger.model.League import League
from src.leeger.model.Matchup import Matchup
from src.leeger.model.Owner import Owner
from src.leeger.model.Team import Team
from src.leeger.model.Week import Week
from src.leeger.model.Year import Year
from src.leeger.util.LeagueNavigator import LeagueNavigator


class TestLeagueNavigator(unittest.TestCase):
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

        b_team1 = Team(ownerId=owner1.id, name="1")
        b_team2 = Team(ownerId=owner2.id, name="2")

        b_matchup1 = Matchup(teamAId=b_team1.id, teamBId=b_team2.id, teamAScore=1, teamBScore=2)
        b_matchup2 = Matchup(teamAId=b_team1.id, teamBId=b_team2.id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.PLAYOFF)
        b_matchup3 = Matchup(teamAId=b_team1.id, teamBId=b_team2.id, teamAScore=1, teamBScore=1,
                             teamAHasTiebreaker=True, matchupType=MatchupType.PLAYOFF)
        b_matchup4 = Matchup(teamAId=b_team1.id, teamBId=b_team2.id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.CHAMPIONSHIP)

        b_week1 = Week(weekNumber=1, matchups=[b_matchup1])
        b_week2 = Week(weekNumber=2, matchups=[b_matchup2])
        b_week3 = Week(weekNumber=3, matchups=[b_matchup3])
        b_week4 = Week(weekNumber=4, matchups=[b_matchup4])

        b_year = Year(yearNumber=2001, teams=[b_team1, b_team2], weeks=[b_week1, b_week2, b_week3, b_week4])

        league = League(name="TEST", owners=[owner1, owner2], years=[a_year, b_year])

        response = LeagueNavigator.getYearByYearNumber(league, 2001)

        self.assertIsInstance(response, Year)
        self.assertEqual(2001, response.yearNumber)

    def test_getYearByYearNumber_yearDoesntExistInLeague_raisesException(self):
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

        league = League(name="TEST", owners=[owner1, owner2], years=[a_year])

        with self.assertRaises(DoesNotExistException) as context:
            LeagueNavigator.getYearByYearNumber(league, 2001)
        self.assertEqual("Year 2001 does not exist in the given League.", str(context.exception))
