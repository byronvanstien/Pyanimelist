from setuptools import setup, find_packages

from pyanimelist.constants import LIBRARY_URL
from pyanimelist import (
    __license__ as license,
    __author__ as author,
    __title__ as title,
    __version__ as version
)

setup(
    name=title,
    version=version,
    packages=find_packages(),
    url=LIBRARY_URL,
    license=license,
    author=author,
    author_email='',
    description='Python 3 bindings for the MyAnimeList API.',
    long_description='An asynchronous wrapper for the MyAnimeList api.',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries'
    ],
    keywords="aiohttp asyncio myanimelist xml parsing",
    install_requires=['aiohttp', 'bs4', 'lxml', 'dicttoxml'],
)
