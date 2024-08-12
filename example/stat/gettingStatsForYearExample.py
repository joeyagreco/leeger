from leeger.calculator.year_calculator import (
    GameOutcomeYearCalculator,
    PointsScoredYearCalculator,
    ScoringShareYearCalculator,
    ScoringStandardDeviationYearCalculator,
    SingleScoreYearCalculator,
)
from leeger.league_loader import ESPNLeagueLoader
from leeger.model.league import League, Year
from leeger.model.stat.YearStatSheet import YearStatSheet
from leeger.util.stat_sheet import yearStatSheet

if __name__ == "__main__":
    # Get a League object.
    # There are many ways to get a League object, here we will just grab one using the ESPN League Loader.

    espnLeagueLoader = ESPNLeagueLoader("12345678", [2019, 2020, 2021, 2022])
    league: League = espnLeagueLoader.loadLeague()

    # Since we want to get stats for just a year, we will extract the year from our league.
    # Let's get year 2019.
    year2019: Year = league.years[0]

    # To get all stats for this year, access the stat sheet.
    yearStats: YearStatSheet = yearStatSheet(year2019)

    # To get a specific stat for this year, use a stat calculator.
    # Get wins.
    wins = GameOutcomeYearCalculator.getWins(year2019)

    # Get opponent points scored per game.
    opponentPointsScoredPerGame = (
        PointsScoredYearCalculator.getOpponentPointsScoredPerGame(year2019)
    )

    # To limit results to only regular season, specify that as a keyword argument.
    maxScore = SingleScoreYearCalculator.getMaxScore(year2019, onlyRegularSeason=True)

    # To limit results to only post-season (playoffs), specify that as a keyword argument.
    scoringShare = ScoringShareYearCalculator.getScoringShare(
        year2019, onlyPostSeason=True
    )

    # To limit results to only championship games, specify that as a keyword argument.
    winPercentage = GameOutcomeYearCalculator.getWinPercentage(
        year2019, onlyChampionship=True
    )

    # To limit results to only certain weeks, specify that as a keyword argument.
    # Let's assume this year has weeks 1-15.

    # Will get weeks 5-15.
    scoringStandardDeviation = (
        ScoringStandardDeviationYearCalculator.getScoringStandardDeviation(
            year2019, weekNumberStart=5
        )
    )
    # Will get weeks 1-10.
    scoringStandardDeviation = (
        ScoringStandardDeviationYearCalculator.getScoringStandardDeviation(
            year2019, weekNumberEnd=10
        )
    )
    # Will get weeks 5-10.
    scoringStandardDeviation = (
        ScoringStandardDeviationYearCalculator.getScoringStandardDeviation(
            year2019, weekNumberStart=5, weekNumberEnd=10
        )
    )
