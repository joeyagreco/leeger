import unittest

from leeger.enum.MatchupType import MatchupType
from leeger.model.league.Matchup import Matchup
from leeger.model.league.Team import Team
from leeger.model.league.Week import Week
from leeger.model.league.Year import Year
from leeger.model.stat.YearStatSheet import YearStatSheet
from test.helper.prototypes import getNDefaultOwnersAndTeams


class TestYear(unittest.TestCase):
    def test_year_init(self):
        week = Week(weekNumber=1, matchups=[])
        team = Team(ownerId="", name="")
        year = Year(yearNumber=2000, teams=[team], weeks=[week])

        self.assertEqual(2000, year.yearNumber)
        self.assertEqual(1, len(year.teams))
        self.assertEqual(1, len(year.weeks))
        self.assertEqual(week.id, year.weeks[0].id)
        self.assertEqual(team.id, year.teams[0].id)

    def test_year_eq_equal(self):
        # create Year 1
        owners_1, teams_1 = getNDefaultOwnersAndTeams(2)

        matchup_1 = Matchup(teamAId=teams_1[0].id, teamBId=teams_1[1].id, teamAScore=1.1, teamBScore=2.2,
                            matchupType=MatchupType.REGULAR_SEASON)
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        year_1 = Year(yearNumber=2000, teams=teams_1, weeks=[week_1])

        # create Year 2
        owners_2, teams_2 = getNDefaultOwnersAndTeams(2)

        matchup_2 = Matchup(teamAId=teams_2[0].id, teamBId=teams_2[1].id, teamAScore=1.1, teamBScore=2.2,
                            matchupType=MatchupType.REGULAR_SEASON)
        week_2 = Week(weekNumber=1, matchups=[matchup_2])
        year_2 = Year(yearNumber=2000, teams=teams_2, weeks=[week_2])

        self.assertEqual(year_1, year_2)

    def test_year_eq_notEqual(self):
        # create Year 1
        owners_1, teams_1 = getNDefaultOwnersAndTeams(2)

        matchup_1 = Matchup(teamAId=teams_1[0].id, teamBId=teams_1[1].id, teamAScore=1.1, teamBScore=2.2,
                            matchupType=MatchupType.REGULAR_SEASON)
        week_1 = Week(weekNumber=1, matchups=[matchup_1])
        year_1 = Year(yearNumber=2000, teams=teams_1, weeks=[week_1])

        # create Year 2
        owners_2, teams_2 = getNDefaultOwnersAndTeams(2)

        matchup_2 = Matchup(teamAId=teams_2[0].id, teamBId=teams_2[1].id, teamAScore=1.1, teamBScore=2.2,
                            matchupType=MatchupType.REGULAR_SEASON)
        week_2 = Week(weekNumber=1, matchups=[matchup_2])
        year_2 = Year(yearNumber=2001, teams=teams_2, weeks=[week_2])

        self.assertNotEqual(year_1, year_2)

    def test_year_statSheet(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        week = Week(weekNumber=1, matchups=[matchup])
        year = Year(yearNumber=2000, teams=teams, weeks=[week])

        yearStatSheet = year.statSheet()

        self.assertIsInstance(yearStatSheet, YearStatSheet)
        self.assertIsInstance(yearStatSheet.wins, dict)
        self.assertIsInstance(yearStatSheet.losses, dict)
        self.assertIsInstance(yearStatSheet.ties, dict)
        self.assertIsInstance(yearStatSheet.winPercentage, dict)
        self.assertIsInstance(yearStatSheet.wal, dict)
        self.assertIsInstance(yearStatSheet.walPerGame, dict)

        self.assertIsInstance(yearStatSheet.awal, dict)
        self.assertIsInstance(yearStatSheet.awalPerGame, dict)
        self.assertIsInstance(yearStatSheet.opponentAWAL, dict)
        self.assertIsInstance(yearStatSheet.opponentAWALPerGame, dict)

        self.assertIsInstance(yearStatSheet.smartWins, dict)
        self.assertIsInstance(yearStatSheet.smartWinsPerGame, dict)
        self.assertIsInstance(yearStatSheet.opponentSmartWins, dict)
        self.assertIsInstance(yearStatSheet.opponentSmartWinsPerGame, dict)

        self.assertIsInstance(yearStatSheet.pointsScored, dict)
        self.assertIsInstance(yearStatSheet.pointsScoredPerGame, dict)
        self.assertIsInstance(yearStatSheet.opponentPointsScored, dict)
        self.assertIsInstance(yearStatSheet.opponentPointsScoredPerGame, dict)

        self.assertIsInstance(yearStatSheet.scoringShare, dict)
        self.assertIsInstance(yearStatSheet.opponentScoringShare, dict)

        self.assertIsInstance(yearStatSheet.maxScore, dict)
        self.assertIsInstance(yearStatSheet.minScore, dict)

        self.assertIsInstance(yearStatSheet.scoringStandardDeviation, dict)

        self.assertIsInstance(yearStatSheet.plusMinus, dict)

        self.assertIsInstance(yearStatSheet.teamScore, dict)
        self.assertIsInstance(yearStatSheet.teamSuccess, dict)
        self.assertIsInstance(yearStatSheet.teamLuck, dict)
