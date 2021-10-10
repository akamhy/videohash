"""This file downloads the
ffmpeg binaries from google
drive and writes them at
os.getcwd()
"""

import requests
import zipfile
import os
from os.path import join
from pathlib import Path


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

ffmpeg_path = join(base, "ffmpeg.exe")
with open(ffmpeg_path, "wb") as fd:
    fd.write(r.content)
print(ffmpeg_path)
