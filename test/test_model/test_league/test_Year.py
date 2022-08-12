import unittest

from leeger.enum.MatchupType import MatchupType
from leeger.model.league.Matchup import Matchup
from leeger.model.league.Team import Team
from leeger.model.league.Week import Week
from leeger.model.league.Year import Year
from test.helper.prototypes import getNDefaultOwnersAndTeams


class TestYear(unittest.TestCase):
    def test_year_init(self):
        week = Week(weekNumber=1, matchups=[])
        team = Team(ownerId="", name="")
        year = Year(yearNumber=2000, teams=[team], weeks=[week])

        self.assertEqual(2000, year.yearNumber)
        self.assertEqual(1, len(year.teams))
        self.assertEqual(1, len(year.weeks))
        self.assertEqual(week.id, year.weeks[0].id)
        self.assertEqual(team.id, year.teams[0].id)

    def test_year_eq_equal(self):
        # create Year 1
        owners_1, teams_1 = getNDefaultOwnersAndTeams(2)

        matchup_1 = Matchup(teamAId=teams_1[0].id, teamBId=teams_1[1].id, teamAScore=1.1, teamBScore=2.2,
                            matchupType=MatchupType.REGULAR_SEASON)
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        year_1 = Year(yearNumber=2000, teams=teams_1, weeks=[week_1])

        # create Year 2
        owners_2, teams_2 = getNDefaultOwnersAndTeams(2)

        matchup_2 = Matchup(teamAId=teams_2[0].id, teamBId=teams_2[1].id, teamAScore=1.1, teamBScore=2.2,
                            matchupType=MatchupType.REGULAR_SEASON)
        week_2 = Week(weekNumber=1, matchups=[matchup_2])
        year_2 = Year(yearNumber=2000, teams=teams_2, weeks=[week_2])

        self.assertEqual(year_1, year_2)

    def test_year_eq_notEqual(self):
        # create Year 1
        owners_1, teams_1 = getNDefaultOwnersAndTeams(2)

        matchup_1 = Matchup(teamAId=teams_1[0].id, teamBId=teams_1[1].id, teamAScore=1.1, teamBScore=2.2,
                            matchupType=MatchupType.REGULAR_SEASON)
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        year_1 = Year(yearNumber=2000, teams=teams_1, weeks=[week_1])

        # create Year 2
        owners_2, teams_2 = getNDefaultOwnersAndTeams(2)

        matchup_2 = Matchup(teamAId=teams_2[0].id, teamBId=teams_2[1].id, teamAScore=1.1, teamBScore=2.2,
                            matchupType=MatchupType.REGULAR_SEASON)
        week_2 = Week(weekNumber=1, matchups=[matchup_2])
        year_2 = Year(yearNumber=2001, teams=teams_2, weeks=[week_2])

        self.assertNotEqual(year_1, year_2)
