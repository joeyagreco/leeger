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
    - [ESPN](https://github.com/joeyagreco/leeger#espn)
    - [MyFantasyLeague](https://github.com/joeyagreco/leeger#myfantasyleague)
    - [Sleeper](https://github.com/joeyagreco/leeger#sleeper)
    - [Yahoo](https://github.com/joeyagreco/leeger#yahoo)
- [Stats Explained](https://github.com/joeyagreco/leeger#stats-explained)
    - [AWAL](https://github.com/joeyagreco/leeger#awal)
    - [Margins of Victory](https://github.com/joeyagreco/leeger#margins-of-victory)
    - [Max Score](https://github.com/joeyagreco/leeger#max-score)
    - [Min Score](https://github.com/joeyagreco/leeger#min-score)
    - [Plus/Minus](https://github.com/joeyagreco/leeger#plusminus)
    - [Points Scored](https://github.com/joeyagreco/leeger#points-scored)
    - [Scoring Share](https://github.com/joeyagreco/leeger#scoring-share)
    - [Scoring Standard Deviation](https://github.com/joeyagreco/leeger#scoring-standard-deviation)
    - [Smart Wins](https://github.com/joeyagreco/leeger#smart-wins)
    - [Team Luck](https://github.com/joeyagreco/leeger#team-luck)
    - [Team Score](https://github.com/joeyagreco/leeger#team-score)
    - [Team Success](https://github.com/joeyagreco/leeger#team-success)
    - [WAL](https://github.com/joeyagreco/leeger#wal)
    - [Win Percentage](https://github.com/joeyagreco/leeger#win-percentage)
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

| Name                                                                    | Website                                   | Supported          |
|-------------------------------------------------------------------------|-------------------------------------------|--------------------|
| [ESPN](https://github.com/joeyagreco/leeger#espn)                       | https://www.espn.com/fantasy/football/    | :heavy_check_mark: |
| [MyFantasyLeague](https://github.com/joeyagreco/leeger#myfantasyleague) | http://home.myfantasyleague.com/          | :heavy_check_mark: |
| NFL                                                                     | https://fantasy.nfl.com/                  | :x:                |
| [Sleeper](https://github.com/joeyagreco/leeger#sleeper)                 | https://sleeper.com/fantasy-football      | :heavy_check_mark: |
| [Yahoo](https://github.com/joeyagreco/leeger#yahoo)                     | https://football.fantasysports.yahoo.com/ | :heavy_check_mark: |

<!---
// @formatter:off
-->
If a fantasy site you use is not listed here and you would like it to be, please [open an issue](https://github.com/joeyagreco/leeger/issues/new/choose).
<!---
// @formatter:on
-->

> ### ESPN
> ___
>
> ##### [Examples](https://github.com/joeyagreco/leeger/blob/main/example/league_loader/espnLeagueLoaderExample.py)
>
> ##### League Info Needed [PUBLIC LEAGUE]
>
> - League ID
>
> ##### League Info Needed [PRIVATE LEAGUE]
>
> - League ID
> - ESPN_S2 parameter
> - SWID parameter
>
> [How to find your ESPN league ID.](https://support.espn.com/hc/en-us/articles/360045432432-League-ID#h_01F10X0506BC0R0MYNH6VMNZ04)
>
> To retrieve ESPN_S2 and SWID, follow these steps:
>
> 1. Visit your main league page (
     > i.e. https://fantasy.espn.com/football/team?leagueId={your_league_id}seasonId={any_season})
> 2. Make sure you are logged in.
> 3. Open Developer Tools (on Chrome/Firefox, right-click anywhere on the page and select Inspect Element)
> 4. Go to Storage (for Firefox) or Application (for Chrome) and browse the Cookies available for fantasy.espn.com
> 5. The values you need are called "SWID" and "ESPN_S2". You can right-click and copy the values from here.

> ### MyFantasyLeague
> ___
>
> ##### [Examples](https://github.com/joeyagreco/leeger/blob/main/example/league_loader/myFantasyLeagueLeagueLoaderExample.py)
>
> ##### League Info Needed
>
> - League ID
> - MFL Username
> - MFL Password
> - MFL User Agent Name
>
> [How to find your MyFantasyLeague league ID.](https://www.dynastyassistant.com/faq#:~:text=Visit%20your%20league's%20homepage%20and,example%20is%20your%20league's%20ID.)
>
> To set up your MyFantasyLeague account, follow these steps:
>
> - Register a client via
    the [API Client Registration Page](http://www.myfantasyleague.com/current_year/csetup?C=APICLI) (replace "
    current_year" with the current year)
> - Set up your API Client, making sure that:\
    - Client Purpose = "Data Collection"\
    - Client User Agent is set (remember what this is as you will need it for the League Loader)\
    - Authorized Users has *at least* your MFL username
> - Validate your client by selecting "Validate" for your newly-created client under "Configured Clients".\
    - This will allow you to validate your API Client via text message.

> ### Sleeper
> ___
>
> ##### [Examples](https://github.com/joeyagreco/leeger/blob/main/example/league_loader/sleeperLeagueLoaderExample.py)
>
> ##### League Info Needed
>
> - League ID
>
> [How to find your Sleeper league ID.](https://support.sleeper.app/en/articles/4121798-how-do-i-find-my-league-id)

> ### Yahoo
> ___
>
> ##### [Examples](https://github.com/joeyagreco/leeger/blob/main/example/league_loader/yahooLeagueLoaderExample.py)
>
> ##### League Info Needed
>
> - League ID
> - Client ID
> - Client secret
>
> [How to find your Yahoo league ID.](https://help.yahoo.com/kb/fantasy-football/find-league-group-number-sln8238.html)
>
> To set up your Yahoo account, follow these steps:
>
> - Register a new application on the [Yahoo Developer Site](https://developer.yahoo.com/apps/)
> - Retrieve the Client ID and Client secret for the application
> - Set the callback/redirect URI of the application to: https://localhost:8000
> - Make sure the application has READ permissions
>
> ##### Notes
>
> - When the Yahoo League Loader is run, Yahoo OAuth will open up a new tab in a browser. You can close this tab.

## Stats Explained

Stats used in this library are documented [here]().

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