from typing import Optional

from leeger.calculator.parent.AllTimeCalculator import AllTimeCalculator
from leeger.calculator.year_calculator.SSLYearCalculator import SSLYearCalculator
from leeger.decorator.validators import validateLeague
from leeger.model.filter import AllTimeFilters
from leeger.model.league.League import League
from leeger.util.Deci import Deci
from leeger.util.navigator import LeagueNavigator


class SSLAllTimeCalculator(AllTimeCalculator):
    """
    Used to calculate all SSL stats.

    SSL stands for "Score Success Luck", which are 3 stats calculated here that go hand in hand.

    Team Score = How good a team is
    Team Success = How successful a team is
    Team Luck = How lucky a team is

    So Team Luck = Team Success - Team Score

    NOTE:
    These formulas uses several "magic" numbers as multipliers, which typically should be avoided.
    However, these numbers can be tweaked and the Team SSL relative to the test_league will remain roughly the same.
    This stat is more accurate with larger sample sizes (the more games played, the better).
    """

    @classmethod
    @validateLeague
    def getAdjustedTeamScore(cls, league: League, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Returns the Adjusted Team Score per Game for each Owner in the given League.
        Returns None for an Owner if all Years for that Owner are None

        Example response:
            {
            "someOwnerId": Deci("118.7"),
            "someOtherOwnerId": Deci("112.2"),
            "yetAnotherOwnerId": Deci("79.1"),
            ...
            }
        """
        from leeger.calculator.year_calculator import TeamSummaryYearCalculator
        teamScoreResultsOrderedByYear = cls._getAllResultDictsByYear(league, SSLYearCalculator.getTeamScore, **kwargs)
        gamesPlayedByYear: dict[str, dict[str, int]] = dict()

        allTimeFilters = AllTimeFilters.getForLeague(league, **kwargs)
        yearFiltersByYear = cls._allTimeFiltersToYearFilters(league, allTimeFilters)

        for yearNumber in teamScoreResultsOrderedByYear.keys():
            year = LeagueNavigator.getYearByYearNumber(league, int(yearNumber))
            gamesPlayedByYear[yearNumber] = TeamSummaryYearCalculator.getGamesPlayed(year,
                                                                                     **yearFiltersByYear[
                                                                                         str(yearNumber)].asKwargs())

        ownerIdToTeamScoreAndGamesPlayedListMap: dict[str, list[tuple[Deci, int]]] = dict()
        # {"someOwnerId": [(Deci("101.5"), 4), (Deci("109.4), 5)]}
        for yearNumber, teamScoreResultDict in teamScoreResultsOrderedByYear.items():
            for teamId, teamScore in teamScoreResultDict.items():
                team = LeagueNavigator.getTeamById(league, teamId)
                gamesPlayed = gamesPlayedByYear[yearNumber][teamId]
                if team.ownerId in ownerIdToTeamScoreAndGamesPlayedListMap:
                    ownerIdToTeamScoreAndGamesPlayedListMap[team.ownerId].append((teamScore, gamesPlayed))
                else:
                    ownerIdToTeamScoreAndGamesPlayedListMap[team.ownerId] = [(teamScore, gamesPlayed)]

        # adjust team scores by games played
        ownerIdAndAdjustedTeamScore: dict[str, Optional[Deci]] = dict()
        for ownerId, teamScoreAndGamesPlayedList in ownerIdToTeamScoreAndGamesPlayedListMap.items():
            totalGamesPlayed = sum([tsagp[1] for tsagp in teamScoreAndGamesPlayedList])
            if totalGamesPlayed > 0:
                for teamScore, gamesPlayed in teamScoreAndGamesPlayedList:
                    if teamScore is not None:
                        percentageOfGamesPlayed = Deci(gamesPlayed / totalGamesPlayed)
                        adjustedTeamScore = Deci(teamScore * percentageOfGamesPlayed)
                        if ownerId in ownerIdAndAdjustedTeamScore:
                            ownerIdAndAdjustedTeamScore[ownerId] += adjustedTeamScore
                        else:
                            ownerIdAndAdjustedTeamScore[ownerId] = adjustedTeamScore

        # set to None if ownerId not in response dict
        for ownerId in LeagueNavigator.getAllOwnerIds(league):
            if ownerId not in ownerIdAndAdjustedTeamScore:
                ownerIdAndAdjustedTeamScore[ownerId] = None

        return ownerIdAndAdjustedTeamScore

    @classmethod
    @validateLeague
    def getAdjustedTeamSuccess(cls, league: League, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Returns the Adjusted Team Success per Game for each Owner in the given League.
        Returns None for an Owner if all Years for that Owner are None

        Example response:
            {
            "someOwnerId": Deci("118.7"),
            "someOtherOwnerId": Deci("112.2"),
            "yetAnotherOwnerId": Deci("79.1"),
            ...
            }
        """
        from leeger.calculator.year_calculator import TeamSummaryYearCalculator
        teamSuccessResultsOrderedByYear = cls._getAllResultDictsByYear(league, SSLYearCalculator.getTeamSuccess,
                                                                       **kwargs)
        gamesPlayedByYear: dict[str, dict[str, int]] = dict()

        allTimeFilters = AllTimeFilters.getForLeague(league, **kwargs)
        yearFiltersByYear = cls._allTimeFiltersToYearFilters(league, allTimeFilters)

        for yearNumber in teamSuccessResultsOrderedByYear.keys():
            year = LeagueNavigator.getYearByYearNumber(league, int(yearNumber))
            gamesPlayedByYear[yearNumber] = TeamSummaryYearCalculator.getGamesPlayed(year,
                                                                                     **yearFiltersByYear[
                                                                                         str(yearNumber)].asKwargs())

        ownerIdToTeamSuccessAndGamesPlayedListMap: dict[str, list[tuple[Deci, int]]] = dict()
        # {"someOwnerId": [(Deci("101.5"), 4), (Deci("109.4), 5)]}
        for yearNumber, teamSuccessResultDict in teamSuccessResultsOrderedByYear.items():
            for teamId, teamSuccess in teamSuccessResultDict.items():
                team = LeagueNavigator.getTeamById(league, teamId)
                gamesPlayed = gamesPlayedByYear[yearNumber][teamId]
                if team.ownerId in ownerIdToTeamSuccessAndGamesPlayedListMap:
                    ownerIdToTeamSuccessAndGamesPlayedListMap[team.ownerId].append((teamSuccess, gamesPlayed))
                else:
                    ownerIdToTeamSuccessAndGamesPlayedListMap[team.ownerId] = [(teamSuccess, gamesPlayed)]

        # adjust team success by games played
        ownerIdAndAdjustedTeamSuccess: dict[str, Optional[Deci]] = dict()
        for ownerId, teamSuccessAndGamesPlayedList in ownerIdToTeamSuccessAndGamesPlayedListMap.items():
            totalGamesPlayed = sum([tsagp[1] for tsagp in teamSuccessAndGamesPlayedList])
            if totalGamesPlayed > 0:
                for teamSuccess, gamesPlayed in teamSuccessAndGamesPlayedList:
                    if teamSuccess is not None:
                        percentageOfGamesPlayed = Deci(gamesPlayed / totalGamesPlayed)
                        adjustedTeamSuccess = Deci(teamSuccess * percentageOfGamesPlayed)
                        if ownerId in ownerIdAndAdjustedTeamSuccess:
                            ownerIdAndAdjustedTeamSuccess[ownerId] += adjustedTeamSuccess
                        else:
                            ownerIdAndAdjustedTeamSuccess[ownerId] = adjustedTeamSuccess

        # set to None if ownerId not in response dict
        for ownerId in LeagueNavigator.getAllOwnerIds(league):
            if ownerId not in ownerIdAndAdjustedTeamSuccess:
                ownerIdAndAdjustedTeamSuccess[ownerId] = None

        return ownerIdAndAdjustedTeamSuccess

    @classmethod
    @validateLeague
    def getAdjustedTeamLuck(cls, league: League, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Returns the Adjusted Team Luck per Game for each Owner in the given League.
        Returns None for an Owner if all Years for that Owner are None

        Example response:
            {
            "someOwnerId": Deci("18.7"),
            "someOtherOwnerId": Deci("-12.2"),
            "yetAnotherOwnerId": Deci("49.1"),
            ...
            }
        """
        ownerIdAndAdjustedTeamLuck: dict[str, Optional[Deci]] = dict()
        ownerIdAndAdjustedTeamScore = SSLAllTimeCalculator.getAdjustedTeamScore(league, **kwargs)
        ownerIdAndAdjustedTeamSuccess = SSLAllTimeCalculator.getAdjustedTeamSuccess(league, **kwargs)

        for ownerId in LeagueNavigator.getAllOwnerIds(league):
            adjustedTeamScore = ownerIdAndAdjustedTeamScore[ownerId]
            adjustedTeamSuccess = ownerIdAndAdjustedTeamSuccess[ownerId]
            if adjustedTeamScore is not None and adjustedTeamSuccess is not None:
                ownerIdAndAdjustedTeamLuck[ownerId] = Deci(adjustedTeamSuccess - adjustedTeamScore)
            else:
                ownerIdAndAdjustedTeamLuck[ownerId] = None

        return ownerIdAndAdjustedTeamLuck
