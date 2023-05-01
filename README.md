<div align="center">
    <img src="https://raw.githubusercontent.com/joeyagreco/leeger/main/img/leeger-logo-cropped.png" alt="leeger logo" width="300"/>

Instant stats for any fantasy football league.

<a target="_blank" href="https://www.python.org/downloads/" title="Python version"><img src="https://img.shields.io/badge/python-%3E=_3.10-teal.svg"></a>
![Main Build](https://github.com/joeyagreco/leeger/actions/workflows/main-build.yml/badge.svg)
![Last Commit](https://img.shields.io/github/last-commit/joeyagreco/leeger)
</div>

### Table of Contents

- [Overview](https://github.com/joeyagreco/leeger#overview)
- [Quickstart Guide](https://github.com/joeyagreco/leeger#quickstart-guide)
- [FAQ](https://github.com/joeyagreco/leeger#faq)
- [Installation](https://github.com/joeyagreco/leeger#installation)
- [Supported League Loaders](https://github.com/joeyagreco/leeger#supported-league-loaders)
- [Stats Explained](https://github.com/joeyagreco/leeger#stats-explained)
- [Running Tests](https://github.com/joeyagreco/leeger#running-tests)
- [Contributing](https://github.com/joeyagreco/leeger#contributing)
- [License](https://github.com/joeyagreco/leeger#license)
- [Credit](https://github.com/joeyagreco/leeger#credit)

## Overview

![](https://github.com/joeyagreco/leeger/blob/main/img/leeger-overview-transparent.png)
This library allows you to take data from an existing fantasy football league and get instant stats from that league
into either a Python script or an Excel spreadsheet.\
\
This library supports multiple fantasy sites AND manual league data input.\
\
Python stats will be stored in these objects:

- [AllTimeStatSheet](https://github.com/joeyagreco/leeger/blob/main/leeger/model/stat/AllTimeStatSheet.py)
- [YearStatSheet](https://github.com/joeyagreco/leeger/blob/main/leeger/model/stat/YearStatSheet.py)

Excel sheets will include:

- A tab for each year with team stats
- A tab for each year with matchup info
- A tab for all-time with team stats
- A tab for all-time with matchup info
- A tab for all-time with owner stats

\
The main idea behind this library is:

1. Load stats into a League object
2. Pass this League object into various library methods to extract stats

\
For guides on how to use this library, see the information
under [Supported League Loaders](https://github.com/joeyagreco/leeger#supported-league-loaders) and
in the [`example`](https://github.com/joeyagreco/leeger/tree/main/example) folder.

## Quickstart Guide

#### 1. Download Python

- Download the latest _supported_ version of Python [here](https://www.python.org/downloads/release/python-3109/).
- Currently, Python version 3.10+ is supported

#### 2. Create a basic Python file to use this library

- Create a file that ends in the extension ".py"
   - Example: _my_script.py_

#### 3. Download this library

- Navigate in your terminal to the directory where you created your Python script in Step 2
- Run the command `pip install leeger`
   - If you do not have [pip](https://pip.pypa.io/en/stable/) installed, you will need to install it

#### 4. Download your league data using a league loader

- Find the site/s you use for fantasy football [here](https://github.com/joeyagreco/leeger#supported-league-loaders)
- Follow the **Setup Documentation**
- Once you have everything you need for your selected site/s, use the code examples
  found [here](https://github.com/joeyagreco/leeger/tree/main/example/league_loader) for your specific site/s to
  download your league data
   - You can put the code inside the Python script you created in Step 2
- If you have leagues that are continued in multiple sites, you can pull from multiple sites and add the League objects
  together to combine the different sites
   - An example of this can be
     found [here](https://github.com/joeyagreco/leeger/blob/main/example/league/combiningLeagues.py)

#### 5. Run your script

- Navigate in your terminal to the directory where you created your Python script in Step 2
- Run the command `py my_script.py`
   - Replace _my_script.py_ with whatever you named your script in Step 2

#### 6. Load your league stats into Excel

- Slightly alter your script from Step 2 to include a function call to load your league stats into Excel
- Follow [this example](https://github.com/joeyagreco/leeger/blob/main/example/stat/statsToExcelExample.py)
- Make sure that you are passing the League object that you pulled from the league loader/s into the function call to
  put your stats into Excel

## FAQ

**Question:**
I'm getting this error when I run my script:
<!---
// @formatter:off
-->
```python3
TypeError: dataclass() got an unexpected keyword argument 'kw_only'
```
<!---
// @formatter:on
-->

**Answer:**
This error occurs when the Python version you are using is not 3.10 or greater.\
Make sure you are using Python version 3.10 or a newer version.

**Q:**
How do I use this library to pull stats from my online fantasy league?

**A:**

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
An example of this can be
found [here](https://github.com/joeyagreco/leeger/blob/main/example/league/combiningLeagues.py).
___
**Q:**
Can I disable validation on my League object?

**A:**
Yes. While it is not recommended that you disable this, as validation ensures the stats are calculated properly,
disabling validation can be done by passing `validate=False` into any method that takes a League object OR any `loadLeague()` method from a League Loader.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install.

```bash
pip install leeger
```

## Supported League Loaders

Sites that you can automatically load your league data from.

| Name            | Website                                   | Supported          | Setup Documentation                                                                                                       |
|-----------------|-------------------------------------------|--------------------|---------------------------------------------------------------------------------------------------------------------------|
| ESPN            | https://www.espn.com/fantasy/football/    | :heavy_check_mark: | [ESPN :page_facing_up:](https://github.com/joeyagreco/leeger/blob/main/doc/league_loader/espn.md)                         |
| Fleaflicker     | https://www.fleaflicker.com/              | :heavy_check_mark: | [Fleaflicker :page_facing_up:](https://github.com/joeyagreco/leeger/blob/main/doc/league_loader/fleaflicker.md)           |  
| MyFantasyLeague | http://home.myfantasyleague.com/          | :heavy_check_mark: | [MyFantasyLeague :page_facing_up:](https://github.com/joeyagreco/leeger/blob/main/doc/league_loader/my_fantasy_league.md) |
| NFL             | https://fantasy.nfl.com/                  | :x:                | :x:                                                                                                                       |
| Sleeper         | https://sleeper.com/fantasy-football/     | :heavy_check_mark: | [Sleeper :page_facing_up:](https://github.com/joeyagreco/leeger/blob/main/doc/league_loader/sleeper.md)                   |
| Yahoo           | https://football.fantasysports.yahoo.com/ | :heavy_check_mark: | [Yahoo :page_facing_up:](https://github.com/joeyagreco/leeger/blob/main/doc/league_loader/yahoo.md)                       |
<!---
// @formatter:off
-->
If a fantasy site you use is not listed here and you would like it to be, please [open an issue](https://github.com/joeyagreco/leeger/issues/new/choose).
<!---
// @formatter:on
-->

## Stats Explained

Stats used in this library are
documented [here](https://github.com/joeyagreco/leeger/blob/main/doc/stats.md).

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
- [fleaflicker](https://github.com/joeyagreco/fleaflicker)
- [pymfl](https://github.com/joeyagreco/pymfl)
- [sleeper](https://github.com/joeyagreco/sleeper)
- [YahooFantasy](https://github.com/mattdodge/yahoofantasy)