from typing import Optional

from leeger.calculator.parent.YearCalculator import YearCalculator
from leeger.calculator.year_calculator.PointsScoredYearCalculator import PointsScoredYearCalculator
from leeger.decorator.validators import validateYear
from leeger.model.filter import WeekFilters, YearFilters
from leeger.model.league.Year import Year
from leeger.util.Deci import Deci
from leeger.util.GeneralUtil import GeneralUtil
from leeger.util.navigator import WeekNavigator
from leeger.util.navigator.YearNavigator import YearNavigator


class ScoringShareYearCalculator(YearCalculator):
    """
    Used to calculate all scoring shares.
    """

    @classmethod
    @validateYear
    def getScoringShare(cls, year: Year, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Scoring Share is used to show what percentage of league scoring a team was responsible for.

        Scoring Share = ((ΣA) / (ΣB)) * 100
        WHERE:
        A = All scores by a Team in a Year
        B = All scores by all Teams in a Year

        Returns the Scoring Share for each team in the given Year.
        Returns None for a Team if they have no games played in the range.

        Example response:
            {
            "someTeamId": Deci("10.7"),
            "someOtherTeamId": Deci("14.2"),
            "yetAnotherTeamId": Deci("12.1"),
            ...
            }
        """

        teamIdAndPointsScored = PointsScoredYearCalculator.getPointsScored(year, **kwargs)
        allScores = GeneralUtil.filter(value=None, list_=teamIdAndPointsScored.values())
        totalPointsScoredInYear = sum(allScores)
        teamIdAndScoringShare = dict()
        for teamId in YearNavigator.getAllTeamIds(year):
            if len(allScores) == 0 or teamIdAndPointsScored[teamId] is None:
                teamIdAndScoringShare[teamId] = None
            else:
                # avoid division by 0
                if totalPointsScoredInYear == 0:
                    teamIdAndScoringShare[teamId] = Deci("0")
                else:
                    teamIdAndScoringShare[teamId] = (
                        teamIdAndPointsScored[teamId] / totalPointsScoredInYear
                    ) * Deci(100)

        return teamIdAndScoringShare

    @classmethod
    @validateYear
    def getOpponentScoringShare(cls, year: Year, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Opponent Scoring Share is used to show what percentage of test_league scoring a team's opponent was responsible for.

        Opponent Scoring Share = ((ΣA) / (ΣB)) * 100
        WHERE:
        A = All scores by a Team's opponent in a Year
        B = All scores by all Teams in a Year

        Returns the Opponent Scoring Share for each team in the given Year.
        Returns None for a Team if they have no games played in the range.

        Example response:
            {
            "someTeamId": Deci("10.7"),
            "someOtherTeamId": Deci("14.2"),
            "yetAnotherTeamId": Deci("12.1"),
            ...
            }
        """

        teamIdAndOpponentPointsScored = PointsScoredYearCalculator.getOpponentPointsScored(
            year, **kwargs
        )
        allScores = GeneralUtil.filter(value=None, list_=teamIdAndOpponentPointsScored.values())
        totalPointsScoredInYear = sum(allScores)
        teamIdAndOpponentScoringShare = dict()
        for teamId in YearNavigator.getAllTeamIds(year):
            if len(allScores) == 0 or teamIdAndOpponentPointsScored[teamId] is None:
                teamIdAndOpponentScoringShare[teamId] = None
            else:
                # avoid division by 0
                if totalPointsScoredInYear == 0:
                    teamIdAndOpponentScoringShare[teamId] = Deci("0")
                else:
                    teamIdAndOpponentScoringShare[teamId] = (
                        teamIdAndOpponentPointsScored[teamId] / totalPointsScoredInYear
                    ) * Deci(100)

        return teamIdAndOpponentScoringShare

    @classmethod
    @validateYear
    def getMaxScoringShare(cls, year: Year, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Returns the Max Scoring Share for each team in the given Year.
        Returns None for a Team if they have no games played in the range.

        Example response:
            {
            "someTeamId": Deci("10.7"),
            "someOtherTeamId": Deci("14.2"),
            "yetAnotherTeamId": Deci("12.1"),
            ...
            }
        """

        filters = YearFilters.getForYear(year, **kwargs)

        teamIdAndMaxScoringShare = dict()
        for teamId in YearNavigator.getAllTeamIds(year):
            teamIdAndMaxScoringShare[teamId] = Deci(0)

        for i in range(filters.weekNumberStart - 1, filters.weekNumberEnd):
            week = year.weeks[i]
            totalPointsScoredInWeek = sum(
                WeekNavigator.getTeamIdsAndScores(
                    week, WeekFilters(includeMatchupTypes=filters.includeMatchupTypes)
                ).values()
            )
            # avoid division by 0
            if totalPointsScoredInWeek == 0:
                continue
            else:
                for matchup in week.matchups:
                    if matchup.matchupType in filters.includeMatchupTypes:
                        teamAScoringShare = (
                            Deci(matchup.teamAScore) / Deci(totalPointsScoredInWeek)
                        ) * Deci("100")
                        teamBScoringShare = (
                            Deci(matchup.teamBScore) / Deci(totalPointsScoredInWeek)
                        ) * Deci("100")
                        teamIdAndMaxScoringShare[matchup.teamAId] = max(
                            teamAScoringShare, teamIdAndMaxScoringShare[matchup.teamAId]
                        )
                        teamIdAndMaxScoringShare[matchup.teamBId] = max(
                            teamBScoringShare, teamIdAndMaxScoringShare[matchup.teamBId]
                        )

        cls._setToNoneIfNoGamesPlayed(teamIdAndMaxScoringShare, year, filters, **kwargs)
        return teamIdAndMaxScoringShare

    @classmethod
    @validateYear
    def getMinScoringShare(cls, year: Year, **kwargs) -> dict[str, Optional[Deci]]:
        """
        Returns the Min Scoring Share for each team in the given Year.
        Returns None for a Team if they have no games played in the range.

        Example response:
            {
            "someTeamId": Deci("10.7"),
            "someOtherTeamId": Deci("14.2"),
            "yetAnotherTeamId": Deci("12.1"),
            ...
            }
        """

        filters = YearFilters.getForYear(year, **kwargs)

        teamIdAndMinScoringShare = dict()
        for teamId in YearNavigator.getAllTeamIds(year):
            teamIdAndMinScoringShare[teamId] = None

        for i in range(filters.weekNumberStart - 1, filters.weekNumberEnd):
            week = year.weeks[i]
            totalPointsScoredInWeek = sum(
                WeekNavigator.getTeamIdsAndScores(
                    week, WeekFilters(includeMatchupTypes=filters.includeMatchupTypes)
                ).values()
            )
            for matchup in week.matchups:
                if matchup.matchupType in filters.includeMatchupTypes:
                    # avoid division by 0
                    if totalPointsScoredInWeek == 0:
                        for teamId in YearNavigator.getAllTeamIds(year):
                            teamIdAndMinScoringShare[teamId] = Deci("0")
                        continue
                    teamAScoringShare = (
                        Deci(matchup.teamAScore) / Deci(totalPointsScoredInWeek)
                    ) * Deci("100")
                    teamBScoringShare = (
                        Deci(matchup.teamBScore) / Deci(totalPointsScoredInWeek)
                    ) * Deci("100")
                    if teamIdAndMinScoringShare[matchup.teamAId] is None:
                        teamIdAndMinScoringShare[matchup.teamAId] = teamAScoringShare
                    else:
                        teamIdAndMinScoringShare[matchup.teamAId] = min(
                            teamAScoringShare, teamIdAndMinScoringShare[matchup.teamAId]
                        )
                    if teamIdAndMinScoringShare[matchup.teamBId] is None:
                        teamIdAndMinScoringShare[matchup.teamBId] = teamBScoringShare
                    else:
                        teamIdAndMinScoringShare[matchup.teamBId] = min(
                            teamBScoringShare, teamIdAndMinScoringShare[matchup.teamBId]
                        )

        cls._setToNoneIfNoGamesPlayed(teamIdAndMinScoringShare, year, filters, **kwargs)
        return teamIdAndMinScoringShare
