# Imports
import json
import urllib
from datetime import datetime

import aiohttp
import bs4
from dicttoxml import dicttoxml
from errors import NoContentException, NotAddedException
from lxml import etree

try:
    with open('setup.json') as file:
        setup = json.load(file)
except FileNotFoundError:
    pass


class PyAnimeList:
    # The base url for the API
    __API_BASE_URL = 'http://myanimelist.net/api/'
    # Information for individual users
    __MAL_APP_INFO = 'http://myanimelist.net/malappinfo.php'
    # Version of PyAnimeList
    __version__ = 1.1
    # Author
    __author__ = 'Recchan'
    # License
    __license__ = 'MIT'

    def __init__(self, username=setup['username'], password=setup['password'],
                 user_agent=None):
        """
        :param username: the account that is being used to access the API
        :param password: the password of the account that is being used to access the API
        :param user_agent: useragent of the application, defaults to PyAnimeList/VersionNumber unless explicitly passed
        through the keyword argument
        """
        # Set default User-Agent
        if user_agent is None:
            self.user_agent = {'User-Agent': 'PyAnimeList/' + str(self.__version__)}
        self._username = username
        self.__password = password
        self.__auth = aiohttp.BasicAuth(login=self._username, password=self.__password)
        self.session = aiohttp.ClientSession(auth=self.__auth, headers=self.user_agent)

    # Get rid of unclosed client session error
    def __del__(self):
        self.session.close()

    # Verifies credentials
    async def verify_credentials(self):
        async with self.session.get(self.__API_BASE_URL + 'account/verify_credentials.xml') as response:
            if response.status == 200:
                response_data = await response.read()
                to_parse = etree.fromstring(response_data)
                user = to_parse

                # Returns the username and id in tuple
                return user.find('id').text, user.find('username').text
            else:
                raise aiohttp.ClientResponseError()

    # Gets the anime that is searched for
    async def get_anime(self, search_query: str):
        """ :param search_query: is what'll be queried for results """
        # Params
        params = urllib.parse.urlencode({'q': search_query})
        async with self.session.get(self.__API_BASE_URL + 'anime/search.xml', params=params) as response:
            if response.status == 200:
                response_data = await response.read()
                entry = etree.fromstring(response_data)[0]
                #Anime values for dicttoxml
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
                raise NoContentException("Anime not found")

    async def get_manga(self, search_query: str):
        """ :param search_query: is what'll be queried for results """
        params = urllib.parse.urlencode({'q': search_query})
        async with self.session.get(self.__API_BASE_URL + 'manga/search.xml', params=params) as response:
            if response.status == 200:
                response_data = await response.read()
                manga_entry = etree.fromstring(response_data)[0]
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
                raise NoContentException("Manga not found")

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
        kwargs.update(status=status)
        xml = dicttoxml(kwargs, attr_type=False, custom_root='entry')
        params = urllib.parse.urlencode({'data': xml})
        async with self.session.get(self.__API_BASE_URL + 'animelist/add/' + (str(anime_id)) + '.xml',
                                    params=params) as response:
            if response.status == 201:
                soup = bs4.BeautifulSoup(await response.text(), 'lxml')
                if soup.find('h1').string == 'Created':
                    return soup.find('h1').string
                else:
                    raise NotAddedException()
            else:
                raise aiohttp.ClientResponseError()

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
        kwargs.update(status=status)
        xml_manga_values = dicttoxml(kwargs, attr_type=False, custom_root='entry')
        params = urllib.parse.urlencode({'data': xml_manga_values})
        async with self.session.get(self.__API_BASE_URL + 'mangalist/add/' + str(manga_id) + '.xml',
                                    params=params) as response:
            if response.status == 201:
                soup = bs4.BeautifulSoup(await response.text(), 'lxml')
                return soup.find('h1').string
            else:
                raise aiohttp.ClientResponseError()

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
        # Anime values in dict for dicttoxml
        kwargs.update(status=status)
        xml = dicttoxml(kwargs, attr_type=False, custom_root='entry')
        params = urllib.parse.urlencode({'data': xml})
        async with self.session.get(self.__API_BASE_URL + 'animelist/update/' + (str(anime_id)) + '.xml',
                                    params=params) as response:
            if response.status == 200:
                response.text = await response.text()
                return response.text
            else:
                raise aiohttp.ClientResponseError()

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
        kwargs.update(status=status)
        xml_manga_values = dicttoxml(kwargs, attr_type=False, custom_root='entry')
        params = urllib.parse.urlencode({'data': xml_manga_values})
        async with self.session.get(self.__API_BASE_URL + 'mangalist/update/' + str(manga_id) + '.xml',
                                    params=params) as response:
            if response.status == 200:
                response.text = await response.text()
                return response.text
            else:
                raise aiohttp.ClientResponseError()

    async def delete_anime(self, anime_id: int):
        async with self.session.get(self.__API_BASE_URL + 'animelist/delete/' + str(anime_id) + '.xml') as response:
            if response.status == 200:
                response.text = await response.text()
                return response.text

    async def delete_manga(self, manga_id: int):
        async with self.session.get(self.__API_BASE_URL + 'mangalist/delete/' + str(manga_id) + '.xml') as response:
            if response.status == 200:
                response.text = await response.text()
                return response.text
            else:
                raise aiohttp.ClientResponseError()

    # Zeta wrote this bit
    @staticmethod
    def process_(child):
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
        # Params for the url
        params = urllib.parse.urlencode({
            'u': profile,
            'status': 'all',
            'type': series_type
        })
        # If series_type == anime
        if series_type not in ['anime', 'manga']:
            pass
        else:
            async with self.session.get(
                    self.__MAL_APP_INFO, params=params) as response:
                soup = bs4.BeautifulSoup(await response.text(), "lxml")
            # Return as a dictionary
                return [dict(self.process_(child) for child in anime.children) for anime in soup.find_all(series_type)]
    # End of bit Zeta wrote

    async def get_public_user_data(self, username: str):
        # Params for url
        params = urllib.parse.urlencode({'u': username})
        async with self.session.get(self.__MAL_APP_INFO, params=params) as response:

            # If the response is 200 OK
            if response.status == 200:
                response_data = await response.read()
                to_parse = etree.fromstring(response_data)[0]

                # Return as a dictionary
                return dict(zip(['user_id', 'username', 'watching', 'completed', 'on_hold', 'dropped', 'plan_to_watch',
                                 'days_spent_watching'], [x.text for x in to_parse]))
