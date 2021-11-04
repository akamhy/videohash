import re
import shlex
import os
from shutil import which
from subprocess import check_output, Popen, PIPE

from .utils import does_path_exists
from .exceptions import (
    YouTubeDLNotFound,
    DownloadOutPutDirDoesNotExits,
    DownloadFailed,
    DownloadSoftwareError,
)

from typing import Optional


# Python module to download the video from the input URL.
# Uses youtube_dl or yt-dlp to download the video.
# If both yt-dlp and youtube_dl are installed, it selects
# yt-dlp. yt-dlp is more maintained than youtube_dl.


class Download:

    """
    Class that downloads the video prior to frames extraction.

    Tries to download the lowest quality video possible.
    Uses youtube-dl or yt-dl to download the videos.
    """

    def __init__(
        self,
        url: str,
        output_dir: str,
        youtube_dl_path: Optional[str] = None,
        worst: bool = True,
        default_dl: str = "yt-dlp",
    ) -> None:
        """
        Check if output_dir exists and is a directory, must end with "/".
        Check youtube_dl_path and verify that it is working else raises Exception.

        :param url: The URL of the video. The video will be
                    downloaded from this url. Must be a string.

        :param output_dir: The directory where the downloaded video will be stored.
                           Must be a string and path must be absolute.

        :param youtube_dl_path: If youtube_dl is not in path environment variable,
                                pass the path to the youtube-dl or yt-dlp to this param.
                                Must be string and only absolute path allowed.

        :param worst: The quality of video downloaded by the downloader.
                      True for worst quality and False for the default settings
                      of the downloader. The downloaders are yt-dlp and youtube_dl.
                      Default worst is True

        :param default_dl: The the default downloader, only used if youtube_dl_path
                           is not provided.

        :return: None

        :rtype: NoneType
        """
        self.url = url
        self.output_dir = output_dir
        self.youtube_dl_path = ""
        if youtube_dl_path:
            self.youtube_dl_path = youtube_dl_path

        self.default_dl = default_dl.strip().lower().replace("_", "-")

        self.worst = worst

        if not does_path_exists(self.output_dir):
            raise DownloadOutPutDirDoesNotExits(
                f"No directory called '{self.output_dir}' found for storing the downloaded video. Can not download the video."
            )

        self._check_youtube_dl()

        self.download_video()

    def _check_youtube_dl(self) -> None:
        """Checks the youtube-dl and yt-dlp installations.

        :return: None

        :rtype: NoneType

        """

        def find_dl(dl_name):
            if not which(dl_name):
                raise YouTubeDLNotFound(f"{dl_name} not found on your system path.")
            self.youtube_dl_path = str(which(dl_name))

        if not self.youtube_dl_path:
            find_dl(self.default_dl)

        try:
            output = check_output([str(self.youtube_dl_path), "--version"]).decode()
        except FileNotFoundError:
            raise YouTubeDLNotFound(
                f"Video downloader can not be found at '{self.youtube_dl_path}'."
            )

        if not re.search(
            r"[0-9]{4}\.[0-9]{2}\.[0-9]{2}", output
        ):  # raise Exception is youtube is not installed.
            # check by youtube-dl --version

            raise DownloadSoftwareError(
                f"The output is not matching the expected '{self.youtube_dl_path} --version' output."
                + " Please check your youtube_dl/yt-dlp installation. If the problem persist after "
                + "re-install open an issue at https://github.com/akamhy/videohash/issues"
            )

    def download_video(self) -> None:
        """Download the video from URL

        :return: None

        :rtype: NoneType

        """
        youtube_dl_path = self.youtube_dl_path
        output_dir = self.output_dir
        if os.name == "posix":
            youtube_dl_path = shlex.quote(self.youtube_dl_path)
            output_dir = shlex.quote(self.output_dir)

        worst = " "
        if self.worst:
            worst = " -f worst "

        command = (
            f'"{youtube_dl_path}"'
            + worst
            + " "
            + '"'
            + self.url
            + '"'
            + " -o "
            + '"'
            + output_dir
            + "video_file.%(ext)s"
            + '"'
        )

        process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
        output, error = process.communicate()

        youtube_dl_output = output.decode()
        youtube_dl_error = error.decode()

        if len(os.listdir(self.output_dir)) == 0:
            raise DownloadFailed(
                f"'{self.youtube_dl_path}' failed to download the video at"
                + f" '{self.url}'.\n{youtube_dl_output}\n{youtube_dl_error}"
            )
