# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

- Added "Total Games" stat for leagues with multiple game sources
- Added "Opponent League Median Wins" in stat sheets and Excel sheets for leagues with League Median Games
- Fixed stat calculations for leagues with League Median Games
- Removed unused code
- Updated dependency versions to latest

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

[Unreleased]: https://github.com/joeyagreco/leeger/compare/v1.7.0...HEAD

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
