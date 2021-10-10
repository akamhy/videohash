import os
import tempfile
from pathlib import Path


def get_list_of_all_files_in_dir(dir):
    file_list = [(dir + filename) for filename in os.listdir(dir)]
    return sorted(file_list)


def does_path_exists(path):
    """
    If a directory is supplied then check if it exists.
    If a file is supplied then check if it exists.

    Directory ends with "/" and files do not.

    If directory/file exists returns True else returns False


    """
    if path.endswith("/") or path.endswith("\\"):
        # it's directory
        return os.path.isdir(path)

    else:
        # it's file
        return os.path.isfile(path)


def create_and_return_temporary_directory():
    """
    create a temporary directory where we can store the video, frames and the collage.
    """
    path = os.path.join(tempfile.mkdtemp(), ("temp_storage_dir%s" % os.path.sep))
    Path(path).mkdir(parents=True, exist_ok=True)
    return path
