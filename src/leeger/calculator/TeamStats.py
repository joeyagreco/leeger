from src.leeger.decorator.statCalculator import statCalculator
from src.leeger.model.League import League


class TeamStats:
    @classmethod
    @statCalculator
    def getWins(cls, league: League, **kwargs):
        ...
