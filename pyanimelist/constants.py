from . import __version__ as LIBRARY_VERSION, __title__ as LIBRARY_NAME

LIBRARY_URL = "https://github.com/GetRektByMe/Pyanimelist"

UA = "{} ({}, {})".format(LIBRARY_NAME, LIBRARY_URL, LIBRARY_VERSION)


API_BASE_URL = "https://myanimelist.net/api/"

MAL_APP_INFO = "https://myanimelist.net/malappinfo.php"

VERIFY_CREDENTIALS = API_BASE_URL + "account/verify_credentials.xml"

ANIME_SEARCH_URL = API_BASE_URL + "anime/search.xml"
ANIME_ADD_URL = API_BASE_URL + "animelist/add/{}.xml"
ANIME_UPDATE_URL = API_BASE_URL + "animelist/update/{}.xml"
ANIME_DELETE_URL = API_BASE_URL + "animelist/delete/{}.xml"

MANGA_SEARCH_URL = API_BASE_URL + "manga/search.xml"
MANGA_ADD_URL = API_BASE_URL + "mangalist/add/{}.xml"
MANGA_UPDATE_URL = API_BASE_URL + "mangalist/update/{}.xml"
MANGA_DELETE_URL = API_BASE_URL + "mangalist/delete/{}.xml"
