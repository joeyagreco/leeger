import unittest

from leeger.enum.MatchupType import MatchupType
from leeger.exception.DoesNotExistException import DoesNotExistException
from leeger.model.filter.YearFilters import YearFilters
from leeger.model.league import YearSettings
from leeger.model.league.Division import Division
from leeger.model.league.Matchup import Matchup
from leeger.model.league.Owner import Owner
from leeger.model.league.Team import Team
from leeger.model.league.Week import Week
from leeger.model.league.Year import Year
from leeger.util.navigator.YearNavigator import YearNavigator
from test.helper.prototypes import getNDefaultOwnersAndTeams


class TestYearNavigator(unittest.TestCase):
    def test_getTeamById_happyPath(self):
        team = Team(ownerId="oid", name="t1")
        year = Year(yearNumber=2000, teams=[team], weeks=list())

        response = YearNavigator.getTeamById(year, team.id)
        self.assertTrue(team.equals(response))

    def test_getTeamById_notFound_raisesException(self):
        team = Team(ownerId="oid", name="t1")
        year = Year(yearNumber=2000, teams=[team], weeks=list())

        with self.assertRaises(DoesNotExistException) as context:
            YearNavigator.getTeamById(year, "badId")
        self.assertEqual(
            "Team with ID 'badId' does not exist in the given Year.", str(context.exception)
        )

    def test_getTDivisionById_happyPath(self):
        division = Division(name="d1")
        year = Year(yearNumber=2000, divisions=[division], teams=list(), weeks=list())

        response = YearNavigator.getDivisionById(year, division.id)
        self.assertTrue(division.equals(response))

    def test_getTDivisionById_notFound_raisesException(self):
        division = Division(name="d1")
        year = Year(yearNumber=2000, divisions=[division], teams=list(), weeks=list())

        with self.assertRaises(DoesNotExistException) as context:
            YearNavigator.getDivisionById(year, "badId")
        self.assertEqual(
            "Division with ID 'badId' does not exist in the given Year.", str(context.exception)
        )

    def test_getYearByYearNumber_happyPath(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")

        a_team1 = Team(ownerId=owner1.id, name="1")
        a_team2 = Team(ownerId=owner2.id, name="2")

        a_matchup1 = Matchup(teamAId=a_team1.id, teamBId=a_team2.id, teamAScore=1, teamBScore=2)
        a_matchup2 = Matchup(
            teamAId=a_team1.id,
            teamBId=a_team2.id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        a_matchup3 = Matchup(
            teamAId=a_team1.id,
            teamBId=a_team2.id,
            teamAScore=1,
            teamBScore=1,
            teamAHasTiebreaker=True,
            matchupType=MatchupType.PLAYOFF,
        )
        a_matchup4 = Matchup(
            teamAId=a_team1.id,
            teamBId=a_team2.id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        a_week1 = Week(weekNumber=1, matchups=[a_matchup1])
        a_week2 = Week(weekNumber=2, matchups=[a_matchup2])
        a_week3 = Week(weekNumber=3, matchups=[a_matchup3])
        a_week4 = Week(weekNumber=4, matchups=[a_matchup4])

        a_year = Year(
            yearNumber=2000, teams=[a_team1, a_team2], weeks=[a_week1, a_week2, a_week3, a_week4]
        )

        response = YearNavigator.getAllTeamIds(a_year)

        self.assertIsInstance(response, list)
        self.assertEqual(2, len(response))
        self.assertEqual(a_team1.id, response[0])
        self.assertEqual(a_team2.id, response[1])

    def test_getNumberOfGamesPlayed_happyPath(self):
        _, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2])

        yearFilters = YearFilters(weekNumberStart=1, weekNumberEnd=2)
        response = YearNavigator.getNumberOfGamesPlayed(year, yearFilters)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(2, response[teams[0].id])
        self.assertEqual(2, response[teams[1].id])

    def test_getNumberOfGamesPlayed_countLeagueMedianGamesAsTwoGames_countsLeagueMedianGamesAsTwoGames(
        self,
    ):
        _, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])

        yearSettings = YearSettings(leagueMedianGames=True)
        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2], yearSettings=yearSettings)

        yearFilters = YearFilters(weekNumberStart=1, weekNumberEnd=2)
        response = YearNavigator.getNumberOfGamesPlayed(
            year, yearFilters, countLeagueMedianGamesAsTwoGames=True
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(4, response[teams[0].id])
        self.assertEqual(4, response[teams[1].id])

    def test_getNumberOfGamesPlayed_countMultiWeekMatchupsAsOneGameIsTrue_countsMultiWeekMatchupsAsOneGame(
        self,
    ):
        _, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            multiWeekMatchupId="1",
        )
        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            multiWeekMatchupId="1",
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2])

        yearFilters = YearFilters(weekNumberStart=1, weekNumberEnd=2)
        response = YearNavigator.getNumberOfGamesPlayed(
            year, yearFilters, countMultiWeekMatchupsAsOneGame=True
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(1, response[teams[0].id])
        self.assertEqual(1, response[teams[1].id])

    def test_getNumberOfGamesPlayed_countMultiWeekMatchupsAsOneGameIsFalse_countsMultiWeekMatchupsAsMultipleGames(
        self,
    ):
        _, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            multiWeekMatchupId="1",
        )
        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            multiWeekMatchupId="1",
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2])

        yearFilters = YearFilters(weekNumberStart=1, weekNumberEnd=2)
        response = YearNavigator.getNumberOfGamesPlayed(
            year, yearFilters, countMultiWeekMatchupsAsOneGame=False
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(2, response[teams[0].id])
        self.assertEqual(2, response[teams[1].id])

    def test_getNumberOfGamesPlayed_onlyPostSeasonIsTrue(self):
        _, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        yearFilters = YearFilters(weekNumberStart=1, weekNumberEnd=3, onlyPostSeason=True)
        response = YearNavigator.getNumberOfGamesPlayed(year, yearFilters)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(2, response[teams[0].id])
        self.assertEqual(2, response[teams[1].id])

    def test_getNumberOfGamesPlayed_onlyRegularSeasonIsTrue(self):
        _, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        yearFilters = YearFilters(weekNumberStart=1, weekNumberEnd=3, onlyRegularSeason=True)
        response = YearNavigator.getNumberOfGamesPlayed(year, yearFilters)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(1, response[teams[0].id])
        self.assertEqual(1, response[teams[1].id])

    def test_getNumberOfGamesPlayed_weekNumberStartGiven(self):
        _, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        yearFilters = YearFilters(weekNumberStart=2, weekNumberEnd=3)
        response = YearNavigator.getNumberOfGamesPlayed(year, yearFilters)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(2, response[teams[0].id])
        self.assertEqual(2, response[teams[1].id])

    def test_getNumberOfGamesPlayed_weekNumberEndGiven(self):
        _, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        yearFilters = YearFilters(weekNumberStart=1, weekNumberEnd=2)
        response = YearNavigator.getNumberOfGamesPlayed(year, yearFilters)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(2, response[teams[0].id])
        self.assertEqual(2, response[teams[1].id])

    def test_getNumberOfGamesPlayed_weekNumberStartGivenAndWeekNumberEndGiven(self):
        _, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup4 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])
        week4 = Week(weekNumber=4, matchups=[matchup4])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3, week4])

        yearFilters = YearFilters(weekNumberStart=2, weekNumberEnd=3)
        response = YearNavigator.getNumberOfGamesPlayed(year, yearFilters)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(2, response[teams[0].id])
        self.assertEqual(2, response[teams[1].id])

    def test_getAllScoresInYear_happyPath(self):
        _, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.IGNORE,
        )
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=5, teamBScore=6)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = YearNavigator.getAllScoresInYear(year)

        self.assertIsInstance(response, list)
        self.assertEqual(4, len(response))
        self.assertEqual([1, 2, 5, 6], sorted(response))

    def test_getAllScoresInYear_simplifyMultiWeekMatchupsIsTrue(self):
        _, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            multiWeekMatchupId="1",
        )
        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=3,
            teamBScore=4,
            multiWeekMatchupId="1",
        )
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=5, teamBScore=6)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = YearNavigator.getAllScoresInYear(year, simplifyMultiWeekMatchups=True)

        self.assertIsInstance(response, list)
        self.assertEqual(4, len(response))
        self.assertEqual([4, 5, 6, 6], sorted(response))

    def test_getAllMultiWeekMatchups_happyPath(self):
        _, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            multiWeekMatchupId="1",
        )
        matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=3,
            teamBScore=4,
            multiWeekMatchupId="1",
        )
        matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=5,
            teamBScore=6,
            multiWeekMatchupId="1",
        )

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = YearNavigator.getAllMultiWeekMatchups(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(1, len(response.keys()))
        self.assertIsInstance(response["1"], list)
        self.assertEqual(3, len(response["1"]))
        self.assertEqual(matchup1.id, response["1"][0].id)
        self.assertEqual(matchup2.id, response["1"][1].id)
        self.assertEqual(matchup3.id, response["1"][2].id)

    def test_getAllMultiWeekMatchups_noMultiWeekMatchupsFound_returnsEmptyDict(self):
        _, teams = getNDefaultOwnersAndTeams(2)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=5, teamBScore=6)

        week1 = Week(weekNumber=1, matchups=[matchup1])
        week2 = Week(weekNumber=2, matchups=[matchup2])
        week3 = Week(weekNumber=3, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2, week3])

        response = YearNavigator.getAllMultiWeekMatchups(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(0, len(response.keys()))

    def test_getAllMultiWeekMatchups_includeMultiWeekMatchupsIsFalse_raisesException(self):
        with self.assertRaises(ValueError) as context:
            YearNavigator.getAllMultiWeekMatchups(
                None,
                YearFilters(
                    weekNumberStart=1,
                    weekNumberEnd=3,
                    onlyRegularSeason=True,
                    includeMultiWeekMatchups=False,
                ),
            )
        self.assertEqual(
            "Multi-Week matchups must be included in this calculation.", str(context.exception)
        )

    def test_getAllMatchupsInYear_noFilterGiven_happyPath(self):
        _, teams = getNDefaultOwnersAndTeams(2)

        a_matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        a_matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        a_matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=1,
            teamAHasTiebreaker=True,
            matchupType=MatchupType.PLAYOFF,
        )
        a_matchup4 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        a_week1 = Week(weekNumber=1, matchups=[a_matchup1])
        a_week2 = Week(weekNumber=2, matchups=[a_matchup2])
        a_week3 = Week(weekNumber=3, matchups=[a_matchup3])
        a_week4 = Week(weekNumber=4, matchups=[a_matchup4])

        a_year = Year(yearNumber=2000, teams=teams, weeks=[a_week1, a_week2, a_week3, a_week4])

        response = YearNavigator.getAllMatchupsInYear(a_year)

        self.assertIsInstance(response, list)
        self.assertEqual(4, len(response))
        self.assertEqual(a_matchup1.id, response[0].id)
        self.assertEqual(a_matchup2.id, response[1].id)
        self.assertEqual(a_matchup3.id, response[2].id)
        self.assertEqual(a_matchup4.id, response[3].id)

    def test_getAllMatchupsInYear_filterGiven_happyPath(self):
        _, teams = getNDefaultOwnersAndTeams(2)

        a_matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        a_matchup2 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        a_matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=1,
            teamAHasTiebreaker=True,
            matchupType=MatchupType.PLAYOFF,
        )
        a_matchup4 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        a_week1 = Week(weekNumber=1, matchups=[a_matchup1])
        a_week2 = Week(weekNumber=2, matchups=[a_matchup2])
        a_week3 = Week(weekNumber=3, matchups=[a_matchup3])
        a_week4 = Week(weekNumber=4, matchups=[a_matchup4])

        a_year = Year(yearNumber=2000, teams=teams, weeks=[a_week1, a_week2, a_week3, a_week4])

        response = YearNavigator.getAllMatchupsInYear(
            a_year, YearFilters(weekNumberStart=2, weekNumberEnd=3, onlyPostSeason=True)
        )

        self.assertIsInstance(response, list)
        self.assertEqual(1, len(response))
        self.assertEqual(a_matchup3.id, response[0].id)

    def test_getAllMatchupsInYear_filterGiven_includeMultiWeekMatchupsIsTrue_happyPath(self):
        _, teams = getNDefaultOwnersAndTeams(2)

        a_matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            multiWeekMatchupId="1",
        )
        a_matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            multiWeekMatchupId="1",
        )
        a_matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)

        a_week1 = Week(weekNumber=1, matchups=[a_matchup1])
        a_week2 = Week(weekNumber=2, matchups=[a_matchup2])
        a_week3 = Week(weekNumber=3, matchups=[a_matchup3])

        a_year = Year(yearNumber=2000, teams=teams, weeks=[a_week1, a_week2, a_week3])

        response = YearNavigator.getAllMatchupsInYear(
            a_year,
            YearFilters(
                weekNumberStart=1,
                weekNumberEnd=3,
                onlyRegularSeason=True,
                includeMultiWeekMatchups=True,
            ),
        )

        self.assertIsInstance(response, list)
        self.assertEqual(3, len(response))
        self.assertEqual(a_matchup1.id, response[0].id)
        self.assertEqual(a_matchup2.id, response[1].id)
        self.assertEqual(a_matchup3.id, response[2].id)

    def test_getAllMatchupsInYear_filterGiven_includeMultiWeekMatchupsIsFalse_happyPath(self):
        _, teams = getNDefaultOwnersAndTeams(2)

        a_matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            multiWeekMatchupId="1",
        )
        a_matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            multiWeekMatchupId="1",
        )
        a_matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)

        a_week1 = Week(weekNumber=1, matchups=[a_matchup1])
        a_week2 = Week(weekNumber=2, matchups=[a_matchup2])
        a_week3 = Week(weekNumber=3, matchups=[a_matchup3])

        a_year = Year(yearNumber=2000, teams=teams, weeks=[a_week1, a_week2, a_week3])

        response = YearNavigator.getAllMatchupsInYear(
            a_year,
            YearFilters(
                weekNumberStart=1,
                weekNumberEnd=3,
                onlyRegularSeason=True,
                includeMultiWeekMatchups=False,
            ),
        )

        self.assertIsInstance(response, list)
        self.assertEqual(1, len(response))
        self.assertEqual(a_matchup3.id, response[0].id)

    def test_getAllSimplifiedMatchupsInYear_noFilterGiven_happyPath(self):
        _, teams = getNDefaultOwnersAndTeams(2)

        a_matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            multiWeekMatchupId="1",
        )
        a_matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            multiWeekMatchupId="1",
        )
        a_matchup3 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)

        a_week1 = Week(weekNumber=1, matchups=[a_matchup1])
        a_week2 = Week(weekNumber=2, matchups=[a_matchup2])
        a_week3 = Week(weekNumber=3, matchups=[a_matchup3])

        a_year = Year(yearNumber=2000, teams=teams, weeks=[a_week1, a_week2, a_week3])

        response = YearNavigator.getAllSimplifiedMatchupsInYear(a_year)

        self.assertIsInstance(response, list)
        self.assertEqual(2, len(response))
        self.assertEqual(a_matchup3.id, response[0].id)
        self.assertEqual(teams[0].id, response[1].teamAId)
        self.assertEqual(teams[1].id, response[1].teamBId)
        self.assertEqual(2, response[1].teamAScore)
        self.assertEqual(4, response[1].teamBScore)

    def test_getAllSimplifiedMatchupsInYear_filterGiven_happyPath(self):
        _, teams = getNDefaultOwnersAndTeams(2)

        a_matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        a_matchup2 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            multiWeekMatchupId="1",
        )
        a_matchup3 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            multiWeekMatchupId="1",
        )
        a_matchup4 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )

        a_week1 = Week(weekNumber=1, matchups=[a_matchup1])
        a_week2 = Week(weekNumber=2, matchups=[a_matchup2])
        a_week3 = Week(weekNumber=3, matchups=[a_matchup3])

        a_year = Year(yearNumber=2000, teams=teams, weeks=[a_week1, a_week2, a_week3])

        response = YearNavigator.getAllSimplifiedMatchupsInYear(
            a_year,
            YearFilters(
                weekNumberStart=2,
                weekNumberEnd=3,
                onlyRegularSeason=True,
                includeMultiWeekMatchups=True,
            ),
        )

        self.assertIsInstance(response, list)
        self.assertEqual(1, len(response))
        self.assertEqual(teams[0].id, response[0].teamAId)
        self.assertEqual(teams[1].id, response[0].teamBId)
        self.assertEqual(2, response[0].teamAScore)
        self.assertEqual(4, response[0].teamBScore)

    def test_getAllSimplifiedMatchupsInYear_includeMultiWeekMatchupsIsFalse_raisesException(self):
        with self.assertRaises(ValueError) as context:
            YearNavigator.getAllSimplifiedMatchupsInYear(
                None,
                YearFilters(
                    weekNumberStart=1,
                    weekNumberEnd=3,
                    onlyRegularSeason=True,
                    includeMultiWeekMatchups=False,
                ),
            )
        self.assertEqual(
            "Multi-Week matchups must be included in this calculation.", str(context.exception)
        )
