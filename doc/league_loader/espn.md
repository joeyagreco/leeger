# ESPN

___

##### [Examples](https://github.com/joeyagreco/leeger/blob/main/example/league_loader/espnLeagueLoaderExample.py)

##### League Info Needed [PUBLIC LEAGUE]

- League ID

##### League Info Needed [PRIVATE LEAGUE]

- League ID
- ESPN_S2 parameter
- SWID parameter

[How to find your ESPN league ID.](https://support.espn.com/hc/en-us/articles/360045432432-League-ID#h_01F10X0506BC0R0MYNH6VMNZ04)

To retrieve ESPN_S2 and SWID, follow these steps:

1. Visit your main league page (
   i.e. https://fantasy.espn.com/football/team?leagueId={your_league_id}seasonId={any_season})
2. Make sure you are logged in.
3. Open Developer Tools (on Chrome/Firefox, right-click anywhere on the page and select Inspect Element)
4. Go to Storage (for Firefox) or Application (for Chrome) and browse the Cookies available for fantasy.espn.com
5. The values you need are called "SWID" and "ESPN_S2". You can right-click and copy the values from here.

### [Code Template for ESPN](https://github.com/joeyagreco/leeger/blob/main/example/league_loader/espnLeagueLoaderExample.py)