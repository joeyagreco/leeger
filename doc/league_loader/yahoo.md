## Yahoo

___

##### [Examples](https://github.com/joeyagreco/leeger/blob/main/example/league_loader/yahooLeagueLoaderExample.py)

##### League Info Needed

- League ID
- Client ID
- Client secret

[How to find your Yahoo league ID.](https://help.yahoo.com/kb/fantasy-football/find-league-group-number-sln8238.html)

To set up your Yahoo account, follow these steps:

- Register a new application on the [Yahoo Developer Site](https://developer.yahoo.com/apps/)
- Retrieve the Client ID and Client secret for the application
- Set the callback/redirect URI of the application to: https://localhost:8000
- Make sure the application has READ permissions

##### Notes

- When the Yahoo League Loader is run, Yahoo OAuth will open up a new tab in a browser. You can close this tab.
