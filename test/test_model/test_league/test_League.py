import copy
import unittest

from leeger.enum.MatchupType import MatchupType
from leeger.exception.InvalidLeagueFormatException import InvalidLeagueFormatException
from leeger.model.league.League import League
from leeger.model.league.LeagueSettings import LeagueSettings
from leeger.model.league.Matchup import Matchup
from leeger.model.league.Owner import Owner
from leeger.model.league.Week import Week
from leeger.model.league.Year import Year
from test.helper.prototypes import getNDefaultOwnersAndTeams


class TestLeague(unittest.TestCase):
    def test_league_init(self):
        year = Year(yearNumber=0, teams=[], weeks=[])
        owner = Owner(name="")
        leagueSettings = LeagueSettings(leagueMedianGames=True)
        league = League(name="leagueName", owners=[owner], years=[year], leagueSettings=leagueSettings)

        self.assertEqual("leagueName", league.name)
        self.assertEqual(1, len(league.owners))
        self.assertEqual(1, len(league.years))
        self.assertEqual(owner.id, league.owners[0].id)
        self.assertEqual(year.id, league.years[0].id)
        self.assertTrue(league.leagueSettings.leagueMedianGames)

    def test_league_eq_equal(self):
        # create League 1
        owners_1, teams_1 = getNDefaultOwnersAndTeams(2)

        matchup_1 = Matchup(teamAId=teams_1[0].id, teamBId=teams_1[1].id, teamAScore=1.1, teamBScore=2.2,
                            matchupType=MatchupType.REGULAR_SEASON)
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        year_1 = Year(yearNumber=2000, teams=teams_1, weeks=[week_1])
        leagueSettings_1 = LeagueSettings(leagueMedianGames=True)
        league_1 = League(name="LEAGUE", owners=owners_1, years=[year_1], leagueSettings=leagueSettings_1)

        # create League 2
        owners_2, teams_2 = getNDefaultOwnersAndTeams(2)

        matchup_2 = Matchup(teamAId=teams_2[0].id, teamBId=teams_2[1].id, teamAScore=1.1, teamBScore=2.2,
                            matchupType=MatchupType.REGULAR_SEASON)
        week_2 = Week(weekNumber=1, matchups=[matchup_2])
        year_2 = Year(yearNumber=2000, teams=teams_2, weeks=[week_2])
        leagueSettings_2 = LeagueSettings(leagueMedianGames=True)
        league_2 = League(name="LEAGUE", owners=owners_2, years=[year_2], leagueSettings=leagueSettings_2)

        self.assertEqual(league_1, league_2)

    def test_league_eq_notEqual(self):
        # create League 1
        owners_1, teams_1 = getNDefaultOwnersAndTeams(2)

        matchup_1 = Matchup(teamAId=teams_1[0].id, teamBId=teams_1[1].id, teamAScore=1.1, teamBScore=2.2,
                            matchupType=MatchupType.REGULAR_SEASON)
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        year_1 = Year(yearNumber=2000, teams=teams_1, weeks=[week_1])
        league_1 = League(name="LEAGUE 1", owners=owners_1, years=[year_1])

        # create League 2
        owners_2, teams_2 = getNDefaultOwnersAndTeams(2)

        matchup_2 = Matchup(teamAId=teams_2[0].id, teamBId=teams_2[1].id, teamAScore=1.1, teamBScore=2.2,
                            matchupType=MatchupType.REGULAR_SEASON)
        week_2 = Week(weekNumber=1, matchups=[matchup_2])
        year_2 = Year(yearNumber=2000, teams=teams_2, weeks=[week_2])
        league_2 = League(name="LEAGUE 2", owners=owners_2, years=[year_2])

        self.assertNotEqual(league_1, league_2)

    def test_league_add_happyPath(self):
        # create League 1
        owners_1, teams_1 = getNDefaultOwnersAndTeams(2)

        matchup_1 = Matchup(teamAId=teams_1[0].id, teamBId=teams_1[1].id, teamAScore=1.1, teamBScore=2.2,
                            matchupType=MatchupType.REGULAR_SEASON)
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        year_1 = Year(yearNumber=2000, teams=teams_1, weeks=[week_1])
        leagueSettings_1 = LeagueSettings(leagueMedianGames=True)
        league_1 = League(name="LEAGUE 1", owners=owners_1, years=[year_1], leagueSettings=leagueSettings_1)

        # create League 2
        owners_2, teams_2 = getNDefaultOwnersAndTeams(2)

        matchup_2 = Matchup(teamAId=teams_2[0].id, teamBId=teams_2[1].id, teamAScore=1.1, teamBScore=2.2,
                            matchupType=MatchupType.REGULAR_SEASON)
        week_2 = Week(weekNumber=1, matchups=[matchup_2])
        year_2 = Year(yearNumber=2001, teams=teams_2, weeks=[week_2])
        leagueSettings_2 = LeagueSettings(leagueMedianGames=True)
        league_2 = League(name="LEAGUE 2", owners=owners_2, years=[year_2], leagueSettings=leagueSettings_2)

        combinedLeague = league_1 + league_2
        self.assertIsInstance(combinedLeague, League)
        self.assertEqual("'LEAGUE 1' + 'LEAGUE 2' League", combinedLeague.name)
        self.assertEqual(2, len(combinedLeague.owners))
        self.assertEqual([owner.name for owner in league_1.owners], [owner.name for owner in league_1.owners])
        self.assertEqual(2, len(combinedLeague.years))
        self.assertEqual(2000, combinedLeague.years[0].yearNumber)
        self.assertEqual(2001, combinedLeague.years[1].yearNumber)
        self.assertTrue(combinedLeague.leagueSettings.leagueMedianGames)

    def test_league_add_originalLeaguesAreTheSameAfterAdding(self):
        # create League 1
        owners_1, teams_1 = getNDefaultOwnersAndTeams(2)

        matchup_1 = Matchup(teamAId=teams_1[0].id, teamBId=teams_1[1].id, teamAScore=1.1, teamBScore=2.2,
                            matchupType=MatchupType.REGULAR_SEASON)
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        year_1 = Year(yearNumber=2000, teams=teams_1, weeks=[week_1])
        league_1 = League(name="LEAGUE 1", owners=owners_1, years=[year_1])
        league_1_copy = copy.deepcopy(league_1)

        # create League 2
        owners_2, teams_2 = getNDefaultOwnersAndTeams(2)

        matchup_2 = Matchup(teamAId=teams_2[0].id, teamBId=teams_2[1].id, teamAScore=1.1, teamBScore=2.2,
                            matchupType=MatchupType.REGULAR_SEASON)
        week_2 = Week(weekNumber=1, matchups=[matchup_2])
        year_2 = Year(yearNumber=2001, teams=teams_2, weeks=[week_2])
        league_2 = League(name="LEAGUE 2", owners=owners_2, years=[year_2])
        league_2_copy = copy.deepcopy(league_2)

        combinedLeague = league_1 + league_2
        self.assertEqual(league_1, league_1_copy)
        self.assertEqual(league_2, league_2_copy)

    def test_league_add_teamsWithSameOwnersHaveSameOwnerIdAcrossYears(self):
        # create League 1
        owners_1, teams_1 = getNDefaultOwnersAndTeams(2)

        matchup_1 = Matchup(teamAId=teams_1[0].id, teamBId=teams_1[1].id, teamAScore=1.1, teamBScore=2.2,
                            matchupType=MatchupType.REGULAR_SEASON)
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        year_1 = Year(yearNumber=2000, teams=teams_1, weeks=[week_1])
        league_1 = League(name="LEAGUE 1", owners=owners_1, years=[year_1])

        # create League 2
        owners_2, teams_2 = getNDefaultOwnersAndTeams(2)

        matchup_2 = Matchup(teamAId=teams_2[0].id, teamBId=teams_2[1].id, teamAScore=1.1, teamBScore=2.2,
                            matchupType=MatchupType.REGULAR_SEASON)
        week_2 = Week(weekNumber=1, matchups=[matchup_2])
        year_2 = Year(yearNumber=2001, teams=teams_2, weeks=[week_2])
        league_2 = League(name="LEAGUE 2", owners=owners_2, years=[year_2])

        combinedLeague = league_1 + league_2
        allOwnerIds = set()
        for year in combinedLeague.years:
            for team in year.teams:
                allOwnerIds.add(team.ownerId)

        self.assertEqual(2, len(allOwnerIds))

    def test_league_add_addingOrderDoesNotMatter(self):
        # create League 1
        owners_1, teams_1 = getNDefaultOwnersAndTeams(2)

        matchup_1 = Matchup(teamAId=teams_1[0].id, teamBId=teams_1[1].id, teamAScore=1.1, teamBScore=2.2,
                            matchupType=MatchupType.REGULAR_SEASON)
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        year_1 = Year(yearNumber=2000, teams=teams_1, weeks=[week_1])
        league_1 = League(name="LEAGUE", owners=owners_1, years=[year_1])

        # create League 2
        owners_2, teams_2 = getNDefaultOwnersAndTeams(2)

        matchup_2 = Matchup(teamAId=teams_2[0].id, teamBId=teams_2[1].id, teamAScore=1.1, teamBScore=2.2,
                            matchupType=MatchupType.REGULAR_SEASON)
        week_2 = Week(weekNumber=1, matchups=[matchup_2])
        year_2 = Year(yearNumber=2001, teams=teams_2, weeks=[week_2])
        league_2 = League(name="LEAGUE", owners=owners_2, years=[year_2])

        combinedLeague1 = league_1 + league_2
        combinedLeague2 = league_2 + league_1
        self.assertIsInstance(combinedLeague1, League)
        self.assertIsInstance(combinedLeague2, League)
        self.assertEqual(combinedLeague1, combinedLeague2)

    def test_league_add_sameLeagueName_nameIsntChanged(self):
        # create League 1
        owners_1, teams_1 = getNDefaultOwnersAndTeams(2)

        matchup_1 = Matchup(teamAId=teams_1[0].id, teamBId=teams_1[1].id, teamAScore=1.1, teamBScore=2.2,
                            matchupType=MatchupType.REGULAR_SEASON)
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        year_1 = Year(yearNumber=2000, teams=teams_1, weeks=[week_1])
        league_1 = League(name="LEAGUE", owners=owners_1, years=[year_1])

        # create League 2
        owners_2, teams_2 = getNDefaultOwnersAndTeams(2)

        matchup_2 = Matchup(teamAId=teams_2[0].id, teamBId=teams_2[1].id, teamAScore=1.1, teamBScore=2.2,
                            matchupType=MatchupType.REGULAR_SEASON)
        week_2 = Week(weekNumber=1, matchups=[matchup_2])
        year_2 = Year(yearNumber=2001, teams=teams_2, weeks=[week_2])
        league_2 = League(name="LEAGUE", owners=owners_2, years=[year_2])

        combinedLeague = league_1 + league_2
        self.assertIsInstance(combinedLeague, League)
        self.assertEqual("LEAGUE", combinedLeague.name)

    def test_league_add_leaguesHaveOwnersThatDontHaveMatchingNames_ownersAreCombined(self):
        # create League 1
        owners_1, teams_1 = getNDefaultOwnersAndTeams(2)
        owners_1[0].name = "league 1 owner 1"
        owners_1[1].name = "league 1 owner 2"

        matchup_1 = Matchup(teamAId=teams_1[0].id, teamBId=teams_1[1].id, teamAScore=1.1, teamBScore=2.2,
                            matchupType=MatchupType.REGULAR_SEASON)
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        year_1 = Year(yearNumber=2000, teams=teams_1, weeks=[week_1])
        league_1 = League(name="LEAGUE", owners=owners_1, years=[year_1])

        # create League 2
        owners_2, teams_2 = getNDefaultOwnersAndTeams(2)
        owners_2[0].name = "league 2 owner 1"
        owners_2[1].name = "league 2 owner 2"

        matchup_2 = Matchup(teamAId=teams_2[0].id, teamBId=teams_2[1].id, teamAScore=1.1, teamBScore=2.2,
                            matchupType=MatchupType.REGULAR_SEASON)
        week_2 = Week(weekNumber=1, matchups=[matchup_2])
        year_2 = Year(yearNumber=2001, teams=teams_2, weeks=[week_2])
        league_2 = League(name="LEAGUE", owners=owners_2, years=[year_2])

        combinedLeague = league_1 + league_2
        self.assertIsInstance(combinedLeague, League)
        self.assertEqual(4, len(combinedLeague.owners))
        self.assertEqual("league 1 owner 1", combinedLeague.owners[0].name)
        self.assertEqual("league 1 owner 2", combinedLeague.owners[1].name)
        self.assertEqual("league 2 owner 1", combinedLeague.owners[2].name)
        self.assertEqual("league 2 owner 2", combinedLeague.owners[3].name)

    def test_league_add_combinedLeagueYearsAreInCorrectOrder(self):
        # first example, League 1 has years that come first
        # create League 1
        owners_1, teams_1 = getNDefaultOwnersAndTeams(2)

        matchup_1 = Matchup(teamAId=teams_1[0].id, teamBId=teams_1[1].id, teamAScore=1.1, teamBScore=2.2,
                            matchupType=MatchupType.REGULAR_SEASON)
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        year_1 = Year(yearNumber=2000, teams=teams_1, weeks=[week_1])
        league_1 = League(name="LEAGUE 1", owners=owners_1, years=[year_1])

        # create League 2
        owners_2, teams_2 = getNDefaultOwnersAndTeams(2)

        matchup_2 = Matchup(teamAId=teams_2[0].id, teamBId=teams_2[1].id, teamAScore=1.1, teamBScore=2.2,
                            matchupType=MatchupType.REGULAR_SEASON)
        week_2 = Week(weekNumber=1, matchups=[matchup_2])
        year_2 = Year(yearNumber=2001, teams=teams_2, weeks=[week_2])
        league_2 = League(name="LEAGUE 2", owners=owners_2, years=[year_2])

        combinedLeague = league_1 + league_2
        self.assertIsInstance(combinedLeague, League)
        self.assertEqual(2000, combinedLeague.years[0].yearNumber)
        self.assertEqual(2001, combinedLeague.years[1].yearNumber)

        # second example, League 2 has years that come first
        # create League 1
        owners_1, teams_1 = getNDefaultOwnersAndTeams(2)

        matchup_1 = Matchup(teamAId=teams_1[0].id, teamBId=teams_1[1].id, teamAScore=1.1, teamBScore=2.2,
                            matchupType=MatchupType.REGULAR_SEASON)
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        year_1 = Year(yearNumber=2001, teams=teams_1, weeks=[week_1])
        league_1 = League(name="LEAGUE 1", owners=owners_1, years=[year_1])

        # create League 2
        owners_2, teams_2 = getNDefaultOwnersAndTeams(2)

        matchup_2 = Matchup(teamAId=teams_2[0].id, teamBId=teams_2[1].id, teamAScore=1.1, teamBScore=2.2,
                            matchupType=MatchupType.REGULAR_SEASON)
        week_2 = Week(weekNumber=1, matchups=[matchup_2])
        year_2 = Year(yearNumber=2000, teams=teams_2, weeks=[week_2])
        league_2 = League(name="LEAGUE 2", owners=owners_2, years=[year_2])

        combinedLeague = league_1 + league_2
        self.assertIsInstance(combinedLeague, League)
        self.assertEqual(2000, combinedLeague.years[0].yearNumber)
        self.assertEqual(2001, combinedLeague.years[1].yearNumber)

    def test_league_add_duplicateYearsAcrossCombinedLeagues_raisesException(self):
        # create League 1
        owners_1, teams_1 = getNDefaultOwnersAndTeams(2)

        matchup_1 = Matchup(teamAId=teams_1[0].id, teamBId=teams_1[1].id, teamAScore=1.1, teamBScore=2.2,
                            matchupType=MatchupType.REGULAR_SEASON)
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        year_1 = Year(yearNumber=2000, teams=teams_1, weeks=[week_1])
        league_1 = League(name="LEAGUE 1", owners=owners_1, years=[year_1])

        # create League 2
        owners_2, teams_2 = getNDefaultOwnersAndTeams(2)

        matchup_2 = Matchup(teamAId=teams_2[0].id, teamBId=teams_2[1].id, teamAScore=1.1, teamBScore=2.2,
                            matchupType=MatchupType.REGULAR_SEASON)
        week_2 = Week(weekNumber=1, matchups=[matchup_2])
        year_2 = Year(yearNumber=2000, teams=teams_2, weeks=[week_2])
        league_2 = League(name="LEAGUE 2", owners=owners_2, years=[year_2])

        with self.assertRaises(InvalidLeagueFormatException) as context:
            league_1 + league_2
        self.assertEqual("Can only have 1 of each year number within a league.", str(context.exception))

    def test_league_add_leagueSettingsNotEqual_raisesException(self):
        # create League 1
        owners_1, teams_1 = getNDefaultOwnersAndTeams(2)

        matchup_1 = Matchup(teamAId=teams_1[0].id, teamBId=teams_1[1].id, teamAScore=1.1, teamBScore=2.2,
                            matchupType=MatchupType.REGULAR_SEASON)
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        year_1 = Year(yearNumber=2000, teams=teams_1, weeks=[week_1])
        leagueSettings_1 = LeagueSettings(leagueMedianGames=True)
        league_1 = League(name="LEAGUE 1", owners=owners_1, years=[year_1], leagueSettings=leagueSettings_1)

        # create League 2
        owners_2, teams_2 = getNDefaultOwnersAndTeams(2)

        matchup_2 = Matchup(teamAId=teams_2[0].id, teamBId=teams_2[1].id, teamAScore=1.1, teamBScore=2.2,
                            matchupType=MatchupType.REGULAR_SEASON)
        week_2 = Week(weekNumber=1, matchups=[matchup_2])
        year_2 = Year(yearNumber=2001, teams=teams_2, weeks=[week_2])
        leagueSettings_2 = LeagueSettings(leagueMedianGames=False)
        league_2 = League(name="LEAGUE 2", owners=owners_2, years=[year_2], leagueSettings=leagueSettings_2)

        with self.assertRaises(ValueError) as context:
            league_1 + league_2
        self.assertEqual("LeagueSettings are conflicting.", str(context.exception))

    def test_league_toJson(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup_1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.2,
                            matchupType=MatchupType.REGULAR_SEASON)
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        year_1 = Year(yearNumber=2000, teams=teams, weeks=[week_1])
        leagueSettings = LeagueSettings(leagueMedianGames=True)
        league = League(name="LEAGUE", owners=owners, years=[year_1], leagueSettings=leagueSettings)
        leagueJson = league.toJson()

        self.assertIsInstance(leagueJson, dict)
        self.assertEqual("LEAGUE", leagueJson["name"])
        self.assertEqual(2, len(leagueJson["owners"]))
        self.assertEqual("1", leagueJson["owners"][0]["name"])
        self.assertEqual("2", leagueJson["owners"][1]["name"])
        self.assertEqual(1, len(leagueJson["years"]))
        self.assertEqual(2000, leagueJson["years"][0]["yearNumber"])
        self.assertEqual(2, len(leagueJson["years"][0]["teams"]))
        self.assertEqual("1", leagueJson["years"][0]["teams"][0]["name"])
        self.assertEqual("2", leagueJson["years"][0]["teams"][1]["name"])
        self.assertEqual(1, len(leagueJson["years"][0]["weeks"]))
        self.assertEqual(1, leagueJson["years"][0]["weeks"][0]["weekNumber"])
        self.assertEqual(1, len(leagueJson["years"][0]["weeks"][0]["matchups"]))
        self.assertEqual(teams[0].id, leagueJson["years"][0]["weeks"][0]["matchups"][0]["teamAId"])
        self.assertEqual(teams[1].id, leagueJson["years"][0]["weeks"][0]["matchups"][0]["teamBId"])
        self.assertEqual(1.1, leagueJson["years"][0]["weeks"][0]["matchups"][0]["teamAScore"])
        self.assertEqual(2.2, leagueJson["years"][0]["weeks"][0]["matchups"][0]["teamBScore"])
        self.assertEqual("REGULAR_SEASON", leagueJson["years"][0]["weeks"][0]["matchups"][0]["matchupType"])
        self.assertFalse(leagueJson["years"][0]["weeks"][0]["matchups"][0]["teamAHasTieBreaker"])
        self.assertFalse(leagueJson["years"][0]["weeks"][0]["matchups"][0]["teamBHasTieBreaker"])
        self.assertTrue(leagueJson["leagueSettings"]["leagueMedianGames"])
