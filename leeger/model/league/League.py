from __future__ import annotations

from dataclasses import dataclass

from leeger.model.abstract.UniqueId import UniqueId
from leeger.model.league.Owner import Owner
from leeger.model.league.Year import Year
from leeger.util.JSONSerializable import JSONSerializable


@dataclass(kw_only=True, eq=False)
class League(UniqueId, JSONSerializable):
    name: str
    owners: list[Owner]
    years: list[Year]

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
        newOwners = list()
        newYears = list()

        # merge/combine owners
        thisLeagueOwnerNames = [owner.name for owner in self.owners]
        otherLeagueOwnerNames = [owner.name for owner in otherLeague.owners]

        for ownerName in thisLeagueOwnerNames:
            if ownerName in otherLeagueOwnerNames:
                otherLeagueOwnerNames.remove(ownerName)
            newOwners.append(Owner(name=ownerName))
        for ownerName in otherLeagueOwnerNames:
            newOwners.append(Owner(name=ownerName))

        # combine years in order
        if self.years[-1].yearNumber < otherLeague.years[0].yearNumber:
            # order of years goes *this* League -> otherLeague
            newYears = self.years + otherLeague.years
        else:
            # order of years goes otherLeague -> *this* League
            newYears = otherLeague.years + self.years

        newLeague = League(name=newName, owners=newOwners, years=newYears)

        # validate new league
        leagueValidation.runAllChecks(newLeague)
        return newLeague

    def toJson(self) -> dict:
        return {
            "id": self.id,
            "owners": [owner.toJson() for owner in self.owners],
            "years": [year.toJson() for year in self.years]
        }
