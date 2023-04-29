from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from leeger.util.JSONDeserializable import JSONDeserializable
from leeger.util.JSONSerializable import JSONSerializable


@dataclass(kw_only=True, eq=False)
class YearSettings(JSONSerializable, JSONDeserializable):
    leagueMedianGames: Optional[bool] = False

    def __post_init__(self):
        if self.leagueMedianGames is None:
            self.leagueMedianGames = False

    def __eq__(self, otherYearSettings: YearSettings) -> bool:
        """
        Checks if *this* YearSettings is the same as the given YearSettings.
        """
        return self.leagueMedianGames == otherYearSettings.leagueMedianGames

    def toJson(self) -> dict:
        return {"leagueMedianGames": self.leagueMedianGames}

    @staticmethod
    def fromJson(d: dict) -> YearSettings:
        return YearSettings(leagueMedianGames=d.get("leagueMedianGames"))
