import pytest
import os
from shutil import which
from videohash.downloader import Download
from videohash.exceptions import DownloadFailed, YouTubeDLNotFound
from videohash.utils import create_and_return_temporary_directory, get_list_of_all_files_in_dir

this_dir = os.path.dirname(os.path.realpath(__file__))

def test_all():
    url = "https://www.youtube.com/watch?v=s7X5JuqEXuI" # patagonia
    dir = create_and_return_temporary_directory()
    download1 = Download(url=url,output_dir=dir, youtube_dl_path=None)
    file_list = get_list_of_all_files_in_dir(dir)
    total_files = len(file_list)
    if total_files == 0:
        raise Exception("File not downloaded. Url is %s ")


    url = "https://www.youtube.com/watch?v=ThisVideoDN"
    dir = create_and_return_temporary_directory()
    with pytest.raises(DownloadFailed):
        download2 = Download(url=url,output_dir=dir, youtube_dl_path=None) # non downloadable

    url = "https://www.youtube.com/watch?v=ThisVideoDN"
    dir = create_and_return_temporary_directory()
    with pytest.raises(YouTubeDLNotFound):
        download2 = Download(url=url,output_dir=dir, youtube_dl_path="/home/akamhy/ytdlfake") # non existant youtube_dl path

    if which("yt-dlp"):
        url = "https://www.youtube.com/watch?v=YLslsZuEaNE" # dog
        dir = create_and_return_temporary_directory()
        download3 = Download(url=url,output_dir=dir, youtube_dl_path=str(which("yt-dlp")))
        file_list = get_list_of_all_files_in_dir(dir)
        total_files = len(file_list)
        if total_files == 0:
            raise Exception("File not downloaded. Url is %s ")

    if which("youtube-dl"):
        url = "https://www.youtube.com/watch?v=o9aaoiyJlcM" # italy
        dir = create_and_return_temporary_directory()
        download4 = Download(url=url,output_dir=dir, youtube_dl_path=str(which("youtube-dl")))
        file_list = get_list_of_all_files_in_dir(dir)
        total_files = len(file_list)
        if total_files == 0:
            raise Exception("File not downloaded. Url is %s ")
