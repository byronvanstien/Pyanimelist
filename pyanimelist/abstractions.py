class Titles(object):

    def __init__(self, jp: str, english: str, synonyms: list = None):
        self.jp = jp
        self.english = english
        self.synonyms = synonyms or []


class Dates(object):

    def __init__(self, start: str, end: str):
        self.start = start
        self.end = end
