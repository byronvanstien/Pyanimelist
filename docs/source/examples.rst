Examples
--------

Search anime
~~~~~~~~~~~~

.. code-block:: py

   import asyncio

   import pyanimelist

   instance = pyanimelist.PyAnimeList(username, password)
   loop = asyncio.get_event_loop()

   loop.run_until_complete(instance.verify_credentials())
   results = loop.run_until_complete(instance.search_all_anime("Mahouka koukou no rettousei"))

   print(results)


Search manga
~~~~~~~~~~~~

.. code-block:: py

   import asyncio

   import pyanimelist

   instance = pyanimelist.PyAnimeList(username, password)
   loop = asyncio.get_event_loop()

   loop.run_until_complete(instance.verify_credentials())
   results = loop.run_until_complete(instance.search_all_manga("Mahouka koukou no rettousei"))

   print(results)


Add anime
~~~~~~~~~

.. code-block:: py

   import asyncio

   import pyanimelist
   from pyanimelist.enumerations import AnimeStatus

   instance = pyanimelist.PyAnimeList(username, password)
   loop = asyncio.get_event_loop()

   loop.run_until_complete(instance.verify_credentials())

   # The first argument is the anime id, the second argument is the status
   loop.run_until_complete(instance.add_anime(1, AnimeStatus.WATCHING.value))


Add manga
~~~~~~~~~

.. code-block:: py

   import asyncio

   import pyanimelist
   from pyanimelist.enumerations import MangaStatus

   instance = pyanimelist.PyAnimeList(username, password)
   loop = asyncio.get_event_loop()

   loop.run_until_complete(instance.verify_credentials())

   # The first argument is the manga id, the second is the status
   loop.run_until_complete(instance.add_manga(1, MangaStatus.READING.value))


Update anime
~~~~~~~~~~~~

.. code-block:: py

   import asyncio
   import pyanimelist

   instance = pyanimelist.PyAnimeList(username, password)
   loop = asyncio.get_event_loop()

   loop.run_until_complete(instance.verify_credentials())

   # This can take anything specified in the docstring but nothing is required besides the animes id
   loop.run_until_complete(instance.update_anime(1))


Update manga
~~~~~~~~~~~~

.. code-block:: py

   import asyncio
   import pyanimelist

   instance = pyanimelist.PyAnimeList(username, password)
   loop = asyncio.get_event_loop()

   loop.run_until_complete(instance.verify_credentials())

   # This can take anything specified in the docstring but nothing is required besides the animes id
   loop.run_until_complete(instance.update_manga(1))


Delete anime
~~~~~~~~~~~~

.. code-block:: py

   import asyncio
   import pyanimelist

   instance = pyanimelist.PyAnimeList(username, password)
   loop = asyncio.get_event_loop()

   loop.run_until_complete(instance.verify_credentials())

   loop.run_until_complete(instance.delete_anime(1))


Delete manga
~~~~~~~~~~~~

.. code-block:: py

   import asyncio
   import pyanimelist

   instance = pyanimelist.PyAnimeList(username, password)
   loop = asyncio.get_event_loop()

   loop.run_until_complete(instance.verify_credentials())

   loop.run_until_complete(instance.delete_manga(1))


Get user series
~~~~~~~~~~~~~~~

.. code-block:: py

   import asyncio
   import pyanimelist

   # This can be either anime or manga
   series_type = "anime"

   instance = pyanimelist.PyAnimeList(username, password)
   loop = asyncio.get_event_loop()

   loop.run_until_complete(instance.verify_credentials())

   loop.run_until_complete(instance.get_user_series(username, series_type))


Get user data
~~~~~~~~~~~~~

.. code-block:: py

   import asyncio
   import pyanimelist

   instance = pyanimelist.PyAnimeList(username, password)
   loop = asyncio.get_event_loop()

   loop.run_until_complete(instance.verify_credentials())

   loop.run_until_complete(instance.get_user_data(username))
