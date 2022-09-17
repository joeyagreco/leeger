# Stats Explained

### An explanation of some stats offered in this library that may not be obvious.

#### _This is not a list of **all** stats in this library._

#### To see a list of all stats retrieved by this library, see the following models:

- [AllTimeStatSheet](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md/blob/main/leeger/model/stat/AllTimeStatSheet.py)
- [YearStatSheet](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md/blob/main/leeger/model/stat/YearStatSheet.py)

___

## Table of Contents

- [AWAL](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md#awal)
- [Margins of Victory](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md#margins-of-victory)
- [Max Score](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md#max-score)
- [Min Score](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md#min-score)
- [Plus/Minus](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md#plus-minus)
- [Points Scored](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md#points-scored)
- [Scoring Share](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md#scoring-share)
- [Scoring Standard Deviation](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md#scoring-standard-deviation)
- [Smart Wins](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md#smart-wins)
- [Team Luck](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md#team-luck)
- [Team Score](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md#team-score)
- [Team Success](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md#team-success)
- [WAL](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md#wal)
- [Win Percentage](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md#win-percentage)

___

> ## AWAL
> ___
> ### Purpose
> AWAL stands for Adjusted Wins Against the League.\
> It is exactly that, an adjustment added to the Wins Against the League (
> or [WAL](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md#wal)) of a team.\
> In simple terms, this stat more accurately represents how
> many [WAL](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md#wal) any
> given team should have.\
> Ex: A team with 6.3 AWAL "deserves" 6.3 [WAL](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md#wal).
> ### Formula
> AWAL = W * (1/L) + T * (0.5/L)\
> Where:\
> W = Teams outscored in a week\
> T = Teams tied in a week\
> L = Opponents in a week (usually league size - 1)\
> ### Formula Explained
> To properly calculate AWAL, the AWAL must be calculated once for each team every week.
> Each week's AWAL can then be added together to create an aggregate AWAL for each team.
> A team's AWAL for any given week will always be between 0 and 1 (inclusive).
>
> ## Margins of Victory
> ___
> ### Purpose
> Margins of Victory (or MOV) is used to measure the magnitude of any given win.
> ### Formula
> (In any given matchup)\
> MOV = |Team A Score - Team B Score|\
> OR\
> MOV = Winning Team Score - Losing Team Score
> ### Formula Explained
> Note: Margins of Victory must be greater than 0.\
> Games that result in a Tie will never qualify for the Margins of Victory stat.
>
> ## Max Score
> ___
> ### Purpose
> Max Score is used to retrieve the highest score for an individual team.\
> It is the inverse of [Min Score](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md#min-score).
> ### Formula
> Max Score = max(A)\
> WHERE:\
> A = List of every score by a single team within a sample
> ### Formula Explained
> Note: If a team has multiple "max" scores, this does not change the outcome.\
> Ex: A team with scores: [100, 105, 104, 102] has a Max Score of 105.\
> AND\
> A team with scores: [99, 105, 105, 101] has a Max Score of 105.
>
> ## Min Score
> ___
> ### Purpose
> Min Score is used to retrieve the lowest score for an individual team.\
> It is the inverse of [Max Score](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md#max-score).
> ### Formula
> Min Score = min(A)\
> WHERE:\
> A = List of every score by a single team in a sample size
> ### Formula Explained
> Note: If a team has multiple "min" scores, this does not change the outcome.\
> Ex: A team with scores: [100, 105, 104, 102] has a Min Score of 100.\
> AND\
> A team with scores: [99, 100, 100, 101] has a Min Score of 100.
>
> ## Plus/Minus
> ___
> ### Purpose
> Plus/Minus (+/-) is used to show the net score differential for a team within a sample.
> ### Formula
> Plus/Minus = ΣA - ΣB\
> WHERE:\
> A = All scores by a team within a sample\
> B = All scores against a team within a sample
> ### Formula Explained
> Plus/Minus can be a misleading stat, as a team with a high Plus/Minus isn't necessarily a better team than one with a
> low Plus/Minus.\
> However, it is typically a good indication of how successful a team was, as a positive net score differential
> typically translates to more wins.
>
> ## Points Scored
> ___
> ### Purpose
> Points Scored Per Game is the total number of points a team scored.
> ### Formula
> Points Scored Per Game = Σ A\
> WHERE:\
> A = All scores by a team within a sample\
> ### Formula Explained
> N/A
>
> ## Scoring Share
> ___
> ### Purpose
> Scoring Share is used to show what percentage of league scoring a team was responsible for.
> ### Formula
> Scoring Share = ((ΣA) / (ΣB)) * 100\
> WHERE:\
> A = All scores by a team within a sample\
> B = All scores by all teams within a sample
> ### Formula Explained
> Scoring Share is a good way to compare how a team performed in a league one year vs another year.\
> While 100 Points Scored Per Game one year may not be equivalent to 100 Points Scored Per Game another year,\
> scoring 10% of the league's points *will* be equivalent to scoring 10% of the league's points another year.
>
> ## Scoring Standard Deviation
> ___
> ### Purpose
> Scoring Standard Deviation is used to show how volatile a team's scoring was.\
> This stat measures a team's scores relative to the Points Scored Per Game of all of their scores.
> ### Formula
> Scoring Standard Deviation = sqrt((Σ|x-u|²)/N)\
> WHERE:\
> x = A score\
> u = PPG\
> N = Number of scores (typically weeks played)
> ### Formula Explained
> A team with low Scoring Standard Deviation has been consistent in their scoring patterns.\
> A team with high Scoring Standard Deviation has been volatile in their scoring patterns.\
> It should be noted that if a team has lower Scoring Standard Deviation than another team, it is not an indication that
> the team with lower Scoring Standard Deviation has performed better.\
> Ex: Team A has scores: [100, 120, 150, 160] and a Scoring STDEV of 23.8\
> Team B has scores: [70, 72, 71, 69] and a Scoring STDEV of 1.12\
> Team B has a lower Scoring STDEV than Team A, but has definitely performed worse.
>
> ## Smart Wins
> ___
> ### Purpose
> Smart Wins show how many wins a team would have if it played against every score in the league within a sample.
> ### Formula
> Smart Wins = Σ((W + (T/2)) / S)\
> WHERE:\
> W = Total scores in the league beat within a sample\
> T = Total scores in the league tied within a sample\
> S = Number of scores in the league within a sample - 1
> ### Formula Explained
> Smart Wins is a good compliment to [AWAL](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md#awal) when
> comparing
> both to a
> team's [WAL](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md#wal).\
> Smart Wins is better than [AWAL](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md#awal) at giving a team
> credit
> if they lose by a
> small margin in any given week.
>
> ## Team Luck
> ___
> ### Purpose
> Team Luck is used to show how much more successful a team was than what they should have been.
> ### Formula
> Team Luck = [Team Success](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md#team-success) -
> [Team Score](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md#team-score)
>
> ### Formula Explained
> A team with a higher [Team Success](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md#team-success)
> than [Team Score](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md#team-score) likely has a
> higher [WAL](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md#wal)
> than they deserve.\
> Team Luck helps to quantify just how much better a team ended up than they should have.\
> A team with 0 Team Luck has a "fair" amount of [WAL](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md#wal)
> .\
> A team with positive (+) Team Luck has a higher amount
> of [WAL](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md#wal) than they
> deserve.\
> A team with negative (-) Team Luck has a lower amount
> of [WAL](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md#wal) than they
> deserve.\
> Note: This stat is more accurate with larger sample sizes (the more games played, the better).\
> Note2: The sum of all Team Luck's within a league will be ≈ 0.
>
> ## Team Score
> ___
> ### Purpose
> Team Score is a score given to a team that is representative of how "good" that team is.\
> It is the sister score of [Team Success](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md#team-success).
> ### Formula
> Team Score = (([AWAL](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md#awal) / G) * 100) +
> ([Scoring Share](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md#scoring-share) * 2) +
> (([Max Score](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md#max-score) +
> [Min Score](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md#min-score)) * 0.05)
>
> WHERE:\
> G = Total games played by a team within a sample
> ### Formula Explained
> This formula uses several "magic" numbers as multipliers, which typically should be avoided.\
> However, these numbers can be tweaked and the general Team Score for each team relative to the league will remain
> roughly the same.\
> Note: This stat is more accurate with larger sample sizes (the more games played, the better).
>
> ## Team Success
> ___
> ### Purpose
> Team Success is a score given to a team that is representative of how successful that team has been.\
> It is the sister score of [Team Score](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md#team-score).
> ### Formula
> Team Success = (([WAL](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md#wal) / G) * 100) +
> ([Scoring Share](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md#scoring-share) * 2) +
> (([Max Score](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md#max-score) +
> [Min Score](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md#min-score)) * 0.05)\
> WHERE:\
> G = Total games played by a team in a sample size
> ### Formula Explained
> This formula uses several "magic" numbers as multipliers, which typically should be avoided.\
> However, these numbers can be tweaked and the general Team Success for each team relative to the league will remain
> roughly the same.\
> Note: This stat is more accurate with larger sample sizes (the more games played, the better).
>
> ## WAL
> ___
> ### Purpose
> WAL stands for Wins Against the League.\
> It is representative of the total amount of wins and ties a team has.
> ### Formula
> WAL = W + (T * 0.5)\
> WHERE:\
> W = Total number of wins a team has within a sample\
> T = Total number of ties a team has within a sample
> ### Formula Explained
> WAL is a quick and useful stat that is used typically to see how successful a team has been.
>
> ## Win Percentage
> ___
> ### Purpose
> Win Percentage is [WAL](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md#wal) represented as a percentage (
> %).
> ### Formula
> Win Percentage = [WAL](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md#wal) / G\
> WHERE:\
> G = Total number of games played by a team within a sample
> ### Formula Explained
> Win Percentage is simply another way of representing how successful a team has been throughout a sample.
