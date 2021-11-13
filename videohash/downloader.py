from shutil import which
from subprocess import Popen, PIPE

from .utils import does_path_exists, get_list_of_all_files_in_dir
from .exceptions import DownloadOutPutDirDoesNotExist, DownloadFailed

# Python module to download the video from the input URL.
# Uses yt-dlp to download the video.


class Download:

    """
    Class that downloads the video prior to frames extraction.

    Tries to download the lowest quality video possible.
    Uses yt-dlp to download the videos.
    """

    def __init__(
        self,
        url: str,
        output_dir: str,
        worst: bool = True,
    ) -> None:
        """
        :param url: The URL of the video. The video will be
                    downloaded from this url. Must be a string.

        :param output_dir: The directory where the downloaded video will be stored.
                           Must be a string and path must be absolute.

        :param worst: The quality of video downloaded by yt-dlp.
                      True for worst quality and False for the default settings
                      of the downloader. Default value for worst is True.

        :return: None

        :rtype: NoneType
        """
        self.url = url
        self.output_dir = output_dir
        self.worst = worst

        if not does_path_exists(self.output_dir):
            raise DownloadOutPutDirDoesNotExist(
                f"No directory found at '{self.output_dir}' for storing the downloaded video. Can not download the video."
            )

        self.yt_dlp_path = str(which("yt-dlp"))
        self.download_video()

    def download_video(self) -> None:
        """Download the video from URL

        :return: None

        :rtype: NoneType

        """
        worst = " "
        if self.worst:
            worst = " -f worst "

        command = (
            f'"{self.yt_dlp_path}"'
            + worst
            + " "
            + '"'
            + self.url
            + '"'
            + " -o "
            + '"'
            + self.output_dir
            + "video_file.%(ext)s"
            + '"'
        )

        process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
        output, error = process.communicate()
        yt_dlp_output = output.decode()
        yt_dlp_error = error.decode()

        if len(get_list_of_all_files_in_dir(self.output_dir)) == 0:
            raise DownloadFailed(
                f"'{self.yt_dlp_path}' failed to download the video at"
                + f" '{self.url}'.\n{yt_dlp_output}\n{yt_dlp_error}"
            )
