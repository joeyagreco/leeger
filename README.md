<div align="center">
    <img src="https://raw.githubusercontent.com/joeyagreco/leeger/main/img/leeger-logo-cropped.png" alt="leeger logo" width="300"/>

Instant stats for your fantasy football league.

<a target="_blank" href="https://www.python.org/downloads/" title="Python version"><img src="https://img.shields.io/badge/python-%3E=_3.10-teal.svg"></a>
![Main Build](https://github.com/joeyagreco/leeger/actions/workflows/main-build.yml/badge.svg)
![Last Commit](https://img.shields.io/github/last-commit/joeyagreco/leeger)
</div>

### Table of Contents

- [Overview](https://github.com/joeyagreco/leeger#overview)
- [FAQ](https://github.com/joeyagreco/leeger#faq)
- [Installation](https://github.com/joeyagreco/leeger#installation)
- [Supported League Loaders](https://github.com/joeyagreco/leeger#supported-league-loaders)
- [Stats Explained](https://github.com/joeyagreco/leeger#stats-explained)
- [Running Tests](https://github.com/joeyagreco/leeger#running-tests)
- [Contributing](https://github.com/joeyagreco/leeger#contributing)
- [License](https://github.com/joeyagreco/leeger#license)
- [Credit](https://github.com/joeyagreco/leeger#credit)

## Overview

![](https://raw.githubusercontent.com/joeyagreco/leeger/main/img/library-overview.png)
This library allows you to take data from an existing fantasy football league and get instant stats from that league
into either a Python script or an Excel spreadsheet.\
\
This library supports multiple fantasy sites AND manual league data input.\
\
Python stats will be stored in these objects:

- [AllTimeStatSheet](https://github.com/joeyagreco/leeger/blob/main/leeger/model/stat/AllTimeStatSheet.py)
- [YearStatSheet](https://github.com/joeyagreco/leeger/blob/main/leeger/model/stat/YearStatSheet.py)

Excel sheets will include:

- A tab with stats for each year the league has existed
- A tab with all-time stats for the league
- Sortable rows for each team and owner

\
The main idea behind this library is:

1. Load stats into a League object
2. Pass this League object into various library methods to extract stats

\
For guides on how to use this library, see the information
under [Supported League Loaders](https://github.com/joeyagreco/leeger#supported-league-loaders) and
in the [`example`](https://github.com/joeyagreco/leeger/tree/main/example) folder.

## FAQ

**Question:**
How do I use this library to pull stats from my online fantasy league?

**Answer:**

1. Find your fantasy site [here](https://github.com/joeyagreco/leeger#supported-league-loaders) and ensure you have
   everything you need for the site you are using
2. Follow the [example code snippets](https://github.com/joeyagreco/leeger/tree/main/example/league_loader) for your
   fantasy site to load the League object

___
**Q:**
How can I get stats into Excel once I have my League object?

**A:**
Follow [this example code](https://github.com/joeyagreco/leeger/blob/main/example/stat/statsToExcelExample.py).
___
**Q:**
Can I combine years from different fantasy sites that are loaded as separate League objects into a single League object?

**A:**
Yes, the League object supports addition (+) to combine multiple league objects.\
An example of this can be found [here](https://github.com/joeyagreco/leeger/blob/main/example/league/leagueFeatures.py).
___
**Q:**
Can I disable validation on my League object?

**A:**
Yes. While it is not recommended that you disable this, as validation ensures the stats are calculated properly,
disabling validation can be done by passing `validate=False` into any method that takes a League object.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install.

```bash
pip install leeger
```

## Supported League Loaders

Sites that you can automatically load your league data from.

| Name       | Website                                   | Supported          | Setup Documentation                                                               |
|------------|-------------------------------------------|--------------------|-----------------------------------------------------------------------------------|
| ESPN       | https://www.espn.com/fantasy/football/    | :heavy_check_mark: | [ESPN](https://github.com/joeyagreco/leeger/blob/doc/league_loader/espn.md)       |
| NFL        | https://fantasy.nfl.com/                  | :x:                | N/A                                                                               |
| Sleeper    | https://sleeper.com/fantasy-football      | :heavy_check_mark: | [Sleeper](https://github.com/joeyagreco/leeger/blob/doc/league_loader/sleeper.md) |
| Yahoo      | https://football.fantasysports.yahoo.com/ | :heavy_check_mark: | [Yahoo](https://github.com/joeyagreco/leeger/blob/doc/league_loader/yahoo.md)     |

:page_facing_up:
<!---
// @formatter:off
-->
If a fantasy site you use is not listed here and you would like it to be, please [open an issue](https://github.com/joeyagreco/leeger/issues/new/choose).
<!---
// @formatter:on
-->

## Stats Explained

Stats used in this library are
documented [here](https://github.com/joeyagreco/leeger/blob/multi-week-matchup-stat-support/doc/stats.md).

## Running Tests

To run tests, run the following command:

```bash
  pytest
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Credit

- [ESPN API](https://github.com/cwendt94/espn-api)
- [ESPN Private Leagues](https://cran.r-project.org/web/packages/ffscrapr/vignettes/espn_authentication.html)
- [YahooFantasy](https://github.com/mattdodge/yahoofantasy)