# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

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

[Unreleased]: https://github.com/joeyagreco/leeger/compare/v1.4.1...HEAD

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
