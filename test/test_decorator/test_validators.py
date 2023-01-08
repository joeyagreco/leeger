import unittest

from leeger.decorator.validators import validateLeague, validateYear, validateWeek, validateMatchup
from leeger.enum import MatchupType
from leeger.model.league import Matchup
from leeger.model.league.League import League
from leeger.model.league.Week import Week
from leeger.model.league.Year import Year
from test.helper.prototypes import getNDefaultOwnersAndTeams


class TestValidators(unittest.TestCase):

    @validateLeague
    def dummyLeagueFunction(self, league: League, **kwargs):
        """
        This is used to represent any function that can be wrapped by @validateLeague.
        """
        ...

    @validateYear
    def dummyYearFunction(self, year: Year, **kwargs):
        """
        This is used to represent any function that can be wrapped by @validateYear.
        """
        ...

    @validateWeek
    def dummyWeekFunction(self, week: Week, **kwargs):
        """
        This is used to represent any function that can be wrapped by @validateWeek.
        """
        ...

    @validateMatchup
    def dummyMatchupFunction(self, week: Week, **kwargs):
        """
        This is used to represent any function that can be wrapped by @validateMatchup.
        """
        ...

    # Validate League

    def test_validateLeague_noLeagueParameterGiven_raisesException(self):
        with self.assertRaises(ValueError) as context:
            self.dummyLeagueFunction(None)
        self.assertEqual("No valid League argument given to validate.", str(context.exception))

    def test_validateLeague_validateLeagueKwargIsFalse_doesntRunValidation(self):
        self.dummyLeagueFunction(None, validate=False)

    def test_validateLeague_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(2)
        matchup = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.2,
                          matchupType=MatchupType.REGULAR_SEASON)
        week = Week(weekNumber=1, matchups=[matchup])
        year = Year(yearNumber=2000, teams=teams, weeks=[week])
        league = League(name="LEAGUE", owners=owners, years=[year])
        self.dummyLeagueFunction(league)

    # Validate Year

    def test_validateYear_noYearParameterGiven_raisesException(self):
        with self.assertRaises(ValueError) as context:
            self.dummyYearFunction(None)
        self.assertEqual("No valid Year argument given to validate.", str(context.exception))

    def test_validateYear_validateYearKwargIsFalse_doesntRunValidation(self):
        self.dummyYearFunction(None, validate=False)

    def test_validateYear_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(2)
        matchup = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.2,
                          matchupType=MatchupType.REGULAR_SEASON)
        week = Week(weekNumber=1, matchups=[matchup])
        year = Year(yearNumber=2000, teams=teams, weeks=[week])
        self.dummyYearFunction(year)

    # Validate Week

    def test_validateWeek_noWeekParameterGiven_raisesException(self):
        with self.assertRaises(ValueError) as context:
            self.dummyWeekFunction(None)
        self.assertEqual("No valid Week argument given to validate.", str(context.exception))

    def test_validateWeek_validateWeekKwargIsFalse_doesntRunValidation(self):
        self.dummyWeekFunction(None, validate=False)

    def test_validateWeek_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(2)
        matchup = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.2,
                          matchupType=MatchupType.REGULAR_SEASON)
        week = Week(weekNumber=1, matchups=[matchup])
        self.dummyWeekFunction(week)

    # Validate Matchup

    def test_validateMatchup_noMatchupParameterGiven_raisesException(self):
        with self.assertRaises(ValueError) as context:
            self.dummyMatchupFunction(None)
        self.assertEqual("No valid Matchup argument given to validate.", str(context.exception))

    def test_validateMatchup_validateMatchupKwargIsFalse_doesntRunValidation(self):
        self.dummyMatchupFunction(None, validate=False)

    def test_validateMatchup_happyPath(self):
        owners, teams = getNDefaultOwnersAndTeams(2)
        matchup = Matchup(teamAId=teams[0].id, teamBId=teams[1].id, teamAScore=1.1, teamBScore=2.2,
                          matchupType=MatchupType.REGULAR_SEASON)
        self.dummyMatchupFunction(matchup)
