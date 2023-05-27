from leeger.league_loader.ESPNLeagueLoader import ESPNLeagueLoader

from leeger.model.league import League

if __name__ == "__main__":
    # to compare a League model (or any of its child models) you can use .equals()

    # 1. take any model (let's get a dummy League) for an example
    espnLeagueLoader = ESPNLeagueLoader("12345678", [2019, 2020])
    league: League = espnLeagueLoader.loadLeague()

    # 2. lets compare it
    league.equals(league)  # compares models with all fields
    league.equals(league, ignoreBaseIds=True)  # ignores the base "id" field in each object
    league.equals(
        league, ignoreIds=True
    )  # ignores fields that hold an id but not the base "id" fields
    league.equals(
        league, logDifferences=True
    )  # logs all differences IF the equality check is False

    # 3. you can also use "=="
    league == league  # compares models using all of the .equals() defaults
