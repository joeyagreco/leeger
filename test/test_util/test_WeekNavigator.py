import unittest

from src.leeger.enum.MatchupType import MatchupType
from src.leeger.model.Matchup import Matchup
from src.leeger.model.Week import Week
from src.leeger.model.WeekFilters import WeekFilters
from src.leeger.util.WeekNavigator import WeekNavigator
from test.helper.prototypes import getNDefaultOwnersAndTeams


class TestWeekNavigator(unittest.TestCase):
    def test_getTeamIdsAndScores_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.IGNORE)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        weekFilters = WeekFilters(
            includeMatchupTypes=[MatchupType.REGULAR_SEASON, MatchupType.PLAYOFF, MatchupType.CHAMPIONSHIP])
        response = WeekNavigator.getTeamIdsAndScores(week1, weekFilters)

        self.assertIsInstance(response, dict)
        self.assertEqual(4, len(response.keys()))
        self.assertEqual(1, response[teams[0].id])
        self.assertEqual(2, response[teams[1].id])
        self.assertEqual(1, response[teams[4].id])
        self.assertEqual(2, response[teams[5].id])

    def test_getTeamIdsAndOpponentScores_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.IGNORE)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        weekFilters = WeekFilters(
            includeMatchupTypes=[MatchupType.REGULAR_SEASON, MatchupType.PLAYOFF, MatchupType.CHAMPIONSHIP])
        response = WeekNavigator.getTeamIdsAndOpponentScores(week1, weekFilters)

        self.assertIsInstance(response, dict)
        self.assertEqual(4, len(response.keys()))
        self.assertEqual(2, response[teams[0].id])
        self.assertEqual(1, response[teams[1].id])
        self.assertEqual(2, response[teams[4].id])
        self.assertEqual(1, response[teams[5].id])

    def test_getNumberOfValidTeamsInWeek_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.IGNORE)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])

        weekFilters = WeekFilters(
            includeMatchupTypes=[MatchupType.REGULAR_SEASON, MatchupType.PLAYOFF, MatchupType.CHAMPIONSHIP])
        response1 = WeekNavigator.getNumberOfValidTeamsInWeek(week1, weekFilters)
        response2 = WeekNavigator.getNumberOfValidTeamsInWeek(week2, weekFilters)

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

        weekFilters = WeekFilters(
            includeMatchupTypes=[MatchupType.PLAYOFF, MatchupType.CHAMPIONSHIP])
        response = WeekNavigator.getNumberOfValidTeamsInWeek(week1, weekFilters)

        self.assertIsInstance(response, int)
        self.assertEqual(4, response)

    def test_getNumberOfValidTeamsInWeek_onlyRegularSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(4)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.REGULAR_SEASON)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.REGULAR_SEASON)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2])

        weekFilters = WeekFilters(
            includeMatchupTypes=[MatchupType.REGULAR_SEASON])
        response = WeekNavigator.getNumberOfValidTeamsInWeek(week1, weekFilters)

        self.assertIsInstance(response, int)
        self.assertEqual(4, response)
