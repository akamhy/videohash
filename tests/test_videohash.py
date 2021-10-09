import pytest
import os
from videohash.videohash import VideoHash
from videohash.exceptions import DidNotSupplyPathOrUrl, StoragePathDoesNotExist
from videohash.utils import create_and_return_temporary_directory

this_dir = os.path.dirname(os.path.realpath(__file__))


def test_all():

    source1 = (
        "https://raw.githubusercontent.com/akamhy/videohash/main/assets/rocket.mkv"
    )
    videohash1 = VideoHash(url=source1)
    hash1 = videohash1.hash
    hash_hex1 = videohash1.hash_hex
    assert hash1 == "0b0011010000011111111011111111111110001111011110000000000000000000"
    assert (
        str(videohash1)
        == "0b0011010000011111111011111111111110001111011110000000000000000000"
    )
    assert hash_hex1 == "0x341fefff8f780000"
    assert (
        videohash1
        - "0b0011010000011111111011111111111110001111011110000000000000000000"
        == 0
    )
    assert hash_hex1 in repr(videohash1)
    assert hash1 in repr(videohash1)
    assert (len(videohash1) - 2) == videohash1.bits_in_hash
    with pytest.raises(AssertionError):
        assert videohash1 != hash_hex1

    with pytest.raises(TypeError):
        none_err_diff = videohash1 - None

    with pytest.raises(ValueError):
        bin_len_err_diff = videohash1 - hash1[0:-2]

    with pytest.raises(TypeError):
        prefix_err_diff = videohash1 - ("XX" + hash1[2:])

    with pytest.raises(TypeError):
        non_str_and_videohash_error = videohash1 - True

    source2 = (
        this_dir
        + os.path.sep
        + os.path.pardir
        + os.path.sep
        + "assets"
        + os.path.sep
        + "rocket.mkv"
    )
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
    hash_hex4 = videohash4.hash_hex

    assert hash4 != hash1
    assert hash4 != hash2
    assert hash4 != hash3

    assert videohash1 != videohash4
    assert videohash2 != videohash4
    assert videohash3 != videohash4

    with pytest.raises(ValueError):
        # not padded with 0x
        VideoHash.hex2bin("741fcfff8f780000", 64)

    with pytest.raises(ValueError):
        # not padded with 0b
        VideoHash.bin2hex("010101001")

    with pytest.raises(ValueError):
        # hamming_distance is not defined.
        VideoHash.hamming_distance("abc", "abcd")

    with pytest.raises(DidNotSupplyPathOrUrl):
        VideoHash(url=None, path=None)

    with pytest.raises(StoragePathDoesNotExist):
        storage_path = os.path.join(
            create_and_return_temporary_directory(),
            ("thisdirdoesnotexist" + os.path.sep),
        )
        VideoHash(url="https://example.com", storage_path=storage_path)

    with pytest.raises(ValueError):
        VideoHash(
            url="https://example.com", path=create_and_return_temporary_directory()
        )

    with pytest.raises(ValueError):
        path = os.path.join(
            create_and_return_temporary_directory(), "file_extension_less_video"
        )
        VideoHash(path=path)
