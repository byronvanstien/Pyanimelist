Pyanimelist
-----------

About
-----

*Pyanimelist* is an asynchronous wrapper for the MyAnimeList API, using lxml and aiohttp.

Installation
------------

Pyanimelist will only work on Python 3.5+ as it heavily uses the `Typing`_ library, which is only available from 3.5 onwards. It also uses the 3.5 syntax *async def* rather than the *@asyncio.coroutine*.

Pyanimelist is installed through pip for the latest released version.

::

    $ pip install pyanimelist

If you want the latest development version you can install from the git repo on `GitHub`_

::

    $ pip install git+https://github.com/GetRektByMe/Pyanimelist.git

**Note that the Git version isn't guarenteed to be work properly and lots of things may be broken.**

Contents:
---------
.. toctree ::
   :maxdepth: 2

   examples.rst
   whats_new.rst
   api.rst
   faq.rst



.. _Typing: https://docs.python.org/3.5/library/typing.html
.. _GitHub: https://github.com/GetRektByMe/Pyanimelist
.. _Examples: https://github.com/GetRektByMe/tree/master/examples
