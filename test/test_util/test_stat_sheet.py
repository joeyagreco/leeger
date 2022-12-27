import unittest

from leeger.model.league import YearSettings
from leeger.model.league.League import League
from leeger.model.league.Matchup import Matchup
from leeger.model.league.Week import Week
from leeger.model.league.Year import Year
from leeger.model.stat.AllTimeStatSheet import AllTimeStatSheet
from leeger.model.stat.YearStatSheet import YearStatSheet
from test.helper.prototypes import getNDefaultOwnersAndTeams


class TestStatSheet(unittest.TestCase):

    def test_leagueStatSheet(self):
        from leeger.util.stat_sheet import leagueStatSheet
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        week = Week(weekNumber=1, matchups=[matchup])
        year = Year(yearNumber=2000, teams=teams, weeks=[week])

        league = League(name="TEST", owners=owners, years=[year])

        leagueStatSheet = leagueStatSheet(league)

        self.assertIsInstance(leagueStatSheet, AllTimeStatSheet)
        self.assertIsInstance(leagueStatSheet.gamesPlayed, dict)
        self.assertIsInstance(leagueStatSheet.wins, dict)
        self.assertIsInstance(leagueStatSheet.losses, dict)
        self.assertIsInstance(leagueStatSheet.ties, dict)
        self.assertIsInstance(leagueStatSheet.winPercentage, dict)
        self.assertIsInstance(leagueStatSheet.wal, dict)
        self.assertIsInstance(leagueStatSheet.walPerGame, dict)

        self.assertIsInstance(leagueStatSheet.awal, dict)
        self.assertIsInstance(leagueStatSheet.awalPerGame, dict)
        self.assertIsInstance(leagueStatSheet.opponentAWAL, dict)
        self.assertIsInstance(leagueStatSheet.opponentAWALPerGame, dict)

        self.assertIsInstance(leagueStatSheet.smartWins, dict)
        self.assertIsInstance(leagueStatSheet.smartWinsPerGame, dict)
        self.assertIsInstance(leagueStatSheet.opponentSmartWins, dict)
        self.assertIsInstance(leagueStatSheet.opponentSmartWinsPerGame, dict)

        self.assertIsInstance(leagueStatSheet.pointsScored, dict)
        self.assertIsInstance(leagueStatSheet.pointsScoredPerGame, dict)
        self.assertIsInstance(leagueStatSheet.opponentPointsScored, dict)
        self.assertIsInstance(leagueStatSheet.opponentPointsScoredPerGame, dict)

        self.assertIsInstance(leagueStatSheet.scoringShare, dict)
        self.assertIsInstance(leagueStatSheet.opponentScoringShare, dict)
        self.assertIsInstance(leagueStatSheet.maxScoringShare, dict)
        self.assertIsInstance(leagueStatSheet.minScoringShare, dict)

        self.assertIsInstance(leagueStatSheet.maxScore, dict)
        self.assertIsInstance(leagueStatSheet.minScore, dict)

        self.assertIsInstance(leagueStatSheet.scoringStandardDeviation, dict)

        self.assertIsInstance(leagueStatSheet.plusMinus, dict)

        self.assertIsInstance(leagueStatSheet.adjustedTeamScore, dict)
        self.assertIsInstance(leagueStatSheet.adjustedTeamSuccess, dict)
        self.assertIsInstance(leagueStatSheet.adjustedTeamLuck, dict)

        # check optional stats are None
        self.assertIsNone(leagueStatSheet.leagueMedianWins)

    def test_leagueStatSheet_leagueMedianGamesIsTrueInAnyYearSettings(self):
        from leeger.util.stat_sheet import leagueStatSheet
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        week = Week(weekNumber=1, matchups=[matchup])
        yearSettings = YearSettings(leagueMedianGames=True)
        year = Year(yearNumber=2000, teams=teams, weeks=[week], yearSettings=yearSettings)

        league = League(name="TEST", owners=owners, years=[year])

        leagueStatSheet = leagueStatSheet(league)

        self.assertIsInstance(leagueStatSheet, AllTimeStatSheet)
        self.assertIsInstance(leagueStatSheet.leagueMedianWins, dict)

    def test_yearStatSheet(self):
        from leeger.util.stat_sheet import yearStatSheet
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        week = Week(weekNumber=1, matchups=[matchup])
        year = Year(yearNumber=2000, teams=teams, weeks=[week])

        yearStatSheet = yearStatSheet(year)

        self.assertIsInstance(yearStatSheet, YearStatSheet)
        self.assertIsInstance(yearStatSheet.gamesPlayed, dict)
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
        self.assertIsInstance(yearStatSheet.maxScoringShare, dict)
        self.assertIsInstance(yearStatSheet.minScoringShare, dict)

        self.assertIsInstance(yearStatSheet.maxScore, dict)
        self.assertIsInstance(yearStatSheet.minScore, dict)

        self.assertIsInstance(yearStatSheet.scoringStandardDeviation, dict)

        self.assertIsInstance(yearStatSheet.plusMinus, dict)

        self.assertIsInstance(yearStatSheet.teamScore, dict)
        self.assertIsInstance(yearStatSheet.teamSuccess, dict)
        self.assertIsInstance(yearStatSheet.teamLuck, dict)

        # check optional stats are None
        self.assertIsNone(yearStatSheet.leagueMedianWins)
        self.assertIsNone(yearStatSheet.totalGames)
        self.assertIsNone(yearStatSheet.opponentLeagueMedianWins)

        self.assertIsNone(yearStatSheet.ownerNames)
        self.assertIsNone(yearStatSheet.years)

    def test_yearStatSheet_ownerNamesAndYearsGiven(self):
        from leeger.util.stat_sheet import yearStatSheet
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        week = Week(weekNumber=1, matchups=[matchup])
        year = Year(yearNumber=2000, teams=teams, weeks=[week])

        ownerNames = {
            teams[0].id: "owner0",
            teams[1].id: "owner1"
        }

        years = {
            teams[0].id: 2000,
            teams[1].id: 2000
        }

        yearStatSheet = yearStatSheet(year, ownerNames=ownerNames, years=years)

        self.assertIsInstance(yearStatSheet, YearStatSheet)
        self.assertIsInstance(yearStatSheet.gamesPlayed, dict)
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
        self.assertIsInstance(yearStatSheet.maxScoringShare, dict)
        self.assertIsInstance(yearStatSheet.minScoringShare, dict)

        self.assertIsInstance(yearStatSheet.maxScore, dict)
        self.assertIsInstance(yearStatSheet.minScore, dict)

        self.assertIsInstance(yearStatSheet.scoringStandardDeviation, dict)

        self.assertIsInstance(yearStatSheet.plusMinus, dict)

        self.assertIsInstance(yearStatSheet.teamScore, dict)
        self.assertIsInstance(yearStatSheet.teamSuccess, dict)
        self.assertIsInstance(yearStatSheet.teamLuck, dict)

        self.assertIsInstance(yearStatSheet.ownerNames, dict)
        self.assertIsInstance(yearStatSheet.years, dict)

        # check optional stats are None
        self.assertIsNone(yearStatSheet.leagueMedianWins)
        self.assertIsNone(yearStatSheet.totalGames)
        self.assertIsNone(yearStatSheet.opponentLeagueMedianWins)

    def test_yearStatSheet_leagueMedianGamesIsTrue(self):
        from leeger.util.stat_sheet import yearStatSheet
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        week = Week(weekNumber=1, matchups=[matchup])
        yearSettings = YearSettings(leagueMedianGames=True)
        year = Year(yearNumber=2000, teams=teams, weeks=[week], yearSettings=yearSettings)

        yearStatSheet = yearStatSheet(year)

        self.assertIsInstance(yearStatSheet, YearStatSheet)
        self.assertIsInstance(yearStatSheet.leagueMedianWins, dict)
        self.assertIsInstance(yearStatSheet.totalGames, dict)
        self.assertIsInstance(yearStatSheet.opponentLeagueMedianWins, dict)

    def test_allTimeTeamsStatSheet_happyPath(self):
        from leeger.util.stat_sheet import allTimeTeamsStatSheet
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        week = Week(weekNumber=1, matchups=[matchup])
        year = Year(yearNumber=2000, teams=teams, weeks=[week])

        league = League(name="TEST", owners=owners, years=[year])

        allTimeTeamsStatSheet_ = allTimeTeamsStatSheet(league)

        self.assertEquals(32, len(allTimeTeamsStatSheet_))
        for tup in allTimeTeamsStatSheet_:
            self.assertIsInstance(tup, tuple)
        self.assertEquals("Owner", allTimeTeamsStatSheet_[0][0])
        self.assertEquals("Year", allTimeTeamsStatSheet_[1][0])
        self.assertEquals("Games Played", allTimeTeamsStatSheet_[2][0])
        self.assertEquals("Wins", allTimeTeamsStatSheet_[3][0])
        self.assertEquals("Losses", allTimeTeamsStatSheet_[4][0])
        self.assertEquals("Ties", allTimeTeamsStatSheet_[5][0])
        self.assertEquals("Win Percentage", allTimeTeamsStatSheet_[6][0])
        self.assertEquals("WAL", allTimeTeamsStatSheet_[7][0])
        self.assertEquals("WAL Per Game", allTimeTeamsStatSheet_[8][0])
        self.assertEquals("AWAL", allTimeTeamsStatSheet_[9][0])
        self.assertEquals("AWAL Per Game", allTimeTeamsStatSheet_[10][0])
        self.assertEquals("Opponent AWAL", allTimeTeamsStatSheet_[11][0])
        self.assertEquals("Opponent AWAL Per Game", allTimeTeamsStatSheet_[12][0])
        self.assertEquals("Smart Wins", allTimeTeamsStatSheet_[13][0])
        self.assertEquals("Smart Wins Per Game", allTimeTeamsStatSheet_[14][0])
        self.assertEquals("Opponent Smart Wins", allTimeTeamsStatSheet_[15][0])
        self.assertEquals("Opponent Smart Wins Per Game", allTimeTeamsStatSheet_[16][0])
        self.assertEquals("Points Scored", allTimeTeamsStatSheet_[17][0])
        self.assertEquals("Points Scored Per Game", allTimeTeamsStatSheet_[18][0])
        self.assertEquals("Opponent Points Scored", allTimeTeamsStatSheet_[19][0])
        self.assertEquals("Opponent Points Scored Per Game", allTimeTeamsStatSheet_[20][0])
        self.assertEquals("Scoring Share", allTimeTeamsStatSheet_[21][0])
        self.assertEquals("Opponent Scoring Share", allTimeTeamsStatSheet_[22][0])
        self.assertEquals("Max Scoring Share", allTimeTeamsStatSheet_[23][0])
        self.assertEquals("Min Scoring Share", allTimeTeamsStatSheet_[24][0])
        self.assertEquals("Max Score", allTimeTeamsStatSheet_[25][0])
        self.assertEquals("Min Score", allTimeTeamsStatSheet_[26][0])
        self.assertEquals("Scoring Standard Deviation", allTimeTeamsStatSheet_[27][0])
        self.assertEquals("Plus/Minus", allTimeTeamsStatSheet_[28][0])
        self.assertEquals("Team Score", allTimeTeamsStatSheet_[29][0])
        self.assertEquals("Team Success", allTimeTeamsStatSheet_[30][0])
        self.assertEquals("Team Luck", allTimeTeamsStatSheet_[31][0])

    def test_allTimeTeamsStatSheet_leagueMedianGamesIsTrueInAnyYearSettings(self):
        from leeger.util.stat_sheet import allTimeTeamsStatSheet
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        week = Week(weekNumber=1, matchups=[matchup])
        yearSettings = YearSettings(leagueMedianGames=True)
        year1 = Year(yearNumber=2000, teams=teams, weeks=[week], yearSettings=yearSettings)

        _, teams = getNDefaultOwnersAndTeams(2)
        teams[0].ownerId = owners[0].id
        teams[1].ownerId = owners[1].id

        matchup = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        week = Week(weekNumber=1, matchups=[matchup])
        year2 = Year(yearNumber=2001, teams=teams, weeks=[week])

        league = League(name="TEST", owners=owners, years=[year1, year2])

        allTimeTeamsStatSheet_ = allTimeTeamsStatSheet(league)

        self.assertEquals(35, len(allTimeTeamsStatSheet_))
        for tup in allTimeTeamsStatSheet_:
            self.assertIsInstance(tup, tuple)
        self.assertEquals("Owner", allTimeTeamsStatSheet_[0][0])
        self.assertEquals("Year", allTimeTeamsStatSheet_[1][0])
        self.assertEquals("Games Played", allTimeTeamsStatSheet_[2][0])
        self.assertEquals("Total Games", allTimeTeamsStatSheet_[3][0])
        self.assertEquals("Wins", allTimeTeamsStatSheet_[4][0])
        self.assertEquals("Losses", allTimeTeamsStatSheet_[5][0])
        self.assertEquals("League Median Wins", allTimeTeamsStatSheet_[6][0])
        self.assertEquals("Opponent League Median Wins", allTimeTeamsStatSheet_[7][0])
        self.assertEquals("Ties", allTimeTeamsStatSheet_[8][0])
        self.assertEquals("Win Percentage", allTimeTeamsStatSheet_[9][0])
        self.assertEquals("WAL", allTimeTeamsStatSheet_[10][0])
        self.assertEquals("WAL Per Game", allTimeTeamsStatSheet_[11][0])
        self.assertEquals("AWAL", allTimeTeamsStatSheet_[12][0])
        self.assertEquals("AWAL Per Game", allTimeTeamsStatSheet_[13][0])
        self.assertEquals("Opponent AWAL", allTimeTeamsStatSheet_[14][0])
        self.assertEquals("Opponent AWAL Per Game", allTimeTeamsStatSheet_[15][0])
        self.assertEquals("Smart Wins", allTimeTeamsStatSheet_[16][0])
        self.assertEquals("Smart Wins Per Game", allTimeTeamsStatSheet_[17][0])
        self.assertEquals("Opponent Smart Wins", allTimeTeamsStatSheet_[18][0])
        self.assertEquals("Opponent Smart Wins Per Game", allTimeTeamsStatSheet_[19][0])
        self.assertEquals("Points Scored", allTimeTeamsStatSheet_[20][0])
        self.assertEquals("Points Scored Per Game", allTimeTeamsStatSheet_[21][0])
        self.assertEquals("Opponent Points Scored", allTimeTeamsStatSheet_[22][0])
        self.assertEquals("Opponent Points Scored Per Game", allTimeTeamsStatSheet_[23][0])
        self.assertEquals("Scoring Share", allTimeTeamsStatSheet_[24][0])
        self.assertEquals("Opponent Scoring Share", allTimeTeamsStatSheet_[25][0])
        self.assertEquals("Max Scoring Share", allTimeTeamsStatSheet_[26][0])
        self.assertEquals("Min Scoring Share", allTimeTeamsStatSheet_[27][0])
        self.assertEquals("Max Score", allTimeTeamsStatSheet_[28][0])
        self.assertEquals("Min Score", allTimeTeamsStatSheet_[29][0])
        self.assertEquals("Scoring Standard Deviation", allTimeTeamsStatSheet_[30][0])
        self.assertEquals("Plus/Minus", allTimeTeamsStatSheet_[31][0])
        self.assertEquals("Team Score", allTimeTeamsStatSheet_[32][0])
        self.assertEquals("Team Success", allTimeTeamsStatSheet_[33][0])
        self.assertEquals("Team Luck", allTimeTeamsStatSheet_[34][0])
