from leeger.calculator.all_time_calculator import AWALAllTimeCalculator, TeamSummaryAllTimeCalculator
from leeger.calculator.all_time_calculator.GameOutcomeAllTimeCalculator import \
    GameOutcomeAllTimeCalculator
from leeger.calculator.all_time_calculator.PlusMinusAllTimeCalculator import PlusMinusAllTimeCalculator
from leeger.calculator.all_time_calculator.PointsScoredAllTimeCalculator import \
    PointsScoredAllTimeCalculator
from leeger.calculator.all_time_calculator.SSLAllTimeCalculator import SSLAllTimeCalculator
from leeger.calculator.all_time_calculator.ScoringShareAllTimeCalculator import \
    ScoringShareAllTimeCalculator
from leeger.calculator.all_time_calculator.ScoringStandardDeviationAllTimeCalculator import \
    ScoringStandardDeviationAllTimeCalculator
from leeger.calculator.all_time_calculator.SingleScoreAllTimeCalculator import \
    SingleScoreAllTimeCalculator
from leeger.calculator.all_time_calculator.SmartWinsAllTimeCalculator import SmartWinsAllTimeCalculator
from leeger.calculator.year_calculator import \
    ScoringStandardDeviationYearCalculator, TeamSummaryYearCalculator
from leeger.calculator.year_calculator import SingleScoreYearCalculator
from leeger.calculator.year_calculator.AWALYearCalculator import AWALYearCalculator
from leeger.calculator.year_calculator.GameOutcomeYearCalculator import GameOutcomeYearCalculator
from leeger.calculator.year_calculator.PlusMinusYearCalculator import PlusMinusYearCalculator
from leeger.calculator.year_calculator.PointsScoredYearCalculator import PointsScoredYearCalculator
from leeger.calculator.year_calculator.SSLYearCalculator import SSLYearCalculator
from leeger.calculator.year_calculator.ScoringShareYearCalculator import ScoringShareYearCalculator
from leeger.calculator.year_calculator.SmartWinsYearCalculator import SmartWinsYearCalculator
from leeger.model.filter import YearFilters
from leeger.model.league import League, Year
from leeger.model.stat.AllTimeStatSheet import AllTimeStatSheet
from leeger.model.stat.YearStatSheet import YearStatSheet
from leeger.util.navigator import LeagueNavigator, YearNavigator


def leagueStatSheet(league: League, **kwargs) -> AllTimeStatSheet:
    # Team Summary
    gamesPlayed = TeamSummaryAllTimeCalculator.getGamesPlayed(league, **kwargs)

    # Game Outcome
    wins = GameOutcomeAllTimeCalculator.getWins(league, **kwargs)
    losses = GameOutcomeAllTimeCalculator.getLosses(league, **kwargs)
    ties = GameOutcomeAllTimeCalculator.getTies(league, **kwargs)
    winPercentage = GameOutcomeAllTimeCalculator.getWinPercentage(league, **kwargs)
    wal = GameOutcomeAllTimeCalculator.getWAL(league, **kwargs)
    walPerGame = GameOutcomeAllTimeCalculator.getWALPerGame(league, **kwargs)

    # AWAL
    awal = AWALAllTimeCalculator.getAWAL(league, **kwargs)
    awalPerGame = AWALAllTimeCalculator.getAWALPerGame(league, **kwargs)
    opponentAWAL = AWALAllTimeCalculator.getOpponentAWAL(league, **kwargs)
    opponentAWALPerGame = AWALAllTimeCalculator.getOpponentAWALPerGame(league, **kwargs)

    # Smart Wins
    smartWins = SmartWinsAllTimeCalculator.getSmartWins(league, **kwargs)
    smartWinsPerGame = SmartWinsAllTimeCalculator.getSmartWinsPerGame(league, **kwargs)
    opponentSmartWins = SmartWinsAllTimeCalculator.getOpponentSmartWins(league, **kwargs)
    opponentSmartWinsPerGame = SmartWinsAllTimeCalculator.getOpponentSmartWinsPerGame(league, **kwargs)

    # Points Scored
    pointsScored = PointsScoredAllTimeCalculator.getPointsScored(league, **kwargs)
    pointsScoredPerGame = PointsScoredAllTimeCalculator.getPointsScoredPerGame(league, **kwargs)
    opponentPointsScored = PointsScoredAllTimeCalculator.getOpponentPointsScored(league, **kwargs)
    opponentPointsScoredPerGame = PointsScoredAllTimeCalculator.getOpponentPointsScoredPerGame(league,
                                                                                               **kwargs)

    # Scoring Share
    scoringShare = ScoringShareAllTimeCalculator.getScoringShare(league, **kwargs)
    opponentScoringShare = ScoringShareAllTimeCalculator.getOpponentScoringShare(league, **kwargs)
    maxScoringShare = ScoringShareAllTimeCalculator.getMaxScoringShare(league, **kwargs)
    minScoringShare = ScoringShareAllTimeCalculator.getMinScoringShare(league, **kwargs)

    # Single Score
    maxScore = SingleScoreAllTimeCalculator.getMaxScore(league, **kwargs)
    minScore = SingleScoreAllTimeCalculator.getMinScore(league, **kwargs)

    # Scoring Standard Deviation
    scoringStandardDeviation = ScoringStandardDeviationAllTimeCalculator.getScoringStandardDeviation(league,
                                                                                                     **kwargs)

    # Plus Minus
    plusMinus = PlusMinusAllTimeCalculator.getPlusMinus(league, **kwargs)

    # SSL
    adjustedTeamScore = SSLAllTimeCalculator.getAdjustedTeamScore(league, **kwargs)
    adjustedTeamSuccess = SSLAllTimeCalculator.getAdjustedTeamSuccess(league, **kwargs)
    adjustedTeamLuck = SSLAllTimeCalculator.getAdjustedTeamLuck(league, **kwargs)

    # check for optional stats
    totalGames = None
    leagueMedianWins = None
    opponentLeagueMedianWins = None
    for year in league.years:
        if year.yearSettings.leagueMedianGames is True:
            totalGames = TeamSummaryAllTimeCalculator.getTotalGames(league, **kwargs)
            leagueMedianWins = GameOutcomeAllTimeCalculator.getLeagueMedianWins(league, **kwargs)
            opponentLeagueMedianWins = GameOutcomeAllTimeCalculator.getOpponentLeagueMedianWins(league, **kwargs)
            break

    return AllTimeStatSheet(gamesPlayed=gamesPlayed, wins=wins, losses=losses, ties=ties, winPercentage=winPercentage,
                            wal=wal, walPerGame=walPerGame, awal=awal, awalPerGame=awalPerGame,
                            opponentAWAL=opponentAWAL, opponentAWALPerGame=opponentAWALPerGame, smartWins=smartWins,
                            smartWinsPerGame=smartWinsPerGame, opponentSmartWins=opponentSmartWins,
                            opponentSmartWinsPerGame=opponentSmartWinsPerGame, pointsScored=pointsScored,
                            pointsScoredPerGame=pointsScoredPerGame, opponentPointsScored=opponentPointsScored,
                            opponentPointsScoredPerGame=opponentPointsScoredPerGame, scoringShare=scoringShare,
                            opponentScoringShare=opponentScoringShare, maxScore=maxScore, minScore=minScore,
                            scoringStandardDeviation=scoringStandardDeviation, plusMinus=plusMinus,
                            adjustedTeamScore=adjustedTeamScore, adjustedTeamSuccess=adjustedTeamSuccess,
                            adjustedTeamLuck=adjustedTeamLuck, leagueMedianWins=leagueMedianWins, totalGames=totalGames,
                            opponentLeagueMedianWins=opponentLeagueMedianWins, maxScoringShare=maxScoringShare,
                            minScoringShare=minScoringShare)


def yearStatSheet(year: Year, **kwargs) -> YearStatSheet:
    ownerNames = kwargs.pop("ownerNames", None)
    years = kwargs.pop("years", None)
    # Team Summary
    gamesPlayed = TeamSummaryYearCalculator.getGamesPlayed(year, **kwargs)
    # Game Outcome
    wins = GameOutcomeYearCalculator.getWins(year, **kwargs)
    losses = GameOutcomeYearCalculator.getLosses(year, **kwargs)
    ties = GameOutcomeYearCalculator.getTies(year, **kwargs)
    winPercentage = GameOutcomeYearCalculator.getWinPercentage(year, **kwargs)
    wal = GameOutcomeYearCalculator.getWAL(year, **kwargs)
    walPerGame = GameOutcomeYearCalculator.getWALPerGame(year, **kwargs)

    # AWAL
    awal = AWALYearCalculator.getAWAL(year, **kwargs)
    awalPerGame = AWALYearCalculator.getAWALPerGame(year, **kwargs)
    opponentAWAL = AWALYearCalculator.getOpponentAWAL(year, **kwargs)
    opponentAWALPerGame = AWALYearCalculator.getOpponentAWALPerGame(year, **kwargs)

    # Smart Wins
    smartWins = SmartWinsYearCalculator.getSmartWins(year, **kwargs)
    smartWinsPerGame = SmartWinsYearCalculator.getSmartWinsPerGame(year, **kwargs)
    opponentSmartWins = SmartWinsYearCalculator.getOpponentSmartWins(year, **kwargs)
    opponentSmartWinsPerGame = SmartWinsYearCalculator.getOpponentSmartWinsPerGame(year, **kwargs)

    # Points Scored
    pointsScored = PointsScoredYearCalculator.getPointsScored(year, **kwargs)
    pointsScoredPerGame = PointsScoredYearCalculator.getPointsScoredPerGame(year, **kwargs)
    opponentPointsScored = PointsScoredYearCalculator.getOpponentPointsScored(year, **kwargs)
    opponentPointsScoredPerGame = PointsScoredYearCalculator.getOpponentPointsScoredPerGame(year, **kwargs)

    # Scoring Share
    scoringShare = ScoringShareYearCalculator.getScoringShare(year, **kwargs)
    opponentScoringShare = ScoringShareYearCalculator.getOpponentScoringShare(year, **kwargs)
    maxScoringShare = ScoringShareYearCalculator.getMaxScoringShare(year, **kwargs)
    minScoringShare = ScoringShareYearCalculator.getMinScoringShare(year, **kwargs)

    # Single Score
    maxScore = SingleScoreYearCalculator.getMaxScore(year, **kwargs)
    minScore = SingleScoreYearCalculator.getMinScore(year, **kwargs)

    # Scoring Standard Deviation
    scoringStandardDeviation = ScoringStandardDeviationYearCalculator.getScoringStandardDeviation(year, **kwargs)

    # Plus Minus
    plusMinus = PlusMinusYearCalculator.getPlusMinus(year, **kwargs)

    # SSL
    teamScore = SSLYearCalculator.getTeamScore(year, **kwargs)
    teamSuccess = SSLYearCalculator.getTeamSuccess(year, **kwargs)
    teamLuck = SSLYearCalculator.getTeamLuck(year, **kwargs)

    # check for optional stats
    totalGames = None
    leagueMedianWins = None
    opponentLeagueMedianWins = None
    if year.yearSettings.leagueMedianGames is True:
        totalGames = TeamSummaryYearCalculator.getTotalGames(year, **kwargs)
        leagueMedianWins = GameOutcomeYearCalculator.getLeagueMedianWins(year, **kwargs)
        opponentLeagueMedianWins = GameOutcomeYearCalculator.getOpponentLeagueMedianWins(year, **kwargs)

    return YearStatSheet(gamesPlayed=gamesPlayed, wins=wins, losses=losses, ties=ties, winPercentage=winPercentage,
                         wal=wal, walPerGame=walPerGame, awal=awal, awalPerGame=awalPerGame, opponentAWAL=opponentAWAL,
                         opponentAWALPerGame=opponentAWALPerGame, smartWins=smartWins,
                         smartWinsPerGame=smartWinsPerGame, opponentSmartWins=opponentSmartWins,
                         opponentSmartWinsPerGame=opponentSmartWinsPerGame, pointsScored=pointsScored,
                         pointsScoredPerGame=pointsScoredPerGame, opponentPointsScored=opponentPointsScored,
                         opponentPointsScoredPerGame=opponentPointsScoredPerGame, scoringShare=scoringShare,
                         opponentScoringShare=opponentScoringShare, maxScore=maxScore, minScore=minScore,
                         scoringStandardDeviation=scoringStandardDeviation, plusMinus=plusMinus,
                         teamScore=teamScore, teamSuccess=teamSuccess, teamLuck=teamLuck,
                         leagueMedianWins=leagueMedianWins, totalGames=totalGames,
                         opponentLeagueMedianWins=opponentLeagueMedianWins, maxScoringShare=maxScoringShare,
                         minScoringShare=minScoringShare, ownerNames=ownerNames, years=years)


def allTimeTeamsStatSheet(league: League, **kwargs) -> list[tuple[str, dict]]:
    allTimeTeamsStatsWithTitles: list[tuple[str, dict]] = list()
    for year in league.years:
        ownerNames: dict[str, str] = dict()
        years: dict[str, int] = dict()
        for team in year.teams:
            ownerNames[team.id] = LeagueNavigator.getOwnerById(league, team.ownerId).name
            years[team.id] = year.yearNumber
        allTimeTeamsStatsWithTitles += yearStatSheet(year,
                                                     ownerNames=ownerNames,
                                                     years=years,
                                                     **kwargs).preferredOrderWithTitle()

    # condense stats with titles so there's only 1 list value for each title
    condensedAllTimeTeamsStatsWithTitles: list[tuple[str, dict]] = list()
    for titleStr, statsDict in allTimeTeamsStatsWithTitles:
        allTitlesInCondensedList = list()
        if len(condensedAllTimeTeamsStatsWithTitles) > 0:
            allTitlesInCondensedList = [values[0] for values in condensedAllTimeTeamsStatsWithTitles]
        if titleStr in allTitlesInCondensedList:
            # add to stats dict for the existing title
            for i, (title_s, stats_d) in enumerate(condensedAllTimeTeamsStatsWithTitles):
                if title_s == titleStr:
                    condensedAllTimeTeamsStatsWithTitles[i] = (title_s, stats_d | statsDict)
        else:
            condensedAllTimeTeamsStatsWithTitles.append((titleStr, statsDict))
    return condensedAllTimeTeamsStatsWithTitles


def yearMatchupsStatSheet(year: Year, **kwargs) -> list[tuple[str, dict]]:
    yearFilters = YearFilters.getForYear(year, **kwargs)
    teamANames: dict[str, str] = dict()
    teamBNames: dict[str, str] = dict()
    teamAScores: dict[str, float | int] = dict()
    teamBScores: dict[str, float | int] = dict()
    matchupTypes: dict[str, str] = dict()
    weekNumbers: dict[str, int] = dict()

    for week in year.weeks:
        if yearFilters.weekNumberStart <= week.weekNumber <= yearFilters.weekNumberEnd:
            for matchup in week.matchups:
                if matchup.matchupType in yearFilters.includeMatchupTypes \
                        and (matchup.multiWeekMatchupId is None or yearFilters.includeMultiWeekMatchups is True):
                    teamA = YearNavigator.getTeamById(year, matchup.teamAId)
                    teamB = YearNavigator.getTeamById(year, matchup.teamBId)
                    # add matchup for both teams
                    for teamChar in ("A", "B"):
                        teamANames[f"{matchup.id}{teamChar}"] = teamA.name
                        teamBNames[f"{matchup.id}{teamChar}"] = teamB.name
                        teamAScores[f"{matchup.id}{teamChar}"] = matchup.teamAScore
                        teamBScores[f"{matchup.id}{teamChar}"] = matchup.teamBScore
                        matchupTypes[f"{matchup.id}{teamChar}"] = matchup.matchupType.name
                        weekNumbers[f"{matchup.id}{teamChar}"] = week.weekNumber

    return [
        ("Week Number", weekNumbers),
        ("Team For", teamANames),
        ("Points For", teamAScores),
        ("Team Against", teamBNames),
        ("Points Against", teamBScores),
        ("Matchup Type", matchupTypes)
    ]
