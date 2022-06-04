from src.leeger.decorator.validateLeague import validateLeague
from src.leeger.model.League import League


class TeamStats:
    @classmethod
    @validateLeague
    def getWins(cls, league: League, **kwargs):
        ...
