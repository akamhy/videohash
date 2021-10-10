import os
import random
import re
from PIL import Image
import imagehash
import shutil
from pathlib import Path

from .collagemaker import MakeCollage
from .downloader import Download
from .framesextractor import FramesExtractor
from .exceptions import DidNotSupplyPathOrUrl, StoragePathDoesNotExist
from .utils import (
    does_path_exists,
    create_and_return_temporary_directory,
    get_list_of_all_files_in_dir,
)


class VideoHash(object):
    """
    The VideoHash class provides an interface for computing & comparing the hash
    values for files supported by the ffmpeg. Every video format, encoding and
    containers that are supported by the ffmpeg can be used as input for this
    class.
    """

    def __init__(self, path=None, url=None, storage_path=None, download_worst=True):
        """
        :param path: absolute path of the video file.

        :param url: URL of the video file. Every URL that is supported by the
                    youtube-dl or yt-dlp package can be used.

        :param storage_path: If you want to provide a storage path for the files
                             created/downloaded by the instance, pass the
                             absolute path to that directory.

        :param download_worst: If set to False, download the default quality of
                               youtube-dl/yt-dlp downloader. These two downloaders
                               usually default to the best quality available.
                               Worst quality may be an issue for some users, they
                               are free to set the download_worst to False.
        """
        self.path = path
        self.url = url
        self.storage_path = storage_path
        self._storage_path = storage_path
        self.download_worst = download_worst
        self.video_path = None
        self.task_uid = VideoHash._get_task_uid()
        self._create_required_dirs_and_check_for_errors()
        self._copy_video_to_video_dir()
        FramesExtractor(self.video_path, self.frames_dir, interval=1, ffmpeg_path=None)
        self.collage_path = os.path.join(self.collage_dir, "collage.jpg")
        MakeCollage(
            get_list_of_all_files_in_dir(self.frames_dir),
            self.collage_path,
            collage_image_width=1024,
        )
        self.image = Image.open(self.collage_path)
        self.hash = None
        self.hash_hex = None
        self.bits_in_hash = 64

        self._calc_hash()

    def __str__(self):
        """
        The hash value of the instance. The hash value is 64 bit value prefixed
        with '0b', indicating the that the hash is binary.
        """

        return self.hash

    def __repr__(self):
        """
        Developer's representation of the instance.
        """

        return "VideoHash(hash=%s, hash_hex=%s, collage_path=%s, bits_in_hash=%s)" % (
            self.hash,
            self.hash_hex,
            self.collage_path,
            self.bits_in_hash,
        )

    def __len__(self):
        """
        Length of the hash value string. Total length is 66 characters, 64 for
        the bitstring and 2 for the prefix '0b' of the hash value string.
        """
        return len(self.hash)

    def __ne__(self, other):
        """
        Definition of the "!=" operator for the VideoHash objects.

        If the hamming distance of this instance and the other instance
        is zero returns False else returns True.
        """
        if self.__eq__(other):
            return False
        return True

    def __eq__(self, other):
        """
        Definition of the '=' operator on VideoHash objects.

        If the hamming distance of the instance and the other instance
        is zero returns True else returns False.
        """

        if self.__sub__(other) == 0:
            return True
        return False

    def __sub__(self, other):
        """
        Define how the '-' operator should work for the class.

        Checks that the binary strings are prefixed with '0b', hexadecimal
        strings prefixed with '0x' and if the string is not prefixed with
        any of them then raise ValueError.

        Instance of the VideoHash class are also supported.

        Raises ValueError if the object passed is not an instance of string
        nor VideoHash.
        """
        if other is None:
            raise TypeError("Other hash is None. And it should not be None.")

        if isinstance(other, str):
            if other.lower().startswith("0x"):
                return VideoHash.hamming_distance(
                    self.hash, VideoHash.hex2bin(other.lower(), self.bits_in_hash)
                )
            elif other.lower().startswith("0b"):
                if len(other) != len(self.hash):
                    raise ValueError(
                        "Can not compare different bits hashes. You must supply a %d bits hash."
                        % self.bits_in_hash
                    )
                return VideoHash.hamming_distance(self.hash, other.lower())
            else:
                raise TypeError(
                    "Hash string must start with either '0x' for hexadecimal or '0b' for binary."
                )

        if isinstance(other, VideoHash):
            return VideoHash.hamming_distance(self.hash, other.hash)

        raise TypeError(
            "To calculate difference both of the hashes must be either hexadecimal/binary strings or instance of VideoHash"
        )

    def _copy_video_to_video_dir(self):
        """
        Copy the video from the path the video directory.
        It avoids the issues like the user or some other
        processes deleting the instance files while we are
        still processing.

        If instead of the path the uploader specified an url,
        then download the video and copy the file to video
        directory.

        :raises ValueError: If the path supplied by the end user
                            lacks an extension. Like webm or mp4.
        """
        if self.path:
            # create a copy of the video at self.storage_path
            match = re.search(r"\.([^.]+$)", self.path)

            if match:
                extension = match.group(1)
            else:
                raise ValueError("File name (path) does not have an extension.")

            self.video_path = os.path.join(self.video_dir, ("video.%s" % extension))
            shutil.copyfile(self.path, self.video_path)

        if self.url:
            Download(
                self.url,
                self.video_download_dir,
                youtube_dl_path=None,
                worst=self.download_worst,
            )
            downloaded_file = get_list_of_all_files_in_dir(self.video_download_dir)[0]
            self.video_path = "%svideo.%s" % (
                self.video_dir,
                re.search(r"\.(.*?)$", downloaded_file).group(1),
            )
            shutil.copyfile(downloaded_file, self.video_path)

    def _create_required_dirs_and_check_for_errors(self):
        """
        Creates some directories before the main processing starts.
        The files are stored in these directories, no need to worry about
        the end user or some other processes interfering with the instance
        generated files.

        :raises DidNotSupplyPathOrUrl: If the user forgot to specify both the
                                       path and the url. One of them must be
                                       specified.

        :raises ValueError: If user passed both the path and the url. Only pass
                            one of them if the file is available on both the
                            path and the url.

        :raises StoragePathDoesNotExist: If the storage path specified by the
                                         user in does not exists.
        """
        if not self.path and not self.url:
            raise DidNotSupplyPathOrUrl(
                "You must specify either a path or an URL of the video."
            )

        if self.path and self.url:
            raise ValueError("Specify either a path or an URL and NOT both.")

        if not self.storage_path:
            self.storage_path = create_and_return_temporary_directory()

        if not does_path_exists(self.storage_path):
            raise StoragePathDoesNotExist(
                "Storage path '%s' does not exist." % self.storage_path
            )

        self.storage_path = os.path.join(
            self.storage_path, ("%s%s" % (self.task_uid, os.path.sep))
        )
        self.video_dir = os.path.join(self.storage_path, ("video%s" % os.path.sep))
        Path(self.video_dir).mkdir(parents=True, exist_ok=True)
        self.video_download_dir = os.path.join(
            self.storage_path, ("downloadedvideo%s" % os.path.sep)
        )
        Path(self.video_download_dir).mkdir(parents=True, exist_ok=True)
        self.frames_dir = os.path.join(self.storage_path, ("frames%s" % os.path.sep))
        Path(self.frames_dir).mkdir(parents=True, exist_ok=True)
        self.collage_dir = os.path.join(self.storage_path, ("collage%s" % os.path.sep))
        Path(self.collage_dir).mkdir(parents=True, exist_ok=True)

    def delete_storage_path(self):
        """Delete the storage_path directory tree."""
        dir = self.storage_path
        if not self._storage_path:
            dir = "%s%s" % (
                os.path.dirname(os.path.dirname(os.path.dirname(self.storage_path))),
                os.path.sep,
            )
        shutil.rmtree(dir, ignore_errors=True, onerror=None)

    @staticmethod
    def _get_task_uid():
        """
        Returns an unique task id for the instance and the task id is used to
        differentiate the instance files from the other unrelated files.
        """
        sys_random = random.SystemRandom()
        return "".join(
            sys_random.choice("abcdefghijklmnopqrstuvwxyz0123456789") for _ in range(12)
        )

    @staticmethod
    def hamming_distance(string_a, string_b):
        """
        Compute the hamming distance of the input strings.

        :raises ValueError: The input strings are of unequal length. Hamming
                            distance is not defined for unequal length strings.
        """
        if len(string_a) != len(string_b):
            raise ValueError(
                "Strings are of unequal length can not compute hamming distance. Hamming distance is undefined."
            )
        return sum(char_1 != char_2 for char_1, char_2 in zip(string_a, string_b))

    @staticmethod
    def hex2bin(hexstr, padding):
        """
        Convert hexadecimal('0x' prefixed) to bitstring string prefixed
        with '0b'.

        :raises ValueError: It input hexadecimal string is not prefixed
                            with '0x'.
        """
        if not hexstr.lower().startswith("0x"):
            raise ValueError("Input hexadecimal string must have '0x' as the prefix.")
        return "0b%s" % (
            str(bin(int(hexstr.lower(), 0))).replace("0b", "").zfill(padding)
        )

    @staticmethod
    def bin2hex(binstr):
        """
        Convert bitstring('0b' prefixed) to hexadecimal string prefixed
        with '0x'.

        :raises ValueError: It input binary string is not prefixed with '0b'.
        """

        if not binstr.lower().startswith("0b"):
            raise ValueError("Binary string must be prefixed with '0b'.")

        return str(hex(int(binstr, 2)))

    def _calc_hash(self):
        """
        Calculates the binary hash value by calling the whash method of
        imagehash package.

        End-user is not provided any access to the imagehash instance but
        instead the binary and hexadecimal equivalent of the result of
        wavelet-hash.
        """

        wavelethash_bit_list = []
        for row in imagehash.whash(self.image).hash.tolist():
            wavelethash_bit_list.extend(row)

        self.hash = ""

        for bit in wavelethash_bit_list:
            if bit:
                self.hash += "1"
            else:
                self.hash += "0"

        # the binary value must be prefixed with 0b.
        self.hash = "0b%s" % self.hash
        self.hash_hex = VideoHash.bin2hex(self.hash)
