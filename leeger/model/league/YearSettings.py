from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
from leeger.util.CustomLogger import CustomLogger

from leeger.util.JSONDeserializable import JSONDeserializable
from leeger.util.JSONSerializable import JSONSerializable
from leeger.util.equality import modelEquals


@dataclass(kw_only=True, eq=False)
class YearSettings(JSONSerializable, JSONDeserializable):
    __LOGGER = CustomLogger.getLogger()
    leagueMedianGames: Optional[bool] = False

    def __post_init__(self):
        if self.leagueMedianGames is None:
            self.leagueMedianGames = False

    def equals(
        self,
        otherYearSettings: YearSettings,
        *,
        ignoreIds: bool = False,
        ignoreBaseId: bool = False,
        logDifferences: bool = False,
    ) -> bool:
        """
        Checks if *this* YearSettings is the same as the given YearSettings.
        """

        return modelEquals(
            objA=self,
            objB=otherYearSettings,
            baseFields={"leagueMedianGames"},
            parentKey="YearSettings",
            ignoreIdFields=ignoreIds,
            ignoreBaseIdField=ignoreBaseId,
            logDifferences=logDifferences,
        )

    def __eq__(self, otherYearSettings: YearSettings) -> bool:
        self.__LOGGER.info("Use .equals() for more options when comparing YearSettings instances.")
        return self.equals(otherYearSettings=otherYearSettings)

    def toJson(self) -> dict:
        return {"leagueMedianGames": self.leagueMedianGames}

    @staticmethod
    def fromJson(d: dict) -> YearSettings:
        return YearSettings(leagueMedianGames=d.get("leagueMedianGames"))
