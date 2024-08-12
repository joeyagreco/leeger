from leeger.enum import MatchupType
from leeger.model.league import League, Matchup, Owner, Team, Week, Year, YearSettings
from leeger.model.league.Division import Division

ownerFrankie = Owner(name="Frankie")
ownerMonika = Owner(name="Monika")
ownerJoseph = Owner(name="Joseph")
ownerVincent = Owner(name="Vincent")
ownerGiovanna = Owner(name="Giovanna")
ownerDominic = Owner(name="Dominic")

teamFrankie2019 = Team(ownerId=ownerFrankie.id, name="Basil Bombers")
teamMonika2019 = Team(ownerId=ownerMonika.id, name="Philosopher's Thrown")
teamJoseph2019 = Team(ownerId=ownerJoseph.id, name="Leeger Legends")
teamVincent2019 = Team(ownerId=ownerVincent.id, name="Team 300")
teamGiovanna2019 = Team(ownerId=ownerGiovanna.id, name="High Notes")
teamDominic2019 = Team(ownerId=ownerDominic.id, name="Bike Ridas")

matchup1 = Matchup(
    teamAId=teamFrankie2019.id,
    teamBId=teamDominic2019.id,
    teamAScore=101.2,
    teamBScore=122,
)
matchup2 = Matchup(
    teamAId=teamMonika2019.id,
    teamBId=teamGiovanna2019.id,
    teamAScore=78.4,
    teamBScore=114.3,
)
matchup3 = Matchup(
    teamAId=teamJoseph2019.id,
    teamBId=teamVincent2019.id,
    teamAScore=112,
    teamBScore=145.3,
)

matchup4 = Matchup(
    teamAId=teamFrankie2019.id,
    teamBId=teamDominic2019.id,
    teamAScore=98.6,
    teamBScore=109.3,
    matchupType=MatchupType.PLAYOFF,
    multiWeekMatchupId="1",
)
matchup5 = Matchup(
    teamAId=teamMonika2019.id,
    teamBId=teamGiovanna2019.id,
    teamAScore=118.4,
    teamBScore=106.1,
    matchupType=MatchupType.PLAYOFF,
    multiWeekMatchupId="2",
)
matchup6 = Matchup(
    teamAId=teamJoseph2019.id,
    teamBId=teamVincent2019.id,
    teamAScore=89.9,
    teamBScore=100.5,
    matchupType=MatchupType.IGNORE,
)

matchup7 = Matchup(
    teamAId=teamFrankie2019.id,
    teamBId=teamDominic2019.id,
    teamAScore=101.7,
    teamBScore=99.9,
    matchupType=MatchupType.PLAYOFF,
    multiWeekMatchupId="1",
)
matchup8 = Matchup(
    teamAId=teamMonika2019.id,
    teamBId=teamGiovanna2019.id,
    teamAScore=104.1,
    teamBScore=98.3,
    matchupType=MatchupType.PLAYOFF,
    multiWeekMatchupId="2",
)
matchup9 = Matchup(
    teamAId=teamJoseph2019.id,
    teamBId=teamVincent2019.id,
    teamAScore=112.2,
    teamBScore=105.5,
    matchupType=MatchupType.IGNORE,
)

week1 = Week(weekNumber=1, matchups=[matchup1, matchup2, matchup3])
week2 = Week(weekNumber=2, matchups=[matchup4, matchup5, matchup6])
week3 = Week(weekNumber=3, matchups=[matchup7, matchup8, matchup9])

yearSettings = YearSettings(leagueMedianGames=True)

division1 = Division(name="Boyz")
division2 = Division(name="Girlz")

teamFrankie2019.divisionId = division1.id
teamMonika2019.divisionId = division2.id
teamJoseph2019.divisionId = division1.id
teamVincent2019.divisionId = division1.id
teamGiovanna2019.divisionId = division2.id
teamDominic2019.divisionId = division1.id

year2019 = Year(
    yearNumber=2019,
    teams=[
        teamFrankie2019,
        teamMonika2019,
        teamJoseph2019,
        teamVincent2019,
        teamGiovanna2019,
        teamDominic2019,
    ],
    weeks=[week1, week2, week3],
    yearSettings=yearSettings,
    divisions=[division1, division2],
)

LEAGUE = League(
    name="G League",
    owners=[
        ownerFrankie,
        ownerMonika,
        ownerJoseph,
        ownerVincent,
        ownerGiovanna,
        ownerDominic,
    ],
    years=[year2019],
)
