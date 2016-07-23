import asyncio
import json
import urllib

import aiohttp
from dicttoxml import dicttoxml
from errors import NoContentFound
from lxml import etree

with open('setup.json') as file:
    setup = json.load(file)


class PyAnimeList:
    API_BASE_URL = 'http://myanimelist.net/api/'

    def __init__(self, username=setup['username'], password=setup['password']):
        """
        :param username: the account that is being used to access the API
        :param password: the password of the account that is being used to access the API
        """
        self.username = username
        self.password = password
        self.auth = aiohttp.BasicAuth(login=self.username, password=self.password)
        self.session = aiohttp.ClientSession(auth=self.auth)

    def __del__(self):
        self.session.close()

    async def get_anime(self, search_query: str):
        """ :param search_query: is what'll be queried for results """
        to_encode = {'q': search_query}
        params = urllib.parse.urlencode(to_encode)
        async with self.session.get(self.API_BASE_URL + 'anime/search.xml', params=params) as response:
            if response.status == 200:
                response_data = await response.read()
                to_parse = etree.fromstring(response_data)
                entry = to_parse[0]
                return_data = {
                    'id': entry.find('id').text,
                    'title': entry.find('title').text,
                    'english': entry.find('english').text,
                    'synonyms': entry.find('synonyms').text,
                    'episodes': entry.find('episodes').text,
                    'type': entry.find('type').text,
                    'status': entry.find('status').text,
                    'start_date': entry.find('start_date').text,
                    'end_date': entry.find('end_date').text,
                    'synopsis': entry.find('synopsis').text.replace('[i]', '').replace('[/i]', '').replace('<br />',
                                                                                                           ''),
                    'image': entry.find('image').text
                }
                return return_data
            elif response.status == 204:
                raise NoContentFound("Anime not found")

    async def get_manga(self, search_query: str):
        """ :param search_query: is what'll be queried for results """
        to_encode = {'q': search_query}
        params = urllib.parse.urlencode(to_encode)
        async with self.session.get(self.API_BASE_URL + 'manga/search.xml', params=params) as response:
            if response.status == 200:
                response_data = await response.read()
                to_parse = etree.fromstring(response_data)
                manga_entry = to_parse[0]
                return_data = {
                    'id': manga_entry.find('id').text,
                    'title': manga_entry.find('title').text,
                    'english': manga_entry.find('english').text,
                    'synonyms': manga_entry.find('synonyms').text,
                    'volumes': manga_entry.find('volumes').text,
                    'chapters': manga_entry.find('chapters').text,
                    'type': manga_entry.find('type').text,
                    'status': manga_entry.find('status').text,
                    'start_date': manga_entry.find('start_date').text,
                    'end_date': manga_entry.find('end_date').text,
                    'synopsis': manga_entry.find('synopsis').text.replace('[i]', '').replace('[/i]', '').replace(
                        '<br />', ''),
                    'image': manga_entry.find('image').text
                }
                return return_data
            elif response.status == 204:
                raise NoContentFound("Manga not found")

    async def add_anime(self, anime_id: int, status, episodes, score, **kwargs):
        """
        :param anime_id: id is the id of the anime that we'll be adding to the list               Integer (Required)
        :param episodes: Latest episode in the series the user has watched                  Integer (Required)
        :param status: If the user is watching an anime, if the anime is on hold ect.       Integer (Required)
        :param score: the score the user gave the anime                                     Integer
        :param storage_type: (Coming once MAL accept string input)                          Integer for some reason
        :param times_rewatched: the amount of times a user has watched an anime             Integer
        :param rewatch_value: Is the show enjoyable x amount of times                       Integer
        :param date_started: The date the user started the anime                            MMDDYY (I assume integer)
        :param date_finished: The date the user finished the anime                          MMDDYY (I assume integer)
        :param priority: How highly an anime is on your to watch list                       Integer
        :param enable_discussion: Yes or no, do you want to be offered to discuss the anime Integer (1 or 0)
        :param enable_rewatching: Yes or no are you rewatching the anime                    Integer (1 or 0)
        :param comments: Any comments the user wants to leave                               String
        :param fansub_group: What fansub group subbed your anime                            String
        :param tags: Any tags that relate to the anime                                      String, with each tab seperated by a comma
        """
        anime_values = {
            'episode': episodes,
            'status': status,
            'score': score,
            'storage_type': kwargs.get('storage_type'),
            'storage_value': '',
            'times_rewatched': kwargs.get('times_rewatched'),
            'rewatch_value': kwargs.get('rewatch_value'),
            'date_start': kwargs.get('date_started'),
            'date_finish': kwargs.get('date_finished'),
            'priority': kwargs.get('priority'),
            'enable_discussion': kwargs.get('enable_discussion'),
            'enable_rewatching': kwargs.get('enable_rewatching'),
            'comments': kwargs.get('comments'),
            'fansub_group': kwargs.get('fansub_group'),
            'tags': kwargs.get('tags')
        }
        xml = dicttoxml(anime_values, attr_type=False, custom_root='anime')
        async with self.session.post(self.API_BASE_URL + 'animelist/add/' + (str(anime_id)) + '.xml',
                                     data=xml) as response:
            awaited = await response.text()
            print(awaited)


if __name__ == '__main__':
    rip = PyAnimeList()
    getanimu = rip.get_anime('Mahouka Koukou no Rettousei')
    getmangu = rip.get_manga('Mahouka Koukou no Rettousei')
    add_animu = rip.add_anime(31764, 1, 1, 5)
    loop = asyncio.get_event_loop()
    print(loop.run_until_complete(getmangu))
    print(loop.run_until_complete(add_animu))
