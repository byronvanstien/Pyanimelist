import warnings


class PyAnimeListException(Exception):
    """
    Base exception class for pyanimelist exceptions
    """
    pass


class InvalidSeriesTypeException(PyAnimeListException):
    """
    Raised if you pass an invalid series type
    """
    pass


class ResponseError(PyAnimeListException):
    """
    Raised when response.status isn't 200 (OK)
    """
    pass


class InvalidCredentials(ResponseError):
    """
    Raised when invalid login details are passed to verify_credentials

    Inherits from :class:`pyanimelist.errors.ResponseError`
    """
    pass


class ScraperDisabled(PyAnimeListException, warnings.Warning):
    """
    Raised when user tries using a method on :class:`pyanimelist.Client.scraper`
    """
    pass
