# PyAnimeList
An async Python 3 wrapper for the MyAnimeList API

### Requirements
* aiohttp
* bs4
* dicttoxml
* lxml

# Installing PyAnimeList
### Notice
**some people have trouble compiling lxml, if you find yourself having trouble installing lxml on windows, if any troubles arise you should use a precompiled whl file**
 Install from pip
 ```
 pip install pyanimelist
 ```
 Install from git for the cutting edge
 ```
 pip install git+https://github.com/GetRektByMe/Pyanimelist.git
 ```
# Creating the PyAnimeList Object
```
instance = PyAnimeList(username, password)
```
