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

        matchup = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        week = Week(weekNumber=1, matchups=[matchup])
        year = Year(yearNumber=2000, teams=teams, weeks=[week])

        league = League(name="TEST", owners=owners, years=[year])

        allTimeTeamsStatSheet_ = allTimeTeamsStatSheet(league)

        self.assertEqual(33, len(allTimeTeamsStatSheet_))
        for tup in allTimeTeamsStatSheet_:
            self.assertIsInstance(tup, tuple)
        self.assertEqual("Team", allTimeTeamsStatSheet_[0][0])
        self.assertEqual("Owner", allTimeTeamsStatSheet_[1][0])
        self.assertEqual("Year", allTimeTeamsStatSheet_[2][0])
        self.assertEqual("Games Played", allTimeTeamsStatSheet_[3][0])
        self.assertEqual("Wins", allTimeTeamsStatSheet_[4][0])
        self.assertEqual("Losses", allTimeTeamsStatSheet_[5][0])
        self.assertEqual("Ties", allTimeTeamsStatSheet_[6][0])
        self.assertEqual("Win Percentage", allTimeTeamsStatSheet_[7][0])
        self.assertEqual("WAL", allTimeTeamsStatSheet_[8][0])
        self.assertEqual("WAL Per Game", allTimeTeamsStatSheet_[9][0])
        self.assertEqual("AWAL", allTimeTeamsStatSheet_[10][0])
        self.assertEqual("AWAL Per Game", allTimeTeamsStatSheet_[11][0])
        self.assertEqual("Opponent AWAL", allTimeTeamsStatSheet_[12][0])
        self.assertEqual("Opponent AWAL Per Game",
                         allTimeTeamsStatSheet_[13][0])
        self.assertEqual("Smart Wins", allTimeTeamsStatSheet_[14][0])
        self.assertEqual("Smart Wins Per Game", allTimeTeamsStatSheet_[15][0])
        self.assertEqual("Opponent Smart Wins", allTimeTeamsStatSheet_[16][0])
        self.assertEqual("Opponent Smart Wins Per Game",
                         allTimeTeamsStatSheet_[17][0])
        self.assertEqual("Points Scored", allTimeTeamsStatSheet_[18][0])
        self.assertEqual("Points Scored Per Game",
                         allTimeTeamsStatSheet_[19][0])
        self.assertEqual("Opponent Points Scored",
                         allTimeTeamsStatSheet_[20][0])
        self.assertEqual("Opponent Points Scored Per Game",
                         allTimeTeamsStatSheet_[21][0])
        self.assertEqual("Scoring Share", allTimeTeamsStatSheet_[22][0])
        self.assertEqual("Opponent Scoring Share",
                         allTimeTeamsStatSheet_[23][0])
        self.assertEqual("Max Scoring Share", allTimeTeamsStatSheet_[24][0])
        self.assertEqual("Min Scoring Share", allTimeTeamsStatSheet_[25][0])
        self.assertEqual("Max Score", allTimeTeamsStatSheet_[26][0])
        self.assertEqual("Min Score", allTimeTeamsStatSheet_[27][0])
        self.assertEqual("Scoring Standard Deviation",
                         allTimeTeamsStatSheet_[28][0])
        self.assertEqual("Plus/Minus", allTimeTeamsStatSheet_[29][0])
        self.assertEqual("Team Score", allTimeTeamsStatSheet_[30][0])
        self.assertEqual("Team Success", allTimeTeamsStatSheet_[31][0])
        self.assertEqual("Team Luck", allTimeTeamsStatSheet_[32][0])

    def test_allTimeTeamsStatSheet_leagueMedianGamesIsTrueInAnyYearSettings(self):
        owners, teams = getNDefaultOwnersAndTeams(2)

        matchup = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        week = Week(weekNumber=1, matchups=[matchup])
        yearSettings = YearSettings(leagueMedianGames=True)
        year1 = Year(yearNumber=2000, teams=teams, weeks=[
                     week], yearSettings=yearSettings)

        _, teams = getNDefaultOwnersAndTeams(2)
        teams[0].ownerId = owners[0].id
        teams[1].ownerId = owners[1].id

        matchup = Matchup(
            teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1, teamBScore=2)
        week = Week(weekNumber=1, matchups=[matchup])
        year2 = Year(yearNumber=2001, teams=teams, weeks=[week])

        league = League(name="TEST", owners=owners, years=[year1, year2])

        allTimeTeamsStatSheet_ = allTimeTeamsStatSheet(league)

        self.assertEqual(36, len(allTimeTeamsStatSheet_))
        for tup in allTimeTeamsStatSheet_:
            self.assertIsInstance(tup, tuple)
        self.assertEqual("Team", allTimeTeamsStatSheet_[0][0])
        self.assertEqual("Owner", allTimeTeamsStatSheet_[1][0])
        self.assertEqual("Year", allTimeTeamsStatSheet_[2][0])
        self.assertEqual("Games Played", allTimeTeamsStatSheet_[3][0])
        self.assertEqual("Total Games", allTimeTeamsStatSheet_[4][0])
        self.assertEqual("Wins", allTimeTeamsStatSheet_[5][0])
        self.assertEqual("Losses", allTimeTeamsStatSheet_[6][0])
        self.assertEqual("League Median Wins", allTimeTeamsStatSheet_[7][0])
        self.assertEqual("Opponent League Median Wins",
                         allTimeTeamsStatSheet_[8][0])
        self.assertEqual("Ties", allTimeTeamsStatSheet_[9][0])
        self.assertEqual("Win Percentage", allTimeTeamsStatSheet_[10][0])
        self.assertEqual("WAL", allTimeTeamsStatSheet_[11][0])
        self.assertEqual("WAL Per Game", allTimeTeamsStatSheet_[12][0])
        self.assertEqual("AWAL", allTimeTeamsStatSheet_[13][0])
        self.assertEqual("AWAL Per Game", allTimeTeamsStatSheet_[14][0])
        self.assertEqual("Opponent AWAL", allTimeTeamsStatSheet_[15][0])
        self.assertEqual("Opponent AWAL Per Game",
                         allTimeTeamsStatSheet_[16][0])
        self.assertEqual("Smart Wins", allTimeTeamsStatSheet_[17][0])
        self.assertEqual("Smart Wins Per Game", allTimeTeamsStatSheet_[18][0])
        self.assertEqual("Opponent Smart Wins", allTimeTeamsStatSheet_[19][0])
        self.assertEqual("Opponent Smart Wins Per Game",
                         allTimeTeamsStatSheet_[20][0])
        self.assertEqual("Points Scored", allTimeTeamsStatSheet_[21][0])
        self.assertEqual("Points Scored Per Game",
                         allTimeTeamsStatSheet_[22][0])
        self.assertEqual("Opponent Points Scored",
                         allTimeTeamsStatSheet_[23][0])
        self.assertEqual("Opponent Points Scored Per Game",
                         allTimeTeamsStatSheet_[24][0])
        self.assertEqual("Scoring Share", allTimeTeamsStatSheet_[25][0])
        self.assertEqual("Opponent Scoring Share",
                         allTimeTeamsStatSheet_[26][0])
        self.assertEqual("Max Scoring Share", allTimeTeamsStatSheet_[27][0])
        self.assertEqual("Min Scoring Share", allTimeTeamsStatSheet_[28][0])
        self.assertEqual("Max Score", allTimeTeamsStatSheet_[29][0])
        self.assertEqual("Min Score", allTimeTeamsStatSheet_[30][0])
        self.assertEqual("Scoring Standard Deviation",
                         allTimeTeamsStatSheet_[31][0])
        self.assertEqual("Plus/Minus", allTimeTeamsStatSheet_[32][0])
        self.assertEqual("Team Score", allTimeTeamsStatSheet_[33][0])
        self.assertEqual("Team Success", allTimeTeamsStatSheet_[34][0])
        self.assertEqual("Team Luck", allTimeTeamsStatSheet_[35][0])
