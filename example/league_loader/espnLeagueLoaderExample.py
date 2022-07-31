from leeger import ESPNLeagueLoader, League

# PUBLIC LEAGUE
# Get a League object with years 2019 and 2020 for ESPN league with ID: "12345678".
espnLeagueLoader = ESPNLeagueLoader("12345678", [2019, 2020])
league: League = espnLeagueLoader.loadLeague()

# PRIVATE LEAGUE
# You will need the ESPN_S2 and SWID parameters to retrieve a private league.
# To retrieve these, follow these steps:
# 1. Visit your main league page (i.e. https://fantasy.espn.com/football/team?leagueId=12345678seasonId=2020)
# 2. Make sure you are logged in.
# 3. Open Developer Tools (on Chrome/Firefox, right-click anywhere on the page and select Inspect Element)
# 4. Go to Storage (for Firefox) or Application (for Chrome) and browse the Cookies available for fantasy.espn.com
# 5. The values you need are called "SWID" and "ESPN_S2". You can right-click and copy the values from here.
# Get a League object with years 2019 and 2020 for ESPN league with ID: "12345678".
espnS2 = "ABCDEFG1234567"
swid = "{ABC-DEF-GHI-JKL-MNOP}"
espnLeagueLoader = ESPNLeagueLoader("12345678", [2019, 2020], espnS2=espnS2, swid=swid)
league: League = espnLeagueLoader.loadLeague()

# Sometimes the same owner will have a different name in different years.
# Here, the same owner has "John Smith" and "Johnny Smith" as their owner names in ESPN.
# To let the library know that you want these owners to be evaluated as the same owner,
# a dictionary with the desired owner name and their aliases can be passed in.
ownerNamesAndAliases = {"John Smith": ["John Smith", "Johnny Smith"]}
espnLeagueLoader = ESPNLeagueLoader("12345678", [2019, 2020], ownerNamesAndAliases=ownerNamesAndAliases)
league: League = espnLeagueLoader.loadLeague()
