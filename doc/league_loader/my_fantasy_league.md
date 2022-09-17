# MyFantasyLeague

___

##### [Examples](https://github.com/joeyagreco/leeger/blob/main/example/league_loader/myFantasyLeagueLeagueLoaderExample.py)

##### League Info Needed

- League ID
- MFL Username
- MFL Password
- MFL User Agent Name

[How to find your MyFantasyLeague league ID.](https://www.dynastyassistant.com/faq#:~:text=Visit%20your%20league's%20homepage%20and,example%20is%20your%20league's%20ID.)

To set up your MyFantasyLeague account, follow these steps:

- Register a client via
  the [API Client Registration Page](http://www.myfantasyleague.com/current_year/csetup?C=APICLI) (replace "
  current_year" with the current year)
- Set up your API Client, making sure that:
    - Client Purpose = "Data Collection"
    - Client User Agent is set (remember what this is as you will need it for the League Loader)
    - Authorized Users has *at least* your MFL username
- Validate your client by selecting "Validate" for your newly-created client under "Configured Clients".
    - This will allow you to validate your API Client via text message.