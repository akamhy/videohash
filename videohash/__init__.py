# ██╗░░░██╗██╗██████╗░███████╗░█████╗░██╗░░██╗░█████╗░░██████╗██╗░░██╗
# ██║░░░██║██║██╔══██╗██╔════╝██╔══██╗██║░░██║██╔══██╗██╔════╝██║░░██║
# ╚██╗░██╔╝██║██║░░██║█████╗░░██║░░██║███████║███████║╚█████╗░███████║
# ░╚████╔╝░██║██║░░██║██╔══╝░░██║░░██║██╔══██║██╔══██║░╚═══██╗██╔══██║
# ░░╚██╔╝░░██║██████╔╝███████╗╚█████╔╝██║░░██║██║░░██║██████╔╝██║░░██║
# ░░░╚═╝░░░╚═╝╚═════╝░╚══════╝░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░╚═╝░░╚═╝

"""
Python package for Perceptual Video Hashing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
https://github.com/akamhy/videohash

Usage:

>>> from videohash import VideoHash
>>> hash1 = VideoHash(url="https://www.youtube.com/watch?v=PapBjpzRhnA")
>>> str(hash1)
'0b0011010000011111111011111111111110001111011110000000000000000000'
>>> hash1.hash
'0b0011010000011111111011111111111110001111011110000000000000000000'
>>> hash1.hash_hex
'0x341fefff8f780000'
>>> repr(hash1)
'VideoHash(hash=0b0011010000011111111011111111111110001111011110000000000000000000, hash_hex=0x341fefff8f780000, collage_path=/tmp/tmp3kzva948/temp_storage_dir/kyci5lleck1z/collage/collage.jpg, bits_in_hash=64)'
>>> hash1.collage_path
'/tmp/tmp3kzva948/temp_storage_dir/kyci5lleck1z/collage/collage.jpg'
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
'0x341fefff8f780000'
>>> hash1 - hash2
0
>>> hash2 - "0x341fefff8f780000"
0
>>> hash1 - "0b0011010000011111111011111111111110001111011110000000000000000000"0
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
True
>>> hash4 = VideoHash(url="https://www.youtube.com/watch?v=_T8cn2J13-4")
>>> hash4.hash_hex
'0x7cffff000000eff0'
>>> hash4.hash
'0b0111110011111111111111110000000000000000000000001110111111110000'
>>> hash4 == hash3
False
>>> hash4 - hash2
34
>>> hash4 != hash2
True
>>> hash4 - "0b0011010000011111111011111111111110001111011110000000000000000000"34
>>> hash4 - "0b0111110011111111111111110000000000000000000000001110111111110000"0
>>> hash4 - "0x7cffff000000eff0"
0
>>>


:copyright: (c) 2021 Akash Mahanty
:license: MIT
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
