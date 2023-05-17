from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
from leeger.util.ConfigReader import ConfigReader
from leeger.util.CustomLogger import CustomLogger
from leeger.util.GeneralUtil import GeneralUtil

from leeger.util.JSONDeserializable import JSONDeserializable
from leeger.util.JSONSerializable import JSONSerializable


@dataclass(kw_only=True, eq=False)
class YearSettings(JSONSerializable, JSONDeserializable):
    __LOGGER = CustomLogger.getLogger()
    leagueMedianGames: Optional[bool] = False

    def __post_init__(self):
        if self.leagueMedianGames is None:
            self.leagueMedianGames = False

    def __eq__(self, otherYearSettings: YearSettings) -> bool:
        """
        Checks if *this* YearSettings is the same as the given YearSettings.
        """
        equal = self.leagueMedianGames == otherYearSettings.leagueMedianGames
        if not equal:
            differences = GeneralUtil.findDifferentFields(
                self.toJson(),
                otherYearSettings.toJson(),
                parentKey="YearSettings",
                ignoreKeyNames=ConfigReader.get("EQUALITY_CHECK", "IGNORE_KEY_NAMES", asType=list, propFile="league.properties"),
            )
            self.__LOGGER.info(f"Differences: {differences}")
        return equal

    def toJson(self) -> dict:
        return {"leagueMedianGames": self.leagueMedianGames}

    @staticmethod
    def fromJson(d: dict) -> YearSettings:
        return YearSettings(leagueMedianGames=d.get("leagueMedianGames"))
