import pytest
import os
from videohash.collagemaker import MakeCollage
from videohash.exceptions import CollageOfZeroFramesError
from videohash.utils import (
    create_and_return_temporary_directory,
    get_list_of_all_files_in_dir,
)


def test_all():

    image_list = []  # when no files(extracted frames) in frames directory
    output_path = create_and_return_temporary_directory()
    with pytest.raises(CollageOfZeroFramesError):
        MakeCollage(image_list, output_path, collage_image_width=720)

    output_path = os.path.join(output_path, "/ge72y373ggsuagu7iy7y8w4ry83hshfhsduge/")
    image_list = ["img1", "img2", "img3"]
    with pytest.raises(FileNotFoundError):
        MakeCollage(image_list, output_path)
