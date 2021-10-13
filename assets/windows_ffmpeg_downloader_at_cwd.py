from pyunpack import Archive
import requests
import os
from pathlib import Path
from shutil import copyfile


cwd = os.getcwd()
Path(cwd).mkdir(parents=True, exist_ok=True)
ffmpeg_7z_path = os.path.join(cwd, "ffmpeg_full.7z")
with open(ffmpeg_7z_path, "wb") as fd:
    fd.write(
        requests.get("https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z").content
    )
Archive(ffmpeg_7z_path).extractall(".")
for file in os.listdir(cwd):
    if "build" and "ffmpeg" in file:
        copyfile(
            os.path.join(os.path.join(cwd, (file + os.path.sep)), "bin", "ffmpeg.exe"),
            os.path.join(cwd, "ffmpeg.exe"),
        )
        break
