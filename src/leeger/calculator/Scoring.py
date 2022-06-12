from src.leeger.calculator.parent.YearCalculator import YearCalculator
from src.leeger.decorator.validate.validators import validateYear
from src.leeger.model.Year import Year
from src.leeger.util.Deci import Deci
from src.leeger.util.YearNavigator import YearNavigator


class Scoring(YearCalculator):
    """
    Used to calculate all scoring outcomes.
    """

    @classmethod
    @validateYear
    def getPointsScored(cls, year: Year, **kwargs) -> dict[str, Deci]:
        """
        Returns the number of Points Scored for each team in the given Year.

        Example response:
            {
            "someTeamId": Deci("1009.7"),
            "someOtherTeamId": Deci("1412.2"),
            "yetAnotherTeamId": Deci("1227.1"),
            ...
            }
        """
        cls.loadFilters(year, validateYear=False, **kwargs)

        teamIdAndPointsScored = dict()
        for teamId in YearNavigator.getAllTeamIds(year):
            teamIdAndPointsScored[teamId] = Deci(0)

        for i in range(cls._weekNumberStart - 1, cls._weekNumberEnd):
            week = year.weeks[i]
            if (week.isPlayoffWeek and not cls._onlyRegularSeason) or (
                    not week.isPlayoffWeek and not cls._onlyPostSeason):
                for matchup in week.matchups:
                    teamIdAndPointsScored[matchup.teamAId] += Deci(matchup.teamAScore)
                    teamIdAndPointsScored[matchup.teamBId] += Deci(matchup.teamBScore)

        return teamIdAndPointsScored

    @classmethod
    @validateYear
    def getPointsScoredPerGame(cls, year: Year, **kwargs) -> dict[str, Deci]:
        """
        Returns the number of Points Scored per game for each team in the given Year.

        Example response:
            {
            "someTeamId": Deci("100.7"),
            "someOtherTeamId": Deci("141.2"),
            "yetAnotherTeamId": Deci("122.1"),
            ...
            }
        """
        cls.loadFilters(year, validateYear=False, **kwargs)

        teamIdAndPointsScored = cls.getPointsScored(year, **kwargs)
        teamIdAndNumberOfGamesPlayed = cls.getNumberOfGamesPlayed(year, **kwargs)

        teamIdAndPointsScoredPerGame = dict()
        allTeamIds = YearNavigator.getAllTeamIds(year)
        for teamId in allTeamIds:
            teamIdAndPointsScoredPerGame[teamId] = teamIdAndPointsScored[teamId] / teamIdAndNumberOfGamesPlayed[teamId]

        return teamIdAndPointsScoredPerGame

    @classmethod
    @validateYear
    def getOpponentPointsScored(cls, year: Year, **kwargs) -> dict[str, Deci]:
        """
        Returns the number of Opponent Points Scored for each team in the given Year.

        Example response:
            {
            "someTeamId": Deci("1009.7"),
            "someOtherTeamId": Deci("1412.2"),
            "yetAnotherTeamId": Deci("1227.1"),
            ...
            }
        """
        cls.loadFilters(year, validateYear=False, **kwargs)

        teamIdAndOpponentPointsScored = dict()
        for teamId in YearNavigator.getAllTeamIds(year):
            teamIdAndOpponentPointsScored[teamId] = Deci(0)

        for i in range(cls._weekNumberStart - 1, cls._weekNumberEnd):
            week = year.weeks[i]
            if (week.isPlayoffWeek and not cls._onlyRegularSeason) or (
                    not week.isPlayoffWeek and not cls._onlyPostSeason):
                for matchup in week.matchups:
                    teamIdAndOpponentPointsScored[matchup.teamAId] += Deci(matchup.teamBScore)
                    teamIdAndOpponentPointsScored[matchup.teamBId] += Deci(matchup.teamAScore)

        return teamIdAndOpponentPointsScored

    @classmethod
    @validateYear
    def getOpponentPointsScoredPerGame(cls, year: Year, **kwargs) -> dict[str, Deci]:
        """
        Returns the number of Opponent Points Scored per game for each team in the given Year.

        Example response:
            {
            "someTeamId": Deci("100.7"),
            "someOtherTeamId": Deci("141.2"),
            "yetAnotherTeamId": Deci("122.1"),
            ...
            }
        """
        cls.loadFilters(year, validateYear=False, **kwargs)

        teamIdAndOpponentPointsScored = cls.getOpponentPointsScored(year, **kwargs)
        teamIdAndNumberOfGamesPlayed = cls.getNumberOfGamesPlayed(year, **kwargs)

        teamIdAndOpponentPointsScoredPerGame = dict()
        allTeamIds = YearNavigator.getAllTeamIds(year)
        for teamId in allTeamIds:
            teamIdAndOpponentPointsScoredPerGame[teamId] = teamIdAndOpponentPointsScored[teamId] / \
                                                           teamIdAndNumberOfGamesPlayed[teamId]

        return teamIdAndOpponentPointsScoredPerGame

    @classmethod
    @validateYear
    def getScoringShare(cls, year: Year, **kwargs) -> dict[str, Deci]:
        """
        Scoring Share is used to show what percentage of league scoring a team was responsible for.
        Scoring Share = ((ΣA) / (ΣB)) * 100
        WHERE:
        A = All scores by a Team in a Year
        B = All scores by all Teams in a Year

        Returns the Scoring Share for each team in the given Year.

        Example response:
            {
            "someTeamId": Deci("10.7"),
            "someOtherTeamId": Deci("14.2"),
            "yetAnotherTeamId": Deci("12.1"),
            ...
            }
        """
        cls.loadFilters(year, validateYear=False, **kwargs)

        teamIdAndPointsScored = cls.getPointsScored(year, **kwargs)
        totalPointsScoredInYear = sum(teamIdAndPointsScored.values())
        teamIdAndScoringShare = dict()
        for teamId in YearNavigator.getAllTeamIds(year):
            teamIdAndScoringShare[teamId] = (teamIdAndPointsScored[teamId] / totalPointsScoredInYear) * Deci(100)

        return teamIdAndScoringShare

    @classmethod
    @validateYear
    def getOpponentScoringShare(cls, year: Year, **kwargs) -> dict[str, Deci]:
        """
        Opponent Scoring Share is used to show what percentage of league scoring a team's opponent was responsible for.
        Opponent Scoring Share = ((ΣA) / (ΣB)) * 100
        WHERE:
        A = All scores by a Team's opponent in a Year
        B = All scores by all Teams in a Year

        Returns the Opponent Scoring Share for each team in the given Year.

        Example response:
            {
            "someTeamId": Deci("10.7"),
            "someOtherTeamId": Deci("14.2"),
            "yetAnotherTeamId": Deci("12.1"),
            ...
            }
        """
        cls.loadFilters(year, validateYear=False, **kwargs)

        teamIdAndOpponentPointsScored = cls.getOpponentPointsScored(year, **kwargs)
        totalPointsScoredInYear = sum(teamIdAndOpponentPointsScored.values())
        teamIdAndOpponentScoringShare = dict()
        for teamId in YearNavigator.getAllTeamIds(year):
            teamIdAndOpponentScoringShare[teamId] = (teamIdAndOpponentPointsScored[
                                                         teamId] / totalPointsScoredInYear) * Deci(100)

        return teamIdAndOpponentScoringShare
