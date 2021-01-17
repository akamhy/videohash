import subprocess
import os
import random
import string
from pathlib import Path
from PIL import Image
import imagehash
from math import ceil
import shutil
import tempfile

dir = tempfile.mkdtemp() + "/files/"


def download(input_url, output_file):
    command = "youtube-dl -f worst {input_url} -o {output_file}".format(
        input_url=input_url, output_file=output_file
    )
    process = subprocess.Popen(
        command.split(), stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
    )
    output, error = process.communicate()


def frames(input_file, output_prefix):
    command = "ffmpeg -i {input_file} -r 1 {output_prefix}_%07d.jpeg".format(
        input_file=input_file, output_prefix=output_prefix
    )
    process = subprocess.Popen(
        command.split(), stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
    )
    output, error = process.communicate()


def collage_maker(image_dir, task_dir, collage_image_width, images_per_row_in_collage):

    frame_list = sorted([image_dir + image for image in os.listdir(image_dir)])

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
    collage_image.save(task_dir + "collage.jpeg")


def task_uid_dir():
    sys_random = random.SystemRandom()
    task_uid = "vh_" + "".join(
        sys_random.choice(string.ascii_lowercase + string.digits) for _ in range(12)
    )
    task_dir = dir + task_uid + "/"
    Path(task_dir).mkdir(parents=True, exist_ok=True)
    return (task_uid, task_dir)


def from_url(input_url):
    task_uid, task_dir = task_uid_dir()
    output_file = task_dir + task_uid + ".%(ext)s"
    download(input_url, output_file)
    l = [filename for filename in os.listdir(task_dir) if filename.startswith(task_uid)]
    if len(l) == 0:
        raise FileNotFoundError(
            "0 frame frame_list found! Failed to generate frame_list from frames."
        )
    input_file = task_dir + l[0]
    return from_path(input_file, task_uid=task_uid, task_dir=task_dir)


def from_path(input_file, task_uid=None, task_dir=None):

    if not task_uid or not task_dir:
        task_uid, task_dir = task_uid_dir()
    image_dir = task_dir + "frames/"
    Path(image_dir).mkdir(parents=True, exist_ok=True)
    image_prefix = image_dir + task_uid
    frames(input_file, image_prefix)
    collage_maker(image_dir, task_dir, 800, 8)
    collage = task_dir + "collage.jpeg"
    hash = imagehash.average_hash(Image.open(collage))
    shutil.rmtree(dir)
    return hash
