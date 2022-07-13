from leeger import ESPNLeagueLoader

if __name__ == "__main__":
    # Get a League object.
    # There are many ways to get a League object, here we will just grab one using the ESPN League Loader
    league = ESPNLeagueLoader.loadLeague(12345678, [2019])

    # To get all stats for this league, simply access the stat sheet.
    leagueStats = league.statSheet()
