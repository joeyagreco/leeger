from leeger.league_loader import ESPNLeagueLoader
from leeger.model.league import League
from leeger.util.excel import leagueToExcel

if __name__ == '__main__':
    # set owner aliases
    owner_names_and_aliases = {}
    # 2022
    espnS2 = "AEBjprYwy3wZjmCckUtYkkcli63EkxZ9zWJbkk2DC%2Fto9iox8IjldIhQ5VZ3A6GBi1EdH%2BginLdmbYV1FHTD96R7aFDRKGxZhaJUZAIXwOPm2gQzil4IG8dlGv7Q5hH3Vfjv%2BkFeBxUdklgtco3nfYdTOGaikOThLPCyc%2B1rMOOpl2PcriG9kg0nkpLIXXG%2BCMXwQWe18f73viWdJfX7k8MUb%2BMr8uJ5SsK5NFQ%2FqG1aMTtA8o1nl77wsxON99SBhL6lnYLZG2iHxyXSk5IFMvF7"
    swid = "{0C9373C9-B9C6-4053-9373-C9B9C6505338}"
    espn_league_loader = ESPNLeagueLoader("379727601", [2022], espnS2=espnS2, swid=swid,
                                          ownerNamesAndAliases=owner_names_and_aliases)
    league: League = espn_league_loader.loadLeague()

    leagueToExcel(league, "H:\\Desktop-HDD\\uline_stats_regular_season.xlsx", onlyRegularSeason=True, overwrite=True)
