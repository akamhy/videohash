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
>>> hash1 = VideoHash(url="https://www.youtube.com/watch?v=PapBjpzRhnA", download_worst=False) # video : Artemis I Hot Fire Test
>>> str(hash1) # str representation of VideoHash object (the output is video's videohash value)
'0b0011010000011111111011111111111110001111011110000000000000000000'
>>> hash1.hash # video hash value of the file, value is same as str(hash1)
'0b0011010000011111111011111111111110001111011110000000000000000000'
>>> hash1.hash_hex # hexadecimal representation of the videohash value
'0x341fefff8f780000'
>>> repr(hash1) # representation of VideoHash object
'VideoHash(hash=0b0011010000011111111011111111111110001111011110000000000000000000, hash_hex=0x341fefff8f780000, collage_path=/tmp/tmpvfr41629/temp_storage_dir/79c95zh4bq0s/collage/collage.jpg, bits_in_hash=64)'
>>> hash1.video_path # path of the downloaded video
'/tmp/tmpvfr41629/temp_storage_dir/79c95zh4bq0s/video/video.webm'
>>> hash1.storage_path # the storage directory
'/tmp/tmpvfr41629/temp_storage_dir/79c95zh4bq0s/'
>>> hash1.collage_path # path of the generated collage, the wavelet hash of this special collage is videohash value of the input video
'/tmp/tmpvfr41629/temp_storage_dir/79c95zh4bq0s/collage/collage.jpg'
>>> hash1.delete_storage_path() # To delete the storage path, deleting it will also delete the collage, extracted frames, and the downloaded video.
>>> hash1.bits_in_hash # how many bits in the hash, always 64 (a constant)
64
>>> len(hash1) # length of the hash value string, 64(no of bits in hash) + 2(prefix '0b')
66
>>> hash2 = VideoHash(url="https://raw.githubusercontent.com/akamhy/videohash/main/assets/rocket.mkv") # video : Artemis I Hot Fire Test, yes same as hash1(downscaled)
>>> hash2.hash
'0b0011010000011111111011111111111110001111011110000000000000000000'
>>> hash2.hash_hex
'0x341fefff8f780000'
>>> hash1.hash_hex
'0x341fefff8f780000'
>>> hash1 - hash2 # videohash objects support application of '-' operator on them. The other value must be a string (prefixed with '0x' or '0b') or another VideoHash object
0
>>> hash2 - "0x341fefff8f780000"
0
>>> hash1 - "0b0011010000011111111011111111111110001111011110000000000000000000"
0
>>> hash1 - "0b1111111111111111111111111111111111111111111111111111111111111111"
32
>>> hash1 == hash2 # videohash objects support application of '==' operator on them. The other value must be a string (prefixed with '0x' or '0b') or another VideoHash object.
True
>>> hash1 == "0b0011010000011111111011111111111110001111011110000000000000000000"
True
>>> hash1 != hash2 # videohash objects support application of '!=' operator on them. The other value must be a string (prefixed with '0x' or '0b') or another VideoHash object.
False
>>> hash3 = VideoHash(path="/home/akamhy/Downloads/rocket.mkv") # video : Artemis I Hot Fire Test, yes same as hash2 (downloaded locally)
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
>>> hash4 = VideoHash(url="https://www.youtube.com/watch?v=_T8cn2J13-4") #  video : How We Are Going to the Moon - 4K, a completely different video from the first 3 videos
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
