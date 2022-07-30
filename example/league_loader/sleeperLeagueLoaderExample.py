from leeger import SleeperLeagueLoader

if __name__ == "__main__":
    # Get a League object with all years for Sleeper league with ID: "12345678".
    sleeperLeagueLoader = SleeperLeagueLoader("12345678")
    league = sleeperLeagueLoader.loadLeague()

    # Save league stats to an Excel sheet.
    league.toExcel("C:\\myLeagueStats.xlsx")

    # Sometimes the same owner will have a different name in different years.
    # Here, the same owner has "John Smith" and "Johnny Smith" as their owner names in Sleeper.
    # To let the library know that you want these owners to be evaluated as the same owner,
    # a dictionary with the desired owner name and their aliases can be passed in.
    ownerNamesAndAliases = {"John Smith": ["John Smith", "Johnny Smith"]}
    sleeperLeagueLoader = SleeperLeagueLoader("12345678", ownerNamesAndAliases=ownerNamesAndAliases)
    league = sleeperLeagueLoader.loadLeague()
