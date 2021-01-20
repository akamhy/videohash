import subprocess
import os
import random
from pathlib import Path
from PIL import Image
import imagehash
from math import ceil, sqrt
import shutil
import tempfile
from os.path import join
from .exceptions import DownloadFailed

dir = join(tempfile.mkdtemp(), "files/")


def download(input_url, output_file, task_dir, task_uid):
    """Downloads the video using youtube-dl cli.
    
    Download the worst quality of video if multiple
    quality 20 are available.
    
    output_file is the path(abs) of the downloaded file.

    If downloading fails raise DownloadFailed.
    """
    tries = 0
    while tries <= 3:
        tries += 1

        command = "youtube-dl -f worst {input_url} -o {output_file}".format(
            input_url=input_url, output_file=output_file
        )
        process = subprocess.Popen(
            command.split(), stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
        )
        output, error = process.communicate()

        l = [
            filename
            for filename in os.listdir(task_dir)
            if filename.startswith(task_uid)
        ]
        if l == []:
            continue
        else:
            return l[0]

    raise DownloadFailed(
        "Failed to download the video.\nYouTube-dl Failed to download your file."
    )


def frames(input_file, output_prefix):
    """Extracts frames of the video.
    Export frames as images at output_prefix as 7 digit padded jpeg file.
    """
    command = "ffmpeg -i {input_file} -r 1 {output_prefix}_%07d.jpeg".format(
        input_file=input_file, output_prefix=output_prefix
    )
    process = subprocess.Popen(
        command.split(), stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
    )
    output, error = process.communicate()


def collage_maker(image_dir, task_dir, collage_image_width):
    """Create a collage of all the images(frames).
    
    In sorted manner. Sorting is necessary to maintain consistency.
    collage_image_width decides the width of the collage's width.
    
    images_per_row_in_collage is the number of images in a row in the collage.
    
    images_per_row_in_collage is picked to make the collage as close to a 
    square matrix as possible.
    """
    frame_list = sorted([join(image_dir, image) for image in os.listdir(image_dir)])
    images_per_row_in_collage = int(sqrt(len(frame_list)))
    first_frame_image = Image.open(frame_list[0])
    frame_image_width, frame_image_height = first_frame_image.size
    scale = (collage_image_width) / (images_per_row_in_collage * frame_image_width)
    scaled_frame_image_width = ceil(frame_image_width * scale)
    scaled_frame_image_height = ceil(frame_image_height * scale)
    number_of_rows = ceil(len(frame_list) / images_per_row_in_collage)
    collage_image_height = ceil(scale * frame_image_height * number_of_rows)
    collage_image = Image.new("RGB", (collage_image_width, collage_image_height))
    i, j = (0, 0)
    for count, frame in enumerate(frame_list):
        if (count % images_per_row_in_collage) == 0:
            i = 0
        frame = Image.open(frame)
        frame.thumbnail(
            (scaled_frame_image_width, scaled_frame_image_height), Image.ANTIALIAS
        )
        x = i
        y = (j // images_per_row_in_collage) * scaled_frame_image_height
        collage_image.paste(frame, (x, y))
        i = i + scaled_frame_image_width
        j += 1
    collage_image.save(join(task_dir, "collage.jpeg"))


def hash_manager(collage, image_hash=None):
    """
    Use the hash algo passed in image_hash.
    """
    img = Image.open(collage)

    if image_hash == "phash":
        hash = imagehash.phash(img)
    elif image_hash == "dhash":
        hash = imagehash.dhash(img)
    elif image_hash == "whash":
        hash = imagehash.whash(img)
    elif image_hash == "colorhash":
        hash = imagehash.colorhash(img)
    elif image_hash == "crop_resistant_hash":
        hash = imagehash.crop_resistant_hash(img)
    else:
        hash = imagehash.average_hash(img)

    return hash


def task_uid_dir():
    """
    Create a 12 digits unique task id.
    The task id ensure that we are not messing
    with files created by other instances.

    Infact we indentify the downloaded video and
    the frames using this id.
    """
    sys_random = random.SystemRandom()
    task_uid = "vh_" + "".join(
        sys_random.choice("abcdefghijklmnopqrstuvwxyz" + "0123456789") for _ in range(12)
    )
    task_dir = join(dir, task_uid + "/")
    Path(task_dir).mkdir(parents=True, exist_ok=True)
    return (task_uid, task_dir)


def from_url(input_url, image_hash=None):
    """
    download the video as input_url using YouTube-dl
    and calculate the hash.
    """
    task_uid, task_dir = task_uid_dir()
    output_file = join(task_dir, task_uid + ".%(ext)s")
    downloaded_file = download(input_url, output_file, task_dir, task_uid)
    input_file = join(task_dir, downloaded_file)
    return from_path(
        input_file, task_uid=task_uid, task_dir=task_dir, image_hash=image_hash
    )


def from_path(input_file, task_uid=None, task_dir=None, image_hash=None):
    """
    calculate videohash of file at absolute path input_file.
    from_url relies upon this function to do the main job after downloading
    the video.
    Ensure that the video exist at absolute path input_file, if not raise FileNotFoundError.
    Delete the tempfile after we are done.
    """

    if not Path(input_file).is_file():
        raise FileNotFoundError(
            "Can't find your file on this path.\nMake sure you are using an absolute path."
        )

    if not task_uid or not task_dir:
        task_uid, task_dir = task_uid_dir()
    image_dir = join(task_dir, "frames/")
    Path(image_dir).mkdir(parents=True, exist_ok=True)
    image_prefix = join(image_dir, task_uid)
    frames(input_file, image_prefix)
    collage_maker(image_dir, task_dir, 800)
    collage = join(task_dir, "collage.jpeg")
    _hash = hash_manager(collage, image_hash=image_hash)
    shutil.rmtree(dir)
    return _hash
