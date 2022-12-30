import unittest

from leeger.model.league import YearSettings
from leeger.model.league.League import League
from leeger.model.league.Matchup import Matchup
from leeger.model.league.Week import Week
from leeger.model.league.Year import Year
from leeger.util.excel_helper import allTimeTeamsStatSheet
from test.helper.prototypes import getNDefaultOwnersAndTeams


class TestExcelHelper(unittest.TestCase):

    def test_allTimeTeamsStatSheet_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        week = Week(weekNumber=1, matchups=[matchup])
        year = Year(yearNumber=2000, teams=teams, weeks=[week])

        league = League(name="TEST", owners=owners, years=[year])

        allTimeTeamsStatSheet_ = allTimeTeamsStatSheet(league)

        self.assertEquals(33, len(allTimeTeamsStatSheet_))
        for tup in allTimeTeamsStatSheet_:
            self.assertIsInstance(tup, tuple)
        self.assertEquals("Team", allTimeTeamsStatSheet_[0][0])
        self.assertEquals("Owner", allTimeTeamsStatSheet_[1][0])
        self.assertEquals("Year", allTimeTeamsStatSheet_[2][0])
        self.assertEquals("Games Played", allTimeTeamsStatSheet_[3][0])
        self.assertEquals("Wins", allTimeTeamsStatSheet_[4][0])
        self.assertEquals("Losses", allTimeTeamsStatSheet_[5][0])
        self.assertEquals("Ties", allTimeTeamsStatSheet_[6][0])
        self.assertEquals("Win Percentage", allTimeTeamsStatSheet_[7][0])
        self.assertEquals("WAL", allTimeTeamsStatSheet_[8][0])
        self.assertEquals("WAL Per Game", allTimeTeamsStatSheet_[9][0])
        self.assertEquals("AWAL", allTimeTeamsStatSheet_[10][0])
        self.assertEquals("AWAL Per Game", allTimeTeamsStatSheet_[11][0])
        self.assertEquals("Opponent AWAL", allTimeTeamsStatSheet_[12][0])
        self.assertEquals("Opponent AWAL Per Game", allTimeTeamsStatSheet_[13][0])
        self.assertEquals("Smart Wins", allTimeTeamsStatSheet_[14][0])
        self.assertEquals("Smart Wins Per Game", allTimeTeamsStatSheet_[15][0])
        self.assertEquals("Opponent Smart Wins", allTimeTeamsStatSheet_[16][0])
        self.assertEquals("Opponent Smart Wins Per Game", allTimeTeamsStatSheet_[17][0])
        self.assertEquals("Points Scored", allTimeTeamsStatSheet_[18][0])
        self.assertEquals("Points Scored Per Game", allTimeTeamsStatSheet_[19][0])
        self.assertEquals("Opponent Points Scored", allTimeTeamsStatSheet_[20][0])
        self.assertEquals("Opponent Points Scored Per Game", allTimeTeamsStatSheet_[21][0])
        self.assertEquals("Scoring Share", allTimeTeamsStatSheet_[22][0])
        self.assertEquals("Opponent Scoring Share", allTimeTeamsStatSheet_[23][0])
        self.assertEquals("Max Scoring Share", allTimeTeamsStatSheet_[24][0])
        self.assertEquals("Min Scoring Share", allTimeTeamsStatSheet_[25][0])
        self.assertEquals("Max Score", allTimeTeamsStatSheet_[26][0])
        self.assertEquals("Min Score", allTimeTeamsStatSheet_[27][0])
        self.assertEquals("Scoring Standard Deviation", allTimeTeamsStatSheet_[28][0])
        self.assertEquals("Plus/Minus", allTimeTeamsStatSheet_[29][0])
        self.assertEquals("Team Score", allTimeTeamsStatSheet_[30][0])
        self.assertEquals("Team Success", allTimeTeamsStatSheet_[31][0])
        self.assertEquals("Team Luck", allTimeTeamsStatSheet_[32][0])

    def test_allTimeTeamsStatSheet_leagueMedianGamesIsTrueInAnyYearSettings(self):
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

        self.assertEquals(36, len(allTimeTeamsStatSheet_))
        for tup in allTimeTeamsStatSheet_:
            self.assertIsInstance(tup, tuple)
        self.assertEquals("Team", allTimeTeamsStatSheet_[0][0])
        self.assertEquals("Owner", allTimeTeamsStatSheet_[1][0])
        self.assertEquals("Year", allTimeTeamsStatSheet_[2][0])
        self.assertEquals("Games Played", allTimeTeamsStatSheet_[3][0])
        self.assertEquals("Total Games", allTimeTeamsStatSheet_[4][0])
        self.assertEquals("Wins", allTimeTeamsStatSheet_[5][0])
        self.assertEquals("Losses", allTimeTeamsStatSheet_[6][0])
        self.assertEquals("League Median Wins", allTimeTeamsStatSheet_[7][0])
        self.assertEquals("Opponent League Median Wins", allTimeTeamsStatSheet_[8][0])
        self.assertEquals("Ties", allTimeTeamsStatSheet_[9][0])
        self.assertEquals("Win Percentage", allTimeTeamsStatSheet_[10][0])
        self.assertEquals("WAL", allTimeTeamsStatSheet_[11][0])
        self.assertEquals("WAL Per Game", allTimeTeamsStatSheet_[12][0])
        self.assertEquals("AWAL", allTimeTeamsStatSheet_[13][0])
        self.assertEquals("AWAL Per Game", allTimeTeamsStatSheet_[14][0])
        self.assertEquals("Opponent AWAL", allTimeTeamsStatSheet_[15][0])
        self.assertEquals("Opponent AWAL Per Game", allTimeTeamsStatSheet_[16][0])
        self.assertEquals("Smart Wins", allTimeTeamsStatSheet_[17][0])
        self.assertEquals("Smart Wins Per Game", allTimeTeamsStatSheet_[18][0])
        self.assertEquals("Opponent Smart Wins", allTimeTeamsStatSheet_[19][0])
        self.assertEquals("Opponent Smart Wins Per Game", allTimeTeamsStatSheet_[20][0])
        self.assertEquals("Points Scored", allTimeTeamsStatSheet_[21][0])
        self.assertEquals("Points Scored Per Game", allTimeTeamsStatSheet_[22][0])
        self.assertEquals("Opponent Points Scored", allTimeTeamsStatSheet_[23][0])
        self.assertEquals("Opponent Points Scored Per Game", allTimeTeamsStatSheet_[24][0])
        self.assertEquals("Scoring Share", allTimeTeamsStatSheet_[25][0])
        self.assertEquals("Opponent Scoring Share", allTimeTeamsStatSheet_[26][0])
        self.assertEquals("Max Scoring Share", allTimeTeamsStatSheet_[27][0])
        self.assertEquals("Min Scoring Share", allTimeTeamsStatSheet_[28][0])
        self.assertEquals("Max Score", allTimeTeamsStatSheet_[29][0])
        self.assertEquals("Min Score", allTimeTeamsStatSheet_[30][0])
        self.assertEquals("Scoring Standard Deviation", allTimeTeamsStatSheet_[31][0])
        self.assertEquals("Plus/Minus", allTimeTeamsStatSheet_[32][0])
        self.assertEquals("Team Score", allTimeTeamsStatSheet_[33][0])
        self.assertEquals("Team Success", allTimeTeamsStatSheet_[34][0])
        self.assertEquals("Team Luck", allTimeTeamsStatSheet_[35][0])
