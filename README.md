# PyAnimeList
An async Python 3 wrapper for the MyAnimeList API

#Requirements
* Python 3.5
* aiohttp
* bs4
* dicttoxml
* lxml

***You may fall into trouble trying to download this as PyAnimeList, in which case, go download a c++ compiler and it should fix any issues you run into***


# Installing PyAnimeList
 ```
 pip install pyanimelist
 ```

#Creating the PyAnimeList Object
If not passing the username and password directly into the PyAnimeList object on creation, 
you should have a setup file that is called setup.json and it should look like this, note that this is what PyAnimeList will default to,
if you don't pass a username and password in yourself.
```
{
    "username": "Your MyAnimeList Username"
    "password": "Your MyAnimeList Password"
}
```