from decimal import Decimal

from src.leeger.calculator.BasicGameOutcome import BasicGameOutcome
from src.leeger.calculator.parent.YearCalculator import YearCalculator
from src.leeger.decorator.validate.validators import validateYear
from src.leeger.model.Year import Year
from src.leeger.util.WeekNavigator import WeekNavigator
from src.leeger.util.YearNavigator import YearNavigator


class AdvancedGameOutcome(YearCalculator):
    """
    Used to calculate all advanced game outcomes.
    """

    @classmethod
    @validateYear
    def getWAL(cls, year: Year, **kwargs) -> dict[str, Decimal]:
        """
        WAL is "Wins Against the League"
        Formula: (Number of Wins * 1) + (Number of Ties * 0.5)
        Returns the number of Wins Against the League for each team in the given Year.

        Example response:
            {
            "someTeamId": 8.7,
            "someOtherTeamId": 11.2,
            "yetAnotherTeamId": 7.1,
            ...
            }
        """
        cls.loadFilters(year, validateYear=False, **kwargs)

        teamIdAndWAL = dict()
        teamIdAndWins = BasicGameOutcome.getWins(year, **kwargs)
        teamIdAndTies = BasicGameOutcome.getTies(year, **kwargs)

        for teamId in YearNavigator.getAllTeamIds(year):
            teamIdAndWAL[teamId] = teamIdAndWins[teamId] + (Decimal(0.5) * Decimal(teamIdAndTies[teamId]))

        return teamIdAndWAL

    @classmethod
    @validateYear
    def getAWAL(cls, year: Year, **kwargs) -> dict[str, Decimal]:
        """
        AWAL stands for Adjusted Wins Against the League.
        It is exactly that, an adjustment added to the Wins Against the League (or WAL) of a team.
        In simple terms, this stat more accurately represents how many WAL any given team should have.
        i.e. A team with 6.3 AWAL "deserves" 6.3 WAL.

        AWAL = W * (1/L) + T * (0.5/L)
        Where:
        W = Teams outscored in a week
        T = Teams tied in a week
        L = Opponents in a week (usually league size - 1)

        Returns the number of Adjusted Wins Against the League for each team in the given Year.

        Example response:
            {
            "someTeamId": 8.7,
            "someOtherTeamId": 11.2,
            "yetAnotherTeamId": 7.1,
            ...
            }
        """
        cls.loadFilters(year, validateYear=False, **kwargs)

        teamIdAndAWAL = dict()
        allTeamIds = YearNavigator.getAllTeamIds(year)
        for teamId in allTeamIds:
            teamIdAndAWAL[teamId] = Decimal(0)

        for i in range(cls._weekNumberStart - 1, cls._weekNumberEnd):
            week = year.weeks[i]
            if (week.isPlayoffWeek and not cls._onlyRegularSeason) or (
                    not week.isPlayoffWeek and not cls._onlyPostSeason):
                opponentsInWeek = (len(week.matchups) * 2) - 1
                teamsOutscored = dict()
                teamsTied = dict()
                for teamId in allTeamIds:
                    teamsOutscored[teamId] = 0
                    teamsTied[teamId] = 0
                allTeamIdsAndScoresForWeek = WeekNavigator.getTeamIdsAndScores(week)
                allScores = allTeamIdsAndScoresForWeek.values()

                for teamId in allTeamIdsAndScoresForWeek.keys():
                    teamsOutscored[teamId] = 0
                    teamsTied[teamId] = 0
                    score = allTeamIdsAndScoresForWeek[teamId]
                    for s in allScores:
                        if score > s:
                            teamsOutscored[teamId] += 1
                        if score == s:
                            teamsTied[teamId] += 1
                    # remove 1 from the teamsTied tracker since we will always find a tie for this teams score in the list of all scores in the week
                    teamsTied[teamId] -= 1
                    # calculate the AWAL for each team for this week
                    teamIdAndAWAL[teamId] += (
                            (Decimal(teamsOutscored[teamId])
                             * (Decimal(1) / Decimal(opponentsInWeek)))
                            + (Decimal(teamsTied[teamId])
                               * (Decimal(0.5) / Decimal(opponentsInWeek))))

        return teamIdAndAWAL
