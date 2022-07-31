from leeger import ESPNLeagueLoader

from leeger.calculator.year_calculator.GameOutcomeYearCalculator import GameOutcomeYearCalculator
from leeger.calculator.year_calculator.PointsScoredYearCalculator import PointsScoredYearCalculator
from leeger.calculator.year_calculator.ScoringShareYearCalculator import ScoringShareYearCalculator
from leeger.calculator.year_calculator.ScoringStandardDeviationYearCalculator import \
    ScoringStandardDeviationYearCalculator
from leeger.calculator.year_calculator.SingleScoreYearCalculator import SingleScoreYearCalculator

# Get a League object.
# There are many ways to get a League object, here we will just grab one using the ESPN League Loader.
espnLeagueLoader = ESPNLeagueLoader("12345678", [2019, 2020, 2021, 2022])
league = espnLeagueLoader.loadLeague()

# Since we want to get stats for just a year, we will extract the year from our league.
# Let's get year 2019.
year = league.years[0]

# To get all stats for this year, access the stat sheet.
yearStats = year.statSheet()

# To get a specific stat for this year, use a stat calculator.
# Get wins.
wins = GameOutcomeYearCalculator.getWins(year)

# Get opponent points scored per game.
opponentPointsScoredPerGame = PointsScoredYearCalculator.getOpponentPointsScoredPerGame(year)

# To limit results to only regular season, specify that as a keyword argument.
maxScore = SingleScoreYearCalculator.getMaxScore(year, onlyRegularSeason=True)

# To limit results to only post-season (playoffs), specify that as a keyword argument.
scoringShare = ScoringShareYearCalculator.getScoringShare(year, onlyPostSeason=True)

# To limit results to only championship games, specify that as a keyword argument.
winPercentage = GameOutcomeYearCalculator.getWinPercentage(year, onlyChampionship=True)

# To limit results to only certain weeks, specify that as a keyword argument.
# Let's assume this year has weeks 1-15.

# Will get weeks 5-15.
scoringStandardDeviation = ScoringStandardDeviationYearCalculator.getScoringStandardDeviation(league,
                                                                                              weekNumberStart=5)
# Will get weeks 1-10.
scoringStandardDeviation = ScoringStandardDeviationYearCalculator.getScoringStandardDeviation(league,
                                                                                              weekNumberEnd=10)
# Will get weeks 5-10.
scoringStandardDeviation = ScoringStandardDeviationYearCalculator.getScoringStandardDeviation(league,
                                                                                              weekNumberStart=5,
                                                                                              weekNumberEnd=10)
