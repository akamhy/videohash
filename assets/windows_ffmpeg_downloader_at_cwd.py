from pyunpack import Archive
import requests
import os
from pathlib import Path
from shutil import copyfile


base = os.getcwd()

Path(base).mkdir(parents=True, exist_ok=True)

ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z"

tries = 0
while True:
    tries += 1
    try:
        r = requests.get(ffmpeg_url)
        break
    except Exception as e:
        print(e)
    if tries > 5:
        break

ffmpeg_7z_path = os.path.join(base, "ffmpeg_full.7z")
with open(ffmpeg_7z_path, "wb") as fd:
    fd.write(r.content)
print(ffmpeg_7z_path)


Archive(ffmpeg_7z_path).extractall(".")

build_dir = None
for file in os.listdir(base):
    if "build" in file:
        build_dir = os.path.join(base, (file + os.path.sep))
        break

ffmpeg_path = os.path.join(build_dir, "bin", "ffmpeg.exe")
copyfile(ffmpeg_path, os.path.join(base, "ffmpeg.exe"))
