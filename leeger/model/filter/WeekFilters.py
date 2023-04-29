from dataclasses import dataclass

from leeger.enum.MatchupType import MatchupType


@dataclass(kw_only=True)
class WeekFilters:
    """
    Used to house filters that will be applied to a Week when navigating through it.
    """

    includeMatchupTypes: list[MatchupType]  # include matchups of these types
