class Anime:

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.title = kwargs.get("title")
        self.english = kwargs.get("english")
        self.synonyms = kwargs.get("synonyms")
        self.episodes = kwargs.get("episodes")
        self.type = kwargs.get("type")
        self.status = kwargs.get("status")
        self.start_date = kwargs.get("start_date")
        self.end_date = kwargs.get("end_date")
        self.synopsis = kwargs.get("synopsis")
        self.image = kwargs.get("image")


class Manga:

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.title = kwargs.get("title")
        self.english = kwargs.get("english")
        self.synonyms = kwargs.get("synonyms")
        self.volumes = kwargs.get("volumes")
        self.chapters = kwargs.get("chapters")
        self.type = kwargs.get("type")
        self.status = kwargs.get("status")
        self.start_date = kwargs.get("start_date")
        self.end_date = kwargs.get("end_date")
        self.synopsis = kwargs.get("synopsis")
        self.image = kwargs.get("image")


class UserAnime:

    def __init__(self, **kwargs):
        self.title = kwargs.get("title")
        self.score = kwargs.get("scores")
        self.episodes = kwargs.get("episodes")
        self.my_id = kwargs.get("series")
        # Remember that there's more to do here


class UserManga:

    def __init__(self, **kwargs):
        pass


class UserInfo:

    def __init__(self, **kwargs):
        self.user_id = kwargs.get("user_id")
        self.username = kwargs.get("username")
        self.watching = kwargs.get("watching")
        self.completed = kwargs.get("completed")
        self.on_hold = kwargs.get("on_hold")
        self.dropped = kwargs.get("dropped")
        self.plan_to_watch = kwargs.get("plan_to_watch")
        self.days_spent_watching = kwargs.get("days_spent_watching")


class SuperUser:

    def __init__(self, **kwargs):
        self.anime = kwargs.get("anime")
        self.manga = kwargs.get("manga")
        self.info = kwargs.get("info")
