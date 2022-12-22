import unittest

from leeger.enum.MatchupType import MatchupType
from leeger.exception.DoesNotExistException import DoesNotExistException
from leeger.model.filter.AllTimeFilters import AllTimeFilters
from leeger.model.league import YearSettings
from leeger.model.league.League import League
from leeger.model.league.Matchup import Matchup
from leeger.model.league.Owner import Owner
from leeger.model.league.Team import Team
from leeger.model.league.Week import Week
from leeger.model.league.Year import Year
from leeger.util.navigator.LeagueNavigator import LeagueNavigator
from test.helper.prototypes import getNDefaultOwnersAndTeams, getTeamsFromOwners


class TestLeagueNavigator(unittest.TestCase):
    def test_getYearByYearNumber_happyPath(self):
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

        league = League(name="TEST", owners=[owner1, owner2], years=[a_year, b_year])

        response = LeagueNavigator.getYearByYearNumber(league, 2001)

        self.assertIsInstance(response, Year)
        self.assertEqual(2001, response.yearNumber)

    def test_getYearByYearNumber_yearDoesntExistInLeague_raisesException(self):
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

        league = League(name="TEST", owners=[owner1, owner2], years=[a_year])

        with self.assertRaises(DoesNotExistException) as context:
            LeagueNavigator.getYearByYearNumber(league, 2001)
        self.assertEqual("Year 2001 does not exist in the given League.", str(context.exception))

    def test_getAllOwnerIds_happyPath(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")

        a_team1 = Team(ownerId=owner1.id, name="1")
        a_team2 = Team(ownerId=owner2.id, name="2")

        a_matchup1 = Matchup(teamAId=a_team1.id, teamBId=a_team2.id, teamAScore=1, teamBScore=2)

        a_week1 = Week(weekNumber=1, matchups=[a_matchup1])

        a_year = Year(yearNumber=2000, teams=[a_team1, a_team2], weeks=[a_week1])

        league = League(name="TEST", owners=[owner1, owner2], years=[a_year])

        response = LeagueNavigator.getAllOwnerIds(league)

        self.assertIsInstance(response, list)
        self.assertEqual(2, len(response))
        self.assertEqual(owner1.id, response[0])
        self.assertEqual(owner2.id, response[1])

    def test_getTeamById_happyPath(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")

        a_team1 = Team(ownerId=owner1.id, name="1")
        a_team2 = Team(ownerId=owner2.id, name="2")

        a_matchup1 = Matchup(teamAId=a_team1.id, teamBId=a_team2.id, teamAScore=1, teamBScore=2)

        a_week1 = Week(weekNumber=1, matchups=[a_matchup1])

        a_year = Year(yearNumber=2000, teams=[a_team1, a_team2], weeks=[a_week1])

        league = League(name="TEST", owners=[owner1, owner2], years=[a_year])

        response1 = LeagueNavigator.getTeamById(league, a_team1.id)
        response2 = LeagueNavigator.getTeamById(league, a_team2.id)

        self.assertIsInstance(response1, Team)
        self.assertIsInstance(response2, Team)
        self.assertEqual(a_team1, response1)
        self.assertEqual(a_team2, response2)

    def test_getTeamById_teamIdNotFound_raisesException(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")

        a_team1 = Team(ownerId=owner1.id, name="1")
        a_team2 = Team(ownerId=owner2.id, name="2")

        a_matchup1 = Matchup(teamAId=a_team1.id, teamBId=a_team2.id, teamAScore=1, teamBScore=2)

        a_week1 = Week(weekNumber=1, matchups=[a_matchup1])

        a_year = Year(yearNumber=2000, teams=[a_team1, a_team2], weeks=[a_week1])

        league = League(name="TEST", owners=[owner1, owner2], years=[a_year])

        with self.assertRaises(DoesNotExistException) as context:
            LeagueNavigator.getTeamById(league, "imABadID")
        self.assertEqual("Team with ID imABadID does not exist in the given League.", str(context.exception))

    def test_getOwnerById_happyPath(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")

        a_team1 = Team(ownerId=owner1.id, name="1")
        a_team2 = Team(ownerId=owner2.id, name="2")

        a_matchup1 = Matchup(teamAId=a_team1.id, teamBId=a_team2.id, teamAScore=1, teamBScore=2)

        a_week1 = Week(weekNumber=1, matchups=[a_matchup1])

        a_year = Year(yearNumber=2000, teams=[a_team1, a_team2], weeks=[a_week1])

        league = League(name="TEST", owners=[owner1, owner2], years=[a_year])

        response1 = LeagueNavigator.getOwnerById(league, owner1.id)
        response2 = LeagueNavigator.getOwnerById(league, owner2.id)

        self.assertIsInstance(response1, Owner)
        self.assertIsInstance(response2, Owner)
        self.assertEqual(owner1, response1)
        self.assertEqual(owner2, response2)

    def test_getOwnerById_ownerIdNotFound_raisesException(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")

        a_team1 = Team(ownerId=owner1.id, name="1")
        a_team2 = Team(ownerId=owner2.id, name="2")

        a_matchup1 = Matchup(teamAId=a_team1.id, teamBId=a_team2.id, teamAScore=1, teamBScore=2)

        a_week1 = Week(weekNumber=1, matchups=[a_matchup1])

        a_year = Year(yearNumber=2000, teams=[a_team1, a_team2], weeks=[a_week1])

        league = League(name="TEST", owners=[owner1, owner2], years=[a_year])

        with self.assertRaises(DoesNotExistException) as context:
            LeagueNavigator.getOwnerById(league, "imABadID")
        self.assertEqual("Owner with ID imABadID does not exist in the given League.", str(context.exception))

    def test_getNumberOfGamesPlayed_happyPath(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)
        teamsD = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=2, teamBScore=1,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=2, teamBScore=1,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=1)
        matchup2_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        matchup1_d = Matchup(teamAId=teamsD[0].id, teamBId=teamsD[1].id, teamAScore=1, teamBScore=2)
        matchup2_d = Matchup(teamAId=teamsD[0].id, teamBId=teamsD[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_d = Matchup(teamAId=teamsD[0].id, teamBId=teamsD[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_d = Week(weekNumber=1, matchups=[matchup1_d])
        week2_d = Week(weekNumber=2, matchups=[matchup2_d])
        week3_d = Week(weekNumber=3, matchups=[matchup3_d])
        yearD = Year(yearNumber=2003, teams=teamsD, weeks=[week1_d, week2_d, week3_d])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC, yearD])

        allTimeFilters = AllTimeFilters(yearNumberStart=2000, weekNumberStart=1, yearNumberEnd=2003, weekNumberEnd=3,
                                        onlyChampionship=False, onlyPostSeason=False, onlyRegularSeason=False)
        response = LeagueNavigator.getNumberOfGamesPlayed(league, allTimeFilters)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(12, response[owners[0].id])
        self.assertEqual(12, response[owners[1].id])

    def test_getNumberOfGamesPlayed_countLeagueMedianGamesAsTwoGames_countsLeagueMedianGamesAsTwoGames(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)
        teamsD = getTeamsFromOwners(owners)
        yearSettings = YearSettings(leagueMedianGames=True)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup3_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a], yearSettings=yearSettings)

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=2, teamBScore=1)
        matchup3_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=2, teamBScore=1)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b], yearSettings=yearSettings)

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=1)
        matchup2_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        matchup3_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c], yearSettings=yearSettings)

        matchup1_d = Matchup(teamAId=teamsD[0].id, teamBId=teamsD[1].id, teamAScore=1, teamBScore=2)
        matchup2_d = Matchup(teamAId=teamsD[0].id, teamBId=teamsD[1].id, teamAScore=1, teamBScore=2)
        matchup3_d = Matchup(teamAId=teamsD[0].id, teamBId=teamsD[1].id, teamAScore=1, teamBScore=2)
        week1_d = Week(weekNumber=1, matchups=[matchup1_d])
        week2_d = Week(weekNumber=2, matchups=[matchup2_d])
        week3_d = Week(weekNumber=3, matchups=[matchup3_d])
        yearD = Year(yearNumber=2003, teams=teamsD, weeks=[week1_d, week2_d, week3_d], yearSettings=yearSettings)

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC, yearD])

        allTimeFilters = AllTimeFilters(yearNumberStart=2000, weekNumberStart=1, yearNumberEnd=2003, weekNumberEnd=3,
                                        onlyChampionship=False, onlyPostSeason=False, onlyRegularSeason=False)
        response = LeagueNavigator.getNumberOfGamesPlayed(league, allTimeFilters, countLeagueMedianGamesAsTwoGames=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(24, response[owners[0].id])
        self.assertEqual(24, response[owners[1].id])

    def test_getNumberOfGamesPlayed_countMultiWeekMatchupsAsOneGameIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)
        teamsD = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.PLAYOFF, multiWeekMatchupId="1")
        matchup3_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.PLAYOFF, multiWeekMatchupId="1")
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=2, teamBScore=1,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=2, teamBScore=1,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=1)
        matchup2_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        matchup1_d = Matchup(teamAId=teamsD[0].id, teamBId=teamsD[1].id, teamAScore=1, teamBScore=2)
        matchup2_d = Matchup(teamAId=teamsD[0].id, teamBId=teamsD[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_d = Matchup(teamAId=teamsD[0].id, teamBId=teamsD[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_d = Week(weekNumber=1, matchups=[matchup1_d])
        week2_d = Week(weekNumber=2, matchups=[matchup2_d])
        week3_d = Week(weekNumber=3, matchups=[matchup3_d])
        yearD = Year(yearNumber=2003, teams=teamsD, weeks=[week1_d, week2_d, week3_d])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC, yearD])

        allTimeFilters = AllTimeFilters(yearNumberStart=2000, weekNumberStart=1, yearNumberEnd=2003, weekNumberEnd=3,
                                        onlyChampionship=False, onlyPostSeason=False, onlyRegularSeason=False)
        response = LeagueNavigator.getNumberOfGamesPlayed(league, allTimeFilters, countMultiWeekMatchupsAsOneGame=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(11, response[owners[0].id])
        self.assertEqual(11, response[owners[1].id])

    def test_getNumberOfGamesPlayed_onlyRegularSeason(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)
        teamsD = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=2, teamBScore=1,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=2, teamBScore=1,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=1)
        matchup2_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        matchup1_d = Matchup(teamAId=teamsD[0].id, teamBId=teamsD[1].id, teamAScore=1, teamBScore=2)
        matchup2_d = Matchup(teamAId=teamsD[0].id, teamBId=teamsD[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_d = Matchup(teamAId=teamsD[0].id, teamBId=teamsD[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_d = Week(weekNumber=1, matchups=[matchup1_d])
        week2_d = Week(weekNumber=2, matchups=[matchup2_d])
        week3_d = Week(weekNumber=3, matchups=[matchup3_d])
        yearD = Year(yearNumber=2003, teams=teamsD, weeks=[week1_d, week2_d, week3_d])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC, yearD])

        allTimeFilters = AllTimeFilters(yearNumberStart=2000, weekNumberStart=1, yearNumberEnd=2003, weekNumberEnd=3,
                                        onlyChampionship=False, onlyPostSeason=False, onlyRegularSeason=True)
        response = LeagueNavigator.getNumberOfGamesPlayed(league, allTimeFilters)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(4, response[owners[0].id])
        self.assertEqual(4, response[owners[1].id])

    def test_getNumberOfGamesPlayed_onlyPostSeason(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)
        teamsD = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=2, teamBScore=1,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=2, teamBScore=1,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=1)
        matchup2_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        matchup1_d = Matchup(teamAId=teamsD[0].id, teamBId=teamsD[1].id, teamAScore=1, teamBScore=2)
        matchup2_d = Matchup(teamAId=teamsD[0].id, teamBId=teamsD[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_d = Matchup(teamAId=teamsD[0].id, teamBId=teamsD[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_d = Week(weekNumber=1, matchups=[matchup1_d])
        week2_d = Week(weekNumber=2, matchups=[matchup2_d])
        week3_d = Week(weekNumber=3, matchups=[matchup3_d])
        yearD = Year(yearNumber=2003, teams=teamsD, weeks=[week1_d, week2_d, week3_d])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC, yearD])

        allTimeFilters = AllTimeFilters(yearNumberStart=2000, weekNumberStart=1, yearNumberEnd=2003, weekNumberEnd=3,
                                        onlyChampionship=False, onlyPostSeason=True, onlyRegularSeason=False)
        response = LeagueNavigator.getNumberOfGamesPlayed(league, allTimeFilters)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(8, response[owners[0].id])
        self.assertEqual(8, response[owners[1].id])

    def test_getNumberOfGamesPlayed_onlyChampionship(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)
        teamsD = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=2, teamBScore=1,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=2, teamBScore=1,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=1)
        matchup2_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        matchup1_d = Matchup(teamAId=teamsD[0].id, teamBId=teamsD[1].id, teamAScore=1, teamBScore=2)
        matchup2_d = Matchup(teamAId=teamsD[0].id, teamBId=teamsD[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_d = Matchup(teamAId=teamsD[0].id, teamBId=teamsD[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_d = Week(weekNumber=1, matchups=[matchup1_d])
        week2_d = Week(weekNumber=2, matchups=[matchup2_d])
        week3_d = Week(weekNumber=3, matchups=[matchup3_d])
        yearD = Year(yearNumber=2003, teams=teamsD, weeks=[week1_d, week2_d, week3_d])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC, yearD])

        allTimeFilters = AllTimeFilters(yearNumberStart=2000, weekNumberStart=1, yearNumberEnd=2003, weekNumberEnd=3,
                                        onlyChampionship=True, onlyPostSeason=False, onlyRegularSeason=False)
        response = LeagueNavigator.getNumberOfGamesPlayed(league, allTimeFilters)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(4, response[owners[0].id])
        self.assertEqual(4, response[owners[1].id])

    def test_getNumberOfGamesPlayed_yearNumberStartWeekNumberStart(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)
        teamsD = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=2, teamBScore=1,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=2, teamBScore=1,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=1)
        matchup2_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        matchup1_d = Matchup(teamAId=teamsD[0].id, teamBId=teamsD[1].id, teamAScore=1, teamBScore=2)
        matchup2_d = Matchup(teamAId=teamsD[0].id, teamBId=teamsD[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_d = Matchup(teamAId=teamsD[0].id, teamBId=teamsD[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_d = Week(weekNumber=1, matchups=[matchup1_d])
        week2_d = Week(weekNumber=2, matchups=[matchup2_d])
        week3_d = Week(weekNumber=3, matchups=[matchup3_d])
        yearD = Year(yearNumber=2003, teams=teamsD, weeks=[week1_d, week2_d, week3_d])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC, yearD])

        allTimeFilters = AllTimeFilters(yearNumberStart=2001, weekNumberStart=2, yearNumberEnd=2003, weekNumberEnd=3,
                                        onlyChampionship=False, onlyPostSeason=False, onlyRegularSeason=False)
        response = LeagueNavigator.getNumberOfGamesPlayed(league, allTimeFilters)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(8, response[owners[0].id])
        self.assertEqual(8, response[owners[1].id])

    def test_getNumberOfGamesPlayed_yearNumberEndWeekNumberEnd(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)
        teamsD = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=2, teamBScore=1,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=2, teamBScore=1,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=1)
        matchup2_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        matchup1_d = Matchup(teamAId=teamsD[0].id, teamBId=teamsD[1].id, teamAScore=1, teamBScore=2)
        matchup2_d = Matchup(teamAId=teamsD[0].id, teamBId=teamsD[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_d = Matchup(teamAId=teamsD[0].id, teamBId=teamsD[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_d = Week(weekNumber=1, matchups=[matchup1_d])
        week2_d = Week(weekNumber=2, matchups=[matchup2_d])
        week3_d = Week(weekNumber=3, matchups=[matchup3_d])
        yearD = Year(yearNumber=2003, teams=teamsD, weeks=[week1_d, week2_d, week3_d])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC, yearD])

        allTimeFilters = AllTimeFilters(yearNumberStart=2000, weekNumberStart=1, yearNumberEnd=2002, weekNumberEnd=2,
                                        onlyChampionship=False, onlyPostSeason=False, onlyRegularSeason=False)
        response = LeagueNavigator.getNumberOfGamesPlayed(league, allTimeFilters)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(8, response[owners[0].id])
        self.assertEqual(8, response[owners[1].id])

    def test_getNumberOfGamesPlayed_yearNumberStartWeekNumberStartYearNumberEndWeekNumberEnd(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)
        teamsD = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2)
        matchup2_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=1, teamBScore=2)
        matchup2_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=2, teamBScore=1,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=2, teamBScore=1,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=1)
        matchup2_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        matchup1_d = Matchup(teamAId=teamsD[0].id, teamBId=teamsD[1].id, teamAScore=1, teamBScore=2)
        matchup2_d = Matchup(teamAId=teamsD[0].id, teamBId=teamsD[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_d = Matchup(teamAId=teamsD[0].id, teamBId=teamsD[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_d = Week(weekNumber=1, matchups=[matchup1_d])
        week2_d = Week(weekNumber=2, matchups=[matchup2_d])
        week3_d = Week(weekNumber=3, matchups=[matchup3_d])
        yearD = Year(yearNumber=2003, teams=teamsD, weeks=[week1_d, week2_d, week3_d])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC, yearD])

        allTimeFilters = AllTimeFilters(yearNumberStart=2001, weekNumberStart=2, yearNumberEnd=2002, weekNumberEnd=2,
                                        onlyChampionship=False, onlyPostSeason=False, onlyRegularSeason=False)
        response = LeagueNavigator.getNumberOfGamesPlayed(league, allTimeFilters)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(4, response[owners[0].id])
        self.assertEqual(4, response[owners[1].id])

    def test_getAllScoresInLeague_happyPath(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)
        teamsD = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2,
                             matchupType=MatchupType.IGNORE)
        matchup2_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=3, teamBScore=4,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=5, teamBScore=6,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        matchup1_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=7, teamBScore=8,
                             matchupType=MatchupType.IGNORE)
        matchup2_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=9, teamBScore=10,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_b = Matchup(teamAId=teamsB[0].id, teamBId=teamsB[1].id, teamAScore=11, teamBScore=12,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_b = Week(weekNumber=1, matchups=[matchup1_b])
        week2_b = Week(weekNumber=2, matchups=[matchup2_b])
        week3_b = Week(weekNumber=3, matchups=[matchup3_b])
        yearB = Year(yearNumber=2001, teams=teamsB, weeks=[week1_b, week2_b, week3_b])

        matchup1_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=13, teamBScore=14,
                             matchupType=MatchupType.IGNORE)
        matchup2_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=15, teamBScore=16,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_c = Matchup(teamAId=teamsC[0].id, teamBId=teamsC[1].id, teamAScore=17, teamBScore=18,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_c = Week(weekNumber=1, matchups=[matchup1_c])
        week2_c = Week(weekNumber=2, matchups=[matchup2_c])
        week3_c = Week(weekNumber=3, matchups=[matchup3_c])
        yearC = Year(yearNumber=2002, teams=teamsC, weeks=[week1_c, week2_c, week3_c])

        matchup1_d = Matchup(teamAId=teamsD[0].id, teamBId=teamsD[1].id, teamAScore=19, teamBScore=20,
                             matchupType=MatchupType.IGNORE)
        matchup2_d = Matchup(teamAId=teamsD[0].id, teamBId=teamsD[1].id, teamAScore=21, teamBScore=22,
                             matchupType=MatchupType.PLAYOFF)
        matchup3_d = Matchup(teamAId=teamsD[0].id, teamBId=teamsD[1].id, teamAScore=23, teamBScore=24,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_d = Week(weekNumber=1, matchups=[matchup1_d])
        week2_d = Week(weekNumber=2, matchups=[matchup2_d])
        week3_d = Week(weekNumber=3, matchups=[matchup3_d])
        yearD = Year(yearNumber=2003, teams=teamsD, weeks=[week1_d, week2_d, week3_d])

        league = League(name="TEST", owners=owners, years=[yearA, yearB, yearC, yearD])

        response = LeagueNavigator.getAllScoresInLeague(league)

        self.assertIsInstance(response, list)
        self.assertEqual(16, len(response))
        self.assertEqual([3, 4, 5, 6, 9, 10, 11, 12, 15, 16, 17, 18, 21, 22, 23, 24], sorted(response))

    def test_getAllScoresInLeague_simplifyMultiWeekMatchupsIsTrue(self):
        owners, teamsA = getNDefaultOwnersAndTeams(2)
        teamsB = getTeamsFromOwners(owners)
        teamsC = getTeamsFromOwners(owners)
        teamsD = getTeamsFromOwners(owners)

        matchup1_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=1, teamBScore=2,
                             multiWeekMatchupId="1")
        matchup2_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=3, teamBScore=4,
                             multiWeekMatchupId="1")
        matchup3_a = Matchup(teamAId=teamsA[0].id, teamBId=teamsA[1].id, teamAScore=5, teamBScore=6,
                             matchupType=MatchupType.CHAMPIONSHIP)
        week1_a = Week(weekNumber=1, matchups=[matchup1_a])
        week2_a = Week(weekNumber=2, matchups=[matchup2_a])
        week3_a = Week(weekNumber=3, matchups=[matchup3_a])
        yearA = Year(yearNumber=2000, teams=teamsA, weeks=[week1_a, week2_a, week3_a])

        league = League(name="TEST", owners=owners, years=[yearA])

        response = LeagueNavigator.getAllScoresInLeague(league, simplifyMultiWeekMatchups=True)

        self.assertIsInstance(response, list)
        self.assertEqual(4, len(response))
        self.assertEqual([4, 5, 6, 6], sorted(response))
