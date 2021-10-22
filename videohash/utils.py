import os
import tempfile
from pathlib import Path
from typing import List


def get_list_of_all_files_in_dir(directory: str) -> List[str]:
    """
    Returns a list containing all the file paths(absolute path) in a directory.
    The list is sorted.

    :return: List of absolute path of all files in a directory.

    :rtype: List[str]
    """
    return sorted([(directory + filename) for filename in os.listdir(directory)])


def does_path_exists(path: str) -> bool:
    """
    If a directory is supplied then check if it exists.
    If a file is supplied then check if it exists.

    Directory ends with "/" on posix or "\" in windows and files do not.

    If directory/file exists returns True else returns False

    :return: True if dir or file exists else False.

    :rtype: bool
    """
    if path.endswith("/") or path.endswith("\\"):
        # it's directory
        return os.path.isdir(path)

    else:
        # it's file
        return os.path.isfile(path)


def create_and_return_temporary_directory() -> str:
    """
    create a temporary directory where we can store the video, frames and the
    collage.

    :return: Absolute path of the empty directory.

    :rtype: str
    """
    path = os.path.join(tempfile.mkdtemp(), ("temp_storage_dir" + os.path.sep))
    Path(path).mkdir(parents=True, exist_ok=True)
    return path
