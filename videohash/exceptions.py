"""
videohash.exceptions
~~~~~~~~~~~~~~~~~~~
This module contains the videohash's exceptions.
"""


class VideoHashError(Exception):

    """Base Exception for the videohash package."""

    pass


class StoragePathDoesNotExist(VideoHashError):

    """
    The storage path passed by the user does not exist.
    The collage is the image representing your video as an two dimensional bitmap image.
    """

    pass


class FramesExtractorOutPutDirDoesNotExist(VideoHashError):

    """The frames output directory passed to the frame extractor does not exist."""

    pass


class DownloadOutPutDirDoesNotExist(VideoHashError):

    """The output directory passed to downloader for storing the downloaded video does not exist."""

    pass


class DidNotSupplyPathOrUrl(VideoHashError):

    """Must supply either a path for the video or a valid URL"""

    pass


class CollageOfZeroFramesError(VideoHashError):

    """Raised if zero frames are passed for collage making."""

    pass


class DownloadFailed(VideoHashError):

    """Download software failed to download the video from the url."""

    pass


class FFmpegError(VideoHashError):

    """Base error for the FFmpeg software."""

    pass


class FFmpegNotFound(FFmpegError):

    """FFmpeg is either not installed or not in the executable path of the system."""

    pass


class FFmpegFailedToExtractFrames(FFmpegError):

    """FFmpeg failed to extract any frame at all. Maybe the input video is damaged or corrupt."""

    pass
