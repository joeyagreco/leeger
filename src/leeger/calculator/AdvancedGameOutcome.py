from src.leeger.calculator.BasicGameOutcome import BasicGameOutcome
from src.leeger.calculator.parent.YearCalculator import YearCalculator
from src.leeger.decorator.validate.validators import validateYear
from src.leeger.model.Year import Year
from src.leeger.util.Deci import Deci
from src.leeger.util.WeekNavigator import WeekNavigator
from src.leeger.util.YearNavigator import YearNavigator


class AdvancedGameOutcome(YearCalculator):
    """
    Used to calculate all advanced game outcomes.
    """

    @classmethod
    @validateYear
    def getWAL(cls, year: Year, **kwargs) -> dict[str, Deci]:
        """
        WAL is "Wins Against the League"
        Formula: (Number of Wins * 1) + (Number of Ties * 0.5)
        Returns the number of Wins Against the League for each team in the given Year.

        Example response:
            {
            "someTeamId": Deci("8.7"),
            "someOtherTeamId": Deci("11.2"),
            "yetAnotherTeamId": Deci("7.1"),
            ...
            }
        """
        cls.loadFilters(year, validateYear=False, **kwargs)

        teamIdAndWAL = dict()
        teamIdAndWins = BasicGameOutcome.getWins(year, **kwargs)
        teamIdAndTies = BasicGameOutcome.getTies(year, **kwargs)

        for teamId in YearNavigator.getAllTeamIds(year):
            teamIdAndWAL[teamId] = teamIdAndWins[teamId] + (Deci(0.5) * Deci(teamIdAndTies[teamId]))

        return teamIdAndWAL

    @classmethod
    @validateYear
    def getAWAL(cls, year: Year, **kwargs) -> dict[str, Deci]:
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
            "someTeamId": Deci("8.7"),
            "someOtherTeamId": Deci("11.2"),
            "yetAnotherTeamId": Deci("7.1"),
            ...
            }
        """
        cls.loadFilters(year, validateYear=False, **kwargs)

        teamIdAndAWAL = dict()
        allTeamIds = YearNavigator.getAllTeamIds(year)
        for teamId in allTeamIds:
            teamIdAndAWAL[teamId] = Deci(0)

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
                            (Deci(teamsOutscored[teamId])
                             * (Deci(1) / Deci(opponentsInWeek)))
                            + (Deci(teamsTied[teamId])
                               * (Deci(0.5) / Deci(opponentsInWeek))))

        return teamIdAndAWAL

    @classmethod
    @validateYear
    def getAWALPerGame(cls, year: Year, **kwargs) -> dict[str, Deci]:
        """
        Returns the number of Adjusted Wins Against the League per game for each team in the given Year.

        Example response:
            {
            "someTeamId": Deci("8.7"),
            "someOtherTeamId": Deci("11.2"),
            "yetAnotherTeamId": Deci("7.1"),
            ...
            }
        """
        cls.loadFilters(year, validateYear=False, **kwargs)

        teamIdAndAWAL = AdvancedGameOutcome.getAWAL(year, **kwargs)
        teamIdAndNumberOfGamesPlayed = cls.getNumberOfGamesPlayed(year, **kwargs)

        teamIdAndAwalPerGame = dict()
        allTeamIds = YearNavigator.getAllTeamIds(year)
        for teamId in allTeamIds:
            teamIdAndAwalPerGame[teamId] = teamIdAndAWAL[teamId] / teamIdAndNumberOfGamesPlayed[teamId]

        return teamIdAndAwalPerGame

    @classmethod
    @validateYear
    def getSmartWins(cls, year: Year, **kwargs) -> dict[str, Deci]:
        """
        Smart Wins show how many wins a team would have if it played against every score in a given collection.
        In this case, the collection is every score in the given Year.
        Smart Wins = Σ((W + (T/2)) / S)
        WHERE:
        W = Total scores in the Year beat
        T = Total scores in the Year tied
        S = Number of scores in the Year - 1

        Returns the number of Smart Wins for each team in the given Year.

        Example response:
            {
            "someTeamId": Deci("8.7"),
            "someOtherTeamId": Deci("11.2"),
            "yetAnotherTeamId": Deci("7.1"),
            ...
            }
        """

        ####################
        # Helper functions #
        ####################
        def getNumberOfScoresBeatAndTied(score: float | int, scores: list[float | int]) -> list[int, int]:
            scoresBeatAndTied = [0, 0]
            for s in scores:
                if score > s:
                    scoresBeatAndTied[0] += 1
                elif score == s:
                    scoresBeatAndTied[1] += 1
            # remove 1 from the scores tied tracker since we will always find a tie for this teams score in the list of all scores
            scoresBeatAndTied[1] -= 1
            return scoresBeatAndTied

        ####################
        ####################
        ####################

        cls.loadFilters(year, validateYear=False, **kwargs)

        teamIdsAndScores = list()

        for i in range(cls._weekNumberStart - 1, cls._weekNumberEnd):
            week = year.weeks[i]
            if (week.isPlayoffWeek and not cls._onlyRegularSeason) or (
                    not week.isPlayoffWeek and not cls._onlyPostSeason):
                for matchup in week.matchups:
                    teamIdsAndScores.append((matchup.teamAId, matchup.teamAScore))
                    teamIdsAndScores.append((matchup.teamBId, matchup.teamBScore))

        teamIdAndSmartWins = dict()
        allTeamIds = YearNavigator.getAllTeamIds(year)
        for teamId in allTeamIds:
            teamIdAndSmartWins[teamId] = Deci(0)

        allScores = [teamIdAndScore[1] for teamIdAndScore in teamIdsAndScores]
        for teamIdAndScore in teamIdsAndScores:
            scoresBeat, scoresTied = getNumberOfScoresBeatAndTied(teamIdAndScore[1], allScores)
            smartWins = (scoresBeat + (scoresTied / Deci(2))) / (len(allScores) - Deci(1))
            teamIdAndSmartWins[teamIdAndScore[0]] += smartWins

        return teamIdAndSmartWins

    @classmethod
    @validateYear
    def getSmartWinsPerGame(cls, year: Year, **kwargs) -> dict[str, Deci]:
        """
        Returns the number of Smart Wins per game for each team in the given Year.

        Example response:
            {
            "someTeamId": Deci("8.7"),
            "someOtherTeamId": Deci("11.2"),
            "yetAnotherTeamId": Deci("7.1"),
            ...
            }
        """
        cls.loadFilters(year, validateYear=False, **kwargs)

        teamIdAndSmartWins = AdvancedGameOutcome.getSmartWins(year, **kwargs)
        teamIdAndNumberOfGamesPlayed = cls.getNumberOfGamesPlayed(year, **kwargs)

        teamIdAndSmartWinsPerGame = dict()
        allTeamIds = YearNavigator.getAllTeamIds(year)
        for teamId in allTeamIds:
            teamIdAndSmartWinsPerGame[teamId] = teamIdAndSmartWins[teamId] / teamIdAndNumberOfGamesPlayed[teamId]

        return teamIdAndSmartWinsPerGame
