from leeger.model.league.Owner import Owner
from leeger.model.league.Team import Team


def getNDefaultOwnersAndTeams(n: int) -> tuple[list[Owner], list[Team]]:
    teams = list()
    owners = list()
    for i in range(n):
        owner = Owner(name=str(i + 1))
        teams.append(Team(ownerId=owner.id, name=str(i + 1)))
        owners.append(owner)
    return owners, teams


def getTeamsFromOwners(owners: list[Owner]) -> list[Team]:
    teams = list()
    for i, owner in enumerate(owners):
        teams.append(Team(ownerId=owner.id, name=str(i + 1)))
    return teams
