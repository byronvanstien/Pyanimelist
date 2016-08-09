# Imports from standard libs
import urllib
from datetime import datetime

# Imports from external libs
import aiohttp
import bs4
from dicttoxml import dicttoxml
from lxml import etree

# Module level imports
from .errors import NoContentException, InvalidSeriesTypeException


class PyAnimeList:
    # The base url for the API
    __API_BASE_URL = 'http://myanimelist.net/api/'
    # Information for individual users
    __MAL_APP_INFO = 'http://myanimelist.net/malappinfo.php'

    def __init__(self, username, password, user_agent=None):
        """
        :param username: the account that is being used to access the API
        :param password: the password of the account that is being used to access the API
        :param user_agent: useragent of the application, defaults to PyAnimeList/VersionNumber unless explicitly passed
        through the keyword argument
        """
        # Set default User-Agent
        self.user_agent = user_agent or {'User-Agent': 'PyAnimeList'}
        self._username = username
        self._password = password
        self._auth = aiohttp.BasicAuth(login=self._username, password=self._password)
        self.session = aiohttp.ClientSession(auth=self._auth, headers=self.user_agent)

    # Get rid of unclosed client session error
    def __del__(self):
        self.session.close()

    async def verify_credentials(self):
        async with self.session.get(self.__API_BASE_URL + 'account/verify_credentials.xml') as response:
            if response.status == 200:
                response_data = await response.read()
                user = etree.fromstring(response_data)
                # Returns the username and id in tuple
                return user.find('id').text, user.find('username').text
            else:
                raise aiohttp.ClientResponseError(response.status)

    async def search_all_anime(self, search_query: str):
        """:param search_query: is what'll be queried for the search results"""
        # URL Params
        params = urllib.parse.urlencode({'q': search_query})
        async with self.session.get(self.__API_BASE_URL + 'anime/search.xml', params=params) as response:
            if response.status == 200:
                response_data = await response.read()
                entries = etree.fromstring(response_data)
                animes = list()
                for entry in entries:
                    animes.append({
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
                    })
                return animes
            else:
                raise aiohttp.ClientResponseError(response.status)

    async def search_all_manga(self, search_query: str):
        """:param search_query: is what'll be queried for the search results"""
        params = urllib.parse.urlencode({'q': search_query})
        async with self.session.get(self.__API_BASE_URL + 'manga/search.xml', params=params) as response:
            if response.status == 200:
                response_data = await response.read()
                entries = etree.fromstring(response_data)
                manga = list()
                for manga_entry in entries:
                    manga.append({
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
                    })
                return manga
            else:
                raise aiohttp.ClientError(response.status)

    async def get_first_anime_result(self, search_query: str):
        """ :param search_query: is what'll be queried for results """
        # URL Params
        params = urllib.parse.urlencode({'q': search_query})
        async with self.session.get(self.__API_BASE_URL + 'anime/search.xml', params=params) as response:
            if response.status == 200:
                response_data = await response.read()
                # Gets first anime
                manga_entry = etree.fromstring(response_data)[0]
                # Anime values to return
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
                raise NoContentException("Anime not found")

    async def get_first_manga(self, search_query: str):
        """ :param search_query: is what'll be queried for results """
        params = urllib.parse.urlencode({'q': search_query})
        async with self.session.get(self.__API_BASE_URL + 'manga/search.xml', params=params) as response:
            if response.status == 200:
                response_data = await response.read()
                # Gets first manga
                manga_entry = etree.fromstring(response_data)[0]
                # Manga Values to return
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
                # Return as dictionary
                return return_data
            elif response.status == 204:
                raise NoContentException("Manga not found")

    async def add_anime(self, anime_id: int, status: int, **kwargs):
        """
        :param anime_id: id is the id of the anime that we'll be adding to the list
        :param episodes: Latest episode in the series the user has watched
        :param status: If the user is watching an anime, if the anime is on hold ect
        :param score: the score the user gave the anime
        :param storage_type: (Coming once MAL accept string input)
        :param times_rewatched: the amount of times a user has watched an anime
        :param rewatch_value: Is the show enjoyable x amount of times
        :param date_started: The date the user started the anime
        :param date_finished: The date the user finished the anime
        :param priority: How highly an anime is on your to watch list
        :param enable_discussion: Yes or no, do you want to be offered to discuss the anime
        :param enable_rewatching: Yes or no are you rewatching the anime
        :param comments: Any comments the user wants to leave
        :param fansub_group: What fansub group subbed your anime
        :param tags: Any tags that relate to the anime
        """
        # Adds status to kwargs
        kwargs.update(status=status)
        xml = dicttoxml(kwargs, attr_type=False, custom_root='entry')
        params = urllib.parse.urlencode({'data': xml})
        async with self.session.get(self.__API_BASE_URL + 'animelist/add/' + (str(anime_id)) + '.xml',
                                    params=params) as response:
            if response.status == 201:
                return True
            else:
                raise aiohttp.ClientResponseError(response.status)

    async def add_manga(self, manga_id: int, status: int, **kwargs):
        """
        :param manga_id: The id on MAL of the manga
        :param status: What you're currently doing with the manga, watching ect
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
        # Adds status to kwargs
        kwargs.update(status=status)
        xml_manga_values = dicttoxml(kwargs, attr_type=False, custom_root='entry')
        params = urllib.parse.urlencode({'data': xml_manga_values})
        async with self.session.get(self.__API_BASE_URL + 'mangalist/add/' + str(manga_id) + '.xml',
                                    params=params) as response:
            if response.status == 201:
                return True
            else:
                raise aiohttp.ClientResponseError(response.status)

    async def update_anime(self, anime_id: int, status: int, **kwargs):
        """
        :param anime_id: id is the id of the anime that we'll be adding to the list
        :param episodes: Latest episode in the series the user has watched
        :param status: If the user is watching an anime, if the anime is on hold ect.
        :param score: the score the user gave the anime
        :param storage_type: (Coming once MAL accept string input)
        :param times_rewatched: the amount of times a user has watched an anime
        :param rewatch_value: Is the show enjoyable x amount of times
        :param date_started: The date the user started the anime
        :param date_finished: The date the user finished the anime
        :param priority: How highly an anime is on your to watch list
        :param enable_discussion: Yes or no, do you want to be offered to discuss the anime
        :param enable_rewatching: Yes or no are you rewatching the anime
        :param comments: Any comments the user wants to leave
        :param fansub_group: What fansub group subbed your anime
        :param tags: Any tags that relate to the anime
        """
        # Adds status to kwargs
        kwargs.update(status=status)
        # Changes to valid xml data
        xml = dicttoxml(kwargs, attr_type=False, custom_root='entry')
        # Parameters for the URL
        params = urllib.parse.urlencode({'data': xml})
        async with self.session.get(self.__API_BASE_URL + 'animelist/update/' + (str(anime_id)) + '.xml',
                                    params=params) as response:
            if response.status == 200:
                return True
            else:
                raise aiohttp.ClientResponseError(response.status)

    async def update_manga(self, manga_id: int, status: int, **kwargs):
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
        # Adds status to kwargs
        kwargs.update(status=status)
        # Changes to valid xml data
        xml_manga_values = dicttoxml(kwargs, attr_type=False, custom_root='entry')
        # Parameteres for the URL
        params = urllib.parse.urlencode({'data': xml_manga_values})
        async with self.session.get(self.__API_BASE_URL + 'mangalist/update/' + str(manga_id) + '.xml',
                                    params=params) as response:
            # If response is OK
            if response.status == 200:
                return True
            else:
                raise aiohttp.ClientResponseError(response.status)

    async def delete_anime(self, anime_id: int):
        async with self.session.get(self.__API_BASE_URL + 'animelist/delete/' + str(anime_id) + '.xml') as response:
            if response.status == 200:
                return True
            else:
                raise aiohttp.ClientResponseError(response.status)

    async def delete_manga(self, manga_id: int):
        async with self.session.get(self.__API_BASE_URL + 'mangalist/delete/' + str(manga_id) + '.xml') as response:
            if response.status == 200:
                return True
            else:
                raise aiohttp.ClientResponseError(response.status)

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
        if name in ('my_finish_date', 'my_start_date', 'series_end', 'series_start'):
            try:
                text = datetime.strptime(text, "%Y-%m-%d")
            except ValueError:
                text = datetime.fromtimestamp(0)
        return name, text

    async def get_user_series(self, profile: str, series_type: str):
        """
        :param profile: The name of the profile you're trying to get
        :param series_type: If you're looking for their manga or anime
        """
        # Params for the url
        params = urllib.parse.urlencode({
            'u': profile,
            'status': 'all',
            'type': series_type
        })
        # If series_type is in the tuple
        if series_type not in ('anime', 'manga'):
            raise InvalidSeriesTypeException
        else:
            async with self.session.get(
                    self.__MAL_APP_INFO, params=params) as response:
                soup = bs4.BeautifulSoup(await response.text(), "lxml")
            # Return as a dictionary
                return [dict(self.process_(child) for child in anime.children) for anime in soup.find_all(series_type)]
    # End of bit Zeta wrote

    async def get_public_user_data(self, username: str):
        async with self.session.get(self.__MAL_APP_INFO, params=urllib.parse.urlencode({'u': username})) as response:
            if response.status == 200:
                response_data = await response.read()
                # Since public user data is the first result that myanimelist ever gives
                to_parse = etree.fromstring(response_data)[0]
                # Return as a dictionary
                return dict(zip(['user_id', 'username', 'watching', 'completed', 'on_hold', 'dropped', 'plan_to_watch',
                                 'days_spent_watching'], [x.text for x in to_parse]))
            else:
                raise aiohttp.ClientResponseError(response.status)
