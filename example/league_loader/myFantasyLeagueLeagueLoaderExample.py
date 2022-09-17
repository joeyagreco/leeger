from leeger.league_loader import MyFantasyLeagueLeagueLoader
from leeger.model.league import League

if __name__ == '__main__':
    # You will need to log into your MyFantasyLeague account for the following setup.
    # More info on this process can be found at: https://api.myfantasyleague.com/{current_year}/api_info
    # Register a client via the API Client Registration Page: http://www.myfantasyleague.com/{current_year}/csetup?C=APICLI
    # Set up your API Client, making sure that:
    #   - Client Purpose = "Data Collection"
    #   - Client User Agent is set (remember what this is as you will need it for the League Loader)
    #   - Authorized Users has at least your MFL username
    # Validate your client by selecting "Validate" for your newly-created client under "Configured Clients".
    #   - This will validate your client by validating via text message.

    # Get a League object with years 2019 and 2020 for MyFantasyLeague league with ID: "123456".

    MFL_USERNAME = "myUsername"  # The username for your MFL account.
    MFL_PASSWORD = "myPassword"  # The password for your MFL account.
    MFL_USER_AGENT_NAME = "myUserAgentName"  # The Client User Agent you set for your API Client.
    LEAGUE_ID = "123456"

    myFantasyLeagueLoader = MyFantasyLeagueLeagueLoader(LEAGUE_ID,
                                                        [2019, 2020],
                                                        mflUsername=MFL_USERNAME,
                                                        mflPassword=MFL_PASSWORD,
                                                        mflUserAgentName=MFL_USER_AGENT_NAME)
    league: League = myFantasyLeagueLoader.loadLeague()
