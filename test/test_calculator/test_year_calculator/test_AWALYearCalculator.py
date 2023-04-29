import unittest

from leeger.calculator.year_calculator.AWALYearCalculator import AWALYearCalculator
from leeger.enum.MatchupType import MatchupType
from leeger.model.league import YearSettings
from leeger.model.league.Matchup import Matchup
from leeger.model.league.Week import Week
from leeger.model.league.Year import Year
from leeger.util.Deci import Deci
from test.helper.prototypes import getNDefaultOwnersAndTeams


class TestAWALYearCalculator(unittest.TestCase):
    def test_getAWAL_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
            weeks=[week1, week2, week3],
        )

        response = AWALYearCalculator.getAWAL(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0.6"), response[teams[1].id])
        self.assertEqual(Deci("1.2"), response[teams[2].id])
        self.assertEqual(Deci("2.1"), response[teams[3].id])
        self.assertEqual(Deci("2.1"), response[teams[4].id])
        self.assertEqual(Deci("3"), response[teams[5].id])

    def test_getAWAL_leagueMedianGamesIsOn_addsLeagueMedianWinsToAWAL(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        yearSettings = YearSettings(leagueMedianGames=True)
        year = Year(
            yearNumber=2000, teams=teams, weeks=[week1, week2, week3], yearSettings=yearSettings
        )

        response = AWALYearCalculator.getAWAL(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))

    def test_getAWAL_noneIfNoGamesPlayed(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        week1 = Week(weekNumber=1, matchups=[matchup1])

        matchup4 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup5 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup6 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)
        week2 = Week(weekNumber=2, matchups=[matchup4, matchup5, matchup6])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2])

        response = AWALYearCalculator.getAWAL(year, weekNumberEnd=1)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("1"), response[teams[1].id])
        self.assertIsNone(response[teams[2].id])
        self.assertIsNone(response[teams[3].id])
        self.assertIsNone(response[teams[4].id])
        self.assertIsNone(response[teams[5].id])

    def test_getAWAL_onlyPostSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.PLAYOFF,
        )

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
            weeks=[week1, week2, week3],
        )

        response = AWALYearCalculator.getAWAL(year, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0.4"), response[teams[1].id])
        self.assertEqual(Deci("0.8"), response[teams[2].id])
        self.assertEqual(Deci("1.4"), response[teams[3].id])
        self.assertEqual(Deci("1.4"), response[teams[4].id])
        self.assertEqual(Deci("2"), response[teams[5].id])

    def test_getAWAL_onlyRegularSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.PLAYOFF,
        )

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
            weeks=[week1, week2, week3],
        )

        response = AWALYearCalculator.getAWAL(year, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0.2"), response[teams[1].id])
        self.assertEqual(Deci("0.4"), response[teams[2].id])
        self.assertEqual(Deci("0.7"), response[teams[3].id])
        self.assertEqual(Deci("0.7"), response[teams[4].id])
        self.assertEqual(Deci("1"), response[teams[5].id])

    def test_getAWAL_onlyChampionshipIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.PLAYOFF,
        )

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
            weeks=[week1, week2, week3],
        )

        response = AWALYearCalculator.getAWAL(year, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertIsNone(response[teams[0].id])
        self.assertIsNone(response[teams[1].id])
        self.assertIsNone(response[teams[2].id])
        self.assertIsNone(response[teams[3].id])
        self.assertEqual(Deci("0"), response[teams[4].id])
        self.assertEqual(Deci("1"), response[teams[5].id])

    def test_getAWAL_weekNumberStartGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.PLAYOFF,
        )

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
            weeks=[week1, week2, week3],
        )

        response = AWALYearCalculator.getAWAL(year, weekNumberStart=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0.4"), response[teams[1].id])
        self.assertEqual(Deci("0.8"), response[teams[2].id])
        self.assertEqual(Deci("1.4"), response[teams[3].id])
        self.assertEqual(Deci("1.4"), response[teams[4].id])
        self.assertEqual(Deci("2"), response[teams[5].id])

    def test_getAWAL_weekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.PLAYOFF,
        )

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
            weeks=[week1, week2, week3],
        )

        response = AWALYearCalculator.getAWAL(year, weekNumberEnd=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0.4"), response[teams[1].id])
        self.assertEqual(Deci("0.8"), response[teams[2].id])
        self.assertEqual(Deci("1.4"), response[teams[3].id])
        self.assertEqual(Deci("1.4"), response[teams[4].id])
        self.assertEqual(Deci("2"), response[teams[5].id])

    def test_getAWAL_weekNumberStartGivenAndWeekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.PLAYOFF,
        )

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
            weeks=[week1, week2, week3],
        )

        response = AWALYearCalculator.getAWAL(year, weekNumberStart=2, weekNumberEnd=3)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0.4"), response[teams[1].id])
        self.assertEqual(Deci("0.8"), response[teams[2].id])
        self.assertEqual(Deci("1.4"), response[teams[3].id])
        self.assertEqual(Deci("1.4"), response[teams[4].id])
        self.assertEqual(Deci("2"), response[teams[5].id])

    def test_getAWAL_matchupEndsInTie(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=3)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
            weeks=[week1],
        )

        response = AWALYearCalculator.getAWAL(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0.2"), response[teams[1].id])
        self.assertEqual(Deci("0.5"), response[teams[2].id])
        self.assertEqual(Deci("0.5"), response[teams[3].id])
        self.assertEqual(Deci("0.8"), response[teams[4].id])
        self.assertEqual(Deci("1"), response[teams[5].id])

    def test_getAWAL_multipleMatchupsEndInTie(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=3)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
            weeks=[week1],
        )

        response = AWALYearCalculator.getAWAL(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.1"), response[teams[0].id])
        self.assertEqual(Deci("0.1"), response[teams[1].id])
        self.assertEqual(Deci("0.5"), response[teams[2].id])
        self.assertEqual(Deci("0.5"), response[teams[3].id])
        self.assertEqual(Deci("0.8"), response[teams[4].id])
        self.assertEqual(Deci("1"), response[teams[5].id])

    def test_getAWAL_allMatchupsEndInTie(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=2, teamBScore=2)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=3, teamBScore=3)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
            weeks=[week1],
        )

        response = AWALYearCalculator.getAWAL(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.1"), response[teams[0].id])
        self.assertEqual(Deci("0.1"), response[teams[1].id])
        self.assertEqual(Deci("0.5"), response[teams[2].id])
        self.assertEqual(Deci("0.5"), response[teams[3].id])
        self.assertEqual(Deci("0.9"), response[teams[4].id])
        self.assertEqual(Deci("0.9"), response[teams[5].id])

    def test_getAWAL_allMatchupsEndInTieAndHaveSameScore(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=1, teamBScore=1)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=1, teamBScore=1)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
            weeks=[week1],
        )

        response = AWALYearCalculator.getAWAL(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.5"), response[teams[0].id])
        self.assertEqual(Deci("0.5"), response[teams[1].id])
        self.assertEqual(Deci("0.5"), response[teams[2].id])
        self.assertEqual(Deci("0.5"), response[teams[3].id])
        self.assertEqual(Deci("0.5"), response[teams[4].id])
        self.assertEqual(Deci("0.5"), response[teams[5].id])

    def test_getAWAL_sixteenTeams(self):
        owners, teams = getNDefaultOwnersAndTeams(16)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=5, teamBScore=6)
        matchup4 = Matchup(teamAId=teams[6].id, teamBId=teams[7].id, teamAScore=7, teamBScore=8)
        matchup5 = Matchup(teamAId=teams[8].id, teamBId=teams[9].id, teamAScore=9, teamBScore=10)
        matchup6 = Matchup(teamAId=teams[10].id, teamBId=teams[11].id, teamAScore=11, teamBScore=12)
        matchup7 = Matchup(teamAId=teams[12].id, teamBId=teams[13].id, teamAScore=13, teamBScore=14)
        matchup8 = Matchup(teamAId=teams[14].id, teamBId=teams[15].id, teamAScore=15, teamBScore=16)

        week1 = Week(
            weekNumber=1,
            matchups=[
                matchup1,
                matchup2,
                matchup3,
                matchup4,
                matchup5,
                matchup6,
                matchup7,
                matchup8,
            ],
        )

        year = Year(
            yearNumber=2000,
            teams=[
                teams[0],
                teams[1],
                teams[2],
                teams[3],
                teams[4],
                teams[5],
                teams[6],
                teams[7],
                teams[8],
                teams[9],
                teams[10],
                teams[11],
                teams[12],
                teams[13],
                teams[14],
                teams[15],
            ],
            weeks=[week1],
        )

        response = AWALYearCalculator.getAWAL(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(16, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0.06666666666666666666666666667"), response[teams[1].id])
        self.assertEqual(Deci("0.1333333333333333333333333333"), response[teams[2].id])
        self.assertEqual(Deci("0.2"), response[teams[3].id])
        self.assertEqual(Deci("0.2666666666666666666666666667"), response[teams[4].id])
        self.assertEqual(Deci("0.3333333333333333333333333334"), response[teams[5].id])
        self.assertEqual(Deci("0.4"), response[teams[6].id])
        self.assertEqual(Deci("0.4666666666666666666666666667"), response[teams[7].id])
        self.assertEqual(Deci("0.5333333333333333333333333334"), response[teams[8].id])
        self.assertEqual(Deci("0.6"), response[teams[9].id])
        self.assertEqual(Deci("0.6666666666666666666666666667"), response[teams[10].id])
        self.assertEqual(Deci("0.7333333333333333333333333334"), response[teams[11].id])
        self.assertEqual(Deci("0.8"), response[teams[12].id])
        self.assertEqual(Deci("0.8666666666666666666666666667"), response[teams[13].id])
        self.assertEqual(Deci("0.9333333333333333333333333334"), response[teams[14].id])
        self.assertEqual(Deci("1"), response[teams[15].id])

    def test_getAWALPerGame_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
            weeks=[week1, week2, week3],
        )

        response = AWALYearCalculator.getAWALPerGame(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0.2"), response[teams[1].id])
        self.assertEqual(Deci("0.4"), response[teams[2].id])
        self.assertEqual(Deci("0.7"), response[teams[3].id])
        self.assertEqual(Deci("0.7"), response[teams[4].id])
        self.assertEqual(Deci("1"), response[teams[5].id])

    def test_getAWALPerGame_leagueMedianGamesIsOn(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        yearSettings = YearSettings(leagueMedianGames=True)
        year = Year(
            yearNumber=2000, teams=teams, weeks=[week1, week2, week3], yearSettings=yearSettings
        )

        response = AWALYearCalculator.getAWALPerGame(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0.1"), response[teams[1].id])
        self.assertEqual(Deci("0.2"), response[teams[2].id])
        self.assertEqual(Deci("0.85"), response[teams[3].id])
        self.assertEqual(Deci("0.85"), response[teams[4].id])
        self.assertEqual(Deci("1"), response[teams[5].id])

    def test_getAWALPerGame_noneIfNoGamesPlayed(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        week1 = Week(weekNumber=1, matchups=[matchup1])

        matchup4 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup5 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup6 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)
        week2 = Week(weekNumber=2, matchups=[matchup4, matchup5, matchup6])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2])

        response = AWALYearCalculator.getAWALPerGame(year, weekNumberEnd=1)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("1"), response[teams[1].id])
        self.assertIsNone(response[teams[2].id])
        self.assertIsNone(response[teams[3].id])
        self.assertIsNone(response[teams[4].id])
        self.assertIsNone(response[teams[5].id])

    def test_getAWALPerGame_onlyPostSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.PLAYOFF,
        )

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
            weeks=[week1, week2, week3],
        )

        response = AWALYearCalculator.getAWALPerGame(year, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0.2"), response[teams[1].id])
        self.assertEqual(Deci("0.4"), response[teams[2].id])
        self.assertEqual(Deci("0.7"), response[teams[3].id])
        self.assertEqual(Deci("0.7"), response[teams[4].id])
        self.assertEqual(Deci("1"), response[teams[5].id])

    def test_getAWALPerGame_onlyRegularSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.PLAYOFF,
        )

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
            weeks=[week1, week2, week3],
        )

        response = AWALYearCalculator.getAWALPerGame(year, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0.2"), response[teams[1].id])
        self.assertEqual(Deci("0.4"), response[teams[2].id])
        self.assertEqual(Deci("0.7"), response[teams[3].id])
        self.assertEqual(Deci("0.7"), response[teams[4].id])
        self.assertEqual(Deci("1"), response[teams[5].id])

    def test_getAWALPerGame_onlyChampionshipIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.PLAYOFF,
        )

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
            weeks=[week1, week2, week3],
        )

        response = AWALYearCalculator.getAWALPerGame(year, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertIsNone(response[teams[0].id])
        self.assertIsNone(response[teams[1].id])
        self.assertIsNone(response[teams[2].id])
        self.assertIsNone(response[teams[3].id])
        self.assertEqual(Deci("0"), response[teams[4].id])
        self.assertEqual(Deci("1"), response[teams[5].id])

    def test_getAWALPerGame_weekNumberStartGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.PLAYOFF,
        )

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
            weeks=[week1, week2, week3],
        )

        response = AWALYearCalculator.getAWALPerGame(year, weekNumberStart=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0.2"), response[teams[1].id])
        self.assertEqual(Deci("0.4"), response[teams[2].id])
        self.assertEqual(Deci("0.7"), response[teams[3].id])
        self.assertEqual(Deci("0.7"), response[teams[4].id])
        self.assertEqual(Deci("1"), response[teams[5].id])

    def test_getAWALPerGame_weekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.PLAYOFF,
        )

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
            weeks=[week1, week2, week3],
        )

        response = AWALYearCalculator.getAWALPerGame(year, weekNumberEnd=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0.2"), response[teams[1].id])
        self.assertEqual(Deci("0.4"), response[teams[2].id])
        self.assertEqual(Deci("0.7"), response[teams[3].id])
        self.assertEqual(Deci("0.7"), response[teams[4].id])
        self.assertEqual(Deci("1"), response[teams[5].id])

    def test_getAWALPerGame_weekNumberStartGivenAndWeekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.PLAYOFF,
        )

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.PLAYOFF,
        )

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week4 = Week(weekNumber=4, matchups=[matchup1, matchup2, matchup3])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
            weeks=[week1, week2, week3, week4],
        )

        response = AWALYearCalculator.getAWALPerGame(year, weekNumberStart=2, weekNumberEnd=3)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0"), response[teams[0].id])
        self.assertEqual(Deci("0.2"), response[teams[1].id])
        self.assertEqual(Deci("0.4"), response[teams[2].id])
        self.assertEqual(Deci("0.7"), response[teams[3].id])
        self.assertEqual(Deci("0.7"), response[teams[4].id])
        self.assertEqual(Deci("1"), response[teams[5].id])

    def test_getAWALPerGame_teamsDontPlayEveryWeek(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[5].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week2 = Week(weekNumber=2, matchups=[matchup1])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
            weeks=[week1, week2],
        )

        response = AWALYearCalculator.getAWALPerGame(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.5"), response[teams[0].id])
        self.assertEqual(Deci("0.2"), response[teams[1].id])
        self.assertEqual(Deci("0.4"), response[teams[2].id])
        self.assertEqual(Deci("0.7"), response[teams[3].id])
        self.assertEqual(Deci("0.7"), response[teams[4].id])
        self.assertEqual(Deci("0.5"), response[teams[5].id])

    def test_getOpponentAWAL_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
            weeks=[week1, week2, week3],
        )

        response = AWALYearCalculator.getOpponentAWAL(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.6"), response[teams[0].id])
        self.assertEqual(Deci("0"), response[teams[1].id])
        self.assertEqual(Deci("2.1"), response[teams[2].id])
        self.assertEqual(Deci("1.2"), response[teams[3].id])
        self.assertEqual(Deci("3"), response[teams[4].id])
        self.assertEqual(Deci("2.1"), response[teams[5].id])

    def test_getOpponentAWAL_leagueMedianGamesIsOn_countsLeagueMedianGames(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        yearSettings = YearSettings(leagueMedianGames=True)
        year = Year(
            yearNumber=2000, teams=teams, weeks=[week1, week2, week3], yearSettings=yearSettings
        )

        response = AWALYearCalculator.getOpponentAWAL(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.6"), response[teams[0].id])
        self.assertEqual(Deci("0"), response[teams[1].id])
        self.assertEqual(Deci("5.1"), response[teams[2].id])
        self.assertEqual(Deci("1.2"), response[teams[3].id])
        self.assertEqual(Deci("6"), response[teams[4].id])
        self.assertEqual(Deci("5.1"), response[teams[5].id])

    def test_getOpponentAWAL_noneIfNoGamesPlayed(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        week1 = Week(weekNumber=1, matchups=[matchup1])

        matchup4 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup5 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup6 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)
        week2 = Week(weekNumber=2, matchups=[matchup4, matchup5, matchup6])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2])

        response = AWALYearCalculator.getOpponentAWAL(year, weekNumberEnd=1)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("1"), response[teams[0].id])
        self.assertEqual(Deci("0"), response[teams[1].id])
        self.assertIsNone(response[teams[2].id])
        self.assertIsNone(response[teams[3].id])
        self.assertIsNone(response[teams[4].id])
        self.assertIsNone(response[teams[5].id])

    def test_getOpponentAWAL_onlyPostSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.PLAYOFF,
        )

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
            weeks=[week1, week2, week3],
        )

        response = AWALYearCalculator.getOpponentAWAL(year, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.4"), response[teams[0].id])
        self.assertEqual(Deci("0"), response[teams[1].id])
        self.assertEqual(Deci("1.4"), response[teams[2].id])
        self.assertEqual(Deci("0.8"), response[teams[3].id])
        self.assertEqual(Deci("2"), response[teams[4].id])
        self.assertEqual(Deci("1.4"), response[teams[5].id])

    def test_getOpponentAWAL_onlyRegularSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.PLAYOFF,
        )

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
            weeks=[week1, week2, week3],
        )

        response = AWALYearCalculator.getOpponentAWAL(year, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.2"), response[teams[0].id])
        self.assertEqual(Deci("0"), response[teams[1].id])
        self.assertEqual(Deci("0.7"), response[teams[2].id])
        self.assertEqual(Deci("0.4"), response[teams[3].id])
        self.assertEqual(Deci("1"), response[teams[4].id])
        self.assertEqual(Deci("0.7"), response[teams[5].id])

    def test_getOpponentAWAL_onlyChampionshipIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.PLAYOFF,
        )

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
            weeks=[week1, week2, week3],
        )

        response = AWALYearCalculator.getOpponentAWAL(year, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertIsNone(response[teams[0].id])
        self.assertIsNone(response[teams[1].id])
        self.assertIsNone(response[teams[2].id])
        self.assertIsNone(response[teams[3].id])
        self.assertEqual(Deci("1"), response[teams[4].id])
        self.assertEqual(Deci("0"), response[teams[5].id])

    def test_getOpponentAWAL_weekNumberStartGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.PLAYOFF,
        )

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
            weeks=[week1, week2, week3],
        )

        response = AWALYearCalculator.getOpponentAWAL(year, weekNumberStart=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.4"), response[teams[0].id])
        self.assertEqual(Deci("0"), response[teams[1].id])
        self.assertEqual(Deci("1.4"), response[teams[2].id])
        self.assertEqual(Deci("0.8"), response[teams[3].id])
        self.assertEqual(Deci("2"), response[teams[4].id])
        self.assertEqual(Deci("1.4"), response[teams[5].id])

    def test_getOpponentAWAL_weekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.PLAYOFF,
        )

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
            weeks=[week1, week2, week3],
        )

        response = AWALYearCalculator.getOpponentAWAL(year, weekNumberEnd=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.4"), response[teams[0].id])
        self.assertEqual(Deci("0"), response[teams[1].id])
        self.assertEqual(Deci("1.4"), response[teams[2].id])
        self.assertEqual(Deci("0.8"), response[teams[3].id])
        self.assertEqual(Deci("2"), response[teams[4].id])
        self.assertEqual(Deci("1.4"), response[teams[5].id])

    def test_getOpponentAWAL_weekNumberStartGivenAndWeekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.PLAYOFF,
        )

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
            weeks=[week1, week2, week3],
        )

        response = AWALYearCalculator.getOpponentAWAL(year, weekNumberStart=2, weekNumberEnd=3)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.4"), response[teams[0].id])
        self.assertEqual(Deci("0"), response[teams[1].id])
        self.assertEqual(Deci("1.4"), response[teams[2].id])
        self.assertEqual(Deci("0.8"), response[teams[3].id])
        self.assertEqual(Deci("2"), response[teams[4].id])
        self.assertEqual(Deci("1.4"), response[teams[5].id])

    def test_getOpponentAWAL_matchupEndsInTie(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=3)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
            weeks=[week1],
        )

        response = AWALYearCalculator.getOpponentAWAL(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.2"), response[teams[0].id])
        self.assertEqual(Deci("0"), response[teams[1].id])
        self.assertEqual(Deci("0.5"), response[teams[2].id])
        self.assertEqual(Deci("0.5"), response[teams[3].id])
        self.assertEqual(Deci("1"), response[teams[4].id])
        self.assertEqual(Deci("0.8"), response[teams[5].id])

    def test_getOpponentAWAL_multipleMatchupsEndInTie(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=3)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
            weeks=[week1],
        )

        response = AWALYearCalculator.getOpponentAWAL(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.1"), response[teams[0].id])
        self.assertEqual(Deci("0.1"), response[teams[1].id])
        self.assertEqual(Deci("0.5"), response[teams[2].id])
        self.assertEqual(Deci("0.5"), response[teams[3].id])
        self.assertEqual(Deci("1"), response[teams[4].id])
        self.assertEqual(Deci("0.8"), response[teams[5].id])

    def test_getOpponentAWAL_allMatchupsEndInTie(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=2, teamBScore=2)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=3, teamBScore=3)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
            weeks=[week1],
        )

        response = AWALYearCalculator.getOpponentAWAL(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.1"), response[teams[0].id])
        self.assertEqual(Deci("0.1"), response[teams[1].id])
        self.assertEqual(Deci("0.5"), response[teams[2].id])
        self.assertEqual(Deci("0.5"), response[teams[3].id])
        self.assertEqual(Deci("0.9"), response[teams[4].id])
        self.assertEqual(Deci("0.9"), response[teams[5].id])

    def test_getOpponentAWAL_allMatchupsEndInTieAndHaveSameScore(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=1)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=1, teamBScore=1)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=1, teamBScore=1)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
            weeks=[week1],
        )

        response = AWALYearCalculator.getOpponentAWAL(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.5"), response[teams[0].id])
        self.assertEqual(Deci("0.5"), response[teams[1].id])
        self.assertEqual(Deci("0.5"), response[teams[2].id])
        self.assertEqual(Deci("0.5"), response[teams[3].id])
        self.assertEqual(Deci("0.5"), response[teams[4].id])
        self.assertEqual(Deci("0.5"), response[teams[5].id])

    def test_getOpponentAWAL_sixteenTeams(self):
        owners, teams = getNDefaultOwnersAndTeams(16)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=5, teamBScore=6)
        matchup4 = Matchup(teamAId=teams[6].id, teamBId=teams[7].id, teamAScore=7, teamBScore=8)
        matchup5 = Matchup(teamAId=teams[8].id, teamBId=teams[9].id, teamAScore=9, teamBScore=10)
        matchup6 = Matchup(teamAId=teams[10].id, teamBId=teams[11].id, teamAScore=11, teamBScore=12)
        matchup7 = Matchup(teamAId=teams[12].id, teamBId=teams[13].id, teamAScore=13, teamBScore=14)
        matchup8 = Matchup(teamAId=teams[14].id, teamBId=teams[15].id, teamAScore=15, teamBScore=16)

        week1 = Week(
            weekNumber=1,
            matchups=[
                matchup1,
                matchup2,
                matchup3,
                matchup4,
                matchup5,
                matchup6,
                matchup7,
                matchup8,
            ],
        )

        year = Year(
            yearNumber=2000,
            teams=[
                teams[0],
                teams[1],
                teams[2],
                teams[3],
                teams[4],
                teams[5],
                teams[6],
                teams[7],
                teams[8],
                teams[9],
                teams[10],
                teams[11],
                teams[12],
                teams[13],
                teams[14],
                teams[15],
            ],
            weeks=[week1],
        )

        response = AWALYearCalculator.getOpponentAWAL(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(16, len(response.keys()))
        self.assertEqual(Deci("0.06666666666666666666666666667"), response[teams[0].id])
        self.assertEqual(Deci("0"), response[teams[1].id])
        self.assertEqual(Deci("0.2"), response[teams[2].id])
        self.assertEqual(Deci("0.1333333333333333333333333333"), response[teams[3].id])
        self.assertEqual(Deci("0.3333333333333333333333333334"), response[teams[4].id])
        self.assertEqual(Deci("0.2666666666666666666666666667"), response[teams[5].id])
        self.assertEqual(Deci("0.4666666666666666666666666667"), response[teams[6].id])
        self.assertEqual(Deci("0.4"), response[teams[7].id])
        self.assertEqual(Deci("0.6"), response[teams[8].id])
        self.assertEqual(Deci("0.5333333333333333333333333334"), response[teams[9].id])
        self.assertEqual(Deci("0.7333333333333333333333333334"), response[teams[10].id])
        self.assertEqual(Deci("0.6666666666666666666666666667"), response[teams[11].id])
        self.assertEqual(Deci("0.8666666666666666666666666667"), response[teams[12].id])
        self.assertEqual(Deci("0.8"), response[teams[13].id])
        self.assertEqual(Deci("1"), response[teams[14].id])
        self.assertEqual(Deci("0.9333333333333333333333333334"), response[teams[15].id])

    def test_getOpponentAWALPerGame_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
            weeks=[week1, week2, week3],
        )

        response = AWALYearCalculator.getOpponentAWALPerGame(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.2"), response[teams[0].id])
        self.assertEqual(Deci("0"), response[teams[1].id])
        self.assertEqual(Deci("0.7"), response[teams[2].id])
        self.assertEqual(Deci("0.4"), response[teams[3].id])
        self.assertEqual(Deci("1"), response[teams[4].id])
        self.assertEqual(Deci("0.7"), response[teams[5].id])

    def test_getOpponentAWALPerGame_leagueMedianGamesIsOn(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        yearSettings = YearSettings(leagueMedianGames=True)
        year = Year(
            yearNumber=2000, teams=teams, weeks=[week1, week2, week3], yearSettings=yearSettings
        )

        response = AWALYearCalculator.getOpponentAWALPerGame(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.1"), response[teams[0].id])
        self.assertEqual(Deci("0"), response[teams[1].id])
        self.assertEqual(Deci("0.85"), response[teams[2].id])
        self.assertEqual(Deci("0.2"), response[teams[3].id])
        self.assertEqual(Deci("1"), response[teams[4].id])
        self.assertEqual(Deci("0.85"), response[teams[5].id])

    def test_getOpponentAWALPerGame_noneIfNoGamesPlayed(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        week1 = Week(weekNumber=1, matchups=[matchup1])

        matchup4 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup5 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup6 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)
        week2 = Week(weekNumber=2, matchups=[matchup4, matchup5, matchup6])

        year = Year(yearNumber=2000, teams=teams, weeks=[week1, week2])

        response = AWALYearCalculator.getOpponentAWALPerGame(year, weekNumberEnd=1)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("1"), response[teams[0].id])
        self.assertEqual(Deci("0"), response[teams[1].id])
        self.assertIsNone(response[teams[2].id])
        self.assertIsNone(response[teams[3].id])
        self.assertIsNone(response[teams[4].id])
        self.assertIsNone(response[teams[5].id])

    def test_getOpponentAWALPerGame_onlyPostSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.PLAYOFF,
        )

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
            weeks=[week1, week2, week3],
        )

        response = AWALYearCalculator.getOpponentAWALPerGame(year, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.2"), response[teams[0].id])
        self.assertEqual(Deci("0"), response[teams[1].id])
        self.assertEqual(Deci("0.7"), response[teams[2].id])
        self.assertEqual(Deci("0.4"), response[teams[3].id])
        self.assertEqual(Deci("1"), response[teams[4].id])
        self.assertEqual(Deci("0.7"), response[teams[5].id])

    def test_getOpponentAWALPerGame_onlyRegularSeasonIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.PLAYOFF,
        )

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
            weeks=[week1, week2, week3],
        )

        response = AWALYearCalculator.getOpponentAWALPerGame(year, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.2"), response[teams[0].id])
        self.assertEqual(Deci("0"), response[teams[1].id])
        self.assertEqual(Deci("0.7"), response[teams[2].id])
        self.assertEqual(Deci("0.4"), response[teams[3].id])
        self.assertEqual(Deci("1"), response[teams[4].id])
        self.assertEqual(Deci("0.7"), response[teams[5].id])

    def test_getOpponentAWALPerGame_onlyChampionshipIsTrue(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.PLAYOFF,
        )

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
            weeks=[week1, week2, week3],
        )

        response = AWALYearCalculator.getOpponentAWALPerGame(year, onlyChampionship=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertIsNone(response[teams[0].id])
        self.assertIsNone(response[teams[1].id])
        self.assertIsNone(response[teams[2].id])
        self.assertIsNone(response[teams[3].id])
        self.assertEqual(Deci("1"), response[teams[4].id])
        self.assertEqual(Deci("0"), response[teams[5].id])

    def test_getOpponentAWALPerGame_weekNumberStartGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.PLAYOFF,
        )

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
            weeks=[week1, week2, week3],
        )

        response = AWALYearCalculator.getOpponentAWALPerGame(year, weekNumberStart=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.2"), response[teams[0].id])
        self.assertEqual(Deci("0"), response[teams[1].id])
        self.assertEqual(Deci("0.7"), response[teams[2].id])
        self.assertEqual(Deci("0.4"), response[teams[3].id])
        self.assertEqual(Deci("1"), response[teams[4].id])
        self.assertEqual(Deci("0.7"), response[teams[5].id])

    def test_getOpponentAWALPerGame_weekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.PLAYOFF,
        )

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
            weeks=[week1, week2, week3],
        )

        response = AWALYearCalculator.getOpponentAWALPerGame(year, weekNumberEnd=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.2"), response[teams[0].id])
        self.assertEqual(Deci("0"), response[teams[1].id])
        self.assertEqual(Deci("0.7"), response[teams[2].id])
        self.assertEqual(Deci("0.4"), response[teams[3].id])
        self.assertEqual(Deci("1"), response[teams[4].id])
        self.assertEqual(Deci("0.7"), response[teams[5].id])

    def test_getOpponentAWALPerGame_weekNumberStartGivenAndWeekNumberEndGiven(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.PLAYOFF,
        )

        week2 = Week(weekNumber=2, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.PLAYOFF,
        )

        week3 = Week(weekNumber=3, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[1].id,
            teamAScore=1,
            teamBScore=2,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup2 = Matchup(
            teamAId=teams[2].id,
            teamBId=teams[3].id,
            teamAScore=3,
            teamBScore=4,
            matchupType=MatchupType.PLAYOFF,
        )
        matchup3 = Matchup(
            teamAId=teams[4].id,
            teamBId=teams[5].id,
            teamAScore=4,
            teamBScore=5,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week4 = Week(weekNumber=4, matchups=[matchup1, matchup2, matchup3])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
            weeks=[week1, week2, week3, week4],
        )

        response = AWALYearCalculator.getOpponentAWALPerGame(
            year, weekNumberStart=2, weekNumberEnd=3
        )

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.2"), response[teams[0].id])
        self.assertEqual(Deci("0"), response[teams[1].id])
        self.assertEqual(Deci("0.7"), response[teams[2].id])
        self.assertEqual(Deci("0.4"), response[teams[3].id])
        self.assertEqual(Deci("1"), response[teams[4].id])
        self.assertEqual(Deci("0.7"), response[teams[5].id])

    def test_getOpponentAWALPerGame_teamsDontPlayEveryWeek(self):
        owners, teams = getNDefaultOwnersAndTeams(6)

        matchup1 = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=teams[2].id, teamBId=teams[3].id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=teams[4].id, teamBId=teams[5].id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(
            teamAId=teams[0].id,
            teamBId=teams[5].id,
            teamAScore=2,
            teamBScore=1,
            matchupType=MatchupType.CHAMPIONSHIP,
        )

        week2 = Week(weekNumber=2, matchups=[matchup1])

        year = Year(
            yearNumber=2000,
            teams=[teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]],
            weeks=[week1, week2],
        )

        response = AWALYearCalculator.getOpponentAWALPerGame(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Deci("0.1"), response[teams[0].id])
        self.assertEqual(Deci("0.0"), response[teams[1].id])
        self.assertEqual(Deci("0.7"), response[teams[2].id])
        self.assertEqual(Deci("0.4"), response[teams[3].id])
        self.assertEqual(Deci("1"), response[teams[4].id])
        self.assertEqual(Deci("0.85"), response[teams[5].id])
