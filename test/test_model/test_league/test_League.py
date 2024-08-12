import copy
import unittest

from leeger.enum.MatchupType import MatchupType
from leeger.exception import DoesNotExistException
from leeger.exception.InvalidLeagueFormatException import InvalidLeagueFormatException
from leeger.model.league import YearSettings
from leeger.model.league.League import League
from leeger.model.league.Matchup import Matchup
from leeger.model.league.Owner import Owner
from leeger.model.league.Week import Week
from leeger.model.league.Year import Year
from test.helper.prototypes import getNDefaultOwnersAndTeams


class TestLeague(unittest.TestCase):
    def test_league_init(self):
        year = Year(yearNumber=0, teams=[], weeks=[])
        owner = Owner(name="")
        league = League(name="leagueName", owners=[owner], years=[year])

        self.assertEqual("leagueName", league.name)
        self.assertEqual(1, len(league.owners))
        self.assertEqual(1, len(league.years))
        self.assertEqual(owner.id, league.owners[0].id)
        self.assertEqual(year.id, league.years[0].id)

    def test_league_eq_callsEqualsMethod(self):
        # create League 1
        owners_1, teams_1 = getNDefaultOwnersAndTeams(2)

        matchup_1 = Matchup(
            teamAId=teams_1[0].id,
            teamBId=teams_1[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        year_1 = Year(yearNumber=2000, teams=teams_1, weeks=[week_1])
        league_1 = League(name="LEAGUE", owners=owners_1, years=[year_1])

        self.assertTrue(league_1 == league_1)

    def test_league_eq_equal(self):
        # create League 1
        owners_1, teams_1 = getNDefaultOwnersAndTeams(2)

        matchup_1 = Matchup(
            teamAId=teams_1[0].id,
            teamBId=teams_1[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        year_1 = Year(yearNumber=2000, teams=teams_1, weeks=[week_1])
        league_1 = League(name="LEAGUE", owners=owners_1, years=[year_1])

        # create League 2
        owners_2, teams_2 = getNDefaultOwnersAndTeams(2)

        matchup_2 = Matchup(
            teamAId=teams_2[0].id,
            teamBId=teams_2[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        week_2 = Week(weekNumber=1, matchups=[matchup_2])
        year_2 = Year(yearNumber=2000, teams=teams_2, weeks=[week_2])
        league_2 = League(name="LEAGUE", owners=owners_2, years=[year_2])

        self.assertTrue(league_1.equals(league_2, ignoreBaseIds=True, ignoreIds=True))

    def test_league_eq_notEqual(self):
        # create League 1
        owners_1, teams_1 = getNDefaultOwnersAndTeams(2)

        matchup_1 = Matchup(
            teamAId=teams_1[0].id,
            teamBId=teams_1[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        year_1 = Year(yearNumber=2000, teams=teams_1, weeks=[week_1])
        league_1 = League(name="LEAGUE 1", owners=owners_1, years=[year_1])

        # create League 2
        owners_2, teams_2 = getNDefaultOwnersAndTeams(2)

        matchup_2 = Matchup(
            teamAId=teams_2[0].id,
            teamBId=teams_2[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        week_2 = Week(weekNumber=1, matchups=[matchup_2])
        year_2 = Year(yearNumber=2000, teams=teams_2, weeks=[week_2])
        league_2 = League(name="LEAGUE 2", owners=owners_2, years=[year_2])

        self.assertFalse(league_1.equals(league_2, ignoreBaseIds=True, ignoreIds=True))

    def test_league_add_happyPath(self):
        # create League 1
        owners_1, teams_1 = getNDefaultOwnersAndTeams(2)

        matchup_1 = Matchup(
            teamAId=teams_1[0].id,
            teamBId=teams_1[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        year_1 = Year(yearNumber=2000, teams=teams_1, weeks=[week_1])
        league_1 = League(name="LEAGUE 1", owners=owners_1, years=[year_1])

        # create League 2
        owners_2, teams_2 = getNDefaultOwnersAndTeams(2)

        matchup_2 = Matchup(
            teamAId=teams_2[0].id,
            teamBId=teams_2[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        week_2 = Week(weekNumber=1, matchups=[matchup_2])
        year_2 = Year(yearNumber=2001, teams=teams_2, weeks=[week_2])
        league_2 = League(name="LEAGUE 2", owners=owners_2, years=[year_2])

        combinedLeague = league_1 + league_2
        self.assertIsInstance(combinedLeague, League)
        self.assertEqual("'LEAGUE 1' + 'LEAGUE 2' League", combinedLeague.name)
        self.assertEqual(2, len(combinedLeague.owners))
        self.assertEqual(
            [owner.name for owner in league_1.owners],
            [owner.name for owner in league_1.owners],
        )
        self.assertEqual(2, len(combinedLeague.years))
        self.assertEqual(2000, combinedLeague.years[0].yearNumber)
        self.assertEqual(2001, combinedLeague.years[1].yearNumber)

    def test_league_add_originalLeaguesAreTheSameAfterAdding(self):
        # create League 1
        owners_1, teams_1 = getNDefaultOwnersAndTeams(2)

        matchup_1 = Matchup(
            teamAId=teams_1[0].id,
            teamBId=teams_1[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        year_1 = Year(yearNumber=2000, teams=teams_1, weeks=[week_1])
        league_1 = League(name="LEAGUE 1", owners=owners_1, years=[year_1])
        league_1_copy = copy.deepcopy(league_1)

        # create League 2
        owners_2, teams_2 = getNDefaultOwnersAndTeams(2)

        matchup_2 = Matchup(
            teamAId=teams_2[0].id,
            teamBId=teams_2[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        week_2 = Week(weekNumber=1, matchups=[matchup_2])
        year_2 = Year(yearNumber=2001, teams=teams_2, weeks=[week_2])
        league_2 = League(name="LEAGUE 2", owners=owners_2, years=[year_2])
        league_2_copy = copy.deepcopy(league_2)

        league_1 + league_2
        self.assertTrue(
            league_1.equals(league_1_copy, ignoreBaseIds=True, ignoreIds=True)
        )
        self.assertTrue(
            league_2.equals(league_2_copy, ignoreBaseIds=True, ignoreIds=True)
        )

    def test_league_add_teamsWithSameOwnersHaveSameOwnerIdAcrossYears(self):
        # create League 1
        owners_1, teams_1 = getNDefaultOwnersAndTeams(2)

        matchup_1 = Matchup(
            teamAId=teams_1[0].id,
            teamBId=teams_1[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        year_1 = Year(yearNumber=2000, teams=teams_1, weeks=[week_1])
        league_1 = League(name="LEAGUE 1", owners=owners_1, years=[year_1])

        # create League 2
        owners_2, teams_2 = getNDefaultOwnersAndTeams(2)

        matchup_2 = Matchup(
            teamAId=teams_2[0].id,
            teamBId=teams_2[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
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

        matchup_1 = Matchup(
            teamAId=teams_1[0].id,
            teamBId=teams_1[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        year_1 = Year(yearNumber=2000, teams=teams_1, weeks=[week_1])
        league_1 = League(name="LEAGUE", owners=owners_1, years=[year_1])

        # create League 2
        owners_2, teams_2 = getNDefaultOwnersAndTeams(2)

        matchup_2 = Matchup(
            teamAId=teams_2[0].id,
            teamBId=teams_2[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        week_2 = Week(weekNumber=1, matchups=[matchup_2])
        year_2 = Year(yearNumber=2001, teams=teams_2, weeks=[week_2])
        league_2 = League(name="LEAGUE", owners=owners_2, years=[year_2])

        combinedLeague1 = league_1 + league_2
        combinedLeague2 = league_2 + league_1
        self.assertIsInstance(combinedLeague1, League)
        self.assertIsInstance(combinedLeague2, League)
        self.assertTrue(
            combinedLeague1.equals(combinedLeague2, ignoreBaseIds=True, ignoreIds=True)
        )

    def test_league_add_sameLeagueName_nameIsntChanged(self):
        # create League 1
        owners_1, teams_1 = getNDefaultOwnersAndTeams(2)

        matchup_1 = Matchup(
            teamAId=teams_1[0].id,
            teamBId=teams_1[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        year_1 = Year(yearNumber=2000, teams=teams_1, weeks=[week_1])
        league_1 = League(name="LEAGUE", owners=owners_1, years=[year_1])

        # create League 2
        owners_2, teams_2 = getNDefaultOwnersAndTeams(2)

        matchup_2 = Matchup(
            teamAId=teams_2[0].id,
            teamBId=teams_2[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        week_2 = Week(weekNumber=1, matchups=[matchup_2])
        year_2 = Year(yearNumber=2001, teams=teams_2, weeks=[week_2])
        league_2 = League(name="LEAGUE", owners=owners_2, years=[year_2])

        combinedLeague = league_1 + league_2
        self.assertIsInstance(combinedLeague, League)
        self.assertEqual("LEAGUE", combinedLeague.name)

    def test_league_add_leaguesHaveOwnersThatDontHaveMatchingNames_ownersAreCombined(
        self,
    ):
        # create League 1
        owners_1, teams_1 = getNDefaultOwnersAndTeams(2)
        owners_1[0].name = "league 1 owner 1"
        owners_1[1].name = "league 1 owner 2"

        matchup_1 = Matchup(
            teamAId=teams_1[0].id,
            teamBId=teams_1[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        year_1 = Year(yearNumber=2000, teams=teams_1, weeks=[week_1])
        league_1 = League(name="LEAGUE", owners=owners_1, years=[year_1])

        # create League 2
        owners_2, teams_2 = getNDefaultOwnersAndTeams(2)
        owners_2[0].name = "league 2 owner 1"
        owners_2[1].name = "league 2 owner 2"

        matchup_2 = Matchup(
            teamAId=teams_2[0].id,
            teamBId=teams_2[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
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

        matchup_1 = Matchup(
            teamAId=teams_1[0].id,
            teamBId=teams_1[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        year_1 = Year(yearNumber=2000, teams=teams_1, weeks=[week_1])
        league_1 = League(name="LEAGUE 1", owners=owners_1, years=[year_1])

        # create League 2
        owners_2, teams_2 = getNDefaultOwnersAndTeams(2)

        matchup_2 = Matchup(
            teamAId=teams_2[0].id,
            teamBId=teams_2[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
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

        matchup_1 = Matchup(
            teamAId=teams_1[0].id,
            teamBId=teams_1[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        year_1 = Year(yearNumber=2001, teams=teams_1, weeks=[week_1])
        league_1 = League(name="LEAGUE 1", owners=owners_1, years=[year_1])

        # create League 2
        owners_2, teams_2 = getNDefaultOwnersAndTeams(2)

        matchup_2 = Matchup(
            teamAId=teams_2[0].id,
            teamBId=teams_2[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
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

        matchup_1 = Matchup(
            teamAId=teams_1[0].id,
            teamBId=teams_1[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        year_1 = Year(yearNumber=2000, teams=teams_1, weeks=[week_1])
        league_1 = League(name="LEAGUE 1", owners=owners_1, years=[year_1])

        # create League 2
        owners_2, teams_2 = getNDefaultOwnersAndTeams(2)

        matchup_2 = Matchup(
            teamAId=teams_2[0].id,
            teamBId=teams_2[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        week_2 = Week(weekNumber=1, matchups=[matchup_2])
        year_2 = Year(yearNumber=2000, teams=teams_2, weeks=[week_2])
        league_2 = League(name="LEAGUE 2", owners=owners_2, years=[year_2])

        with self.assertRaises(InvalidLeagueFormatException) as context:
            league_1 + league_2
        self.assertEqual(
            "Can only have 1 of each year number within a league.",
            str(context.exception),
        )

    def test_league_toJson(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup_1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        year_1 = Year(yearNumber=2000, teams=teams, weeks=[week_1])
        league = League(name="LEAGUE", owners=owners, years=[year_1])
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
        self.assertEqual(
            teams[0].id, leagueJson["years"][0]["weeks"][0]["matchups"][0]["teamAId"]
        )
        self.assertEqual(
            teams[1].id, leagueJson["years"][0]["weeks"][0]["matchups"][0]["teamBId"]
        )
        self.assertEqual(
            1.1, leagueJson["years"][0]["weeks"][0]["matchups"][0]["teamAScore"]
        )
        self.assertEqual(
            2.2, leagueJson["years"][0]["weeks"][0]["matchups"][0]["teamBScore"]
        )
        self.assertEqual(
            "REGULAR_SEASON",
            leagueJson["years"][0]["weeks"][0]["matchups"][0]["matchupType"],
        )
        self.assertFalse(
            leagueJson["years"][0]["weeks"][0]["matchups"][0]["teamAHasTiebreaker"]
        )
        self.assertFalse(
            leagueJson["years"][0]["weeks"][0]["matchups"][0]["teamBHasTiebreaker"]
        )

    def test_getYearByYearNumber_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup_1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        year_1 = Year(yearNumber=2000, teams=teams, weeks=[week_1])
        league = League(name="LEAGUE", owners=owners, years=[year_1])

        response = league.getYearByYearNumber(2000)
        self.assertEqual(year_1, response)

    def test_getYearByYearNumber_yearNotInLeague_raisesException(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup_1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        year_1 = Year(yearNumber=2000, teams=teams, weeks=[week_1])
        league = League(name="LEAGUE", owners=owners, years=[year_1])

        with self.assertRaises(DoesNotExistException) as context:
            league.getYearByYearNumber(2001)
        self.assertEqual(
            "League does not have a year with year number 2001", str(context.exception)
        )

    def test_getOwnerByName_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        owners[0].name = "owner0"
        matchup_1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        year_1 = Year(yearNumber=2000, teams=teams, weeks=[week_1])
        league = League(name="LEAGUE", owners=owners, years=[year_1])

        response = league.getOwnerByName("owner0")
        self.assertEqual(owners[0], response)

    def test_getOwnerByName_ownerNotInLeague_raisesException(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup_1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
        )
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        year_1 = Year(yearNumber=2000, teams=teams, weeks=[week_1])
        league = League(name="LEAGUE", owners=owners, years=[year_1])

        with self.assertRaises(DoesNotExistException) as context:
            league.getOwnerByName("owner0")
        self.assertEqual(
            "League does not have an owner with name 'owner0'", str(context.exception)
        )

    def test_league_fromJson(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup_1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1.1,
            teamBScore=2.2,
            matchupType=MatchupType.REGULAR_SEASON,
            teamAHasTiebreaker=True,
        )
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        year_1 = Year(yearNumber=2000, teams=teams, weeks=[week_1])
        league = League(name="LEAGUE", owners=owners, years=[year_1])
        leagueJson = league.toJson()
        leagueDerived = League.fromJson(leagueJson)
        self.assertEqual(league, leagueDerived)
        self.assertEqual(league.id, leagueDerived.id)

        # with year settings
        year_1.yearSettings = YearSettings(leagueMedianGames=True)
        leagueJson = league.toJson()
        leagueDerived = League.fromJson(leagueJson)
        self.assertEqual(league, leagueDerived)
        self.assertEqual(league.id, leagueDerived.id)
