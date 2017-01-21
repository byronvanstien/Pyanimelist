class PyAnimeListException(Exception):
    """
    Base exception class for pyanimelist exceptions
    """
    pass


class InvalidSeriesTypeException(PyAnimeListException):
    """
    If you input an invalid series type
    """
    pass


class ResponseError(PyAnimeListException):
    """
    Only raised when response.status isn't 200
    """
    pass


class InvalidCredentials(PyAnimeListException):
    """
    Raised when invalid login details are passed to verify_credentials
    """
    pass
