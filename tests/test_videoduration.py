import os

import pytest

from videohash.videoduration import video_duration

this_dir = os.path.dirname(os.path.realpath(__file__))


def test_video_duration():

    video_path = (
        this_dir
        + os.path.sep
        + os.path.pardir
        + os.path.sep
        + "assets"
        + os.path.sep
        + "rocket.mkv"
    )

    assert (video_duration(video_path) - 52.08) < 0.1
