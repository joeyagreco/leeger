import unittest

from leeger.enum.MatchupType import MatchupType
from leeger.exception import DoesNotExistException
from leeger.model.league import YearSettings
from leeger.model.league.Matchup import Matchup
from leeger.model.league.Team import Team
from leeger.model.league.Week import Week
from leeger.model.league.Year import Year
from test.helper.prototypes import getNDefaultOwnersAndTeams


class TestYear(unittest.TestCase):
    def test_year_init(self):
        week = Week(weekNumber=1, matchups=[])
        team = Team(ownerId="", name="")
        yearSettings = YearSettings(leagueMedianGames=True)
        year = Year(yearNumber=2000, teams=[team], weeks=[week], yearSettings=yearSettings)

        self.assertEqual(2000, year.yearNumber)
        self.assertEqual(1, len(year.teams))
        self.assertEqual(1, len(year.weeks))
        self.assertEqual(week.id, year.weeks[0].id)
        self.assertEqual(team.id, year.teams[0].id)
        self.assertTrue(year.yearSettings.leagueMedianGames)

    def test_year_init_default(self):
        week = Week(weekNumber=1, matchups=[])
        team = Team(ownerId="", name="")
        year = Year(yearNumber=2000, teams=[team], weeks=[week])

        self.assertEqual(2000, year.yearNumber)
        self.assertEqual(1, len(year.teams))
        self.assertEqual(1, len(year.weeks))
        self.assertEqual(week.id, year.weeks[0].id)
        self.assertEqual(team.id, year.teams[0].id)
        self.assertEqual(YearSettings(), year.yearSettings)

    def test_year_eq_equal(self):
        # create Year 1
        owners_1, teams_1 = getNDefaultOwnersAndTeams(2)

        matchup_1 = Matchup(teamAId=teams_1[0].id, teamBId=teams_1[1].id, teamAScore=1.1, teamBScore=2.2,
                            matchupType=MatchupType.REGULAR_SEASON)
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        yearSettings_1 = YearSettings(leagueMedianGames=True)
        year_1 = Year(yearNumber=2000, teams=teams_1, weeks=[week_1], yearSettings=yearSettings_1)

        # create Year 2
        owners_2, teams_2 = getNDefaultOwnersAndTeams(2)

        matchup_2 = Matchup(teamAId=teams_2[0].id, teamBId=teams_2[1].id, teamAScore=1.1, teamBScore=2.2,
                            matchupType=MatchupType.REGULAR_SEASON)
        week_2 = Week(weekNumber=1, matchups=[matchup_2])
        yearSettings_2 = YearSettings(leagueMedianGames=True)
        year_2 = Year(yearNumber=2000, teams=teams_2, weeks=[week_2], yearSettings=yearSettings_2)

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

    def test_year_toJson(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup_1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.2,
                            matchupType=MatchupType.REGULAR_SEASON)
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        yearSettings = YearSettings(leagueMedianGames=True)
        year = Year(yearNumber=2000, teams=teams, weeks=[week_1], yearSettings=yearSettings)
        yearJson = year.toJson()

        self.assertIsInstance(yearJson, dict)
        self.assertEqual(2000, yearJson["yearNumber"])
        self.assertEqual(2, len(yearJson["teams"]))
        self.assertEqual("1", yearJson["teams"][0]["name"])
        self.assertEqual("2", yearJson["teams"][1]["name"])
        self.assertEqual(1, len(yearJson["weeks"]))
        self.assertEqual(1, yearJson["weeks"][0]["weekNumber"])
        self.assertEqual(1, len(yearJson["weeks"][0]["matchups"]))
        self.assertEqual(teams[0].id, yearJson["weeks"][0]["matchups"][0]["teamAId"])
        self.assertEqual(teams[1].id, yearJson["weeks"][0]["matchups"][0]["teamBId"])
        self.assertEqual(1.1, yearJson["weeks"][0]["matchups"][0]["teamAScore"])
        self.assertEqual(2.2, yearJson["weeks"][0]["matchups"][0]["teamBScore"])
        self.assertEqual("REGULAR_SEASON", yearJson["weeks"][0]["matchups"][0]["matchupType"])
        self.assertFalse(yearJson["weeks"][0]["matchups"][0]["teamAHasTieBreaker"])
        self.assertFalse(yearJson["weeks"][0]["matchups"][0]["teamBHasTieBreaker"])
        self.assertTrue(yearJson["yearSettings"]["leagueMedianGames"])

    def test_getTeamByName_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        teams[0].name = "team0"
        matchup_1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.2,
                            matchupType=MatchupType.REGULAR_SEASON)
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        year = Year(yearNumber=2000, teams=teams, weeks=[week_1])

        response = year.getTeamByName("team0")
        self.assertEqual(teams[0], response)

    def test_getTeamByName_teamNotInYear_raisesException(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup_1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.2,
                            matchupType=MatchupType.REGULAR_SEASON)
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        year = Year(yearNumber=2000, teams=teams, weeks=[week_1])

        with self.assertRaises(DoesNotExistException) as context:
            year.getTeamByName("team0")
        self.assertEqual("Year does not have a team with name 'team0'", str(context.exception))
