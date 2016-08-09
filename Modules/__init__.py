"""
A wrapper for the myanimelist API
"""

__version__ = 1.2
__author__ = 'Recchan'
__license__ = 'MIT'
__copyright__ = 'Copyright 2015-2016 Byron'
__title__ = 'PyAnimeList'

from .pyanimelist import PyAnimeList
from .errors import InvalidSeriesTypeException, NoContentException
