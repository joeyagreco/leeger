from src.leeger.calculator.parent.YearCalculator import YearCalculator
from src.leeger.decorator.validate.validators import validateYear
from src.leeger.model.Year import Year
from src.leeger.util.Deci import Deci
from src.leeger.util.YearNavigator import YearNavigator


class PointsScoredCalculator(YearCalculator):
    """
    Used to calculate all points scored.
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
        filters = cls.getFilters(year, validateYear=False, **kwargs)

        teamIdAndPointsScored = dict()
        for teamId in YearNavigator.getAllTeamIds(year):
            teamIdAndPointsScored[teamId] = Deci(0)

        for i in range(filters.weekNumberStart - 1, filters.weekNumberEnd):
            week = year.weeks[i]
            for matchup in week.matchups:
                if matchup.matchupType in filters.includeMatchupTypes:
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
        filters = cls.getFilters(year, validateYear=False, **kwargs)

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
        Returns the number of opponent Points Scored for each team in the given Year.

        Example response:
            {
            "someTeamId": Deci("1009.7"),
            "someOtherTeamId": Deci("1412.2"),
            "yetAnotherTeamId": Deci("1227.1"),
            ...
            }
        """
        filters = cls.getFilters(year, validateYear=False, **kwargs)

        teamIdAndOpponentPointsScored = dict()
        for teamId in YearNavigator.getAllTeamIds(year):
            teamIdAndOpponentPointsScored[teamId] = Deci(0)

        for i in range(filters.weekNumberStart - 1, filters.weekNumberEnd):
            week = year.weeks[i]
            for matchup in week.matchups:
                if matchup.matchupType in filters.includeMatchupTypes:
                    teamIdAndOpponentPointsScored[matchup.teamAId] += Deci(matchup.teamBScore)
                    teamIdAndOpponentPointsScored[matchup.teamBId] += Deci(matchup.teamAScore)

        return teamIdAndOpponentPointsScored

    @classmethod
    @validateYear
    def getOpponentPointsScoredPerGame(cls, year: Year, **kwargs) -> dict[str, Deci]:
        """
        Returns the number of opponent Points Scored per game for each team in the given Year.

        Example response:
            {
            "someTeamId": Deci("100.7"),
            "someOtherTeamId": Deci("141.2"),
            "yetAnotherTeamId": Deci("122.1"),
            ...
            }
        """
        filters = cls.getFilters(year, validateYear=False, **kwargs)

        teamIdAndOpponentPointsScored = cls.getOpponentPointsScored(year, **kwargs)
        teamIdAndNumberOfGamesPlayed = cls.getNumberOfGamesPlayed(year, **kwargs)

        teamIdAndOpponentPointsScoredPerGame = dict()
        allTeamIds = YearNavigator.getAllTeamIds(year)
        for teamId in allTeamIds:
            teamIdAndOpponentPointsScoredPerGame[teamId] = teamIdAndOpponentPointsScored[teamId] / \
                                                           teamIdAndNumberOfGamesPlayed[teamId]

        return teamIdAndOpponentPointsScoredPerGame
