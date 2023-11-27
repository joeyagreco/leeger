import random
import string

from leeger.model.league.Owner import Owner
from leeger.model.league.Team import Team


def getNDefaultOwnersAndTeams(
    n: int, *, randomNames: bool = False
) -> tuple[list[Owner], list[Team]]:
    teams = list()
    owners = list()
    for i in range(n):
        name = (
            str(i + 1)
            if not randomNames
            else "".join(random.choice(string.ascii_lowercase) for _ in range(10))
        )
        owner = Owner(name=name)
        teams.append(Team(ownerId=owner.id, name=name))
        owners.append(owner)
    return owners, teams


def getTeamsFromOwners(owners: list[Owner]) -> list[Team]:
    teams = list()
    for i, owner in enumerate(owners):
        teams.append(Team(ownerId=owner.id, name=str(i + 1)))
    return teams
