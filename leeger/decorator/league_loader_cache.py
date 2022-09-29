from functools import wraps
from typing import Callable, Optional

from leeger.model.league import League


def cachedLeague(function: Callable) -> Callable:
    """
    """

    @wraps(function)
    def wrapFunction(*args, **kwargs):
        # check if we should run this method
        # if "cache" not in kwargs or kwargs["cache"] is False:
        #     return function(*args, **kwargs)

        instance = function.__self__

        if not instance.cache:
            return function(*args, **kwargs)

        league: Optional[League] = instance.getLeagueFromCache(instance)
        if league is None:
            print("no cached league, saving")
            # no cached league, get league and cache it
            league: League = function(*args, **kwargs)
            # save league to cache
            instance.upsertLeagueToCache(instance, league)
        else:
            print("found cached league")

        return league

    return wrapFunction
