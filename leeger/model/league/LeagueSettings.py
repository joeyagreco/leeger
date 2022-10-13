from __future__ import annotations

from dataclasses import dataclass

from leeger.util.JSONSerializable import JSONSerializable


@dataclass(kw_only=True, eq=False)
class LeagueSettings(JSONSerializable):
    leagueMedianGames: bool = False

    def __eq__(self, otherLeagueSettings: LeagueSettings) -> bool:
        """
        Checks if *this* LeagueSettings is the same as the given LeagueSettings.
        """
        return self.leagueMedianGames == otherLeagueSettings.leagueMedianGames

    def toJson(self) -> dict:
        return {
            "leagueMedianGames": self.leagueMedianGames
        }
