from src.leeger.decorator.validate.validators import validateYear
from src.leeger.model.Year import Year


class YearNavigator:
    """
    Used to navigate the Year model.
    """

    @staticmethod
    @validateYear
    def getAllTeamIds(year: Year, **kwargs) -> list[str]:
        return [team.id for team in year.teams]
