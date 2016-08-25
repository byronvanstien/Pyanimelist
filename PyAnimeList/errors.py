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
