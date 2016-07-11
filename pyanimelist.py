import aiohttp
import asyncio
from lxml import etree
import json
import urllib


with open('setup.json') as file:
    setup = json.load(file)

class PyAnimeList:

    BASEURL = 'http://myanimelist.net/api/'
    STATUS = {
        'watching': '1',
        'completed': '2',
        'onhold': '3',
        'dropped': '4',
        'plantowatch': '6'}

    def __init__(self, username=setup['username'], password=setup['password']):
        """
        :param username: the account that is being used to access the API
        :param password: the password of the account that is being used to access the API
        """
        self.username = username
        self.password = password
        self.auth = aiohttp.BasicAuth(login=self.username, password=self.password)
        self.session = aiohttp.ClientSession(auth=self.auth)


    async def get_anime(self, search_query: str):
        """ :param search_query: is what'll be queried for results """
        to_encode = {'q': search_query}
        params = urllib.parse.urlencode(to_encode)
        async with self.session.get(self.BASEURL + 'anime/search.xml', params=params) as resp:
            if resp.status == 200:
                return resp

    async def get_manga(self, search_query: str):
        """ :param search_query: is what'll be queried for results """
        to_encode = {'q': search_query}
        params = urllib.parse.urlencode(to_encode)
        async with self.session.get(self.BASEURL + 'manga/search.xml', params=params) as resp:
            if resp.status == 200:
                return resp

    async def add_anime(self, anime_id: int, status, episode=None, score=None, storage_value=None, times_rewatched=None, rewatch_value=None, date_start=None,
                        date_finished=None, priority=None, enable_discussion=None, enable_rewatching=None, comments=None, fansub_group=None, tags=None):
        """
        :param id: id is the id of the anime that we'll be adding to the list               Integer (Required)
        :param episode: Latest episode in the series the user has watched                   Integer
        :param status: If the user is watching an anime, if the anime is on hold ect.       Integer (Required)
        :param score: the score the user gave the anime                                     Integer
        :param storage_type: (Coming once MAL accept string input)                          Integer for some reason
        :param times_rewatched: the amount of times a user has watched an anime             Integer
        :param rewatch_value: Is the show enjoyable x amount of times                       Integer
        :param date_start: The date the user started the anime                              MMDDYY (I assume integer)
        :param date_finished: The date the user finished the anime                          MMDDYY (I assume integer)
        :param priority: How highly an anime is on your to watch list                       Integer
        :param enable_discussion: Yes or no, do you want to be offered to discuss the anime Integer (1 or 0)
        :param enable_rewatching: Yes or no are you rewatching the anime                    Integer (1 or 0)
        :param comments: Any comments the user wants to leave                               String
        :param fansub_group: What fansub group subbed your anime                            String
        :param tags: Any tags that relate to the anime                                      String, with each tab seperated by a comma
        """
        xml = ''' '''
        async with self.session.post(self.BASEURL + 'animelist/add/' + (str(anime_id)), data=xml) as resp:
            if resp.status == 201:
                return resp.text


if __name__ == '__main__':
    rip = PyAnimeList()
    getanimu = rip.get_anime('Mahouka koukou no rettousei')
    getmangu = rip.get_manga('mahouka koukou no rettousei')
    add_animu = rip.add_anime(31764, 1)
    loop = asyncio.get_event_loop()
    print(loop.run_until_complete(getanimu))
    print(loop.run_until_complete(getmangu))
    print(loop.run_until_complete(add_animu))
