# ██╗░░░██╗██╗██████╗░███████╗░█████╗░██╗░░██╗░█████╗░░██████╗██╗░░██╗
# ██║░░░██║██║██╔══██╗██╔════╝██╔══██╗██║░░██║██╔══██╗██╔════╝██║░░██║
# ╚██╗░██╔╝██║██║░░██║█████╗░░██║░░██║███████║███████║╚█████╗░███████║
# ░╚████╔╝░██║██║░░██║██╔══╝░░██║░░██║██╔══██║██╔══██║░╚═══██╗██╔══██║
# ░░╚██╔╝░░██║██████╔╝███████╗╚█████╔╝██║░░██║██║░░██║██████╔╝██║░░██║
# ░░░╚═╝░░░╚═╝╚═════╝░╚══════╝░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░╚═╝░░╚═╝

"""
videohash is a video hashing library written in Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
https://github.com/akamhy/videohash

Usage:
    >>> import videohash
    >>> hash1 = videohash.from_url("https://raw.githubusercontent.com/akamhy/videohash/main/assets/rocket.webm")
    >>> str(hash1)
    '7c7e7ff9ffff0000'
    >>> hash2 = videohash.from_url("https://www.youtube.com/watch?v=PapBjpzRhnA")
    >>> str(hash2)
    'fc7e7ffbffff0000'
    >>>
    >>> diff = hash1 - hash2
    >>> diff
    2
    >>>
    >>> hash3 = videohash.from_url("https://www.youtube.com/watch?v=_T8cn2J13-4")
    >>> diff = hash1 - hash3
    >>> diff
    37
    >>> str(hash3)
    '3cffff0000000eff'
    >>>
    >>> #hash4 file is hash1 file downloaded locally. Use absolute path
    >>> hash4 = videohash.from_path("/home/akamhy/Downloads/rocket.webm")
    >>> diff = hash4 - hash1
    >>> diff
    0
    >>>

:copyright: (c) 2021 Akash Mahanty Et al.
:license: MIT
"""

from .vhash import from_path, from_url
from .__version__ import (
    __title__,
    __description__,
    __url__,
    __version__,
    __author__,
    __author_email__,
    __license__,
    __copyright__,
)
