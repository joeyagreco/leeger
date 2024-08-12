from leeger.model.league import Year, YearSettings

if __name__ == "__main__":
    # Year Settings are settings for each year in a league that represent features of the league.
    # By default, all League objects have a YearSettings object with all features turned off.

    # To turn on League Median Games in a league for a given year,
    # simply turn the feature on in the YearSettings object and pass it into any Year object you would like to apply the settings to.
    yearSettings = YearSettings(leagueMedianGames=True)
    year = Year(yearNumber=2020, teams=list(), weeks=list(), yearSettings=yearSettings)

    # The YearSettings object can be used for multiple years if desired
    anotherYear = Year(
        yearNumber=2021, teams=list(), weeks=list(), yearSettings=yearSettings
    )
