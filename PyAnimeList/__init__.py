"""
A wrapper for the MyAnimeList API
"""

__version__ = "1.1.0"
__author__ = 'Recchan'
__license__ = 'MIT'
__copyright__ = 'Copyright 2015-2016 Byron'
__title__ = 'PyAnimeList'

from .errors import InvalidSeriesTypeException
from .pyanimelist import PyAnimeList
