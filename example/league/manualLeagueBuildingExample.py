from leeger import Owner, Team, Matchup, Week, Year, League

if __name__ == "__main__":
    # Build a league manually.

    # Create owners.
    # One owner can have multiple teams (1 per year) but a team can only have 1 owner.
    ownerFrankie = Owner(name="Frankie")
    ownerMonika = Owner(name="Monika")
    ownerJoseph = Owner(name="Joseph")
    ownerVincent = Owner(name="Vincent")
    ownerGiovanna = Owner(name="Giovanna")
    ownerDominic = Owner(name="Dominic")

    # Create teams for 2019 season
    # Use the owner IDs for that team's owner when creating a team.
    teamFrankie2019 = Team(ownerId=ownerFrankie.id, name="Basil Bombers")
    teamMonika2019 = Team(ownerId=ownerMonika.id, name="Philosopher's Thrown")
    teamJoseph2019 = Team(ownerId=ownerJoseph.id, name="Leeger Legends")
    teamVincent2019 = Team(ownerId=ownerVincent.id, name="Team 300")
    teamGiovanna2019 = Team(ownerId=ownerGiovanna.id, name="High Notes")
    teamDominic2019 = Team(ownerId=ownerDominic.id, name="Bike Ridas")

    # Create matchups for week 1.
    # Use the team IDs when creating a matchup.
    matchup1 = Matchup(teamAId=teamFrankie2019.id, teamBId=teamDominic2019.id, teamAScore=101.2, teamBScore=122)
    matchup2 = Matchup(teamAId=teamMonika2019.id, teamBId=teamGiovanna2019.id, teamAScore=78.4, teamBScore=114.3)
    matchup3 = Matchup(teamAId=teamJoseph2019.id, teamBId=teamVincent2019.id, teamAScore=112, teamBScore=145.3)

    # Create week 1 with matchups.
    week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])

    # Create the 2019 year (season).
    year2019 = Year(yearNumber=2019, teams=[teamFrankie2019,
                                            teamMonika2019,
                                            teamJoseph2019,
                                            teamVincent2019,
                                            teamGiovanna2019,
                                            teamDominic2019],
                    weeks=[week1])

    # Create the league.
    league = League(name="G League",
                    owners=[ownerFrankie,
                            ownerMonika,
                            ownerJoseph,
                            ownerVincent,
                            ownerGiovanna,
                            ownerDominic],
                    years=[year2019])
