# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

- N/A

## [1.15.0]

- League objects can now be built from a Python dictionary
- None values for Matchup tiebreakers will default to False instead of raising an exception
- None values for YearSettings leagueMedianGames will default to False instead of raising an exception

## [1.14.0]

- Now validate leagues before returning them in all league loaders
- Updated README

## [1.13.1]

- Fixed ESPN League Loader issue where teams with byes would cause championship matchups to count as playoff matchups
- Team names are now counted as too similar within a Year if they have the same text minus whitespace and letter case
- Package version updates
- Added a Code of Conduct
- Updated README

## [1.13.0]

- Added Performance model to represent a Team's performance in a given week
- Added method to get a Year by year number to League model
- Added method to get a Team by name to Year model
- Added method to get a Week by week number to Year model
- Added method to get a Matchup with a Team ID to Matchup model
- Added method to split a Matchup model into 2 Performance models to Matchup model
- Added method to get a Performance for a Team ID to Matchup model
- Added validation to ensure no Matchup has 2 of the same Team IDs
- Added a test for Excel

## [1.12.1]

- Fixed bug in the ESPN League Loader where championship weeks could not be added

## [1.12.0]

- Added Excel sheet for each matchup in a year
- Added Excel sheet for each matchup in a league
- Added legend to Excel sheets to show all filters applied to sheet
- Fixed bug where keyword arguments may not work for All Time Teams stat sheet in Excel
- Fixed bug where leagues with some League Median years and some non League Median years would not save to excel
- Improved Excel tests
- Improved filtering flow

## [1.11.0]

- Added All-Time Teams stat sheet to Excel
- Fixed formatting in stats documentation
- Fixed broken link in README
- Updated flow diagram
- Updated setup file to ignore unneeded packages
- Upgraded Sleeper package version
- Better documentation flow for setting up league loaders

## [1.10.0]

- Added Max Scoring Share stat
- Added Min Scoring Share stat
- Added Fleaflicker tag to setup file.

## [1.9.0]

- Added support for Fleaflicker leagues
- Added caching to validation flow, resulting in a ~33% speed increase for stat calculations
- Updated GitHub issue templates

## [1.8.0]

- Added "Total Games" stat for leagues with multiple game sources
- Added "Opponent League Median Wins" in stat sheets and Excel sheets for leagues with League Median Games
- Fixed stat calculations for leagues with League Median Games
- Updated dependency versions to latest
- Removed unused code

## [1.7.0]

- Added YearSettings object that will be used in Year objects to turn on features and stat calculations based on league
  settings
- Added support for League Median Games in stat sheets and Excel sheets
- Added support for League Median Games in Sleeper leagues
- Updated dependency versions to latest
- Updated code documentation

## [1.6.1]

- Now check if a week is completed before adding week for ESPN leagues
- Now check if a week is completed before adding week for MyFantasyLeague leagues

## [1.6.0]

- Buffed setup.py file
- Now freeze team/owner name columns for easier navigating of Excel data
- Now freeze header row for easier navigating of team/owner data
- Now allow users to overwrite an existing Excel file using a keyword argument
- Excel sheets now have consistent row colors
- Excel sheets now dynamically adjust column width

## [1.5.0]

- Added "Games Played" stat to Year and All-Time stats
- Added "Adjusted Team Score" stat to All-Time stats
- Added "Adjusted Team Success" stat to All-Time stats
- Added "Adjusted Team Luck" stat to All-Time stats
- Removed "Team Score" from All-Time stats
- Removed "Team Success" from All-Time stats
- Removed "Team Luck" from All-Time stats

## [1.4.1]

- Fixed bugs so users can now properly add 2 League objects
- Cleaned up examples
- Fixed README

## [1.4.0]

- Added support for multi-week matchup stat calculations
- Added support for multi-week matchups for Sleeper leagues
- Organized parts of README into documentation files
- Updated example files

## [1.3.3]

- Fixed bug that caused Sleeper leagues to not count playoff weeks correctly
- Fixed bug that caused Sleeper leagues to count in-progress matchups as completed matchups
- Now raise an exception for multi-week matchups in Sleeper leagues until the multi-week feature is added to leeger

## [1.3.2]

- Fixed bug that caused Yahoo leagues that had unfinished matchups to raise an exception

## [1.3.1]

- Fixed bug where Yahoo consolation matchups could count as a championship matchup

## [1.3.0]

- Updated versions of dependent libraries
- Added ability to find multiple years for Yahoo leagues

## [1.2.0]

- Added better type checking for validation
- Fixed bug in YahooLeagueLoader that caused tied matchups to raise an exception

## [1.1.1]

- For ESPN leagues, added check for teams on bye week.

## [1.1.0]

- Added way to get League objects in a Python dictionary / JSON via the toJson() method
- Now allow users to turn off validation on methods that use League objects via the `validate=False` keyword argument
- Added a FAQ section to README.md

## [1.0.0]

### Initial Release

[Unreleased]: https://github.com/joeyagreco/leeger/compare/v1.15.0...HEAD

[1.14.0]: https://github.com/joeyagreco/leeger/releases/tag/v1.15.0

[1.14.0]: https://github.com/joeyagreco/leeger/releases/tag/v1.14.0

[1.13.1]: https://github.com/joeyagreco/leeger/releases/tag/v1.13.1

[1.13.0]: https://github.com/joeyagreco/leeger/releases/tag/v1.13.0

[1.12.0]: https://github.com/joeyagreco/leeger/releases/tag/v1.12.0

[1.11.0]: https://github.com/joeyagreco/leeger/releases/tag/v1.11.0

[1.10.0]: https://github.com/joeyagreco/leeger/releases/tag/v1.10.0

[1.9.0]: https://github.com/joeyagreco/leeger/releases/tag/v1.9.0

[1.8.0]: https://github.com/joeyagreco/leeger/releases/tag/v1.8.0

[1.7.0]: https://github.com/joeyagreco/leeger/releases/tag/v1.7.0

[1.6.1]: https://github.com/joeyagreco/leeger/releases/tag/v1.6.1

[1.6.0]: https://github.com/joeyagreco/leeger/releases/tag/v1.6.0

[1.5.0]: https://github.com/joeyagreco/leeger/releases/tag/v1.5.0

[1.4.1]: https://github.com/joeyagreco/leeger/releases/tag/v1.4.1

[1.4.0]: https://github.com/joeyagreco/leeger/releases/tag/v1.4.0

[1.3.3]: https://github.com/joeyagreco/leeger/releases/tag/v1.3.3

[1.3.2]: https://github.com/joeyagreco/leeger/releases/tag/v1.3.2

[1.3.1]: https://github.com/joeyagreco/leeger/releases/tag/v1.3.1

[1.3.0]: https://github.com/joeyagreco/leeger/releases/tag/v1.3.0

[1.2.0]: https://github.com/joeyagreco/leeger/releases/tag/v1.2.0

[1.1.1]: https://github.com/joeyagreco/leeger/releases/tag/v1.1.1

[1.1.0]: https://github.com/joeyagreco/leeger/releases/tag/v1.1.0

[1.0.0]: https://github.com/joeyagreco/leeger/releases/tag/v1.0.0
