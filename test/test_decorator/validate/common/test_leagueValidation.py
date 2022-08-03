import unittest

from leeger.decorator.validate.common import leagueValidation
from leeger.enum.MatchupType import MatchupType
from leeger.exception.InvalidLeagueFormatException import InvalidLeagueFormatException
from leeger.model.league.League import League
from leeger.model.league.Matchup import Matchup
from leeger.model.league.Owner import Owner
from leeger.model.league.Team import Team
from leeger.model.league.Week import Week
from leeger.model.league.Year import Year
from test.helper.prototypes import getNDefaultOwnersAndTeams


class TestLeagueValidation(unittest.TestCase):

    def test_runAllChecks_happyPath(self):
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

        leagueValidation.runAllChecks(League(name="TEST", owners=[owner1, owner2], years=[a_year, b_year]))

    def test_checkYearsAreInCorrectOrder_yearsArentInCorrectOrder_raisesException(self):
        a_week1 = Week(weekNumber=1, matchups=list())
        a_team1 = Team(ownerId="1", name="1")
        a_team2 = Team(ownerId="2", name="2")
        a_year = Year(yearNumber=2000, teams=[a_team1, a_team2], weeks=[a_week1])

        b_week1 = Week(weekNumber=1, matchups=list())
        b_team1 = Team(ownerId="1", name="1")
        b_team2 = Team(ownerId="2", name="2")
        b_year = Year(yearNumber=2001, teams=[b_team1, b_team2], weeks=[b_week1])

        with self.assertRaises(InvalidLeagueFormatException) as context:
            leagueValidation.checkYearsAreInCorrectOrder(League(name="TEST", owners=list(), years=[b_year, a_year]))
        self.assertEqual("Years are not in chronological order (oldest -> newest).", str(context.exception))

    def test_checkNoDuplicateYearNumbers_duplicateYearNumbers_raisesException(self):
        a_week1 = Week(weekNumber=1, matchups=list())
        a_team1 = Team(ownerId="1", name="1")
        a_team2 = Team(ownerId="2", name="2")
        a_year = Year(yearNumber=2000, teams=[a_team1, a_team2], weeks=[a_week1])

        b_week1 = Week(weekNumber=1, matchups=list())
        b_team1 = Team(ownerId="1", name="1")
        b_team2 = Team(ownerId="2", name="2")
        b_year = Year(yearNumber=2000, teams=[b_team1, b_team2], weeks=[b_week1])

        with self.assertRaises(InvalidLeagueFormatException) as context:
            leagueValidation.checkNoDuplicateYearNumbers(League(name="TEST", owners=list(), years=[a_year, b_year]))
        self.assertEqual("Can only have 1 of each year number within a league.", str(context.exception))

    def test_checkForDuplicateOwners_duplicateOwnerInstances_raisesException(self):
        owner = Owner(name="1")
        with self.assertRaises(InvalidLeagueFormatException) as context:
            leagueValidation.checkForDuplicateOwners(League(name="TEST", owners=[owner, owner], years=list()))
        self.assertEqual("Owners must all be unique instances.", str(context.exception))

    def test_checkForDuplicateTeams_duplicateOwnerInstances_raisesException(self):
        owner = Owner(name="1")
        year = Year(yearNumber=2000, teams=list(), weeks=list())
        with self.assertRaises(InvalidLeagueFormatException) as context:
            leagueValidation.checkForDuplicateYears(
                League(name="TEST", owners=[owner], years=[year, year]))
        self.assertEqual("Years must all be unique instances.", str(context.exception))

    def test_checkNoDuplicateOwnerNames_duplicateOwnerNames_raisesException(self):
        owner1 = Owner(name="name")
        owner2 = Owner(name="name")
        with self.assertRaises(InvalidLeagueFormatException) as context:
            leagueValidation.checkNoDuplicateOwnerNames(
                League(name="TEST", owners=[owner1, owner2], years=list()))
        self.assertEqual("All owners must have a unique name.", str(context.exception))

    def test_checkForDuplicateTeams_duplicateTeams_raisesException(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        week1 = Week(weekNumber=1, matchups=[matchup1])
        year1 = Year(yearNumber=2000, teams=teams, weeks=[week1])

        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        week2 = Week(weekNumber=1, matchups=[matchup2])
        year2 = Year(yearNumber=2001, teams=teams, weeks=[week2])

        with self.assertRaises(InvalidLeagueFormatException) as context:
            leagueValidation.checkForDuplicateTeams(League(name="", owners=owners, years=[year1, year2]))
        self.assertEqual("Teams must all be unique instances.", str(context.exception))

    def test_checkLeagueHasAtLeastOneYear_leagueHasNoYears_raisesException(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        with self.assertRaises(InvalidLeagueFormatException) as context:
            leagueValidation.checkLeagueHasAtLeastOneYear(
                League(name="TEST", owners=owners, years=list()))
        self.assertEqual("League must have at least 1 year.", str(context.exception))

    """
    TYPE CHECK TESTS
    """

    def test_checkAllTypes_leagueNameIsntTypeString_raisesException(self):
        with self.assertRaises(InvalidLeagueFormatException) as context:
            leagueValidation.checkAllTypes(League(name=None, owners=list(), years=list()))
        self.assertEqual("name must be type 'str'.", str(context.exception))

    def test_checkAllTypes_leagueOwnersIsntTypeList_raisesException(self):
        with self.assertRaises(InvalidLeagueFormatException) as context:
            leagueValidation.checkAllTypes(League(name="TEST", owners=None, years=list()))
        self.assertEqual("owners must be type 'list'.", str(context.exception))

    def test_checkAllTypes_leagueYearsIsntTypeList_raisesException(self):
        with self.assertRaises(InvalidLeagueFormatException) as context:
            leagueValidation.checkAllTypes(League(name="TEST", owners=list(), years=None))
        self.assertEqual("years must be type 'list'.", str(context.exception))
