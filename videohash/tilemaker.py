# This module has some code from <https://github.com/samdobson/image_slicer>

# Copyright (c) 2013 Sam Dobson

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
from math import ceil, floor, sqrt

from PIL import Image

from .utils import get_list_of_all_files_in_dir


class Tile:
    """Represents a single tile."""

    def __init__(self, image, number, position, coords, filename=None):
        self.image = image
        self.number = number
        self.position = position
        self.coords = coords
        self.filename = filename

    @property
    def row(self):
        return self.position[0]

    @property
    def column(self):
        return self.position[1]

    def generate_filename(
        self, directory=os.getcwd(), prefix="tile", file_format="png", path=True
    ):
        """Construct and return a filename for this tile."""
        filename = prefix + "_{col:02d}_{row:02d}.{ext}".format(
            col=self.column,
            row=self.row,
            ext=file_format.lower().replace("jpeg", "jpg"),
        )
        if not path:
            return filename
        return os.path.join(directory, filename)

    def save(self, filename=None, file_format="png"):
        if not filename:
            filename = self.generate_filename(file_format=file_format)
        self.image.save(filename, file_format)
        self.filename = filename


def calc_columns_rows(n):
    """
    Calculate the number of columns and rows required to divide an image
    into ``n`` parts.
    Return a tuple of integers in the format (num_columns, num_rows)
    """
    num_columns = int(ceil(sqrt(n)))
    num_rows = int(ceil(n / float(num_columns)))
    return (num_columns, num_rows)


def validate_image(number_tiles):
    """Basic sanity checks prior to performing a split."""
    TILE_LIMIT = 99 * 99

    try:
        number_tiles = int(number_tiles)
    except BaseException:
        raise ValueError("number_tiles could not be cast to integer.")

    if number_tiles > TILE_LIMIT or number_tiles < 2:
        raise ValueError(
            "Number of tiles must be between 2 and {} (you \
                          asked for {}).".format(
                TILE_LIMIT, number_tiles
            )
        )


def save_tiles(tiles, prefix="", directory=os.getcwd(), file_format="png"):
    """
    Write image files to disk. Create specified folder(s) if they
       don't exist. Return list of :class:`Tile` instance.
    Args:
       tiles (list):  List, tuple or set of :class:`Tile` objects to save.
       prefix (str):  Filename prefix of saved tiles.
    Kwargs:
       directory (str):  Directory to save tiles. Created if non-existant.
    Returns:
        Tuple of :class:`Tile` instances.
    """
    for tile in tiles:
        tile.save(
            filename=tile.generate_filename(
                prefix=prefix, directory=directory, file_format=file_format
            ),
            file_format=file_format,
        )
    return tuple(tiles)


def slicer(
    filename,
    number_tiles=None,
    col=None,
    row=None,
):

    Image.MAX_IMAGE_PIXELS = None

    im = Image.open(filename)
    im_w, im_h = im.size

    columns = 0
    rows = 0
    if number_tiles:
        validate_image(number_tiles)
        columns, rows = calc_columns_rows(number_tiles)

    tile_w, tile_h = int(floor(im_w / columns)), int(floor(im_h / rows))

    tiles = []
    number = 1
    for pos_y in range(0, im_h - rows, tile_h):  # -rows for rounding error.
        for pos_x in range(0, im_w - columns, tile_w):  # as above.
            area = (pos_x, pos_y, pos_x + tile_w, pos_y + tile_h)
            image = im.crop(area)
            position = (int(floor(pos_x / tile_w)) + 1, int(floor(pos_y / tile_h)) + 1)
            coords = (pos_x, pos_y)
            tile = Tile(image, number, position, coords)
            tiles.append(tile)
            number += 1
    im.close()
    return tuple(tiles)


def concatenate_video_frames_horizontally(
    frames_dir, horizontally_concatenated_image_path
) -> None:
    image_file_names = get_list_of_all_files_in_dir(frames_dir)
    total_images = len(image_file_names)
    first_image_filename = image_file_names[0]
    with Image.open(first_image_filename) as first_frame_image_in_list:
        width, height = first_frame_image_in_list.size

    base_image = Image.new("RGB", (width * total_images, height))

    x_offset = 0
    for image_filename in image_file_names:
        img = Image.open(image_filename)
        base_image.paste(img, (x_offset, 0))
        img.close()
        x_offset += width

    base_image.save(horizontally_concatenated_image_path)


def make_tile(frames_dir, horizontally_concatenated_image_path, tiles_dir) -> None:
    concatenate_video_frames_horizontally(
        frames_dir, horizontally_concatenated_image_path
    )
    tiles = list(
        slicer(
            horizontally_concatenated_image_path,
            number_tiles=64,
            col=8,
            row=8,
        )
    )
    save_tiles(tiles, prefix="tile", directory=tiles_dir, file_format="png")
