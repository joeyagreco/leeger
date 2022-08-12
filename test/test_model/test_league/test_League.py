import unittest

from leeger.enum.MatchupType import MatchupType
from leeger.exception.InvalidLeagueFormatException import InvalidLeagueFormatException
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

    def test_league_eq_equal(self):
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
        year_2 = Year(yearNumber=2000, teams=teams_2, weeks=[week_2])
        league_2 = League(name="LEAGUE", owners=owners_2, years=[year_2])

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
        self.assertEqual("'LEAGUE 1' + 'LEAGUE 2' League", combinedLeague.name)
        self.assertEqual(2, len(combinedLeague.owners))
        self.assertEqual([owner.name for owner in league_1.owners], [owner.name for owner in league_1.owners])
        self.assertEqual(2, len(combinedLeague.years))
        self.assertEqual(2000, combinedLeague.years[0].yearNumber)
        self.assertEqual(2001, combinedLeague.years[1].yearNumber)

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


