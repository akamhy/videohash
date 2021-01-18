import pytest
import os
from videohash.vhash import from_url, from_path


def test_all():
    hash_url = from_url(
        "https://raw.githubusercontent.com/akamhy/videohash/main/assets/rocket.webm"
    )
    assert str(hash_url) == "7c7e7ff9ffff0000"
    this_dir = os.path.dirname(os.path.realpath(__file__))
    local_video = this_dir + "/../assets/rocket.webm"
    hash_path = from_path(local_video)
    assert str(hash_path) == "7c7e7ff9ffff0000"
    assert hash_url - hash_path == 0
    different_file_hash = from_url("https://www.youtube.com/watch?v=_T8cn2J13-4")
    assert str(different_file_hash) == "3cffff0000000eff"
    diff = different_file_hash - hash_url
    assert diff == 37
