from src.leeger.decorator.validate.validators import validateYear
from src.leeger.model.Year import Year
from src.leeger.util.YearNavigator import YearNavigator


class YearStats:
    @classmethod
    @validateYear
    def getWins(cls, year: Year, **kwargs) -> dict[str, int]:
        """
        Returns the number of wins for each team in the given Year.

        Example response:
            {
            "someTeamId": 8,
            "someOtherTeamId": 11,
            "yetAnotherTeamId": 7,
            ...
            }
        """
        onlyPostSeason = kwargs.pop("onlyPostSeason", False)  # only include post season wins
        onlyRegularSeason = kwargs.pop("onlyRegularSeason", False)  # only include regular season wins
        weekNumberStart = kwargs.pop("weekNumberStart",
                                     year.weeks[0].weekNumber)  # week to start the calculations at (inclusive)
        weekNumberEnd = kwargs.pop("weekNumberEnd",
                                   year.weeks[-1].weekNumber)  # week to end the calculations at (inclusive)

        teamIdAndWins = dict()
        for teamId in YearNavigator.getAllTeamIds(year):
            teamIdAndWins[teamId] = 0

        for i in range(weekNumberStart - 1, weekNumberEnd):
            week = year.weeks[i]
            if (week.isPlayoffWeek and not onlyRegularSeason) or (not week.isPlayoffWeek and not onlyPostSeason):
                for matchup in week.matchups:
                    # team A won
                    if (matchup.teamAScore > matchup.teamBScore) or (
                            matchup.teamAScore == matchup.teamBScore and matchup.teamAHasTiebreaker):
                        teamIdAndWins[matchup.teamAId] += 1
                    # team B won
                    elif (matchup.teamBScore > matchup.teamAScore) or (
                            matchup.teamAScore == matchup.teamBScore and matchup.teamBHasTiebreaker):
                        teamIdAndWins[matchup.teamBId] += 1
        return teamIdAndWins

    @classmethod
    @validateYear
    def getLosses(cls, year: Year, **kwargs) -> dict[str, int]:
        """
        Returns the number of losses for each team in the given Year.

        Example response:
            {
            "someTeamId": 8,
            "someOtherTeamId": 11,
            "yetAnotherTeamId": 7,
            ...
            }
        """
        onlyPostSeason = kwargs.pop("onlyPostSeason", False)  # only include post season losses
        onlyRegularSeason = kwargs.pop("onlyRegularSeason", False)  # only include regular season losses
        weekNumberStart = kwargs.pop("weekNumberStart",
                                     year.weeks[0].weekNumber)  # week to start the calculations at (inclusive)
        weekNumberEnd = kwargs.pop("weekNumberEnd",
                                   year.weeks[-1].weekNumber)  # week to end the calculations at (inclusive)

        teamIdAndLosses = dict()
        for teamId in YearNavigator.getAllTeamIds(year):
            teamIdAndLosses[teamId] = 0

        for i in range(weekNumberStart - 1, weekNumberEnd):
            week = year.weeks[i]
            if (week.isPlayoffWeek and not onlyRegularSeason) or (not week.isPlayoffWeek and not onlyPostSeason):
                for matchup in week.matchups:
                    # team A lost
                    if (matchup.teamAScore < matchup.teamBScore) or (
                            matchup.teamAScore == matchup.teamBScore and matchup.teamBHasTiebreaker):
                        teamIdAndLosses[matchup.teamAId] += 1
                    # team B lost
                    elif (matchup.teamBScore < matchup.teamAScore) or (
                            matchup.teamAScore == matchup.teamBScore and matchup.teamAHasTiebreaker):
                        teamIdAndLosses[matchup.teamBId] += 1
        return teamIdAndLosses
