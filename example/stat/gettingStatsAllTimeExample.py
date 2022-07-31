from leeger.calculator.all_time_calculator import GameOutcomeAllTimeCalculator, PointsScoredAllTimeCalculator, \
    SingleScoreAllTimeCalculator, ScoringShareAllTimeCalculator, AWALAllTimeCalculator, \
    ScoringStandardDeviationAllTimeCalculator, SmartWinsAllTimeCalculator
from leeger.league_loader import ESPNLeagueLoader

# Get a League object.
# There are many ways to get a League object, here we will just grab one using the ESPN League Loader.
espnLeagueLoader = ESPNLeagueLoader("12345678", [2019, 2020, 2021, 2022])
league = espnLeagueLoader.loadLeague()

# To get all stats for this league, access the stat sheet.
leagueStats = league.statSheet()

# To get a specific stat for this league, use a stat calculator.
# Get wins.
wins = GameOutcomeAllTimeCalculator.getWins(league)

# Get opponent points scored per game.
opponentPointsScoredPerGame = PointsScoredAllTimeCalculator.getOpponentPointsScoredPerGame(league)

# To limit results to only regular season, specify that as a keyword argument.
maxScore = SingleScoreAllTimeCalculator.getMaxScore(league, onlyRegularSeason=True)

# To limit results to only post-season (playoffs), specify that as a keyword argument.
scoringShare = ScoringShareAllTimeCalculator.getScoringShare(league, onlyPostSeason=True)

# To limit results to only championship games, specify that as a keyword argument.
winPercentage = GameOutcomeAllTimeCalculator.getWinPercentage(league, onlyChampionship=True)

# To limit results to only certain years, specify that as a keyword argument.
# This league has years 2019, 2020, 2021, 2022.

# Will get years 2020-2022.
awalPerGame = AWALAllTimeCalculator.getAWALPerGame(league, yearNumberStart=2020)
# Will get years 2019-2020.
awalPerGame = AWALAllTimeCalculator.getAWALPerGame(league, yearNumberEnd=2020)
# Will get years 2020-2021.
awalPerGame = AWALAllTimeCalculator.getAWALPerGame(league, yearNumberStart=2020, yearNumberEnd=2021)

# To limit results to only certain weeks, specify that as a keyword argument.
# Let's assume each year in this league has weeks 1-15.

# Will get weeks 5-15.
scoringStandardDeviation = ScoringStandardDeviationAllTimeCalculator.getScoringStandardDeviation(league,
                                                                                                 weekNumberStart=5)
# Will get weeks 1-10.
scoringStandardDeviation = ScoringStandardDeviationAllTimeCalculator.getScoringStandardDeviation(league,
                                                                                                 weekNumberEnd=10)
# Will get weeks 5-10.
scoringStandardDeviation = ScoringStandardDeviationAllTimeCalculator.getScoringStandardDeviation(league,
                                                                                                 weekNumberStart=5,
                                                                                                 weekNumberEnd=10)

# You can combine week and year filters to get specific weeks that span across years.
# To limit results to only certain weeks across years, specify that as a keyword argument.
# This league has years 2019, 2020, 2021, 2022.
# Let's assume each year in this league has weeks 1-15.

# Will get week 5, 2020 - week 15, 2022.
smartWins = SmartWinsAllTimeCalculator.getSmartWins(league, weekNumberStart=5, yearNumberStart=2020)
# Will get week 1, 2019 - week 10, 2020.
smartWins = SmartWinsAllTimeCalculator.getSmartWins(league, weekNumberEnd=10, yearNumberEnd=2020)
# Will get week 5, 2020 - week 10, 2021.
smartWins = SmartWinsAllTimeCalculator.getSmartWins(league, weekNumberStart=5, yearNumberStart=2020, weekNumberEnd=10,
                                                    yearNumberEnd=2021)
