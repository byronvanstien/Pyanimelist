# Standard library imports
import asyncio
import json
import unittest

# Third party libraries
import aiohttp
from PyAnimeList import PyAnimeList, errors

with open("setup.json") as file:
    setup_file = json.load(file)


class PyAnimeListTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._auth = aiohttp.BasicAuth(login=setup_file["username"], password=setup_file["password"])
        cls.session = aiohttp.ClientSession(auth=cls._auth)
        cls.loop = asyncio.get_event_loop()
        cls.pyanilist = PyAnimeList(session=cls.session)

    # Check that we get the proper response from anime searching
    def test_search_anime():
        pass

    @classmethod
    def tearDownClass(cls):
        loop = asyncio.get_event_loop()
        loop.close()
