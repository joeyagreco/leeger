from leeger.league_loader.FleaflickerLeagueLoader import FleaflickerLeagueLoader
from leeger.model.league import League

if __name__ == '__main__':
    # Get a League object with year 2020 for Fleaflicker league with ID: "12345678".
    fleaflickerLeagueLoader = FleaflickerLeagueLoader("12345678", [2020])
    league: League = fleaflickerLeagueLoader.loadLeague()
