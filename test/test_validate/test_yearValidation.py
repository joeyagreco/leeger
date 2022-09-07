import unittest

from leeger.enum.MatchupType import MatchupType
from leeger.exception.InvalidYearFormatException import InvalidYearFormatException
from leeger.model.league.Matchup import Matchup
from leeger.model.league.Owner import Owner
from leeger.model.league.Team import Team
from leeger.model.league.Week import Week
from leeger.model.league.Year import Year
from leeger.validate import yearValidation
from test.helper.prototypes import getNDefaultOwnersAndTeams


class TestYearValidation(unittest.TestCase):

    def test_checkOnlyOneChampionshipWeekInYear_twoChampionshipWeeksInYear_raisesException(self):
        owners, teams = getNDefaultOwnersAndTeams(2)
        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.CHAMPIONSHIP)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.CHAMPIONSHIP)
        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])

        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkOnlyOneChampionshipWeekInYear(Year(yearNumber=2000, teams=list(), weeks=[week1, week2]))
        self.assertEqual("Year 2000 has 2 championship weeks. Maximum is 1.", str(context.exception))

    def test_checkAtLeastOneWeekInYear_yearHasNoWeeks_raisesException(self):
        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkAtLeastOneWeekInYear(Year(yearNumber=2000, teams=list(), weeks=list()))
        self.assertEqual("Year 2000 does not have at least 1 week.", str(context.exception))

    def test_checkWeekNumberingInYear_yearDuplicateWeekNumbers_raisesException(self):
        week1 = Week(weekNumber=1, matchups=list())
        week1duplicate = Week(weekNumber=1, matchups=list())

        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkWeekNumberingInYear(Year(yearNumber=2000, teams=list(), weeks=[week1, week1duplicate]))
        self.assertEqual("Year 2000 has duplicate week numbers.", str(context.exception))

    def test_checkWeekNumberingInYear_lowestWeekNumberIsNotOne_raisesException(self):
        week2 = Week(weekNumber=2, matchups=list())

        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkWeekNumberingInYear(Year(yearNumber=2000, teams=list(), weeks=[week2]))
        self.assertEqual("First week in year 2000 must be 1, not 2.", str(context.exception))

    def test_checkWeekNumberingInYear_weekNumbersNotOneThroughN_raisesException(self):
        week1 = Week(weekNumber=1, matchups=list())
        week2 = Week(weekNumber=2, matchups=list())
        week3 = Week(weekNumber=3, matchups=list())
        week4 = Week(weekNumber=4, matchups=list())

        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkWeekNumberingInYear(
                Year(yearNumber=2000, teams=list(), weeks=[week1, week2, week4]))  # no week 3
        self.assertEqual("Year 2000 does not have week numbers in order (1-n).", str(context.exception))

        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkWeekNumberingInYear(
                Year(yearNumber=2000, teams=list(), weeks=[week1, week2, week4, week3]))  # weeks not in order
        self.assertEqual("Year 2000 does not have week numbers in order (1-n).", str(context.exception))

    def test_checkPlayoffWeekOrderingInYear_nonPlayoffWeekAfterPlayoffWeek_raisesException(self):
        matchup1 = Matchup(teamAId="", teamBId="", teamAScore=0, teamBScore=0, matchupType=MatchupType.PLAYOFF)
        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=list())

        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkPlayoffWeekOrderingInYear(Year(yearNumber=2000, teams=list(), weeks=[week1, week2]))
        self.assertEqual("Year 2000 has a non-playoff week after a playoff week.", str(context.exception))

    def test_checkPlayoffWeekOrderingInYear_nonChampionshipWeekAfterChampionshipWeek_raisesException(self):
        owners, teams = getNDefaultOwnersAndTeams(2)
        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.CHAMPIONSHIP)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2,
                           matchupType=MatchupType.PLAYOFF)
        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])

        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkPlayoffWeekOrderingInYear(Year(yearNumber=2000, teams=list(), weeks=[week1, week2]))
        self.assertEqual("Year 2000 has a non-championship week after a championship week.", str(context.exception))

    def test_checkAtLeastTwoTeamsInYear_yearHasLessThanTwoTeams_raisesException(self):
        week1 = Week(weekNumber=1, matchups=list())
        week2 = Week(weekNumber=2, matchups=list())
        team1 = Team(ownerId="1", name="1")

        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkAtLeastTwoTeamsInYear(Year(yearNumber=2000, teams=[team1], weeks=[week1, week2]))
        self.assertEqual("Year 2000 needs at least 2 teams.", str(context.exception))

    def test_checkGivenYearHasValidYearNumber_yearNumberIsntInValidRange_raisesException(self):
        week1 = Week(weekNumber=1, matchups=list())
        team1 = Team(ownerId="1", name="1")
        team2 = Team(ownerId="2", name="2")

        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkGivenYearHasValidYearNumber(Year(yearNumber=1919, teams=[team1, team2], weeks=[week1]))
        self.assertEqual("Year 1919 is not in range 1920-2XXX.", str(context.exception))

        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkGivenYearHasValidYearNumber(Year(yearNumber=3000, teams=[team1, team2], weeks=[week1]))
        self.assertEqual("Year 3000 is not in range 1920-2XXX.", str(context.exception))

    def test_checkTeamOwnerIdsInYear_teamsHaveDuplicateOwnerIds_raisesException(self):
        week1 = Week(weekNumber=1, matchups=list())
        team1 = Team(ownerId="1", name="1")
        team2 = Team(ownerId="1", name="2")

        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkTeamOwnerIdsInYear(Year(yearNumber=2000, teams=[team1, team2], weeks=[week1]))
        self.assertEqual("Year 2000 has teams with the same owner IDs.", str(context.exception))

    def test_checkTeamNamesInYear_teamsInAYearHaveDuplicateNames_raisesException(self):
        week1 = Week(weekNumber=1, matchups=list())

        owner1 = Owner(name="1")
        owner2 = Owner(name="2")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="1")

        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkTeamNamesInYear(Year(yearNumber=2000, teams=[team1, team2], weeks=[week1]))
        self.assertEqual("Year 2000 has teams with duplicate names.", str(context.exception))

    def test_checkTeamNamesInYear_teamsInAYearHaveSimilarNames_raisesException(self):
        week1 = Week(weekNumber=1, matchups=list())

        # SPACE DIFFERENCE
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")

        team1 = Team(ownerId=owner1.id, name="1 ")  # has a space in name
        team2 = Team(ownerId=owner2.id, name="1")

        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkTeamNamesInYear(Year(yearNumber=2000, teams=[team1, team2], weeks=[week1]))
        self.assertEqual("Year 2000 has teams with very similar names.", str(context.exception))

        # TAB DIFFERENCE
        team1 = Team(ownerId=owner1.id, name="1\t")  # has a tab in name
        team2 = Team(ownerId=owner2.id, name="1")

        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkTeamNamesInYear(Year(yearNumber=2000, teams=[team1, team2], weeks=[week1]))
        self.assertEqual("Year 2000 has teams with very similar names.", str(context.exception))

        # NEWLINE DIFFERENCE
        team1 = Team(ownerId=owner1.id, name="1\n")  # has a newline in name
        team2 = Team(ownerId=owner2.id, name="1")

        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkTeamNamesInYear(Year(yearNumber=2000, teams=[team1, team2], weeks=[week1]))
        self.assertEqual("Year 2000 has teams with very similar names.", str(context.exception))

    def test_checkForDuplicateTeams_duplicateTeams_raisesException(self):
        owners, teams = getNDefaultOwnersAndTeams(1)
        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkForDuplicateTeams(Year(yearNumber=2000, teams=[teams[0], teams[0]], weeks=list()))
        self.assertEqual("Teams must all be unique instances.", str(context.exception))

    def test_checkForDuplicateWeeks_duplicateWeeks_raisesException(self):
        week = Week(weekNumber=1, matchups=list())
        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkForDuplicateWeeks(Year(yearNumber=2000, teams=list(), weeks=[week, week]))
        self.assertEqual("Weeks must all be unique instances.", str(context.exception))

    def test_checkEveryTeamInYearIsInAMatchup_teamNotInAnyMatchups_raisesException(self):
        owners, teams = getNDefaultOwnersAndTeams(3)
        matchup = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        week = Week(weekNumber=1, matchups=[matchup])
        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkEveryTeamInYearIsInAMatchup(Year(yearNumber=2000, teams=teams, weeks=[week, week]))
        self.assertEqual(
            f"Year 2000 has teams that are not in any matchups. Team IDs not in matchups: ['{teams[2].id}']",
            str(context.exception))

    def test_checkMultiWeekMatchupIdUsedInNonConsecutiveWeeks_raisesException(self):
        owners, teams = getNDefaultOwnersAndTeams(3)
        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2, multiWeekMatchupId="1")
        week1 = Week(weekNumber=1, matchups=[matchup1])
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        week2 = Week(weekNumber=2, matchups=[matchup2])
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2, multiWeekMatchupId="1")
        week3 = Week(weekNumber=3, matchups=[matchup3])
        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkMultiWeekMatchupsAreInConsecutiveWeeks(
                Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3]))
        self.assertEqual(
            f"Year 2000 has multi-week matchups with ID '1' that are not in consecutive weeks.", str(context.exception))

    def test_checkMultiWeekMatchupIdUsedInConsecutiveWeeks_doesNotRaiseException(self):
        owners, teams = getNDefaultOwnersAndTeams(3)
        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2, multiWeekMatchupId="1")
        week1 = Week(weekNumber=1, matchups=[matchup1])
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2, multiWeekMatchupId="1")
        week2 = Week(weekNumber=2, matchups=[matchup2])
        yearValidation.checkMultiWeekMatchupsAreInConsecutiveWeeks(
            Year(yearNumber=2000, teams=teams, weeks=[week1, week2]))

    def test_checkMultiWeekMatchupIdUsedInOneWeek_doesNotRaiseException(self):
        owners, teams = getNDefaultOwnersAndTeams(3)
        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2, multiWeekMatchupId="1")
        week1 = Week(weekNumber=1, matchups=[matchup1])
        yearValidation.checkMultiWeekMatchupsAreInConsecutiveWeeks(Year(yearNumber=2000, teams=teams, weeks=[week1]))

    """
    TYPE CHECK TESTS
    """

    def test_checkAllTypes_yearNumberIsntTypeInt_raisesException(self):
        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkAllTypes(Year(yearNumber=None, teams=list(), weeks=list()))
        self.assertEqual("yearNumber must be type 'int'.", str(context.exception))

    def test_checkAllTypes_yearTeamsIsntTypeList_raisesException(self):
        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkAllTypes(Year(yearNumber=2000, teams=None, weeks=list()))
        self.assertEqual("teams must be type 'list'.", str(context.exception))

    def test_checkAllTypes_yearWeeksIsntTypeList_raisesException(self):
        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkAllTypes(Year(yearNumber=2000, teams=list(), weeks=None))
        self.assertEqual("weeks must be type 'list'.", str(context.exception))
