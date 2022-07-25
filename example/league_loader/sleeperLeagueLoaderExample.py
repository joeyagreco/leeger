from leeger import SleeperLeagueLoader

if __name__ == "__main__":
    # Get a League object with all years for Sleeper league with ID: "12345678".
    league = SleeperLeagueLoader.loadLeague("12345678")

    # Save league stats to an Excel sheet.
    league.toExcel("C:\\myLeagueStats.xlsx")
