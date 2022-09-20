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

    So Team Luck = Team Success = Team Score

    NOTE:
    These formulas uses several "magic" numbers as multipliers, which typically should be avoided.
    However, these numbers can be tweaked and the Team SSL relative to the test_league will remain roughly the same.
    This stat is more accurate with larger sample sizes (the more games played, the better).
    """

    @classmethod
    @validateLeague
    def getTeamScore(cls, league: League, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Team Score is a score given to a team that is representative of how good that team is.

        Formula:
        Team Score = ((AWAL Per Game) * aMultiplier) + (Scoring Share * bMultiplier) + ((Max Score + Min Score) * cMultiplier)

        Returns the combined Team Score for each Owner in the given League.
        Returns None for an Owner if all Years for that Owner are None

        Example response:
            {
            "someOwnerId": Deci("1118.7"),
            "someOtherOwnerId": Deci("1112.2"),
            "yetAnotherOwnerId": Deci("779.1"),
            ...
            }
        """

        return cls._addAndCombineResults(league, SSLYearCalculator.getTeamScore, **kwargs)

    @classmethod
    @validateLeague
    def getTeamSuccess(cls, league: League, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Team Success is a score given to a team that is representative of how successful that team is.

        Formula:
        Team Success = ((WAL Per Game) * aMultiplier) + (Scoring Share * bMultiplier) + ((Max Score + Min Score) * cMultiplier)

        Returns the combined Team Success for each Owner in the given League.
        Returns None for an Owner if all Years for that Owner are None

        Example response:
            {
            "someTeamId": Deci("1118.7"),
            "someOtherTeamId": Deci("1112.2"),
            "yetAnotherTeamId": Deci("779.1"),
            ...
            }
        """
        return cls._addAndCombineResults(league, SSLYearCalculator.getTeamSuccess, **kwargs)

    @classmethod
    @validateLeague
    def getTeamLuck(cls, league: League, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Team Luck is a score given to a team that is representative of how lucky that team is.

        Formula:
        Team Luck = Team Success - Team Score

        Returns the combined Team Luck for each Owner in the given League.
        Returns None for an Owner if all Years for that Owner are None

        Example response:
            {
            "someTeamId": Deci("118.7"),
            "someOtherTeamId": Deci("112.2"),
            "yetAnotherTeamId": Deci("-19.1"),
            ...
            }
        """
        return cls._addAndCombineResults(league, SSLYearCalculator.getTeamLuck, **kwargs)

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
            test = yearFiltersByYear[str(yearNumber)].asKwargs()
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
