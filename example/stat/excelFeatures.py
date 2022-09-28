from leeger.league_loader import ESPNLeagueLoader
from leeger.model.league import League
from leeger.util.excel import leagueToExcel

if __name__ == '__main__':
    # Get a dummy League object
    espnLeagueLoader = ESPNLeagueLoader("12345678", [2019, 2020, 2021, 2022])
    league: League = espnLeagueLoader.loadLeague()

    # Overwrite an existing file by using the 'overwrite' keyword argument
    leagueToExcel(league, "C:\\myLeagueStats.xlsx", overwrite=True)
