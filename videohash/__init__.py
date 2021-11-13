# ██╗░░░██╗██╗██████╗░███████╗░█████╗░██╗░░██╗░█████╗░░██████╗██╗░░██╗
# ██║░░░██║██║██╔══██╗██╔════╝██╔══██╗██║░░██║██╔══██╗██╔════╝██║░░██║
# ╚██╗░██╔╝██║██║░░██║█████╗░░██║░░██║███████║███████║╚█████╗░███████║
# ░╚████╔╝░██║██║░░██║██╔══╝░░██║░░██║██╔══██║██╔══██║░╚═══██╗██╔══██║
# ░░╚██╔╝░░██║██████╔╝███████╗╚█████╔╝██║░░██║██║░░██║██████╔╝██║░░██║
# ░░░╚═╝░░░╚═╝╚═════╝░╚══════╝░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░╚═╝░░╚═╝


"""
The Python package for near duplicate video detection

https://github.com/akamhy/videohash

Usage:

>>> from videohash import VideoHash
>>> # video: Artemis I Hot Fire Test
>>> videohash1 = VideoHash(url="https://www.youtube.com/watch?v=PapBjpzRhnA", download_worst=False)
>>>
>>> videohash1.hash # video hash value of the file, value is same as str(videohash1)
'0b0011010000011111111011111111111110001111011110000000000000000000'
>>>
>>> #VIDEO:Artemis I Hot Fire Test
>>> url2="https://raw.githubusercontent.com/akamhy/videohash/main/assets/rocket.mkv"
>>> videohash2 = VideoHash(url=url2)
>>> videohash2.hash
'0b0011010000011111111011111111111110001111011110000000000000000000'
>>> videohash2.hash_hex
'0x341fefff8f780000'
>>> videohash2.hash_hex
'0x341fefff8f780000'
>>> videohash1 - videohash2
0
>>> videohash1 == videohash2
True
>>> videohash1 == "0b0011010000011111111011111111111110001111011110000000000000000000"
True
>>> videohash1 != videohash2
False
>>> path3 = "/home/akamhy/Downloads/rocket.mkv" #VIDEO: Artemis I Hot Fire Test
>>> videohash3 = VideoHash(path=path3)
>>> videohash3.hash
'0b0011010000011111111011111111111110001111011110000000000000000000'
>>> videohash3 - videohash2
0
>>> videohash3 == videohash1
True
>>> url4 = "https://www.youtube.com/watch?v=_T8cn2J13-4" #VIDEO: How We Are Going to the Moon
>>> videohash4 = VideoHash(url=url4)
>>> videohash4.hash_hex
'0x7cffff000000eff0'
>>> videohash4 - "0x7cffff000000eff0"
0
>>> videohash4.hash
'0b0111110011111111111111110000000000000000000000001110111111110000'
>>> videohash4 - videohash2
34
>>> videohash4 != videohash2
True

Run the above code @ https://replit.com/@akamhy/videohash-usage-2xx-example-code-for-video-hashing#main.py

Extended Usage : https://github.com/akamhy/videohash/wiki/Extended-Usage

API Reference : https://github.com/akamhy/videohash/wiki/API-Reference


:copyright: (c) 2021 Akash Mahanty
:license: MIT, see LICENSE for more details.
:pypi: https://pypi.org/project/videohash/
:wiki: https://github.com/akamhy/videohash/wiki
:cite: https://doi.org/10.5281/zenodo.4448295
"""

from .videohash import VideoHash

from .__version__ import (
    __title__,
    __description__,
    __url__,
    __version__,
    __status__,
    __author__,
    __author_email__,
    __license__,
    __copyright__,
)

from .exceptions import (
    VideoHashError,
    FFmpegError,
    DownloadFailed,
    DownloadOutPutDirDoesNotExist,
    FFmpegNotFound,
    FFmpegFailedToExtractFrames,
    FramesExtractorOutPutDirDoesNotExist,
    StoragePathDoesNotExist,
    DidNotSupplyPathOrUrl,
    CollageOfZeroFramesError,
)
