from leeger.league_loader import ESPNLeagueLoader

# Get a League object.
# There are many ways to get a League object, here we will just grab one using the ESPN League Loader.
espnLeagueLoader = ESPNLeagueLoader("12345678", [2019, 2020, 2021, 2022])
league = espnLeagueLoader.loadLeague()

# Save league stats to an Excel sheet.
league.toExcel("C:\\myLeagueStats.xlsx")

# Get a Year object.
# Let's get the 2019 year.
year = league.years[0]

# Save year stats to an Excel sheet.
league.toExcel("C:\\myLeagueStats.xlsx")
