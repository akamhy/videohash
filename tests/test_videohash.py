import pytest
import os
from videohash.videohash import VideoHash

this_dir = os.path.dirname(os.path.realpath(__file__))

def test_all():

    source1 = "https://raw.githubusercontent.com/akamhy/videohash/main/assets/rocket.mkv"
    videohash1 = VideoHash(url=source1)
    hash1 = videohash1.hash
    hash_hex1 = videohash1.hash_hex
    assert hash1 == "0b0011010000011111111011111111111110001111011110000000000000000000"
    assert hash_hex1 == "0x341fefff8f780000"

    source2 = this_dir + "/../assets/rocket.mkv"
    videohash2 = VideoHash(path=source2)
    hash2 = videohash2.hash
    hash_hex2 = videohash2.hash_hex
    assert hash2 == "0b0011010000011111111011111111111110001111011110000000000000000000"
    assert hash_hex2 == "0x341fefff8f780000"

    source3 = "https://www.youtube.com/watch?v=PapBjpzRhnA"
    videohash3 = VideoHash(url=source3)
    hash3 = videohash3.hash
    hash_hex3 = videohash3.hash_hex
    assert hash3 == "0b0111010000011111110011111111111110001111011110000000000000000000"
    assert hash_hex3 == "0x741fcfff8f780000"



    assert hash1 == hash2

    assert hash_hex1 == hash_hex2
    assert videohash1 - hash_hex3 == 2

    assert videohash1 == videohash2
    assert videohash1 - videohash3 == 2




    source4 = "https://www.youtube.com/watch?v=_T8cn2J13-4"
    videohash4 = VideoHash(url=source4)
    hash4 = videohash4.hash
    hash_hex4  = videohash4.hash_hex

    assert hash4 != hash1
    assert hash4 != hash2
    assert hash4 != hash3

    assert  videohash1 != videohash4
    assert  videohash2 != videohash4
    assert  videohash3 != videohash4
