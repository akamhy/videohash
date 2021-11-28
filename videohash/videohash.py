import os
import shutil
from pathlib import Path
import re
import random
from PIL import Image
import imagehash
import numpy as np

from .collagemaker import MakeCollage
from .downloader import Download
from .framesextractor import FramesExtractor
from .exceptions import DidNotSupplyPathOrUrl, StoragePathDoesNotExist
from .utils import (
    does_path_exists,
    create_and_return_temporary_directory,
    get_list_of_all_files_in_dir,
)

from typing import List, Optional, Union


class VideoHash:

    """
    VideoHash class provides an interface for computing & comparing the video
    hash values for videos(codec, containers etc) supported by FFmpeg.
    """

    def __init__(
        self,
        path: Optional[str] = None,
        url: Optional[str] = None,
        storage_path: Optional[str] = None,
        download_worst: bool = True,
        frame_interval: Union[int, float] = 1,
    ) -> None:
        """
        :param path: Absolute path of the input video file.

        :param url: URL of the input video file. Every URL that is supported by
                    the yt-dlp package can be passed.

        :param storage_path: Storage path for the files created/downloaded by
                             the instance, pass the absolute path of the
                             directory.
                             If no argument is passed then the instance will
                             itself create the storage directory inside the
                             temporary directory of the system.

        :param download_worst: If set to False, download the default quality of
                               yt-dlp downloader. yt-dlp usually default to the
                               best quality video available.
                               Worst quality might be an issue for some users,
                               they may set the download_worst to False.
                               The default value is True to conserve bandwidth.

        :param frame_interval: Number of frames extracted per unit time, the
                               default value is 1 per unit time. For 1 frame
                               per 5 seconds pass 1/5 or 0.2. For 5 fps pass 5.
                               Smaller frame_interval implies fewer frames and
                               vice-versa.


        :return: None

        :rtype: NoneType
        """
        self.path = path
        self.url = url

        self.storage_path = ""
        if storage_path:
            self.storage_path = storage_path

        self._storage_path = self.storage_path
        self.download_worst = download_worst
        self.frame_interval = frame_interval

        self.task_uid = VideoHash._get_task_uid()

        self._create_required_dirs_and_check_for_errors()

        self._copy_video_to_video_dir()

        FramesExtractor(self.video_path, self.frames_dir, interval=self.frame_interval)

        self.collage_path = os.path.join(self.collage_dir, "collage.jpg")

        MakeCollage(
            get_list_of_all_files_in_dir(self.frames_dir),
            self.collage_path,
            collage_image_width=1024,
        )

        self.image = Image.open(self.collage_path)
        self.bits_in_hash = 64

        self._calc_hash()

    def __str__(self) -> str:
        """
        The video hash value of the instance. The hash value is 64 bit string
        prefixed with '0b', indicating the that the hash value is a bitstring.

        :return: The string representation of the instance. The video hash value
                 itself is the returned value.

        :rtype: str
        """

        return self.hash

    def __repr__(self) -> str:
        """
        Developer's representation of the VideoHash object.

        :return: Developer's representation of the instance.

        :rtype: str
        """

        return (
            f"VideoHash(hash={self.hash}, hash_hex={self.hash_hex}, "
            + f"collage_path={self.collage_path}, bits_in_hash={self.bits_in_hash})"
        )

    def __len__(self) -> int:
        """
        Length of the hash value string. Total length is 66 characters, 64 for
        the bitstring and 2 for the prefix '0b'.

        :return: Length of the the hash value, including the prefix '0b'.

        :rtype: int
        """
        return len(self.hash)

    def __ne__(self, other: object) -> bool:
        """
        Definition of the "!=" operator for the VideoHash objects.

        Instance of the VideoHash class, lists(bitlist) and string prefixed with
         '0x' and '0b' are accepted other types.


        If the hamming distance of this instance and the other instance
        is zero returns False else returns True.

        :return: True if other object and instance do not have the same hash
                 value else False.

        :rtype: bool
        """

        if self == other:
            return False
        return True

    def __eq__(self, other: object) -> bool:
        """
        Definition of the '=' operator on VideoHash objects.

        Instance of the VideoHash class, lists(bitlist) and string prefixed with
         '0x' and '0b' are accepted other types.

        :return: True if other object and instance have the same hash
                 value else False.

        :rtype: bool
        """

        if self - other == 0:
            return True
        return False

    def __sub__(self, other: object) -> int:
        """
        Definition of the '-' operator on VideoHash objects.

        Instance of the VideoHash class, lists(bitlist) and string prefixed with
         '0x' and '0b' are accepted other types.

        The method checks that the binary strings are prefixed with '0b',
        hexadecimal strings prefixed with '0x' and if the string is not
        prefixed then raise ValueError.

        :return: The hamming distance of hash values of the instance and other
                 object.

        :rtype: int

        :raises TypeError: If the object passed is not an instance of string, list
        or VideoHash.

        :raises ValueError: If the length of the hash values/bitlist of the
                            instance and the other object are not equal.

        :raises TypeError: If the hash values are python string objects but do
                           not have '0x' or '0b' as prefix.
        """
        if other is None:
            raise TypeError("Other hash is None. And it should not be None.")

        if isinstance(other, str):

            if other.lower().startswith("0x"):

                return self.hamming_distance(
                    string_a=self.hash,
                    string_b=VideoHash.hex2bin(other.lower(), self.bits_in_hash),
                )

            elif other.lower().startswith("0b"):

                if len(other) != len(self.hash):
                    raise ValueError(
                        "Can not compare different bits hashes. You must supply a %d bits hash."
                        % self.bits_in_hash
                    )
                return self.hamming_distance(string_a=self.hash, string_b=other.lower())

            else:

                raise TypeError(
                    "Hash string must start with either '0x' for hexadecimal or '0b' for binary."
                )

        if isinstance(other, list):

            if len(other) != self.bits_in_hash:
                raise ValueError(
                    f"The list does not have {self.bits_in_hash} bits. Can not calculate hamming distance."
                )

            return self.hamming_distance(bitlist_a=self.bitlist, bitlist_b=other)

        if isinstance(other, VideoHash):
            return self.hamming_distance(
                bitlist_a=self.bitlist, bitlist_b=other.bitlist
            )

        raise TypeError(
            "To calculate difference both of the hashes must be either "
            + "hexadecimal/binary strings or instance of VideoHash class."
        )

    def _copy_video_to_video_dir(self) -> None:
        """
        Copy the video from the path to the video directory.

        Copying avoids issues such as the user or some other
        process deleting the instance files while we are still
        processing.

        If instead of the path the uploader specified an url,
        then download the video and copy the file to video
        directory.


        :return: None

        :rtype: NoneType

        :raises ValueError: If the path supplied by the end user
                            lacks an extension. E.g. webm, mkv and mp4.
        """
        self.video_path: str = ""

        if self.path:
            # create a copy of the video at self.storage_path
            match = re.search(r"\.([^.]+$)", self.path)

            if match:
                extension = match.group(1)

            else:
                raise ValueError("File name (path) does not have an extension.")

            self.video_path = os.path.join(self.video_dir, (f"video.{extension}"))

            shutil.copyfile(self.path, self.video_path)

        if self.url:

            Download(
                self.url,
                self.video_download_dir,
                worst=self.download_worst,
            )

            downloaded_file = get_list_of_all_files_in_dir(self.video_download_dir)[0]
            match = re.search(r"\.(.*?)$", downloaded_file)

            extension = "mkv"

            if match:
                extension = match.group(1)

            self.video_path = f"{self.video_dir}video.{extension}"

            shutil.copyfile(downloaded_file, self.video_path)

    def _create_required_dirs_and_check_for_errors(self) -> None:
        """
        Creates important directories before the main processing starts.

        The instance files are stored in these directories, no need to worry
        about the end user or some other processes interfering with the instance
        generated files.


        :raises DidNotSupplyPathOrUrl: If the user forgot to specify both the
                                       path and the url. One of them must be
                                       specified for creating the object.

        :raises ValueError: If user passed both path and url. Only pass
                            one of them if the file is available on both
                            then pass the path only.

        :raises StoragePathDoesNotExist: If the storage path specified by the
                                         user does not exist.

        :return: None

        :rtype: NoneType
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
                f"Storage path '{self.storage_path}' does not exist."
            )

        os_path_sep = os.path.sep

        self.storage_path = os.path.join(
            self.storage_path, (f"{self.task_uid}{os_path_sep}")
        )

        self.video_dir = os.path.join(self.storage_path, (f"video{os_path_sep}"))
        Path(self.video_dir).mkdir(parents=True, exist_ok=True)

        self.video_download_dir = os.path.join(
            self.storage_path, (f"downloadedvideo{os_path_sep}")
        )
        Path(self.video_download_dir).mkdir(parents=True, exist_ok=True)

        self.frames_dir = os.path.join(self.storage_path, (f"frames{os_path_sep}"))
        Path(self.frames_dir).mkdir(parents=True, exist_ok=True)

        self.collage_dir = os.path.join(self.storage_path, (f"collage{os_path_sep}"))
        Path(self.collage_dir).mkdir(parents=True, exist_ok=True)

    def delete_storage_path(self) -> None:
        """
        Delete the storage_path directory tree.

        Remember that deleting the storage directory will also delete the
        collage, extracted frames, and the downloaded video. If you passed an
        argument to the storage_path that directory will not be deleted but
        only the files and directories created inside that directory by the
        instance will be deleted, this is a feature(not a bug) to ensure that
        multiple instances of the same program are not deleting the storage
        path while other instances still require that storage directory.

        Many OS delete the temporary directory on boot or they never delete it.
        If you will be calculating videohash-value for many videos and don't
        want to run out of storage don't forget to delete the storage path.

        :return: None

        :rtype: NoneType
        """
        directory = self.storage_path

        if not self._storage_path:
            directory = (
                os.path.dirname(os.path.dirname(os.path.dirname(self.storage_path)))
                + os.path.sep
            )

        shutil.rmtree(directory, ignore_errors=True, onerror=None)

    @staticmethod
    def _get_task_uid() -> str:
        """
        Returns an unique task id for the instance. Task id is used to
        differentiate the instance files from the other unrelated files.

        We want to make sure that only the instance is manipulating the instance files
        and no other process nor user by accident deletes or edits instance files while
        we are still processing.

        :return: instance's unique task id.

        :rtype: str
        """
        sys_random = random.SystemRandom()

        return "".join(
            sys_random.choice(
                "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
            )
            for _ in range(20)
        )

    def hamming_distance(
        self,
        string_a: Optional[str] = None,
        string_b: Optional[str] = None,
        bitlist_a: Optional[List[int]] = None,
        bitlist_b: Optional[List[int]] = None,
    ) -> int:
        """
        Computes the hamming distance of the input bitstrings or bitlists.
        string_a and string_b must be bitstrings.
        bitlist_a and bitlist_b must be python strings containing only the
        bits and not the prefix "0b".

        :return: Hamming distance of the input bitstrings or bitlists.

        :rtype: int

        :raises ValueError: The input strings are of unequal length or bitlists
                            have different number of bits. Hamming distance is
                            not defined for unequal length strings.
        """
        if bitlist_a and bitlist_b:

            if len(bitlist_a) != len(bitlist_b):
                raise ValueError(
                    "Bit lists have unequal number of bits."
                    + " Can not compute hamming distance. Hamming distance is undefined."
                )

            _bitlist_a = bitlist_a
            _bitlist_b = bitlist_b

        if string_a and string_b:

            if len(string_a) != len(string_b):
                raise ValueError(
                    "Strings are of unequal length. Can not compute hamming distance. Hamming distance is undefined."
                )

            if string_a == self.hash:
                _bitlist_a = self.bitlist

            else:
                _bitlist_a = list(map(int, string_a.replace("0b", "")))

            if string_b == self.hash:
                _bitlist_b = self.bitlist

            else:
                _bitlist_b = list(map(int, string_b.replace("0b", "")))

        return len(
            np.bitwise_xor(
                _bitlist_a,
                _bitlist_b,
            ).nonzero()[0]
        )

    @staticmethod
    def hex2bin(hexstr: str, padding: int) -> str:
        """
        Convert hexadecimal('0x' prefixed) to bitstring string prefixed
        with '0b'.

        :return: Padded binary representation(bitstring) of the hexadecimal
                 input.

        :rtype: str

        :raises ValueError: If input hexadecimal string is not prefixed
                            with '0x'.
        """
        if not hexstr.lower().startswith("0x"):
            raise ValueError("Input hexadecimal string must have '0x' as the prefix.")

        return "0b" + str(bin(int(hexstr.lower(), 0))).replace("0b", "").zfill(padding)

    @staticmethod
    def bin2hex(binstr: str) -> str:
        """
        Convert bitstring('0b' prefixed) to hexadecimal string prefixed
        with '0x'.

        :return: Hex representation of the input bitstring.

        :rtype: str

        :raises ValueError: It input binary string is not prefixed with '0b'.
        """

        if not binstr.lower().startswith("0b"):
            raise ValueError("Binary string must be prefixed with '0b'.")

        return str(hex(int(binstr, 2)))

    def _calc_hash(self) -> None:
        """
        Calculates the hash value by calling the whash(wavelet hash) method of
        imagehash package. The wavelet hash of the collage is the videohash for
        the original input video.

        End-user is not provided any access to the imagehash instance but
        instead the binary and hexadecimal equivalent of the result of
        wavelet-hash.

        :return: None

        :rtype: NoneType
        """

        self.bitlist: List = []

        for row in imagehash.whash(self.image).hash.astype(int).tolist():
            self.bitlist.extend(row)

        self.hash: str = ""

        for bit in self.bitlist:

            if bit:
                self.hash += "1"
            else:
                self.hash += "0"

        # the binary value is prefixed with 0b.
        self.hash = f"0b{self.hash}"
        self.hash_hex: str = VideoHash.bin2hex(self.hash)
