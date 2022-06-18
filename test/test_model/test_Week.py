import unittest

from src.leeger.enum.MatchupType import MatchupType
from src.leeger.model.Matchup import Matchup
from src.leeger.model.Week import Week
from test.helper.prototypes import getNDefaultOwnersAndTeams


class TestWeek(unittest.TestCase):
    def test_week_init(self):
        matchup1 = Matchup(teamAId="", teamBId="", teamAScore=0, teamBScore=0, matchupType=MatchupType.REGULAR)
        matchup2 = Matchup(teamAId="", teamBId="", teamAScore=0, teamBScore=0, matchupType=MatchupType.PLAYOFF)
        matchup3 = Matchup(teamAId="", teamBId="", teamAScore=0, teamBScore=0, matchupType=MatchupType.CHAMPIONSHIP)
        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        self.assertEqual(1, week1.weekNumber)
        self.assertFalse(week1.isPlayoffWeek)
        self.assertFalse(week1.isChampionshipWeek)
        self.assertTrue(week2.isPlayoffWeek)
        self.assertFalse(week2.isChampionshipWeek)
        self.assertTrue(week3.isPlayoffWeek)
        self.assertTrue(week3.isChampionshipWeek)
        self.assertEqual(1, len(week1.matchups))
        self.assertEqual(matchup1.id, week1.matchups[0].id)
        self.assertEqual(matchup2.id, week2.matchups[0].id)
        self.assertEqual(matchup3.id, week3.matchups[0].id)

    def test_isPlayoffWeek_weekHasPlayoffMatchups_returnsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)

        week1 = Week(weekNumber=1, matchups=[matchup1])

        response = week1.isPlayoffWeek

        self.assertIsInstance(response, bool)
        self.assertTrue(response)

    def test_isPlayoffWeek_weekDoesNotHavePlayoffMatchups_returnsFalse(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.REGULAR)

        week1 = Week(weekNumber=1, matchups=[matchup1])

        response = week1.isPlayoffWeek

        self.assertIsInstance(response, bool)
        self.assertFalse(response)

    def test_isChampionshipWeek_weekHasAChampionshipMatchup_returnsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.CHAMPIONSHIP)

        week1 = Week(weekNumber=1, matchups=[matchup1])

        response1 = week1.isChampionshipWeek
        response2 = week1.isPlayoffWeek

        self.assertIsInstance(response1, bool)
        self.assertTrue(response1)
        self.assertIsInstance(response2, bool)
        self.assertTrue(response2)

    def test_isChampionshipWeek_weekDoesNotHaveAnyChampionshipMatchups_returnsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.REGULAR)

        week1 = Week(weekNumber=1, matchups=[matchup1])

        response = week1.isChampionshipWeek

        self.assertIsInstance(response, bool)
        self.assertFalse(response)
