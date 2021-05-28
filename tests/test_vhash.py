import pytest
import os
from videohash.vhash import from_url, from_path, hash_manager
from videohash.exceptions import DownloadFailed


def test_all():
    this_dir = os.path.dirname(os.path.realpath(__file__))

    hash_url = from_url(
        "https://raw.githubusercontent.com/akamhy/videohash/main/assets/rocket.mkv"
    )
    assert str(hash_url) == "fe3fffff8ff80000"

    local_video = this_dir + "/../assets/rocket.mkv"
    hash_path = from_path(local_video)
    assert str(hash_path) == "fe3fffff8ff80000"
    assert hash_url - hash_path == 0
    different_file_hash = from_url("https://www.youtube.com/watch?v=_T8cn2J13-4")
    assert str(different_file_hash) == "3cffff00000081f0"
    diff = different_file_hash - hash_url
    assert diff == 29

    collage = this_dir + "/../assets/collage.jpeg"
    assert str(hash_manager(collage, image_hash="phash")) == "df8700d397e4c073"
    assert str(hash_manager(collage, image_hash="dhash")) == "4c62426678880280"
    assert str(hash_manager(collage, image_hash="whash")) == "e03df7ff87f80000"
    assert str(hash_manager(collage, image_hash="colorhash")) == "31c00000000"
    assert (
        str(hash_manager(collage, image_hash="crop_resistant_hash"))
        == "4c62426678880280"
    )
    assert str(hash_manager(collage)) == "fe3fffff8ff80000"

    with pytest.raises(FileNotFoundError):
        hash = from_path(this_dir)

    with pytest.raises(DownloadFailed):
        hash = from_url("https://www.youtube.com/watch?v=_x8cnakamh4")
