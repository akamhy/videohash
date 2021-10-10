import os
import shlex
from shutil import which
from subprocess import check_output, Popen, PIPE
from .utils import does_path_exists
from .exceptions import (
    FramesExtractorOutPutDirDoesNotExits,
    FFmpegNotFound,
    FFmpegFailedToExtractFrames,
)


"""
python module to extract the frames from a video.
"""


class FramesExtractor(object):
    """
    extract from from the passed video file and save at the output directory.
    """

    def __init__(self, video_path, output_dir, interval=1, ffmpeg_path=None):
        """
        Raises Exeception if video_path does not exists.
        Raises Exeception if output_dir does not exists or if not a directory.
        Checks  the ffmpeg installation and the path; thus ensure that we can use it.

        :param video_path: absolute path of the video

        :param output_dir: absolute path of the directory
                           where to save the frames.

        :param interval: interval is seconds. interval must be an integer.
                         Extract one frame every given number of seconds.
                         Default is 1, that is one frame every second.

        :param ffmpeg_path: path of the ffmpeg software if not in path.

        """
        self.video_path = video_path
        self.output_dir = output_dir
        self.interval = interval
        self.ffmpeg_path = ffmpeg_path

        if not does_path_exists(self.video_path):
            raise FileNotFoundError(
                "No video found at '%s' for frame extraction." % self.video_path
            )

        if not does_path_exists(self.output_dir):
            raise FramesExtractorOutPutDirDoesNotExits(
                "No directory called '%s' found for storing the frames."
                % self.output_dir
            )

        self._check_ffmpeg()

        self.extract()

    def _check_ffmpeg(self):
        """
        Checks the ffmpeg path and runs 'ffmpeg -version' to verify that the
        software, ffmpeg is found and works.
        """
        if not self.ffmpeg_path:
            if not which("ffmpeg"):
                raise FFmpegNotFound(
                    "FFmpeg is not on the path. Install FFmpeg and add it to the path."
                    + "Or you can also pass the path via the 'ffmpeg_path' param."
                )
            else:
                self.ffmpeg_path = str(which("ffmpeg"))

        # Check the ffmpeg
        try:
            # check_output will raise FileNotFoundError if it does not finds the ffmpeg
            output = check_output([str(self.ffmpeg_path), "-version"]).decode()
        except FileNotFoundError:
            raise FFmpegNotFound("FFmpeg not found at '%s'." % self.ffmpeg_path)
        else:
            if not "ffmpeg version" in output:
                raise FFmpegNotFound(
                    "ffmpeg at '%s' is not really ffmpeg. Output of ffmpeg -version is \n'%s'."
                    % (self.ffmpeg_path, output)
                )

    def extract(self):
        """
        Extract the frames at every n seconds where n is the
        integer set to self.interval.
        """
        ffmpeg_path = self.ffmpeg_path
        video_path = self.video_path
        output_dir = self.output_dir
        if os.name == "posix":
            ffmpeg_path = shlex.quote(self.ffmpeg_path)
            video_path = shlex.quote(self.video_path)
            output_dir = shlex.quote(self.output_dir)

        command = (
            ffmpeg_path
            + " -i "
            + '"'
            + video_path
            + '"'
            + " -s 144x144 "
            + " -r "
            + str(self.interval)
            + " "
            + '"'
            + self.output_dir
            + "video_frame_%07d.jpeg"
            + '"'
        )

        process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
        output, error = process.communicate()

        ffmpeg_output = output.decode()
        ffmpeg_error = error.decode()

        if len(os.listdir(self.output_dir)) == 0:
            raise FFmpegFailedToExtractFrames(
                "FFmpeg could not extract any frames.\n%s\n%s\n%s"
                % (command, ffmpeg_output, ffmpeg_error)
            )
