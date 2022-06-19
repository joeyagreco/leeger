from src.leeger.decorator.validate.validators import validateYear
from src.leeger.enum.MatchupType import MatchupType
from src.leeger.exception.InvalidFilterException import InvalidFilterException
from src.leeger.model.Year import Year
from src.leeger.model.YearFilters import YearFilters
from src.leeger.util.Deci import Deci
from src.leeger.util.YearNavigator import YearNavigator


class YearCalculator:
    """
    Should be inherited by all stat calculators that calculate stats for a Year.
    """

    @classmethod
    @validateYear
    def getFilters(cls, year: Year, **kwargs) -> YearFilters:
        onlyChampionship = kwargs.pop("onlyChampionship", False)
        onlyPostSeason = kwargs.pop("onlyPostSeason", False)
        onlyRegularSeason = kwargs.pop("onlyRegularSeason", False)
        weekNumberStart = kwargs.pop("weekNumberStart", year.weeks[0].weekNumber)
        weekNumberEnd = kwargs.pop("weekNumberEnd", year.weeks[-1].weekNumber)

        if onlyChampionship:
            includeMatchupTypes = [
                MatchupType.CHAMPIONSHIP
            ]
        elif onlyPostSeason:
            includeMatchupTypes = [
                MatchupType.PLAYOFF,
                MatchupType.CHAMPIONSHIP
            ]
        elif onlyRegularSeason:
            includeMatchupTypes = [
                MatchupType.REGULAR_SEASON
            ]
        else:
            includeMatchupTypes = [
                MatchupType.REGULAR_SEASON,
                MatchupType.PLAYOFF,
                MatchupType.CHAMPIONSHIP
            ]

        ####################
        # validate filters #
        ####################
        # type checks
        if type(onlyChampionship) != bool:
            raise InvalidFilterException("'onlyChampionship' must be type 'bool'")
        if type(onlyPostSeason) != bool:
            raise InvalidFilterException("'onlyPostSeason' must be type 'bool'")
        if type(onlyRegularSeason) != bool:
            raise InvalidFilterException("'onlyRegularSeason' must be type 'bool'")
        if type(weekNumberStart) != int:
            raise InvalidFilterException("'weekNumberStart' must be type 'int'")
        if type(weekNumberEnd) != int:
            raise InvalidFilterException("'weekNumberEnd' must be type 'int'")

        # logic checks
        if [onlyChampionship, onlyPostSeason, onlyRegularSeason].count(True) > 1:
            raise InvalidFilterException(
                "Only one of 'onlyChampionship', 'onlyPostSeason', 'onlyRegularSeason' can be True")
        if weekNumberStart < 1:
            raise InvalidFilterException("'weekNumberStart' cannot be less than 1.")
        if weekNumberEnd > len(year.weeks):
            raise InvalidFilterException("'weekNumberEnd' cannot be greater than the number of weeks in the year.")
        if weekNumberStart > weekNumberEnd:
            raise InvalidFilterException("'weekNumberEnd' cannot be greater than 'weekNumberStart'.")

        return YearFilters(weekNumberStart=weekNumberStart, weekNumberEnd=weekNumberEnd,
                           includeMatchupTypes=includeMatchupTypes)

    @classmethod
    @validateYear
    def getNumberOfGamesPlayed(cls, year: Year, **kwargs) -> dict[str, Deci]:
        """
        Returns the number of games played for each team in the given Year.

        Example response:
            {
            "someTeamId": Deci("4"),
            "someOtherTeamId": Deci("4"),
            "yetAnotherTeamId": Deci("5"),
            ...
            }
        """
        filters = cls.getFilters(year, **kwargs)

        teamIdAndNumberOfGamesPlayed = dict()
        allTeamIds = YearNavigator.getAllTeamIds(year)
        for teamId in allTeamIds:
            teamIdAndNumberOfGamesPlayed[teamId] = Deci(0)

        for i in range(filters.weekNumberStart - 1, filters.weekNumberEnd):
            week = year.weeks[i]
            for matchup in week.matchups:
                if matchup.matchupType in filters.includeMatchupTypes:
                    teamIdAndNumberOfGamesPlayed[matchup.teamAId] += Deci(1)
                    teamIdAndNumberOfGamesPlayed[matchup.teamBId] += Deci(1)
        return teamIdAndNumberOfGamesPlayed

    @classmethod
    @validateYear
    def getNumberOfValidTeamsInWeek(cls, year: Year, weekNumber: int, **kwargs) -> int:
        """
        Returns the number of valid teams that are playing in the given week.
        A valid team is a team that is NOT in a matchup that is marked to be ignored and also matches the given filters.
        """
        filters = cls.getFilters(year, **kwargs)

        numberOfValidTeams = 0
        for week in year.weeks:
            if week.weekNumber == weekNumber:
                for matchup in week.matchups:
                    if matchup.matchupType in filters.includeMatchupTypes:
                        numberOfValidTeams += 2
        return numberOfValidTeams
