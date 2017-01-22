from enum import Enum


class AnimeStatus(Enum):

    """
    Transforms what MAL returns into an enumeration for easy filtering
    """

    WATCHING = 1
    COMPLETED = 2
    ON_HOLD = 3
    DROPPED = 4
    PLAN_TO_WATCH = 6


class MangaStatus(Enum):

    """
    Transforms what MAL returns into an enumeration for easy filtering
    """

    READING = 1
    COMPLETED = 2
    ON_HOLD = 3
    DROPPED = 4
    PLAN_TO_READ = 6
