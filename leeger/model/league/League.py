from __future__ import annotations

import copy
from dataclasses import dataclass

from leeger.exception import DoesNotExistException
from leeger.model.abstract.UniqueId import UniqueId
from leeger.model.league.Owner import Owner
from leeger.model.league.Year import Year
from leeger.util.JSONDeserializable import JSONDeserializable
from leeger.util.JSONSerializable import JSONSerializable


@dataclass(kw_only=True, eq=False)
class League(UniqueId, JSONSerializable, JSONDeserializable):
    name: str
    owners: list[Owner]
    years: list[Year]

    def __hash__(self):
        return hash(str(self.toJson()))

    def __eq__(self, otherLeague: League) -> bool:
        """
        Checks if *this* League is the same as the given League.
        Does not check for equality of IDs, just values.
        """
        equal = self.name == otherLeague.name
        equal = equal and self.owners == otherLeague.owners
        equal = equal and self.years == otherLeague.years
        return equal

    def __add__(self, otherLeague: League) -> League:
        """
        Combines *this* League with the given League.
        The combined League will be validated before it is returned.

        Special behaviors:
            - name
                - "name" will become a combination of both league's names IF the names are not the same.
            - owners
                - "owners" will be merged on Owner.name, since this field must be unique by League.
                - Unmerged owners will simply be combined.
            - years
                - "years" will be combined in order oldestYearNumber -> newestYearNumber.
                - Duplicate Year.yearNumber across leagues will raise an exception.
        """
        from leeger.validate import leagueValidation
        # first, validate the leagues we want to combine.
        leagueValidation.runAllChecks(self)
        leagueValidation.runAllChecks(otherLeague)

        newName = f"'{self.name}' + '{otherLeague.name}' League" if self.name != otherLeague.name else self.name

        # merge / combine owners
        newOwners = list()
        # keep track of old ownerIDs so we can use them to match teams to owners
        oldOwnerIdToNewOwnerIdMap: dict[str, Owner] = dict()

        otherLeagueOwners = copy.deepcopy(otherLeague.owners)
        thisLeagueOwners = copy.deepcopy(self.owners)

        for owner in self.owners:
            # see if we can find the equivalent owner in the other league
            for otherOwner in otherLeagueOwners:
                if owner.name == otherOwner.name:
                    # this owner is in both leagues
                    otherLeagueOwners.remove(otherOwner)
                    thisLeagueOwners.remove(owner)
                    newOwner = Owner(name=owner.name)
                    oldOwnerIdToNewOwnerIdMap[otherOwner.id] = newOwner.id
                    oldOwnerIdToNewOwnerIdMap[owner.id] = newOwner.id
                    newOwners.append(newOwner)

        for owner in thisLeagueOwners + otherLeagueOwners:
            newOwner = Owner(name=owner.name)
            oldOwnerIdToNewOwnerIdMap[owner.id] = newOwner.id
            newOwners.append(Owner(name=owner.name))

        # combine years in order
        if self.years[-1].yearNumber < otherLeague.years[0].yearNumber:
            # order of years goes *this* League -> otherLeague
            newYears = copy.deepcopy(self.years) + otherLeague.years
        else:
            # order of years goes otherLeague -> *this* League
            newYears = otherLeague.years + copy.deepcopy(self.years)

        # set all team ownerId fields to match combined owner IDs
        for year in newYears:
            for team in year.teams:
                if team.ownerId in oldOwnerIdToNewOwnerIdMap:
                    # replace this team's ownerId with the new ownerId
                    team.ownerId = oldOwnerIdToNewOwnerIdMap[team.ownerId]

        newLeague = League(name=newName, owners=newOwners, years=newYears)

        # validate new league
        leagueValidation.runAllChecks(newLeague)
        return newLeague

    def getYearByYearNumber(self, yearNumber: int) -> Year:
        """
        Returns the Year with the given year number.
        """
        for year in self.years:
            if year.yearNumber == yearNumber:
                return year
        raise DoesNotExistException(f"League does not have a year with year number {yearNumber}")

    def getOwnerByName(self, ownerName: str) -> Owner:
        """
        Returns the Owner with the given name.
        """
        for owner in self.owners:
            if owner.name == ownerName:
                return owner
        raise DoesNotExistException(f"League does not have an owner with name '{ownerName}'")

    def toJson(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "owners": [owner.toJson() for owner in self.owners],
            "years": [year.toJson() for year in self.years]
        }

    @staticmethod
    def fromJson(d: dict) -> League:
        owners = list()
        for ownerDict in d["owners"]:
            owners.append(Owner.fromJson(ownerDict))
        years = list()
        for yearDict in d["years"]:
            years.append(Year.fromJson(yearDict))
        league = League(name=d["name"],
                        owners=owners,
                        years=years)
        league.id = d["id"]
        return league
