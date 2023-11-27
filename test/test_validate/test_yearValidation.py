import unittest
from test.helper.prototypes import getNDefaultOwnersAndTeams

from leeger.enum.MatchupType import MatchupType
from leeger.exception.InvalidYearFormatException import InvalidYearFormatException
from leeger.model.league.Division import Division
from leeger.model.league.Matchup import Matchup
from leeger.model.league.Owner import Owner
from leeger.model.league.Team import Team
from leeger.model.league.Week import Week
from leeger.model.league.Year import Year
from leeger.validate import yearValidation


class TestYearValidation(unittest.TestCase):
    def test_checkAtLeastOneWeekInYear_yearHasNoWeeks_raisesException(self):
        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkAtLeastOneWeekInYear(
                Year(yearNumber=2000, teams=list(), weeks=list())
            )
        self.assertEqual("Year 2000 does not have at least 1 week.", str(context.exception))

    def test_checkWeekNumberingInYear_yearDuplicateWeekNumbers_raisesException(self):
        week1 = Week(weekNumber=1, matchups=list())
        week1duplicate = Week(weekNumber=1, matchups=list())

        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkWeekNumberingInYear(
                Year(yearNumber=2000, teams=list(), weeks=[week1, week1duplicate])
            )
        self.assertEqual("Year 2000 has duplicate week numbers.", str(context.exception))

    def test_checkWeekNumberingInYear_lowestWeekNumberIsNotOne_raisesException(self):
        week2 = Week(weekNumber=2, matchups=list())

        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkWeekNumberingInYear(
                Year(yearNumber=2000, teams=list(), weeks=[week2])
            )
        self.assertEqual("First week in year 2000 must be 1, not 2.", str(context.exception))

    def test_checkWeekNumberingInYear_weekNumbersNotOneThroughN_raisesException(self):
        week1 = Week(weekNumber=1, matchups=list())
        week2 = Week(weekNumber=2, matchups=list())
        week3 = Week(weekNumber=3, matchups=list())
        week4 = Week(weekNumber=4, matchups=list())

        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkWeekNumberingInYear(
                Year(yearNumber=2000, teams=list(), weeks=[week1, week2, week4])
            )  # no week 3
        self.assertEqual(
            "Year 2000 does not have week numbers in order (1-n).", str(context.exception)
        )

        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkWeekNumberingInYear(
                Year(yearNumber=2000, teams=list(), weeks=[week1, week2, week4, week3])
            )  # weeks not in order
        self.assertEqual(
            "Year 2000 does not have week numbers in order (1-n).", str(context.exception)
        )

    def test_checkPlayoffWeekOrderingInYear_nonPlayoffWeekAfterPlayoffWeek_raisesException(self):
        matchup1 = Matchup(
            teamAId="", teamBId="", teamAScore=0, teamBScore=0, matchupType=MatchupType.PLAYOFF
        )
        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=list())

        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkPlayoffWeekOrderingInYear(
                Year(yearNumber=2000, teams=list(), weeks=[week1, week2])
            )
        self.assertEqual(
            "Year 2000 has a non-playoff week after a playoff week.", str(context.exception)
        )

    def test_checkPlayoffWeekOrderingInYear_nonChampionshipWeekAfterChampionshipWeek_raisesException(
        self,
    ):
        owners, teams = getNDefaultOwnersAndTeams(2)
        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )
        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])

        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkPlayoffWeekOrderingInYear(
                Year(yearNumber=2000, teams=list(), weeks=[week1, week2])
            )
        self.assertEqual(
            "Year 2000 has a non-championship week after a championship week.",
            str(context.exception),
        )

    def test_checkAtLeastTwoTeamsInYear_yearHasLessThanTwoTeams_raisesException(self):
        week1 = Week(weekNumber=1, matchups=list())
        week2 = Week(weekNumber=2, matchups=list())
        team1 = Team(ownerId="1", name="1")

        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkAtLeastTwoTeamsInYear(
                Year(yearNumber=2000, teams=[team1], weeks=[week1, week2])
            )
        self.assertEqual("Year 2000 needs at least 2 teams.", str(context.exception))

    def test_checkGivenYearHasValidYearNumber_yearNumberIsntInValidRange_raisesException(self):
        week1 = Week(weekNumber=1, matchups=list())
        team1 = Team(ownerId="1", name="1")
        team2 = Team(ownerId="2", name="2")

        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkGivenYearHasValidYearNumber(
                Year(yearNumber=1919, teams=[team1, team2], weeks=[week1])
            )
        self.assertEqual("Year 1919 is not in range 1920-2XXX.", str(context.exception))

        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkGivenYearHasValidYearNumber(
                Year(yearNumber=3000, teams=[team1, team2], weeks=[week1])
            )
        self.assertEqual("Year 3000 is not in range 1920-2XXX.", str(context.exception))

    def test_checkTeamOwnerIdsInYear_teamsHaveDuplicateOwnerIds_raisesException(self):
        week1 = Week(weekNumber=1, matchups=list())
        team1 = Team(ownerId="1", name="1")
        team2 = Team(ownerId="1", name="2")

        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkTeamOwnerIdsInYear(
                Year(yearNumber=2000, teams=[team1, team2], weeks=[week1])
            )
        self.assertEqual("Year 2000 has teams with the same owner IDs.", str(context.exception))

    def test_checkTeamNamesInYear_teamsInAYearHaveDuplicateNames_raisesException(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="1")

        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkTeamNamesInYear(
                Year(yearNumber=2000, teams=[team1, team2], weeks=list())
            )
        self.assertEqual("Year 2000 has teams with duplicate names.", str(context.exception))

    def test_checkTeamNamesInYear_teamsInAYearHaveSimilarNames_raisesException(self):
        # SPACE DIFFERENCE
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")

        team1 = Team(ownerId=owner1.id, name="1 ")  # has a space in name
        team2 = Team(ownerId=owner2.id, name="1")

        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkTeamNamesInYear(
                Year(yearNumber=2000, teams=[team1, team2], weeks=list())
            )
        self.assertEqual("Year 2000 has teams with very similar names.", str(context.exception))

        # TAB DIFFERENCE
        team1 = Team(ownerId=owner1.id, name="1\t")  # has a tab in name
        team2 = Team(ownerId=owner2.id, name="1")

        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkTeamNamesInYear(
                Year(yearNumber=2000, teams=[team1, team2], weeks=list())
            )
        self.assertEqual("Year 2000 has teams with very similar names.", str(context.exception))

        # NEWLINE DIFFERENCE
        team1 = Team(ownerId=owner1.id, name="1\n")  # has a newline in name
        team2 = Team(ownerId=owner2.id, name="1")

        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkTeamNamesInYear(
                Year(yearNumber=2000, teams=[team1, team2], weeks=list())
            )
        self.assertEqual("Year 2000 has teams with very similar names.", str(context.exception))

        # CASE DIFFERENCE
        team1 = Team(ownerId=owner1.id, name="A")
        team2 = Team(ownerId=owner2.id, name="a")

        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkTeamNamesInYear(
                Year(yearNumber=2000, teams=[team1, team2], weeks=list())
            )
        self.assertEqual("Year 2000 has teams with very similar names.", str(context.exception))

    def test_checkDivisionNamesInYear_divisionsInAYearHaveDuplicateNames_raisesException(self):
        division1 = Division(name="div")
        division2 = Division(name="div")

        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkDivisionNamesInYear(
                Year(yearNumber=2000, teams=list(), weeks=list(), divisions=[division1, division2])
            )
        self.assertEqual("Year 2000 has divisions with duplicate names.", str(context.exception))

    def test_checkDivisionNamesInYear_divisionsInAYearHaveSimilarNames_raisesException(self):
        # SPACE DIFFERENCE
        division1 = Division(name="div ")  # has a space in name
        division2 = Division(name="div")

        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkDivisionNamesInYear(
                Year(yearNumber=2000, teams=list(), weeks=list(), divisions=[division1, division2])
            )
        self.assertEqual("Year 2000 has divisions with very similar names.", str(context.exception))

        # TAB DIFFERENCE
        division1 = Division(name="div\t")  # has a tab in name
        division2 = Division(name="div")

        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkDivisionNamesInYear(
                Year(yearNumber=2000, teams=list(), weeks=list(), divisions=[division1, division2])
            )
        self.assertEqual("Year 2000 has divisions with very similar names.", str(context.exception))

        # NEWLINE DIFFERENCE
        division1 = Division(name="div\t")  # has a newline in name
        division2 = Division(name="div")

        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkDivisionNamesInYear(
                Year(yearNumber=2000, teams=list(), weeks=list(), divisions=[division1, division2])
            )
        self.assertEqual("Year 2000 has divisions with very similar names.", str(context.exception))

        # CASE DIFFERENCE
        division1 = Division(name="DIV")
        division2 = Division(name="div")

        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkDivisionNamesInYear(
                Year(yearNumber=2000, teams=list(), weeks=list(), divisions=[division1, division2])
            )
        self.assertEqual("Year 2000 has divisions with very similar names.", str(context.exception))

    def test_checkForDuplicateTeams_duplicateTeams_raisesException(self):
        _, teams = getNDefaultOwnersAndTeams(1)
        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkForDuplicateTeams(
                Year(yearNumber=2000, teams=[teams[0], teams[0]], weeks=list())
            )
        self.assertEqual("Teams must all be unique instances.", str(context.exception))

    def test_checkForDuplicateWeeks_duplicateWeeks_raisesException(self):
        week = Week(weekNumber=1, matchups=list())
        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkForDuplicateWeeks(
                Year(yearNumber=2000, teams=list(), weeks=[week, week])
            )
        self.assertEqual("Weeks must all be unique instances.", str(context.exception))

    def test_checkForDuplicateDivisions_duplicateDivisions_raisesException(self):
        division = Division(name="div")
        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkForDuplicateDivisions(
                Year(yearNumber=2000, teams=list(), weeks=list(), divisions=[division, division])
            )
        self.assertEqual("Divisions must all be unique instances.", str(context.exception))

    def test_checkEveryTeamInYearIsInAMatchup_teamNotInAnyMatchups_raisesException(self):
        _, teams = getNDefaultOwnersAndTeams(3)
        matchup = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        week = Week(weekNumber=1, matchups=[matchup])
        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkEveryTeamInYearIsInAMatchup(
                Year(yearNumber=2000, teams=teams, weeks=[week, week])
            )
        self.assertEqual(
            f"Year 2000 has teams that are not in any matchups. Team IDs not in matchups: ['{teams[2].id}']",
            str(context.exception),
        )

    def test_checkMultiWeekMatchupsAreInConsecutiveWeeks_multiWeekMatchupIdUsedInNonConsecutiveWeeks_raisesException(
        self,
    ):
        _, teams = getNDefaultOwnersAndTeams(3)
        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            multiWeekMatchupId="1",
        )
        week1 = Week(weekNumber=1, matchups=[matchup1])
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        week2 = Week(weekNumber=2, matchups=[matchup2])
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            multiWeekMatchupId="1",
        )
        week3 = Week(weekNumber=3, matchups=[matchup3])
        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkMultiWeekMatchupsAreInConsecutiveWeeks(
                Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])
            )
        self.assertEqual(
            f"Year 2000 has multi-week matchups with ID '1' that are not in consecutive weeks.",
            str(context.exception),
        )

    def test_checkMultiWeekMatchupIdUsedInConsecutiveWeeks_doesNotRaiseException(self):
        _, teams = getNDefaultOwnersAndTeams(3)
        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            multiWeekMatchupId="1",
        )
        week1 = Week(weekNumber=1, matchups=[matchup1])
        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            multiWeekMatchupId="1",
        )
        week2 = Week(weekNumber=2, matchups=[matchup2])
        yearValidation.checkMultiWeekMatchupsAreInConsecutiveWeeks(
            Year(yearNumber=2000, teams=teams, weeks=[week1, week2])
        )

    def test_checkMultiWeekMatchupIdUsedInOneWeek_doesNotRaiseException(self):
        _, teams = getNDefaultOwnersAndTeams(3)
        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            multiWeekMatchupId="1",
        )
        week1 = Week(weekNumber=1, matchups=[matchup1])
        yearValidation.checkMultiWeekMatchupsAreInConsecutiveWeeks(
            Year(yearNumber=2000, teams=teams, weeks=[week1])
        )

    def test_checkMultiWeekMatchupsAreInMoreThanOneWeekOrAreNotTheMostRecentWeek_multiWeekMatchupOnlyInOneWeekThatIsNotTheMostRecent_raisesException(
        self,
    ):
        _, teams = getNDefaultOwnersAndTeams(3)
        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            multiWeekMatchupId="1",
        )
        week1 = Week(weekNumber=1, matchups=[matchup1])
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        week2 = Week(weekNumber=2, matchups=[matchup2])
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        week3 = Week(weekNumber=3, matchups=[matchup3])
        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkMultiWeekMatchupsAreInMoreThanOneWeekOrAreNotTheMostRecentWeek(
                Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])
            )
        self.assertEqual(
            f"Year 2000 has multi-week matchup with ID '1' that only occurs once and is not the most recent week.",
            str(context.exception),
        )

    def test_checkMultiWeekMatchupsAreInMoreThanOneWeekOrAreNotTheMostRecentWeek_multiWeekMatchupOnlyInOneWeekThatIsTheMostRecent_doesNotRaiseException(
        self,
    ):
        _, teams = getNDefaultOwnersAndTeams(3)
        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        week1 = Week(weekNumber=1, matchups=[matchup1])
        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            multiWeekMatchupId="1",
        )
        week2 = Week(weekNumber=2, matchups=[matchup2])
        yearValidation.checkMultiWeekMatchupsAreInMoreThanOneWeekOrAreNotTheMostRecentWeek(
            Year(yearNumber=2000, teams=teams, weeks=[week1, week2])
        )

    def test_checkMultiWeekMatchupsAreInMoreThanOneWeekOrAreNotTheMostRecentWeek_multiWeekMatchupInOneWeekThatIsTheMostRecentAndOtherMultiWeekMatchupHasMultipleWeeks_doesNotRaiseException(
        self,
    ):
        _, teams = getNDefaultOwnersAndTeams(3)
        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            multiWeekMatchupId="2",
        )
        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2])
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            multiWeekMatchupId="2",
        )
        matchup4 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            multiWeekMatchupId="1",
        )
        week2 = Week(weekNumber=2, matchups=[matchup3, matchup4])
        yearValidation.checkMultiWeekMatchupsAreInMoreThanOneWeekOrAreNotTheMostRecentWeek(
            Year(yearNumber=2000, teams=teams, weeks=[week1, week2])
        )

    def test_checkMultiWeekMatchupsWithSameIdHaveSameMatchupType_multiWeekMatchupsDoNotAllHaveTheSameMatchupType_raisesException(
        self,
    ):
        _, teams = getNDefaultOwnersAndTeams(3)
        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.REGULAR_SEASON,
            multiWeekMatchupId="1",
        )
        week1 = Week(weekNumber=1, matchups=[matchup1])
        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
            multiWeekMatchupId="1",
        )
        week2 = Week(weekNumber=2, matchups=[matchup2])
        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkMultiWeekMatchupsWithSameIdHaveSameMatchupType(
                Year(yearNumber=2000, teams=teams, weeks=[week1, week2])
            )
        self.assertEqual(
            f"Multi-week matchups with ID '1' do not all have the same matchup type.",
            str(context.exception),
        )

    def test_checkMultiWeekMatchupsWithSameIdHaveSameTeamIds_multiWeekMatchupsDoNotAllHaveTheSameTeamA_raisesException(
        self,
    ):
        _, teams = getNDefaultOwnersAndTeams(3)
        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.REGULAR_SEASON,
            multiWeekMatchupId="1",
        )
        week1 = Week(weekNumber=1, matchups=[matchup1])
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
            multiWeekMatchupId="1",
        )
        week2 = Week(weekNumber=2, matchups=[matchup2])
        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkMultiWeekMatchupsWithSameIdHaveSameTeamIds(
                Year(yearNumber=2000, teams=teams, weeks=[week1, week2])
            )
        self.assertEqual(
            f"Multi-week matchups with ID '1' do not all have the same teamA and teamB.",
            str(context.exception),
        )

    def test_checkMultiWeekMatchupsWithSameIdHaveSameTeamIds_multiWeekMatchupsDoNotAllHaveTheSameTeamB_raisesException(
        self,
    ):
        _, teams = getNDefaultOwnersAndTeams(3)
        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.REGULAR_SEASON,
            multiWeekMatchupId="1",
        )
        week1 = Week(weekNumber=1, matchups=[matchup1])
        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[2].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
            multiWeekMatchupId="1",
        )
        week2 = Week(weekNumber=2, matchups=[matchup2])
        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkMultiWeekMatchupsWithSameIdHaveSameTeamIds(
                Year(yearNumber=2000, teams=teams, weeks=[week1, week2])
            )
        self.assertEqual(
            f"Multi-week matchups with ID '1' do not all have the same teamA and teamB.",
            str(context.exception),
        )

    def test_checkMultiWeekMatchupsWithSameIdHaveSameTeamIds_multiWeekMatchupsHaveSwappedTeamAAndTeamB_raisesException(
        self,
    ):
        _, teams = getNDefaultOwnersAndTeams(3)
        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.REGULAR_SEASON,
            multiWeekMatchupId="1",
        )
        week1 = Week(weekNumber=1, matchups=[matchup1])
        matchup2 = Matchup(
            teamAId=teams[1].id,
            teamBId=teams[0].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
            multiWeekMatchupId="1",
        )
        week2 = Week(weekNumber=2, matchups=[matchup2])
        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkMultiWeekMatchupsWithSameIdHaveSameTeamIds(
                Year(yearNumber=2000, teams=teams, weeks=[week1, week2])
            )
        self.assertEqual(
            f"Multi-week matchups with ID '1' do not all have the same teamA and teamB.",
            str(context.exception),
        )

    def test_checkMultiWeekMatchupsWithSameIdHaveSameTiebreakers_differentTiebreakersForTeamA_raisesException(
        self,
    ):
        _, teams = getNDefaultOwnersAndTeams(3)
        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            multiWeekMatchupId="1",
            teamAHasTiebreaker=True,
        )
        week1 = Week(weekNumber=1, matchups=[matchup1])
        matchup2 = Matchup(
            teamAId=teams[1].id,
            teamBId=teams[0].id,
            teamAScore=1,
            teamBScore=2,
            multiWeekMatchupId="1",
        )
        week2 = Week(weekNumber=2, matchups=[matchup2])
        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkMultiWeekMatchupsWithSameIdHaveSameTiebreakers(
                Year(yearNumber=2000, teams=teams, weeks=[week1, week2])
            )
        self.assertEqual(
            f"Multi-week matchups with ID '1' do not all have the same tiebreakers.",
            str(context.exception),
        )

    def test_checkMultiWeekMatchupsWithSameIdHaveSameTiebreakers_differentTiebreakersForTeamB_raisesException(
        self,
    ):
        _, teams = getNDefaultOwnersAndTeams(3)
        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            multiWeekMatchupId="1",
            teamBHasTiebreaker=True,
        )
        week1 = Week(weekNumber=1, matchups=[matchup1])
        matchup2 = Matchup(
            teamAId=teams[1].id,
            teamBId=teams[0].id,
            teamAScore=1,
            teamBScore=2,
            multiWeekMatchupId="1",
        )
        week2 = Week(weekNumber=2, matchups=[matchup2])
        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkMultiWeekMatchupsWithSameIdHaveSameTiebreakers(
                Year(yearNumber=2000, teams=teams, weeks=[week1, week2])
            )
        self.assertEqual(
            f"Multi-week matchups with ID '1' do not all have the same tiebreakers.",
            str(context.exception),
        )

    def test_checkEitherAllTeamsAreInADivisionOrNoTeamsAreInADivision(self):
        # all teams in division, no error
        team1 = Team(ownerId="", name="", divisionId="1")
        team2 = Team(ownerId="", name="", divisionId="2")

        year = Year(yearNumber=2000, teams=[team1, team2], weeks=list())

        yearValidation.checkEitherAllTeamsAreInADivisionOrNoTeamsAreInADivision(year)

        # no teams in division, no error
        team1 = Team(ownerId="", name="", divisionId=None)
        team2 = Team(ownerId="", name="", divisionId=None)

        year = Year(yearNumber=2000, teams=[team1, team2], weeks=list())

        yearValidation.checkEitherAllTeamsAreInADivisionOrNoTeamsAreInADivision(year)

        # some teams in division, has error
        team1 = Team(ownerId="", name="", divisionId="1")
        team2 = Team(ownerId="", name="", divisionId=None)

        year = Year(yearNumber=2000, teams=[team1, team2], weeks=list())

        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkEitherAllTeamsAreInADivisionOrNoTeamsAreInADivision(year)
        self.assertEqual(
            f"Only some teams in Year 2000 have a Division ID.", str(context.exception)
        )

    def test_checkDivisionIdsMatchTeamDivisionIds(self):
        # ids match, no error
        division1 = Division(name="d1")
        division2 = Division(name="d2")
        team1 = Team(ownerId="", name="", divisionId=division1.id)
        team2 = Team(ownerId="", name="", divisionId=division2.id)

        year = Year(
            yearNumber=2000, teams=[team1, team2], weeks=list(), divisions=[division1, division2]
        )

        yearValidation.checkDivisionIdsMatchTeamDivisionIds(year)

        # divisions that do not belong to any team
        division1 = Division(name="d1")
        division2 = Division(name="d2")
        team1 = Team(ownerId="", name="", divisionId=division1.id)
        team2 = Team(ownerId="", name="", divisionId=division1.id)

        year = Year(
            yearNumber=2000, teams=[team1, team2], weeks=list(), divisions=[division1, division2]
        )

        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkDivisionIdsMatchTeamDivisionIds(year)
        self.assertEqual(
            f"There are Divisions in Year 2000 that do not belong to any Team.",
            str(context.exception),
        )

        # team division ids that do not belong to any division
        division1 = Division(name="d1")
        team1 = Team(ownerId="", name="", divisionId=division1.id)
        team2 = Team(ownerId="", name="", divisionId="d2")

        year = Year(yearNumber=2000, teams=[team1, team2], weeks=list(), divisions=[division1])

        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkDivisionIdsMatchTeamDivisionIds(year)
        self.assertEqual(
            f"There are Teams with Division IDs in Year 2000 that do not belong to any Division.",
            str(context.exception),
        )

        # no teams with division IDs in year but year has divisions, has error
        division1 = Division(name="d1")
        division2 = Division(name="d2")
        team1 = Team(ownerId="", name="")
        team2 = Team(ownerId="", name="")

        year = Year(
            yearNumber=2000, teams=[team1, team2], weeks=list(), divisions=[division1, division2]
        )

        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkDivisionIdsMatchTeamDivisionIds(year)
        self.assertEqual(
            f"Year 2000 has Divisions, but Teams in Year 2000 have Division IDs.",
            str(context.exception),
        )

        # no divisions in year but teams have divisions, has error
        team1 = Team(ownerId="", name="", divisionId="a")
        team2 = Team(ownerId="", name="", divisionId="b")

        year = Year(yearNumber=2000, teams=[team1, team2], weeks=list(), divisions=list())

        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkDivisionIdsMatchTeamDivisionIds(year)
        self.assertEqual(
            f"Teams in Year 2000 have Division IDs, but Year 2000 has no Divisions.",
            str(context.exception),
        )

        # division ids do not match between divisions and team division ids
        division1 = Division(name="d1")
        division2 = Division(name="d2")
        team1 = Team(ownerId="", name="", divisionId="d3")
        team2 = Team(ownerId="", name="", divisionId="d4")

        year = Year(
            yearNumber=2000, teams=[team1, team2], weeks=list(), divisions=[division1, division2]
        )

        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkDivisionIdsMatchTeamDivisionIds(year)
        self.assertEqual(
            f"The Divisions in Year 2000 do not corrospond correctly to the Team Division IDs in Year 2000.",
            str(context.exception),
        )

    def test_checkDivisionsHaveNoDuplicateIds(self):
        # no duplicate division ids, no error
        division1 = Division(name="d1")
        division2 = Division(name="d2")
        team1 = Team(ownerId="", name="", divisionId=division1.id)
        team2 = Team(ownerId="", name="", divisionId=division2.id)

        year = Year(
            yearNumber=2000, teams=[team1, team2], weeks=list(), divisions=[division1, division2]
        )

        yearValidation.checkDivisionsHaveNoDuplicateIds(year)

        # duplicate division ids, has error
        division1 = Division(name="d1")
        division2 = Division(name="d2")
        division2_dup = Division(name="d2 dup")
        division2_dup.id = division2.id

        team1 = Team(ownerId="", name="", divisionId=division1.id)
        team2 = Team(ownerId="", name="", divisionId=division2.id)

        year = Year(
            yearNumber=2000,
            teams=[team1, team2],
            weeks=list(),
            divisions=[division1, division2, division2_dup],
        )

        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkDivisionsHaveNoDuplicateIds(year)
        self.assertEqual(f"Year 2000 has duplicate division IDs.", str(context.exception))

    """
    TYPE CHECK TESTS
    """

    def test_checkAllTypes_yearNumberIsntTypeInt_raisesException(self):
        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkAllTypes(Year(yearNumber=None, teams=list(), weeks=list()))
        self.assertEqual("yearNumber must be type 'int'.", str(context.exception))

    def test_checkAllTypes_yearTeamsIsntTypeList_raisesException(self):
        # not given a list
        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkAllTypes(Year(yearNumber=2000, teams=None, weeks=list()))
        self.assertEqual("teams must be type 'list[Team]'.", str(context.exception))

        # given a list of non Team
        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkAllTypes(Year(yearNumber=2000, teams=["foo"], weeks=list()))
        self.assertEqual("teams must be type 'list[Team]'.", str(context.exception))

    def test_checkAllTypes_yearWeeksIsntTypeList_raisesException(self):
        # not given a list
        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkAllTypes(Year(yearNumber=2000, teams=list(), weeks=None))
        self.assertEqual("weeks must be type 'list[Week]'.", str(context.exception))

        # given a list of non Week
        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkAllTypes(Year(yearNumber=2000, teams=list(), weeks=["foo"]))
        self.assertEqual("weeks must be type 'list[Week]'.", str(context.exception))

    def test_checkAllTypes_divisionsIsntTypeList_raisesException(self):
        # not given a list
        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkAllTypes(
                Year(yearNumber=2000, teams=list(), weeks=list(), divisions="")
            )
        self.assertEqual("divisions must be type 'list[Division]'.", str(context.exception))

        # given a list of non Division
        with self.assertRaises(InvalidYearFormatException) as context:
            yearValidation.checkAllTypes(
                Year(yearNumber=2000, teams=list(), weeks=list(), divisions=["foo"])
            )
        self.assertEqual("divisions must be type 'list[Division]'.", str(context.exception))

    def test_checkAllTypes_yearSettingsIsntTypeYearSettings_raisesException(self):
        with self.assertRaises(InvalidYearFormatException) as context:
            year = Year(yearNumber=2000, teams=list(), weeks=list())
            year.yearSettings = None
            yearValidation.checkAllTypes(year)
        self.assertEqual("yearSettings must be type 'YearSettings'.", str(context.exception))
