from src.leeger.decorator.validate.validators import validateLeague
from src.leeger.exception.DoesNotExistException import DoesNotExistException
from src.leeger.model.league.League import League
from src.leeger.model.league.Team import Team
from src.leeger.model.league.Year import Year


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

    @staticmethod
    @validateLeague
    def getTeamById(league: League, teamId: str, **kwargs) -> Team:
        for year in league.years:
            for team in year.teams:
                if team.id == teamId:
                    return team
        raise DoesNotExistException(f"Team with ID {teamId} does not exist in the given League.")

    @staticmethod
    @validateLeague
    def getAllOwnerIds(league: League, **kwargs) -> list[str]:
        return [owner.id for owner in league.owners]
