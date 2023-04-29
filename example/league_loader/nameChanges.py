from leeger.league_loader import ESPNLeagueLoader, SleeperLeagueLoader
from leeger.model.league import League

if __name__ == "__main__":
    # The below examples can be done with ANY league loader.

    # Sometimes the same owner will have a different name in different years.
    # Here, the same owner has "John Smith" and "Johnny Smith" as their owner names on ESPN.
    # To let the library know that you want these owners to be evaluated as the same owner,
    # a dictionary with the desired owner name and their aliases can be passed in.

    ownerNamesAndAliases = {"John Smith": ["John Smith", "Johnny Smith"]}
    espnLeagueLoader = ESPNLeagueLoader(
        "12345678", [2019, 2020], ownerNamesAndAliases=ownerNamesAndAliases
    )
    league: League = espnLeagueLoader.loadLeague()

    # This can also be used to change an owner name from what it is on a particular site.
    # Here, an owner has the name "Mr. Bunny" as their owner name on Sleeper.
    # They would like their owner name to be loaded as "Bugs Bunny" instead.
    # To let the library know that you want this change,
    # a dictionary with the desired owner name and the site-known name (alias) can be passed in.

    ownerNamesAndAliases = {"Bugs Bunny": ["Mr. Bunny"]}
    sleeperLeagueLoader = SleeperLeagueLoader(
        "12345678", [2019, 2020], ownerNamesAndAliases=ownerNamesAndAliases
    )
    league: League = sleeperLeagueLoader.loadLeague()
