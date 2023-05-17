import unittest

from leeger.enum.MatchupType import MatchupType
from leeger.exception import DoesNotExistException
from leeger.model.league import YearSettings
from leeger.model.league.Division import Division
from leeger.model.league.Matchup import Matchup
from leeger.model.league.Team import Team
from leeger.model.league.Week import Week
from leeger.model.league.Year import Year
from test.helper.prototypes import getNDefaultOwnersAndTeams


class TestYear(unittest.TestCase):
    def test_year_init(self):
        week = Week(weekNumber=1, matchups=[])
        team = Team(ownerId="", name="")
        division = Division(name="")
        yearSettings = YearSettings(leagueMedianGames=True)
        year = Year(yearNumber=2000, teams=[team], weeks=[week], divisions=[division], yearSettings=yearSettings)

        self.assertEqual(2000, year.yearNumber)
        self.assertEqual(1, len(year.teams))
        self.assertEqual(1, len(year.weeks))
        self.assertEqual(week.id, year.weeks[0].id)
        self.assertEqual(team.id, year.teams[0].id)
        self.assertEqual(division.id, year.divisions[0].id)
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
        self.assertEqual(list(), year.divisions)

    def test_year_eq_equal(self):
        # create Year 1
        _, teams_1 = getNDefaultOwnersAndTeams(2)

        matchup_1 = Matchup(
            teamAId=teams_1[0].id,
            teamBId=teams_1[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        division_1 = Division(name="div")
        yearSettings_1 = YearSettings(leagueMedianGames=True)
        year_1 = Year(yearNumber=2000, teams=teams_1, weeks=[week_1], divisions=[division_1], yearSettings=yearSettings_1)

        # create Year 2
        _, teams_2 = getNDefaultOwnersAndTeams(2)

        matchup_2 = Matchup(
            teamAId=teams_2[0].id,
            teamBId=teams_2[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        week_2 = Week(weekNumber=1, matchups=[matchup_2])
        division_2 = Division(name="div")
        yearSettings_2 = YearSettings(leagueMedianGames=True)
        year_2 = Year(yearNumber=2000, teams=teams_2, weeks=[week_2], divisions=[division_2], yearSettings=yearSettings_2)

        self.assertEqual(year_1, year_2)

    def test_year_eq_notEqual(self):
        # create Year 1
        _, teams_1 = getNDefaultOwnersAndTeams(2)

        matchup_1 = Matchup(
            teamAId=teams_1[0].id,
            teamBId=teams_1[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        year_1 = Year(yearNumber=2000, teams=teams_1, weeks=[week_1])

        # create Year 2
        _, teams_2 = getNDefaultOwnersAndTeams(2)

        matchup_2 = Matchup(
            teamAId=teams_2[0].id,
            teamBId=teams_2[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        week_2 = Week(weekNumber=1, matchups=[matchup_2])
        year_2 = Year(yearNumber=2001, teams=teams_2, weeks=[week_2])

        self.assertNotEqual(year_1, year_2)
        
    def test_toFromJson(self):
        _, teams = getNDefaultOwnersAndTeams(2)

        matchup_1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        division_1 = Division(name="div")
        yearSettings = YearSettings(leagueMedianGames=True)
        year = Year(yearNumber=2000, teams=teams, weeks=[week_1], divisions=[division_1], yearSettings=yearSettings)
        
        self.assertEqual(year, Year.fromJson(year.toJson()))

    def test_getTeamByName_happyPath(self):
        _, teams = getNDefaultOwnersAndTeams(2)

        teams[0].name = "team0"
        matchup_1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        year = Year(yearNumber=2000, teams=teams, weeks=[week_1])

        response = year.getTeamByName("team0")
        self.assertEqual(teams[0], response)

    def test_getTeamByName_teamNotInYear_raisesException(self):
        _, teams = getNDefaultOwnersAndTeams(2)

        matchup_1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        year = Year(yearNumber=2000, teams=teams, weeks=[week_1])

        with self.assertRaises(DoesNotExistException) as context:
            year.getTeamByName("team0")
        self.assertEqual("Year does not have a team with name 'team0'.", str(context.exception))

    def test_getWeekByWeekNumber_happyPath(self):
        _, teams = getNDefaultOwnersAndTeams(2)

        matchup_1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        year = Year(yearNumber=2000, teams=teams, weeks=[week_1])

        response = year.getWeekByWeekNumber(1)
        self.assertEqual(week_1, response)

    def test_getWeekByWeekNumber_teamNotInYear_raisesException(self):
        _, teams = getNDefaultOwnersAndTeams(2)

        matchup_1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        year = Year(yearNumber=2000, teams=teams, weeks=[week_1])

        with self.assertRaises(DoesNotExistException) as context:
            year.getWeekByWeekNumber(2)
        self.assertEqual("Year does not have a week with week number 2.", str(context.exception))
