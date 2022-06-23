from src.leeger.model.league.Owner import Owner
from src.leeger.model.league.Team import Team


def getNDefaultOwnersAndTeams(n: int) -> tuple[list[Owner], list[Team]]:
    teams = list()
    owners = list()
    for i in range(n):
        owner = Owner(name=str(i + 1))
        team = Team(ownerId=owner.id, name=str(i + 1))
        teams.append(team)
        owners.append(owner)
    return owners, teams
