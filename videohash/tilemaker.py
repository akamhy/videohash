from image_slicer import save_tiles, slice
from PIL import Image

from .utils import get_list_of_all_files_in_dir


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
        slice(
            horizontally_concatenated_image_path,
            number_tiles=64,
            col=8,
            row=8,
            save=False,
            DecompressionBombWarning=False,
        )
    )
    save_tiles(tiles, prefix="tile", directory=tiles_dir, format="jpeg")
