from leeger.league_loader import SleeperLeagueLoader
from leeger.model.league import League

if __name__ == '__main__':
    # Get a League object with years 2019 and 2020 for Sleeper league with ID: "12345678".
    sleeperLeagueLoader = SleeperLeagueLoader("12345678", [2019, 2020])
    league: League = sleeperLeagueLoader.loadLeague()
