# Imports from standard libs
from datetime import datetime

# Imports from external libs
import aiohttp
import bs4
from dicttoxml import dicttoxml
from lxml import etree

# Module level imports
from .errors import InvalidSeriesTypeException, ResponseError
from .objects import Anime, Manga, UserInfo, SuperUser


class PyAnimeList:
    """
    An asynchronous API wrapper for the MyAnimeList API (Which is awful, where's this new one we were promised?)
    """
    # The base url for the API
    __API_BASE_URL = 'https://myanimelist.net/api/'
    # Undocumented endpoint for individual user information
    __MAL_APP_INFO = 'https://myanimelist.net/malappinfo.php'
    # Endpoint for checking credentials work
    __VERIFY_CREDENTIALS = __API_BASE_URL + "account/verify_credentials.xml"
    # Our search endpoints
    __ANIME_SEARCH_URL, __MANGA_SEARCH_URL = __API_BASE_URL + "anime/search.xml", __API_BASE_URL + "manga/search.xml"
    # Our add endpoints
    __ANIME_ADD_URL, __MANGA_ADD_URL = __API_BASE_URL + "animelist/add/{}.xml", __API_BASE_URL + "mangalist/add/{}.xml"
    # Our update endpoints
    __ANIME_UPDATE_URL, __MANGA_UPDATE_URL = __API_BASE_URL + "animelist/update/{}.xml", __API_BASE_URL + "mangalist/update/{}.xml"
    # Endpoints to delete anime/manga
    __ANIME_DELETE_URL, __MANGA_DELETE_URL = __API_BASE_URL + "animelist/delete/{}.xml", __API_BASE_URL + "mangalist/delete/{}.xml"

    def __init__(self, username: str, password: str, user_agent: str = None):
        """
        :param username: the username of the account that is being used to access the API (Only pass in if not using own clientsession)
        :param password: the password of the account that is being used to access the API (Only pass in if not using own clientsession)
        :param user_agent: useragent of the application, defaults to PyAnimeList unless explicitly passed through the keyword argument
        PyAnimeList if doing this, pass it in through your own ClientSession's auth)
        """
        # Set default User-Agent if it's not passed in
        self.user_agent = user_agent or "PyAnimeList (https://github.com/GetRektByMe/PyAnimeList)"
        # The basic auth that's needed to allow us to access the API, we pass the username/pass straight in
        self._auth = aiohttp.BasicAuth(login=username, password=password)

    async def verify_credentials(self):
        """
        This function is used for verifying if a users information is correct, it uses the username and password passed into self._auth)

        # Return
        :return type tuple:
        """
        with aiohttp.ClientSession(auth=self._auth, headers={"User-Agent": self.user_agent}) as session:
            async with session.get(self.__VERIFY_CREDENTIALS) as response:
                if response.status != 200:
                    raise ResponseError(response.status)
                response_data = await response.read()
                user = etree.fromstring(response_data)
                # Returns the username and id in tuple
                return (user.find("id").text, user.find("username").text)

    async def search_all_anime(self, search_query: str):
        """
        A function to get data for all search results from a query

        # Required
        :param search_query: is what'll be queried for the search results

        # Return
        :return type list:
        """
        with aiohttp.ClientSession(auth=self._auth, headers={"User-Agent": self.user_agent}) as session:
            async with session.get(self.__ANIME_SEARCH_URL, params={"q": search_query}) as response:
                # Raise an error if we get the wrong response code
                if response.status != 200:
                    raise ResponseError(response.status)
                response_data = await response.read()
                entries = etree.fromstring(response_data)
                # Create list to append anime objects to
                animes = []
                for entry in entries:
                    try:
                        animes.append(Anime(id=entry.find("id").text,
                                            title=entry.find("title").text,
                                            english=entry.find("english").text,
                                            synonyms=entry.find("synonyms").text,
                                            episodes=entry.find("episodes").text,
                                            type=entry.find("type").text,
                                            status=entry.find("status").text,
                                            start_date=entry.find("start_date").text,
                                            end_date=entry.find("end_date").text,
                                            synopsis=entry.find("synopsis").text.replace("<br />", ""),
                                            image=entry.find("image").text))
                    except AttributeError:  # Except AttributeError so when things are None it doesn't break
                        pass
                # Return as a list containing anime objects with data from the anime returned from the query
                return animes

    async def search_all_manga(self, search_query: str):
        """
        A function to get data for all search results from a query

        # Required
        :param search_query: is what'll be queried for the search results

        # Return
        :return type list:
        """
        with aiohttp.ClientSession(auth=self._auth, headers={"User-Agent": self.user_agent}) as session:
            async with session.get(self.__MANGA_SEARCH_URL, params={"q": search_query}) as response:
                # Raise an error if we get the wrong response code
                if response.status != 200:
                    raise ResponseError(response.status)
                response_data = await response.read()
                entries = etree.fromstring(response_data)
                # Create list to append manga objects to
                mangas = []
                for manga_entry in entries:
                    try:
                        mangas.append(Manga(id=manga_entry.find("id").text,
                                            title=manga_entry.find("title").text,
                                            english=manga_entry.find("english").text,
                                            synonyms=manga_entry.find("synonyms").text,
                                            volumes=manga_entry.find("volumes").text,
                                            chapters=manga_entry.find("chapters").text,
                                            type=manga_entry.find("type").text,
                                            status=manga_entry.find("status").text,
                                            start_date=manga_entry.find("start_date").text,
                                            end_date=manga_entry.find("end_date").text,
                                            synopsis=manga_entry.find("synopsis").text.replace("<br />", ""),
                                            image=manga_entry.find("image").text))
                    except AttributeError:  # Except AttributeError so when things are None it doesn't break
                        pass
                # Return as a list containing manga objects with data from the mangas returned from the query
                return mangas

    async def add_anime(self, anime_id: int, status: int, **kwargs):
        """
        # Required
        :param anime_id: id is the id of the anime that we'll be adding to the list
        :param status: If the user is watching an anime, if the anime is on hold ect

        # Optional
        :param episodes: Latest episode in the series the user has watched
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
        :param storage_types: 0-8 (0 is select storage type, 1 is hard drive, 2 is dvd/cd, 3 is None, 4 is retail dvd,
                                   5 is VHS, 6 is external HDD, 7 is NAS, 8 is blu-ray)
        :param storage_value: depends on storage_types, (if 1 it's total drive space, if two it's number of dvd/cds,
                                                         if 4 it's number of dvds, if 5 it's number of VHS tapes,
                                                         if 6 it's total drive space, if 7 it's total drive space,
                                                         if 8 it's number of blu-rays)

        # Return
        :return type boolean:
        """
        # Adds status to kwargs
        kwargs.update(status=status)
        # Turns kwargs into valid XML
        xml = dicttoxml(kwargs, attr_type=False, custom_root="entry")
        with aiohttp.ClientSession(auth=self._auth, headers={"User-Agent": self.user_agent}) as session:
            async with session.get(self.__ANIME_ADD_URL.format(str(anime_id)), params={"data": xml}) as response:
                # Raise an error if we get the wrong response code
                if response.status == 201:
                    raise ResponseError(response.status)
                # Return True to show adding the item worked
                return True

    async def add_manga(self, manga_id: int, status: int, **kwargs):
        """
        # Required
        :param manga_id: The id on MAL of the manga
        :param status: What you're currently doing with the manga, watching ect

        # Optional
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

        # Return
        :return type boolean:
        """
        # Adds status to kwargs
        kwargs.update(status=status)
        # Turns kwargs into valid XML
        xml = dicttoxml(kwargs, attr_type=False, custom_root="entry")
        with aiohttp.ClientSession(auth=self._auth, headers={"User-Agent": self.user_agent}) as session:
            async with session.get(self.__MANGA_ADD_URL.format(str(manga_id)), params={"data": xml}) as response:
                # Raise an error if we get the wrong response code
                if response.status != 201:
                    raise ResponseError(response.status)
                # Return True to show adding the item worked
                return True

    async def update_anime(self, anime_id: int, **kwargs):
        """
        # Required
        :param anime_id: id is the id of the anime that we'll be adding to the list

        # Optional
        :param episode: Latest episode in the series the user has watched
        :param status: If the user is watching an anime, if the anime is on hold ect.
        :param score: the score the user gave the anime
        :param storage_type: (Coming once MAL accept string input)
        :param times_rewatched: the amount of times a user has watched an anime
        :param rewatch_value: Is the show enjoyable x amount of times
        :param date_start: The date the user started the anime
        :param date_finish: The date the user finished the anime
        :param priority: How highly an anime is on your to watch list
        :param enable_discussion: Yes or no, do you want to be offered to discuss the anime
        :param enable_rewatching: Yes or no are you rewatching the anime
        :param comments: Any comments the user wants to leave
        :param fansub_group: What fansub group subbed your anime
        :param tags: Any tags that relate to the anime
        :param storage_types: 0-8 (0 is select storage type, 1 is hard drive, 2 is dvd/cd, 3 is None, 4 is retail dvd,
                                   5 is VHS, 6 is external HDD, 7 is NAS, 8 is blu-ray)
        :param storage_value: depends on storage_types, (if 1 it's total drive space, if two it's number of dvd/cds,
                                                         if 4 it's number of dvds, if 5 it's number of VHS tapes,
                                                         if 6 it's total drive space, if 7 it's total drive space,
                                                         if 8 it's number of blu-rays)
        # Return
        :return type boolean:
        """
        # Turns kwargs into valid XML
        xml = dicttoxml(kwargs, attr_type=False, custom_root="entry")
        with aiohttp.ClientSession(auth=self._auth, headers={"User-Agent": self.user_agent}) as session:
            async with session.get(self.__ANIME_UPDATE_URL.format(anime_id), params={"data": xml}) as response:
                # Raise an error if we get the wrong response code
                if response.status != 200:
                    raise ResponseError(response.status)
                # Return true to show the item has been updated fine
                return True

    async def update_manga(self, manga_id: int, **kwargs):
        """
        # Required
        :param manga_id:

        # Optional
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

        # Return
        :return type boolean:
        """
        # Turns kwargs into valid XML
        xml = dicttoxml(kwargs, attr_type=False, custom_root="entry")
        with aiohttp.ClientSession(auth=self._auth, headers={"User-Agent": self.user_agent}) as session:
            async with session.get(self.__MANGA_UPDATE_URL.format(manga_id), params={"data": xml}) as response:
                # Raise an error if we get the wrong response code
                if response.status != 200:
                    raise ResponseError(response.status)
                # Return true to show the item has been updated fine
                return True

    async def delete_anime(self, anime_id: int):
        """
        # Required
        :param anime_id: the id of the anime on myanimelist

        # Return
        :return type boolean:
        """
        with aiohttp.ClientSession(auth=self._auth, headers={"User-Agent": self.user_agent}) as session:
            async with session.get(self.__ANIME_DELETE_URL.format(anime_id)) as response:
                # Raise an error if we get the wrong response code
                if response.status != 200:
                    raise ResponseError(response.status)
                # Return True to indicate that deleting the item worked fine
                return True

    async def delete_manga(self, manga_id: int):
        """
        # Required
        :param manga_id: the id of the manga on myanimelist

        # Return
        :return type boolean:
        """
        with aiohttp.ClientSession(auth=self._auth, headers={"User-Agent": self.user_agent}) as session:
            async with session.get(self.__MANGA_DELETE_URL.format(manga_id)) as response:
                # Raise an error if we get the wrong response code
                if response.status != 200:
                    raise ResponseError(response.status)
                # Return True to indicate that deleting the item worked fine
                return True

    # Zeta wrote this bit
    @staticmethod
    def process_(child):
        name, text = child.name, child.get_text()
        try:
            # Try converting text to an integer
            text = int(text)
        # Ignore if we get a bad value
        except ValueError:
            pass
        if name == "my_last_updated":
            text = datetime.fromtimestamp(float(text))
        if name in ('my_finish_date', "my_start_date", "series_end", "series_start"):
            try:
                text = datetime.strptime(text, "%Y-%m-%d")
            except ValueError:
                text = datetime.fromtimestamp(0)
        # Return name and text in tuple
        return (name, text)

    async def get_user_series(self, profile: str, series_type: str):
        """
        # Required
        :param profile: The name of the profile you're trying to get
        :param series_type: If you're looking for manga or anime

        # Return
        :return type list:
        """
        # Params for the url
        params = {
            "u": profile,
            "status": 'all',
            "type": series_type
                }
        # If series_type is in the tuple it continues, otherwise it raises the InvalidSeriesTypeException
        if series_type not in ("anime", "manga"):
            raise InvalidSeriesTypeException()
        else:
            with aiohttp.ClientSession(auth=self._auth, headers={"User-Agent": self.user_agent}) as session:
                async with session.get(self.__MAL_APP_INFO, params=params) as response:
                    # Raise an error if we get the wrong response code
                    if response.status != 200:
                        raise ResponseError(response.status)
                    # Get the response text and set parser
                    soup = bs4.BeautifulSoup(await response.text(), "lxml")
                    # Return as a list
                    return [dict(self.process_(child) for child in anime.children) for anime in soup.find_all(series_type)]

    # End of bit Zeta wrote

    async def get_multiple_users_public_data(self, *users: str):
        """
        # Required
        :param *users: arbitrary amount of usernames who's data we're getting

        :return type list:
        """
        # List that stores all the UserInfo Objects to return
        user_data = []
        with aiohttp.ClientSession(auth=self._auth, headers={"User-Agent": self.user_agent}) as session:
            # Go through all the users the user passes to the function
            for user in users:
                async with session.get(self.__MAL_APP_INFO, params={"u": user}) as response:
                    # Raise an error if we get the wrong response code
                    if response.status != 200:
                        raise ResponseError(response.status)
                    response_data = await response.read()
                    # We want the [0] index as myanimelist always returns the user data first
                    user_info = etree.fromstring(response_data)[0]
                    # Add to list containing UserInfo objects
                    user_data.append(UserInfo(user_id=user_info.find("user_id").text,
                                              username=user_info.find("user_name").text,
                                              watching=user_info.find("user_watching").text,
                                              completed=user_info.find("user_completed").text,
                                              on_hold=user_info.find("user_onhold").text,
                                              dropped=user_info.find("user_dropped").text,
                                              plan_to_watch=user_info.find("user_plantowatch").text,
                                              days_spent_watching=user_info.find("user_days_spent_watching").text))
        # Return list containing UserInfo objects
        return user_data

    # Helper function that no one should touch!
    async def _get_all_user_data_helper(self, user: str):
        with aiohttp.ClientSession(auth=self._auth, headers={"User-Agent": self.user_agent}) as session:
            async with session.get(self.__MAL_APP_INFO, params={"u": user}) as response:
                # Raise an error if we get the wrong response code
                if response.status != 200:
                    raise ResponseError(response.status)
                # Get a bytes like object of the response data for parsing with find on etree
                response_data = await response.read()
                # Get a string from the bytes object
                user_info = etree.fromstring(response_data)[0]
                # Return a UserInfo object will all our needed data
                return UserInfo(user_id=user_info.find("user_id").text,
                                username=user_info.find("user_name").text,
                                watching=user_info.find("user_watching").text,
                                completed=user_info.find("user_completed").text,
                                on_hold=user_info.find("user_onhold").text,
                                dropped=user_info.find("user_dropped").text,
                                plan_to_watch=user_info.find("user_plantowatch").text,
                                days_spent_watching=user_info.find("user_days_spent_watching").text)

    async def get_all_user_data(self, *users: str):
        """
        Gets all the data from a user, note that I highly recommend NOT using this as it's very slow!

        # Required
        :param *users: arbitrary amount of users who's data we're getting

        :return type list:
        """
        # Make our list that's going to hold all our SuperUser Objects
        user_objects = []
        with aiohttp.ClientSession(auth=self._auth, headers={"User-Agent": self.user_agent}) as session:
            # Go through all the users the user passes to the function
            for user in users:
                async with session.get(self.__MAL_APP_INFO, params={"u": user}) as response:
                    # Raise an error if we get the wrong response code
                    if response.status != 200:
                        raise ResponseError(response.status)
                    # Get our objects to pass to the SuperUser object
                    user_info = await self._get_all_user_data_helper(user)
                    user_anime = await self.get_user_series(user, "anime")
                    user_manga = await self.get_user_series(user, "manga")
                    # Append the SuperUser Object to the user_objects list
                    user_objects.append(SuperUser(info=user_info, anime=user_anime, manga=user_manga))
        # Return a list of SuperUser objects
        return user_objects
