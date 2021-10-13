# ██╗░░░██╗██╗██████╗░███████╗░█████╗░██╗░░██╗░█████╗░░██████╗██╗░░██╗
# ██║░░░██║██║██╔══██╗██╔════╝██╔══██╗██║░░██║██╔══██╗██╔════╝██║░░██║
# ╚██╗░██╔╝██║██║░░██║█████╗░░██║░░██║███████║███████║╚█████╗░███████║
# ░╚████╔╝░██║██║░░██║██╔══╝░░██║░░██║██╔══██║██╔══██║░╚═══██╗██╔══██║
# ░░╚██╔╝░░██║██████╔╝███████╗╚█████╔╝██║░░██║██║░░██║██████╔╝██║░░██║
# ░░░╚═╝░░░╚═╝╚═════╝░╚══════╝░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░╚═╝░░╚═╝


"""
Python package for Perceptual Video Hashing (Near Duplicate Video Detection)

https://github.com/akamhy/videohash

Usage:

>>> from videohash import VideoHash
>>> hash1 = VideoHash(url="https://www.youtube.com/watch?v=PapBjpzRhnA", download_worst=False)
>>> str(hash1)
'0b0011010000011111111011111111111110001111011110000000000000000000'
>>> hash1.hash
'0b0011010000011111111011111111111110001111011110000000000000000000'
>>> hash1.hash_hex
'0x341fefff8f780000'
>>> repr(hash1)
'VideoHash(hash=0b0011010000011111111011111111111110001111011110000000000000000000, hash_hex=0x341fefff8f780000, collage_path=/tmp/tmpe07d_b1g/temp_storage_dir/acn6zsdcb40q/collage/collage.jpg, bits_in_hash=64)'
>>> hash1.collage_path
'/tmp/tmpe07d_b1g/temp_storage_dir/acn6zsdcb40q/collage/collage.jpg'
>>> hash1.bits_in_hash
64
>>> len(hash1)
66
>>> hash2 = VideoHash(url="https://raw.githubusercontent.com/akamhy/videohash/main/assets/rocket.mkv")
>>> hash2.hash
'0b0011010000011111111011111111111110001111011110000000000000000000'
>>> hash2.hash_hex
'0x341fefff8f780000'
>>> hash1.hash_hex
'0x741fcfff8f780000'
>>> hash1 - hash2
0
>>> hash2 - "0x341fefff8f780000"
0
>>> hash1 - "0b0011010000011111111011111111111110001111011110000000000000000000"
2
>>> hash1 == hash2
True
>>> hash1 != hash2
False
>>> hash3 = VideoHash(path="/home/akamhy/Downloads/rocket.mkv")
>>> hash3.hash_hex
'0x341fefff8f780000'
>>> hash3.hash
'0b0011010000011111111011111111111110001111011110000000000000000000'
>>> hash3 - hash2
0
>>> hash3 == hash1
False
>>> hash3 == hash2
True
>>> hash4 = VideoHash(url="https://www.youtube.com/watch?v=_T8cn2J13-4")
>>> hash4.hash_hex
'0x7cffff000000eff0'
>>> hash4 - "0x7cffff000000eff0"
0
>>> hash4.hash
'0b0111110011111111111111110000000000000000000000001110111111110000'
>>> hash4 - "0b0111110011111111111111110000000000000000000000001110111111110000"
0
>>> hash4 == hash3
False
>>> hash4 - hash2
34
>>> hash4 != hash2
True
>>> hash4 - "0b0011010000011111111011111111111110001111011110000000000000000000"
34
>>>

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
    DownloadError,
    FFmpegError,
    DownloadSoftwareError,
    DownloadFailed,
    DownloadOutPutDirDoesNotExits,
    YouTubeDLNotFound,
    FFmpegNotFound,
    FFmpegFailedToExtractFrames,
    FramesExtractorOutPutDirDoesNotExits,
    StoragePathDoesNotExist,
    DidNotSupplyPathOrUrl,
    CollageOfZeroFramesError,
)
