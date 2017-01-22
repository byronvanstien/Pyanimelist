class Anime(object):

    """
    Represents a `myanimelist`_ anime
    """

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.titles = kwargs.get("titles")
        self.episode_count = kwargs.get("episode_count")
        self.dates = kwargs.get("dates")
        self.type = kwargs.get("type")
        self.status = kwargs.get("status")
        self.synopsis = kwargs.get("synopsis")
        self.cover = kwargs.get("cover")


class Manga(object):

    """
    Represents a `myanimelist`_ manga
    """

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.titles = kwargs.get("titles")
        self.volumes = kwargs.get("volumes")
        self.chapters = kwargs.get("chapters")
        self.type = kwargs.get("type")
        self.status = kwargs.get("status")
        self.dates = kwargs.get("dates")
        self.synopsis = kwargs.get("synopsis")
        self.cover = kwargs.get("cover")


class UserAnime(object):

    def __init__(self, **kwargs):
        self.title = kwargs.get("title")
        self.score = kwargs.get("scores")
        self.episodes = kwargs.get("episodes")
        self.my_id = kwargs.get("series")
        # Remember that there's more to do here


class UserManga(object):

    def __init__(self, **kwargs):
        pass


class UserInfo(object):

    """
    Represents a users myinfo from the malappinfo endpoint
    """

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.username = kwargs.get("username")
        self.watching = kwargs.get("watching")
        self.completed = kwargs.get("completed")
        self.on_hold = kwargs.get("on_hold")
        self.dropped = kwargs.get("dropped")
        self.plan_to_watch = kwargs.get("plan_to_watch")
        self.days_spent_watching = kwargs.get("days_spent_watching")
