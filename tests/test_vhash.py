import pytest
import os
from videohash.vhash import from_url, from_path, hash_manager
from videohash.exceptions import DownloadFailed


def test_all():
    this_dir = os.path.dirname(os.path.realpath(__file__))

    hash_url = from_url(
        "https://raw.githubusercontent.com/akamhy/videohash/main/assets/rocket.mkv"
    )
    assert str(hash_url) == "be1fffff9ffc0000"

    local_video = this_dir + "/../assets/rocket.mkv"
    hash_path = from_path(local_video)
    assert str(hash_path) == "be1fffff9ffc0000"
    assert hash_url - hash_path == 0
    different_file_hash = from_url("https://www.youtube.com/watch?v=_T8cn2J13-4")
    assert str(different_file_hash) == "3cffff00000081f0"
    diff = different_file_hash - hash_url
    assert diff == 31

    collage = this_dir + "/../assets/collage.jpeg"
    assert str(hash_manager(collage, image_hash="phash")) == "c08257d5df6fb202"
    assert str(hash_manager(collage, image_hash="dhash")) == "c8c0cf23339c0070"
    assert str(hash_manager(collage, image_hash="whash")) == "2c787ffbffe00000"
    assert str(hash_manager(collage, image_hash="colorhash")) == "1ec00000000"
    assert (
        str(hash_manager(collage, image_hash="crop_resistant_hash"))
        == "dc98381819313818,b8f8f4f6ff7cfcfe,c8cbc3e5c5cce8f3,ae9deec68eceeeee,fbf4c48881c48990,dbf5c48881c68890,a929292d15b5d555,c8c0cf23339c0070"
    )
    assert str(hash_manager(collage)) == "fc7e7ff9ffff0000"

    with pytest.raises(FileNotFoundError):
        hash = from_path(this_dir)

    with pytest.raises(DownloadFailed):
        hash = from_url("https://www.youtube.com/watch?v=_x8cnakamh4")
