from leeger.league_loader import ESPNLeagueLoader, SleeperLeagueLoader
from leeger.model.league import League

if __name__ == '__main__':
    # Sometimes, you may want to combine League objects.
    # This may be because you switched fantasy sites and now the league data is split across different sites.
    # You can combine League objects to solve this issue.

    # Say you had a league that had years 2019-2020 on ESPN and years 2021-2022 on Sleeper and you wanted to create a single League object for those years.

    # First, get League from ESPN for 2019-2020.
    espnLeagueLoader = ESPNLeagueLoader("12345678", [2019, 2020])
    espnLeague: League = espnLeagueLoader.loadLeague()

    # Second, get League from Sleeper for 2021-2022.
    sleeperLeagueLoader = SleeperLeagueLoader("12345678", [2021, 2022])
    sleeperLeague: League = sleeperLeagueLoader.loadLeague()

    # Finally, combine the leagues to get a single League object.
    myLeague = espnLeague + sleeperLeague

    #   Special behaviors:
    #       - name
    #           - "name" will become a combination of both league's names IF the names are not the same.
    #       - owners
    #           - "owners" will be merged on Owner.name, since this field must be unique by League.
    #           - Unmerged owners will simply be combined.
    #       - years
    #           - "years" will be combined in order oldestYearNumber -> newestYearNumber.
    #           - Duplicate Year.yearNumber across leagues will raise an exception.
