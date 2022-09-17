from leeger.league_loader import ESPNLeagueLoader
from leeger.model.league import League, Year
from leeger.util.excel import leagueToExcel, yearToExcel

if __name__ == '__main__':
    # Get a League object.
    # There are many ways to get a League object, here we will just grab one using the ESPN League Loader.
    espnLeagueLoader = ESPNLeagueLoader("12345678", [2019, 2020, 2021, 2022])
    league: League = espnLeagueLoader.loadLeague()

    # Save league stats to an Excel sheet.
    leagueToExcel(league, "C:\\myLeagueStats.xlsx")

    # Get a Year object.
    # Let's get the 2019 year.
    year2019: Year = league.years[0]

    # Save year stats to an Excel sheet.
    yearToExcel(year2019, "C:\\my2019YearStats.xlsx")
