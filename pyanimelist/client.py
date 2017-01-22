import html
from datetime import datetime
from typing import List, Tuple

import bs4
import aiohttp
from lxml import etree
from dicttoxml import dicttoxml

from .abstractions import Titles, Dates
from .objects import Anime, Manga, UserInfo
from .errors import InvalidSeriesTypeException, ResponseError, InvalidCredentials
from .constants import (
    UA,
    MAL_APP_INFO,
    VERIFY_CREDENTIALS,
    MANGA_SEARCH_URL,
    MANGA_ADD_URL,
    MANGA_UPDATE_URL,
    MANGA_DELETE_URL,
    ANIME_SEARCH_URL,
    ANIME_ADD_URL,
    ANIME_UPDATE_URL,
    ANIME_DELETE_URL
)


class PyAnimeList(object):
    """
    An asynchronous API wrapper for the MyAnimeList API (Which is awful, where's this new one we were promised?)
    """

    def __init__(self, username: str, password: str, user_agent: str = None):
        """
        :param username: the username of the account that is being used to access the API
        :param password: the password of the account that is being used to access the API
        :param user_agent: useragent of the application
        """
        self.user_agent = user_agent or UA
        self._auth = aiohttp.BasicAuth(login=username, password=password)

    async def verify_credentials(self) -> Tuple[str]:
        """
        This function is used for verifying if a users information is correct, it uses the username and password passed into self._auth)
        :return: The id and the username of the verified user
        :rtype: tuple
        """
        with aiohttp.ClientSession(auth=self._auth, headers={"User-Agent": self.user_agent}) as session:
            async with session.get(VERIFY_CREDENTIALS) as response:
                if response.status != 200:
                    raise InvalidCredentials
                response_data = await response.read()
                user = etree.fromstring(response_data)
                return user.find("id").text, user.find("username").text

    async def search_all_anime(self, search_query: str) -> List[Anime]:
        """
        A function to get data for all search results from a query
        :param str search_query: is what'll be queried for the search results
        :return: List of anime objects
        :rtype: List
        """
        with aiohttp.ClientSession(auth=self._auth, headers={"User-Agent": self.user_agent}) as session:
            async with session.get(ANIME_SEARCH_URL, params={"q": search_query}) as response:
                # Raise an error if we get the wrong response code
                if response.status != 200:
                    raise ResponseError(response.status)
                response_data = await response.read()
                entries = etree.fromstring(response_data)
                animes = []
                for entry in entries:
                    try:
                        animes.append(
                            Anime(
                                id=entry.find("id").text,
                                titles=Titles(
                                    jp=entry.find("title").text,
                                    english=entry.find("english").text,
                                    synonyms=entry.find("synonyms").text.split(";")
                                ),
                                episode_count=entry.find("episodes").text,
                                dates=Dates(
                                    start=entry.find("start_date").text,
                                    end=entry.find("end_date").text
                                ),
                                type=entry.find("type").text,
                                status=entry.find("status").text,
                                synopsis=html.unescape(entry.find("synopsis").text.replace("<br />", "").replace("[i]", "").replace("[/i]", "")),
                                cover=entry.find("image").text
                            )
                        )
                    except AttributeError:
                        continue
                return animes

    async def search_all_manga(self, search_query: str) -> List[Manga]:
        """
        A function to get data for all search results from a query
        :param str search_query: is what'll be queried for the search results
        :return: List of anime objects
        :rtype: List
        """
        with aiohttp.ClientSession(auth=self._auth, headers={"User-Agent": self.user_agent}) as session:
            async with session.get(MANGA_SEARCH_URL, params={"q": search_query}) as response:
                # Raise an error if we get the wrong response code
                if response.status != 200:
                    raise ResponseError(response.status)
                response_data = await response.read()
                entries = etree.fromstring(response_data)
                mangas = []
                for entry in entries:
                    try:
                        mangas.append(
                            Manga(
                                id=entry.find("id").text,
                                titles=Titles(
                                    jp=entry.find("title").text,
                                    english=entry.find("english").text,
                                    synonyms=entry.find("synonyms").text.split(";")
                                ),
                                volumes=entry.find("volumes").text,
                                chapters=entry.find("chapters").text,
                                type=entry.find("type").text,
                                status=entry.find("status").text,
                                dates=Dates(
                                    start=entry.find("start_date").text,
                                    end=entry.find("end_date").text
                                ),
                                synopsis=html.unescape(entry.find("synopsis").text.replace("<br />", "").replace("[i]", "").replace("[/i]", "")),
                                cover=entry.find("image").text
                            )
                        )
                    except AttributeError:
                        continue
                return mangas

    async def add_anime(self, anime_id: int, status: int, **kwargs) -> bool:
        """
        :param int anime_id: id is the id of the anime that we'll be adding to the list
        :param int status: If the user is watching an anime, if the anime is on hold ect
        :param int episodes: Latest episode in the series the user has watched
        :param int score: the score the user gave the anime
        :param int storage_type: (Coming once MAL accept string input)
        :param int times_rewatched: the amount of times a user has watched an anime
        :param int rewatch_value: Is the show enjoyable x amount of times
        :param str date_started: The date the user started the anime
        :param str date_finished: The date the user finished the anime
        :param int priority: How highly an anime is on your to watch list
        :param bool enable_discussion: Yes or no, do you want to be offered to discuss the anime
        :param bool enable_rewatching: Yes or no are you rewatching the anime
        :param str comments: Any comments the user wants to leave
        :param str fansub_group: What fansub group subbed your anime
        :param str tags: Any tags that relate to the anime
        :param int storage_types: 0-8 (0 is select storage type, 1 is hard drive, 2 is dvd/cd, 3 is None, 4 is retail dvd,
                                       5 is VHS, 6 is external HDD, 7 is NAS, 8 is blu-ray)
        :param int storage_value: depends on storage_types, (if 1 it's total drive space, if two it's number of dvd/cds,
                                                             if 4 it's number of dvds, if 5 it's number of VHS tapes,
                                                             if 6 it's total drive space, if 7 it's total drive space,
                                                             if 8 it's number of blu-rays)
        :rtype: bool
        """
        kwargs["status"] = status
        xml = dicttoxml(kwargs, attr_type=False, custom_root="entry")
        with aiohttp.ClientSession(auth=self._auth, headers={"User-Agent": self.user_agent}) as session:
            async with session.get(ANIME_ADD_URL.format(str(anime_id)), params={"data": xml}) as response:
                # Raise an error if we get the wrong response code
                if response.status != 201:
                    raise ResponseError(response.status)
                # Return True to show adding the item worked
                return True

    async def add_manga(self, manga_id: int, status: int, **kwargs) -> bool:
        """
        :param int manga_id: The id on MAL of the manga
        :param int status: What you're currently doing with the manga, watching ect
        :param int chapter: How many read chapters
        :param int volumes: How many read volumes
        :param int status: If currently reading, on hold ect
        :param int score: Score user is giving the manga
        :param int times_reread: How many times the user has read the series
        :param int reread_value: How rereadable a manga is
        :param str date_start: What date the user started reading
        :param str date_finish: What date the user finished the manga
        :param int priority: How highly the user wants to read the manga
        :param bool enable_discussion: If you want to be offered to discuss the manga or not
        :param bool enable_rereading: If you're currently rereading the manga
        :param str comments: A comment to leave for the manga
        :param str scan_group: What groups scans you're reading
        :param str tags: Tags related to the novel, seperated by comma
        :param retail_volumes: How many volumes you own
        :rtype: bool
        """
        kwargs["status"] = status
        xml = dicttoxml(kwargs, attr_type=False, custom_root="entry")
        with aiohttp.ClientSession(auth=self._auth, headers={"User-Agent": self.user_agent}) as session:
            async with session.get(MANGA_ADD_URL.format(str(manga_id)), params={"data": xml}) as response:
                # Raise an error if we get the wrong response code
                if response.status != 201:
                    raise ResponseError(response.status)
                # Return True to show adding the item worked
                return True

    async def update_anime(self, anime_id: int, **kwargs) -> bool:
        """
        :param anime_id: id is the id of the anime that we'll be adding to the list
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
        :param storage_value: depends on storage_types, (if 1 it's total drive space, if 2 it's number of dvd/cds,
                                                         if 4 it's number of dvds, if 5 it's number of VHS tapes,
                                                         if 6 it's total drive space, if 7 it's total drive space,
                                                         if 8 it's number of blu-rays)
        :return type boolean:
        """
        # Turns kwargs into valid XML
        xml = dicttoxml(kwargs, attr_type=False, custom_root="entry")
        with aiohttp.ClientSession(auth=self._auth, headers={"User-Agent": self.user_agent}) as session:
            async with session.get(ANIME_UPDATE_URL.format(anime_id), params={"data": xml}) as response:
                # Raise an error if we get the wrong response code
                if response.status != 200:
                    raise ResponseError(response.status)
                # Return true to show the item has been updated fine
                return True

    async def update_manga(self, manga_id: int, **kwargs) -> bool:
        """
        :param manga_id:
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
        :return type boolean:
        """
        xml = dicttoxml(kwargs, attr_type=False, custom_root="entry")
        with aiohttp.ClientSession(auth=self._auth, headers={"User-Agent": self.user_agent}) as session:
            async with session.get(MANGA_UPDATE_URL.format(manga_id), params={"data": xml}) as response:
                # Raise an error if we get the wrong response code
                if response.status != 200:
                    raise ResponseError(response.status)
                # Return True to show the item has been updated
                return True

    async def delete_anime(self, anime_id: int) -> bool:
        """
        :param anime_id: the id of the anime on myanimelist
        :return type boolean:
        """
        with aiohttp.ClientSession(auth=self._auth, headers={"User-Agent": self.user_agent}) as session:
            async with session.get(ANIME_DELETE_URL.format(anime_id)) as response:
                # Raise an error if we get the wrong response code
                if response.status != 200:
                    raise ResponseError(response.status)
                # Return True to indicate that deleting the item worked
                return True

    async def delete_manga(self, manga_id: int) -> bool:
        """
        :param manga_id: the id of the manga on myanimelist
        :return type boolean:
        """
        with aiohttp.ClientSession(auth=self._auth, headers={"User-Agent": self.user_agent}) as session:
            async with session.get(MANGA_DELETE_URL.format(manga_id)) as response:
                # Raise an error if we get the wrong response code
                if response.status != 200:
                    raise ResponseError(response.status)
                # Return True to indicate that deleting the item worked
                return True

    # Zeta wrote this bit
    @staticmethod
    def process_(child) -> Tuple[str, datetime]:
        name, text = child.name, child.get_text()
        try:
            # Try converting text to an integer
            text = int(text)
        # Ignore if we get a value we can't cast to int
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
        return name, text

    async def get_user_series(self, username: str, series_type: str):
        """
        :param username: The name of the accounts information you're trying to get
        :param series_type: If you're looking for manga or anime
        :return type list:
        """
        params = {
            "u": username,
            "status": 'all',
            "type": series_type
        }
        if series_type not in ("anime", "manga"):
            raise InvalidSeriesTypeException
        else:
            with aiohttp.ClientSession(auth=self._auth, headers={"User-Agent": self.user_agent}) as session:
                async with session.get(MAL_APP_INFO, params=params) as response:
                    # Raise an error if we get the wrong response code
                    if response.status != 200:
                        raise ResponseError(response.status)
                    # Get the response text and set parser
                    soup = bs4.BeautifulSoup(await response.text(), "lxml")
                    return [dict(self.process_(child) for child in anime.children) for anime in soup.find_all(series_type)]
    # End of bit Zeta wrote

    async def get_user_data(self, user: str) -> UserInfo:
        """
        :param user: username who's information we're getting
        :return type list:
        """
        # List that stores all the UserInfo Objects to return
        with aiohttp.ClientSession(auth=self._auth, headers={"User-Agent": self.user_agent}) as session:
            async with session.get(MAL_APP_INFO, params={"u": user}) as response:
                # Raise an error if we get the wrong response code
                if response.status != 200:
                    raise ResponseError(response.status)
                response_data = await response.read()
                # We want the [0] index as myanimelist always returns the user data first
                user_info = etree.fromstring(response_data)[0]
                # Add to list containing UserInfo objects
                return UserInfo(
                    id=user_info.find("user_id").text,
                    username=user_info.find("user_name").text,
                    watching=user_info.find("user_watching").text,
                    completed=user_info.find("user_completed").text,
                    on_hold=user_info.find("user_onhold").text,
                    dropped=user_info.find("user_dropped").text,
                    plan_to_watch=user_info.find("user_plantowatch").text,
                    days_spent_watching=user_info.find("user_days_spent_watching").text
                )
