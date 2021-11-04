import pytest
import os
from shutil import which
from videohash.downloader import Download
from videohash.exceptions import (
    DownloadFailed,
    YouTubeDLNotFound,
    DownloadOutPutDirDoesNotExits,
    DownloadSoftwareError,
)
from videohash.utils import (
    create_and_return_temporary_directory,
    get_list_of_all_files_in_dir,
)


def test_all():
    _dir = os.path.join(
        create_and_return_temporary_directory(), "/gduisgf73r7guai7td7g38yisif7si7/"
    )

    with pytest.raises(DownloadOutPutDirDoesNotExits):
        Download(url="https://example.com", output_dir=_dir, youtube_dl_path=None)

    url = "https://www.youtube.com/watch?v=s7X5JuqEXuI"  # patagonia
    _dir = create_and_return_temporary_directory()
    Download(url=url, output_dir=_dir, youtube_dl_path=None)
    file_list = get_list_of_all_files_in_dir(_dir)
    total_files = len(file_list)
    if total_files == 0:
        raise Exception("File not downloaded. Url is %s ")

    url = "https://www.youtube.com/watch?v=ThisVideoDN"
    _dir = create_and_return_temporary_directory()
    with pytest.raises(DownloadFailed):
        Download(url=url, output_dir=_dir, youtube_dl_path=None)  # non downloadable

    url = "https://www.youtube.com/watch?v=ThisVideoDN"
    _dir = create_and_return_temporary_directory()
    with pytest.raises(YouTubeDLNotFound):
        Download(
            url=url, output_dir=_dir, youtube_dl_path="/home/akamhy/ytdlfake"
        )  # non existant youtube_dl path

    with pytest.raises(YouTubeDLNotFound):
        Download(
            url=url, output_dir=_dir, default_dl="unknown-dl"
        )  # non existant youtube_dl path

    if which("yt-dlp"):
        url = "https://www.youtube.com/watch?v=3NOmU06Vs6o"  # video : A Step Toward Sustainable Lunar Exploration
        _dir = create_and_return_temporary_directory()
        Download(url=url, output_dir=_dir, youtube_dl_path=str(which("yt-dlp")))
        file_list = get_list_of_all_files_in_dir(_dir)
        total_files = len(file_list)
        if total_files == 0:
            raise Exception("File not downloaded. Url is %s ")

    if which("youtube-dl"):
        url = "https://www.youtube.com/watch?v=4fdbfLJYYgI"  # Video : Why Icy Moons are So Juicy
        _dir = create_and_return_temporary_directory()
        Download(
            url=url, output_dir=_dir, youtube_dl_path=None, default_dl="youtube-dl"
        )
        file_list = get_list_of_all_files_in_dir(_dir)
        total_files = len(file_list)
        if total_files == 0:
            raise Exception("File not downloaded. Url is %s ")
