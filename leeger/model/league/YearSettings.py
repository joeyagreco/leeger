from __future__ import annotations

from dataclasses import dataclass

from leeger.util.JSONSerializable import JSONSerializable


@dataclass(kw_only=True, eq=False)
class YearSettings(JSONSerializable):
    leagueMedianGames: bool = False

    def __eq__(self, otherYearSettings: YearSettings) -> bool:
        """
        Checks if *this* YearSettings is the same as the given YearSettings.
        """
        return self.leagueMedianGames == otherYearSettings.leagueMedianGames

    def toJson(self) -> dict:
        return {
            "leagueMedianGames": self.leagueMedianGames
        }
