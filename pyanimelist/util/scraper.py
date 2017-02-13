import warnings
from functools import wraps


def scraper_enabled(func):
    """
    Decorator which ensures that a :class:`pyanimelist.Client.scraper` isn't used without it being explictly allowed

    Example usage:

    .. code-block:: py

       from pyanimelist.util.web import scraper_enabled

       @scraper_enabled
       async def function(func):
           return await func()
    """
    @wraps(func)
    async def wrapped(self, *args, **kwargs):
        if not self.scraper:
            warnings.warn("Usage of scraper is set to {0}. Set to {1} to silence warning".format(self.scraper, not(self.scraper)))
        return await func(self, *args, **kwargs)
    return wrapped
