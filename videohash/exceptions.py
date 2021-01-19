"""
videohash.exceptions
~~~~~~~~~~~~~~~~~~~
This module contains the set of videohash's exceptions.
"""


class VideoHashError(Exception):
    """
    Main exception of this package
    """


class DownloadFailed(VideoHashError):
    """
    YouTube-dl Failed to download the video.
    """
