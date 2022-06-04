from src.leeger.decorator.validateLeague import validateLeague
from src.leeger.exception.DoesNotExistException import DoesNotExistException
from src.leeger.model.League import League
from src.leeger.model.Year import Year


class LeagueNavigator:
    """
    Used to navigate the League model.
    """

    @staticmethod
    @validateLeague
    def getYearByYearNumber(league: League, yearNumber: int, **kwargs) -> Year:
        for year in league.years:
            if year.yearNumber == yearNumber:
                return year
        raise DoesNotExistException(f"Year {yearNumber} does not exist in the given League.")
