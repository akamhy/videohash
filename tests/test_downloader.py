import os

import pytest

from videohash.downloader import Download
from videohash.exceptions import DownloadFailed, DownloadOutPutDirDoesNotExist
from videohash.utils import (
    create_and_return_temporary_directory,
    get_list_of_all_files_in_dir,
)


def test_all():
    _dir = os.path.join(
        create_and_return_temporary_directory(), "/gduisgf73r7guai7td7g38yisif7si7/"
    )

    with pytest.raises(DownloadOutPutDirDoesNotExist):
        Download(url="https://example.com", output_dir=_dir)

    url = "https://www.youtube.com/watch?v=s7X5JuqEXuI"  # patagonia
    _dir = create_and_return_temporary_directory()
    Download(url=url, output_dir=_dir)
    file_list = get_list_of_all_files_in_dir(_dir)
    total_files = len(file_list)
    if total_files == 0:
        raise Exception("File not downloaded. Url is %s ")

    url = "https://www.youtube.com/watch?v=ThisVideoDN"
    _dir = create_and_return_temporary_directory()
    with pytest.raises(DownloadFailed):
        Download(url=url, output_dir=_dir)  # non downloadable
