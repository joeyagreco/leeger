import leeger

if __name__ == "__main__":
    # You will need an application registered on the Yahoo Developer Site: https://developer.yahoo.com/apps/.
    # You will need your client ID and secret.
    # The app only needs to have read permissions.
    # The app will need to have a callback/redirect URI of https://localhost:8000

    # Get a League object with years 2019 and 2020 for Yahoo league with ID: 123456.
    clientId = "myClientId"
    clientSecret = "myClientSecret"
    league = leeger.YahooLeagueLoader.loadLeague(123456, [2019, 2020], clientId=clientId, clientSecret=clientSecret,
                                                 loginTimeoutSeconds=4)

    # Save league stats to an Excel sheet.
    league.toExcel("C:\\myLeagueStats.xlsx")

    # When you load your Yahoo league, it will attempt to authenticate based on your client ID and client secret.
    # You can set a timeout for this by passing in loginTimeoutSeconds.
    clientId = "myClientId"
    clientSecret = "myClientSecret"
    league = leeger.YahooLeagueLoader.loadLeague(123456, [2019, 2020], clientId=clientId, clientSecret=clientSecret,
                                                 loginTimeoutSeconds=4)
