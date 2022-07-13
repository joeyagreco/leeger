from dataclasses import dataclass

from leeger.enum.MatchupType import MatchupType


@dataclass(kw_only=True)
class StreakFilters:
    """
    Used to house filters that will be used to calculate Streak stats.
    """
    yearNumberStart: int  # year to start at (inclusive)
    weekNumberStart: int  # week to start at (inclusive)
    yearNumberEnd: int  # year to end at (inclusive)
    weekNumberEnd: int  # week to end at (inclusive)
    onlyChampionship: bool  # only include championship matchups
    onlyPostSeason: bool  # only include playoff matchups
    onlyRegularSeason: bool  # only include regular season matchups
    onlyOngoing: bool  # streaks that are ongoing
    
    @property
    def includeMatchupTypes(self) -> list[MatchupType]:
        if self.onlyChampionship:
            return [MatchupType.CHAMPIONSHIP]
        elif self.onlyPostSeason:
            return [MatchupType.PLAYOFF, MatchupType.CHAMPIONSHIP]
        elif self.onlyRegularSeason:
            return [MatchupType.REGULAR_SEASON]
        else:
            return [MatchupType.REGULAR_SEASON, MatchupType.PLAYOFF, MatchupType.CHAMPIONSHIP]
