from typing import Dict

import aiohttp


async def fetch_url(url: str, auth: aiohttp.BasicAuth, headers: Dict["str", "str"] = None):
    """
    Function used to eliminate code reuse with creating ClientSessions

    :param str url: The URL you're fetching
    :param aiohttp.BasicAuth auth: The BasicAuth object being passed to aiohttp.ClientSession
    :param dict headers: The headers to be passed to `myanimelist`_

    :rtype: bytes

    Example usage:

    .. code-block:: py

       import asyncio

       loop = asyncio.get_event_loop()
       loop.run_until_complete(fetch_url("url", aiohttp.BasicAuth(login="username", password="password"), {"User-Agent": "PyAnimeList"}))
    """
    if not headers:
        headers = {}
    with aiohttp.ClientSession(auth=auth, headers=headers) as session:
        async with session.get(url) as response:
            return response.read()
