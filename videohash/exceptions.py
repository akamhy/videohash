"""
videohash.exceptions
~~~~~~~~~~~~~~~~~~~
This module contains the videohash's exceptions.
"""


class DownloadFailed(Exception):
    """Failed to download the video file from url supplied"""

    pass


class DownloadOutPutDirDoesNotExits(Exception):
    """The output directory supplied to store the downloaded video does not exists."""

    pass


class YouTubeDLNotFound(Exception):
    """youtube-dl and yt-dl are not found in path"""

    pass


class FileNotFoundError(Exception):
    """Could not find the video file on path supplied"""

    pass


class FFmpegNotFound(Exception):
    """FFmpeg is not is the path"""

    pass


class FFmpegFailedToExtractFrames(Exception):
    """FFmpeg failed to extract any frame"""

    pass


class FramesExtractorOutPutDirDoesNotExits(Exception):
    """The output dir passed to the frame extractor does not exits."""

    pass


class StoragePathDoesNotExist(Exception):
    """
    The supplied storage path does not exists.
    Do not supply if you don't care about the collage or extracted farmes.
    The collage is the image representing your video.
    """

    pass


class DidNotSupplyPathOrUrl(Exception):
    """Must supply either a path for your video or a valid URL"""

    pass


class CollageOfZeroFramesError(Exception):
    """Raised if zero frames are passed for collage making"""

    pass
