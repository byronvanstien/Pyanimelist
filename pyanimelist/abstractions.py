class Titles(object):

    """
    Abstraction class for the three versions of titles myanimelist keeps.
    """

    def __init__(self, jp: str, english: str, synonyms: list = None):
        self.jp = jp
        self.english = english
        self.synonyms = synonyms or []


class Dates(object):

    """
    Abstraction class for the dates myanimelist stores
    """

    def __init__(self, start: str, end: str):
        self.start = start
        self.end = end
