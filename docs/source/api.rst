.. currentmodule:: pyanimelist

API reference
-------------

.. note::

    There is currently nothing logged on the backend of Pyanimelist; This is planned to be added in future commits.

.. note::

   The use of BeautifulSoup will soon be depreciated and will switch to an lxml backend for the one function that uses BeautifulSoup.

Find out the version of Pyanimelist you have
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. data:: __version__

    A string that represents the version of Pyanimelist you're using, for example ``"1.0.0"``

Client
------
.. autoclass:: PyAnimeList
   :members:


Exceptions
----------

.. autoclass:: pyanimelist.errors.PyAnimeListException
   :members:

.. autoclass:: pyanimelist.errors.InvalidSeriesTypeException
   :members:

.. autoclass:: pyanimelist.errors.ResponseError
   :members:

.. autoclass:: pyanimelist.errors.InvalidCredentials
   :members:


Dataclasses
-----------

.. note::

   These are not for creating yourself, these are handled and given to you from the libraries backend.

.. autoclass:: pyanimelist.objects.Anime

   .. attribute:: id: int

      The id of the anime `myanimelist`_ returns

   .. attribute:: titles: pyanimelist.abstractions.Titles

      A :class:`pyanimelist.abstractions.Titles` abstraction which contains all the titles associated with the anime

   .. attribute:: episode_count: int

      The amount of episodes the anime has

   .. attribute:: dates: pyanimelist.abstractions.Dates

      A :class:`pyanimelist.abstractions.Dates` abstraction which contains two datetime objects which are associated with the anime's start and end dates

   .. attribute:: type: str

      The type of show it is, Movie, OVA, TV etc. This is not currently documented by MAL (They don't say what it has the possibility of being).

   .. attribute:: status: pyanimelist.enumerations.AnimeStatus

      A :class:`pyanimelist.enumerations.AnimeStatus` that represents if the anime is completed, dropped etc.

   .. attribute:: synopsis: str

      The entire synopsis of the anime as returned by the `myanimelist`_ API

   .. attribute:: cover: str

      The link to the anime's cover as returned by the `myanimelist`_ API

.. autoclass:: pyanimelist.objects.Manga

   .. attribute:: id: int

      The id of the manga `myanimelist`_ returns

   .. attribute:: titles: pyanimelist.abstractions.Titles

      A :class:`pyanimelist.abstractions.Titles` abstraction which contains all the titles associated with the manga

   .. attribute:: volumes: int

      The amount of volumes the manga has released

   .. attribute:: chapters: int

      The amount of chapters the manga has released

   .. attribute:: type: str

      The type of "manga" it is, Manga, One-shot, Novel etc. This isn't currently documented by MAL (They don't say what it has the possibility of being)

   .. attribute:: status: pyanimelist.enumerations.MangaStatus

      A :class:`pyanimelist.enumerations.MangaStatus` that represents if the manga is completed, dropped etc.

   .. attribute:: dates: pyanimelist.abstractions.Dates

      A :class:`pyanimelist.abstractions.Dates` abstraction which contains two datetime objects which are associated with the anime's start and end dates

   .. attribute:: synopsis: str

      The entire synopsis of the manga as returned by the `myanimelist`_ API

   .. attribute:: cover: str

      The link to the manga's cover as returned by the `myanimelist`_ API

.. autoclass:: pyanimelist.objects.UserInfo

   .. attribute: id: int

      The id of the user

   .. attribute:: username: str

      The name of the user

   .. attribute:: watching: int

      The amount of anime currently being watched by the user

   .. attribute:: completed: int

      The amount of anime completed by the user

   .. attribute:: on_hold: int

      The amount of anime currently on hold by the user

   .. attribute:: dropped: int

      The amount of anime the user has dropped

   .. attribute:: plan_to_watch: int

      The amount of anime that the user plans to watch

   .. attribute:: days_spent_watching: float

      The amount of days spent watching anime by the user

.. _myanimelist: https://myanimelist.net

Enumerations
------------

The API returns integers which we plug into our `enumerations`_ for easy filtering

.. class:: pyanimelist.enumerations.AnimeStatus

   Specifies the status of the :class:`Anime`.

   .. attribute:: WATCHING

      The anime is currently being watched

   .. attribute:: COMPLETED

      The anime has been completely watched

   .. attribute:: ON_HOLD

      The anime is currently on hold

   .. attribute:: DROPPED

      The anime was dropped mid way through watching

   .. attribute:: PLAN_TO_WATCH

      The anime has been planned to be watched


.. class:: pyanimelist.enumerations.MangaStatus

   Specifies the status of the :class:`Manga`.

   .. attribute:: READING

      The manga is currently being read

   .. attribute:: COMPLETED

      The manga has been completely read

   .. attribute:: ON_HOLD

      The manga is currently on hold

   .. attribute:: DROPPED

      The manga was dropped mid way through reading

   .. attribute:: PLAN_TO_READ

      The manga has been planned to be read

.. _enumerations: https://docs.python.org/3/library/enum.html


Abstractions
------------

.. note::

   These are used in the backend of the library and are not for using outside it!

.. autoclass:: pyanimelist.abstractions.Titles
   :members:

.. autoclass:: pyanimelist.abstractions.Dates
   :members:
