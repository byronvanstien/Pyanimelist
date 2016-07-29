import asyncio
import json
import urllib
from datetime import datetime

import aiohttp
import bs4
from dicttoxml import dicttoxml
from lxml import etree

try:
    with open('setup.json') as file:
        setup = json.load(file)
except:
    pass


class PyAnimeList:

    __API_BASE_URL = 'http://myanimelist.net/api/'
    __MAL_APP_INFO = 'http://myanimelist.net/malappinfo.php'
    __version__ = 1.0

    def __init__(self, username=setup['username'], password=setup['password'],
                 user_agent=None):
        """
        :param username: the account that is being used to access the API
        :param password: the password of the account that is being used to access the API
        :param user_agent: useragent of the application, defaults to PyAnimeList/VersionNumber unless explicitly passed
        through the keyword argument
        """
        if user_agent is None:
            self.user_agent = {'User-Agent': 'PyAnimeList/' + str(self.__version__)}
        self.__username = username
        self.__password = password
        self.__auth = aiohttp.BasicAuth(login=self.__username, password=self.__password)
        self.session = aiohttp.ClientSession(auth=self.__auth, headers=self.user_agent)

    def __del__(self):
        self.session.close()

    async def verify_credentials(self):
        async with self.session.get(self.__API_BASE_URL + 'account/verify_credentials.xml') as response:
            if response.status == 200:
                response_data = await response.read()
                to_parse = etree.fromstring(response_data)
                user = to_parse
                return_data = {
                    'id': user.find('id').text,
                    'username': user.find('username').text
                }
                return return_data

    async def get_anime(self, search_query: str):
        """ :param search_query: is what'll be queried for results """
        to_encode = {'q': search_query}
        params = urllib.parse.urlencode(to_encode)
        async with self.session.get(self.__API_BASE_URL + 'anime/search.xml', params=params) as response:
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
        async with self.session.get(self.__API_BASE_URL + 'manga/search.xml', params=params) as response:
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
                    'image': manga_entry.find('image').text,
                }
                return return_data
            elif response.status == 204:
                raise NoContentFound("Manga not found")

    async def add_anime(self, anime_id: int, status, **kwargs):
        """
        :param anime_id: id is the id of the anime that we'll be adding to the list         Integer (Required)
        :param episodes: Latest episode in the series the user has watched                  Integer
        :param status: If the user is watching an anime, if the anime is on hold ect.       Integer
        :param score: the score the user gave the anime                                     Integer
        :param storage_type: (Coming once MAL accept string input)                          Integer
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
            'episode': kwargs.get('episodes'),
            'status': status,
            'score': kwargs.get('score'),
            'storage_type': kwargs.get('storage_type'),
            'storage_value': kwargs.get('storage_value'),
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
        xml = dicttoxml(anime_values, attr_type=False, custom_root='entry')
        params = {'data': xml}
        params = urllib.parse.urlencode(params)
        async with self.session.get(self.__API_BASE_URL + 'animelist/add/' + (str(anime_id)) + '.xml',
                                    params=params) as response:
            if response.status == 201:
                return True
            else:
                return False

    async def add_manga(self, manga_id: int, status, **kwargs):
        """
        :param manga_id:
        :param status:
        :param chapter: How many read chapters
        :param volumes: How many read volumes
        :param status: If currently reading, on hold ect
        :param score: Score user is giving the manga
        :param times_reread: How many times the user has read the series
        :param reread_value: How rereadable a manga is
        :param date_start: What date the user started reading
        :param date_finish: What date the user finished the manga
        :param priority: How highly the user wants to read the manga
        :param enable_discussion: If you want to be offered to discuss the manga or not
        :param enable_rereading: If you're currently rereading the manga
        :param comments: A comment to leave for the manga
        :param scan_group: What groups scans you're reading
        :param tags: Tags related to the novel, seperated by comma
        :param retail_volumes: How many volumes you own
        """
        manga_values = {
            'status': status,
            'chapter': kwargs.get('chapter'),
            'volumes': kwargs.get('volumes'),
            'score': kwargs.get('score'),
            'times_reread': kwargs.get('times_reread'),
            'reread_value': kwargs.get('reread_value'),
            'date_start': kwargs.get('date_start'),
            'date_finish': kwargs.get('date_finish'),
            'priority': kwargs.get('priority'),
            'enable_discussion': kwargs.get('enable_discussion'),
            'enable_rereading': kwargs.get('enable_rereading'),
            'comments': kwargs.get('comments'),
            'scan_group': kwargs.get('scan_group'),
            'tags': kwargs.get('tags'),
            'retail_volumes': kwargs.get('retail_volumes')
        }
        xml_manga_values = dicttoxml(manga_values, attr_type=False, custom_root='entry')
        params = {'data': xml_manga_values}
        params = urllib.parse.urlencode(params)
        async with self.session.get(self.__API_BASE_URL + 'mangalist/add/' + str(manga_id) + '.xml',
                                    params=params) as response:
            if response.status == 201:
                return True
            else:
                return False

    async def update_anime(self, anime_id: int, status, **kwargs):
        """
        :param anime_id: id is the id of the anime that we'll be adding to the list         Integer (Required)
        :param episodes: Latest episode in the series the user has watched                  Integer
        :param status: If the user is watching an anime, if the anime is on hold ect.       Integer
        :param score: the score the user gave the anime                                     Integer
        :param storage_type: (Coming once MAL accept string input)                          Integer
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
            'episode': kwargs.get('episodes'),
            'status': status,
            'score': kwargs.get('score'),
            'storage_type': kwargs.get('storage_type'),
            'storage_value': kwargs.get('storage_value'),
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
        xml = dicttoxml(anime_values, attr_type=False, custom_root='entry')
        params = {'data': xml}
        params = urllib.parse.urlencode(params)
        async with self.session.get(self.__API_BASE_URL + 'animelist/update/' + (str(anime_id)) + '.xml',
                                    params=params) as response:
            if response.status == 200:
                return True
            else:
                return False

    async def update_manga(self, manga_id: int, status, **kwargs):
        """
        :param manga_id:
        :param status:
        :param chapter: How many read chapters
        :param volumes: How many read volumes
        :param status: If currently reading, on hold ect
        :param score: Score user is giving the manga
        :param times_reread: How many times the user has read the series
        :param reread_value: How rereadable a manga is
        :param date_start: What date the user started reading
        :param date_finish: What date the user finished the manga
        :param priority: How highly the user wants to read the manga
        :param enable_discussion: If you want to be offered to discuss the manga or not
        :param enable_rereading: If you're currently rereading the manga
        :param comments: A comment to leave for the manga
        :param scan_group: What groups scans you're reading
        :param tags: Tags related to the novel, seperated by comma
        :param retail_volumes: How many volumes you own
        """
        manga_values = {
            'status': status,
            'chapter': kwargs.get('chapter'),
            'volumes': kwargs.get('volumes'),
            'score': kwargs.get('score'),
            'times_reread': kwargs.get('times_reread'),
            'reread_value': kwargs.get('reread_value'),
            'date_start': kwargs.get('date_start'),
            'date_finish': kwargs.get('date_finish'),
            'priority': kwargs.get('priority'),
            'enable_discussion': kwargs.get('enable_discussion'),
            'enable_rereading': kwargs.get('enable_rereading'),
            'comments': kwargs.get('comments'),
            'scan_group': kwargs.get('scan_group'),
            'tags': kwargs.get('tags'),
            'retail_volumes': kwargs.get('retail_volumes')
        }
        xml_manga_values = dicttoxml(manga_values, attr_type=False, custom_root='entry')
        params = {'data': xml_manga_values}
        params = urllib.parse.urlencode(params)
        async with self.session.get(self.__API_BASE_URL + 'mangalist/update/' + str(manga_id) + '.xml',
                                    params=params) as response:
            if response.status == 200:
                return True
            else:
                return False

    async def delete_anime(self, anime_id: int):
        async with self.session.get(self.__API_BASE_URL + 'animelist/delete/' + str(anime_id) + '.xml') as response:
            try:
                if response.status == 200:
                    return True
            except Exception as e:
                print(e)

    async def delete_manga(self, manga_id: int):
        async with self.session.get(self.__API_BASE_URL + 'mangalist/delete/' + str(manga_id) + '.xml') as response:
            try:
                if response.status == 200:
                    return True
            except Exception as e:
                print(e)

    async def get_user_series(self, username: str, series_type: str):
        params = {
            'u': username,
            'type': series_type,
            'status': 'all'
        }
        params = urllib.parse.urlencode(params)
        async with self.session.get(self.__MAL_APP_INFO, params=params) as response:
            if response.status == 200:
                response_data = await response.read()
                to_parse = etree.fromstring(response_data)
                data = to_parse
                if series_type == 'anime':
                    pass
                elif series_type == 'manga':
                    pass

    def process_(self, child):
        name, text = child.name, child.get_text()
        try:
            text = int(text)
        except ValueError:
            pass
        if name == 'my_last_updated':
            text = datetime.fromtimestamp(float(text))
        if name in ['my_finish_date', 'my_start_date', 'series_end', 'series_start']:
            try:
                text = datetime.strptime(text, "%Y-%m-%d")
            except ValueError:
                text = datetime.fromtimestamp(0)
        return name, text

    async def get_user_series(self, profile: str, series_type: str):
        params = urllib.parse.urlencode({
            'u': profile,
            'status': 'all',
            'type': series_type
        })
        if series_type == 'anime':
            async with self.session.get(
                    self.__MAL_APP_INFO, params=params) as response:
                soup = bs4.BeautifulSoup(await response.text(), "lxml")
            return [dict(self.process_(child) for child in anime.children) for anime in soup.find_all('anime')]
        elif series_type == 'manga':
            async with self.session.get(self.__MAL_APP_INFO, params=params) as response:
                soup = bs4.BeautifulSoup(await response.text(), "lxml")
                return [dict(self.process_(child) for child in manga.children) for manga in soup.find_all('manga')]


    async def get_public_user_data(self, username: str):
        params = urllib.parse.urlencode({'u': username})
        async with self.session.get(self.__MAL_APP_INFO, params=params) as response:
            if response.status == 200:
                response_data = await response.read()
                to_parse = etree.fromstring(response_data)
                data = to_parse[0]
                final_userinfo = dict(zip(['user_id', 'username', 'watching', 'completed', 'on_hold', 'dropped', 'plan_to_watch', 'days_spent_watching'], [x.text for x in data]))
                return final_userinfo

if __name__ == '__main__':
    rip = PyAnimeList()
    loop = asyncio.get_event_loop()
    print(loop.run_until_complete(rip.get_public_user_data('GetRektByMe')))
    print(loop.run_until_complete(rip.get_user_series('GetRektByMe', 'manga')))

