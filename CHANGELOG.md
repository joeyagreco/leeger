# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

- N/A

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

[Unreleased]: https://github.com/joeyagreco/leeger/compare/v1.3.1...HEAD

[1.3.1]: https://github.com/joeyagreco/leeger/releases/tag/v1.3.1

[1.3.0]: https://github.com/joeyagreco/leeger/releases/tag/v1.3.0

[1.2.0]: https://github.com/joeyagreco/leeger/releases/tag/v1.2.0

[1.1.1]: https://github.com/joeyagreco/leeger/releases/tag/v1.1.1

[1.1.0]: https://github.com/joeyagreco/leeger/releases/tag/v1.1.0

[1.0.0]: https://github.com/joeyagreco/leeger/releases/tag/v1.0.0
