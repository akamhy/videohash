<div align="center">

<h1> VideoHash </h1>

<h3>A Python Perceptual Video Hashing/Fingerprinting Package</h3>

</div>

<p align="center">
<a href="https://github.com/akamhy/videohash/actions?query=workflow%3AUbuntu"><img alt="Build Status" src="https://github.com/akamhy/videohash/workflows/Ubuntu/badge.svg"></a>
<a href="https://github.com/akamhy/videohash/actions?query=workflow%3AWindows"><img alt="Build Status" src="https://github.com/akamhy/videohash/workflows/Windows/badge.svg"></a>
<a href="https://github.com/akamhy/videohash/actions?query=workflow%3AmacOS"><img alt="Build Status" src="https://github.com/akamhy/videohash/workflows/macOS/badge.svg"></a>
<a href="https://codecov.io/gh/akamhy/videohash"><img alt="codecov" src="https://codecov.io/gh/akamhy/videohash/branch/main/graph/badge.svg"></a>
<a href="https://pypi.org/project/videohash/"><img alt="pypi" src="https://img.shields.io/pypi/v/videohash.svg"></a>
<a href="https://pepy.tech/project/videohash?versions=1*"><img alt="Downloads" src="https://pepy.tech/badge/videohash/month"></a>
<a href="https://github.com/akamhy/videohash/commits/main"><img alt="GitHub lastest commit" src="https://img.shields.io/github/last-commit/akamhy/videohash?color=blue&style=flat-square"></a>
<a href="#"><img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/videohash?style=flat-square"></a>
</p>

--------------------------------------------------------------------------


### Installation
You must have [ffmpeg](https://ffmpeg.org/) installed to use this library.
<details><summary>➤ Install FFmpeg</summary>
<p>

###### Linux

  - APT
```bash
sudo apt-get update
sudo apt install ffmpeg
```
  - Snap
```bash
sudo snap install ffmpeg
```

###### Windows
Steps are [based on video.stackexchange.com/a/20496](https://video.stackexchange.com/a/20496), please note that the download site is outdated as of January 2021.
  - Download the `release full` variant from <https://www.gyan.dev/ffmpeg/builds/>. You can download any variant you want, but I prefer the full release.
  - Decompress the archive.
  - Copy the bin directory from the decompressed folder, and paste inside `C:\Program Files\ffmpeg\`.
  - Right click on "This PC" and navigate to `Properties > Advanced System Settings > Advanced tab > Environment Variables`.
  - In the Environment Variables window, click the "Path" row under the "Variable" column, then click Edit.
  - Click New and add `C:\Program Files\ffmpeg\bin\`to the list.
  - Click Ok on all the windows we just opened up. (Answer postive)

If you still have doubts read the answer <https://video.stackexchange.com/a/20496>, it has images to guide you.

Prefer video? <https://www.youtube.com/watch?v=qjtmgCb8NcE>.

###### macOS
```bash
brew install ffmpeg
```
</p>
</details>


#### Install videohash

  - Using [pip](https://en.wikipedia.org/wiki/Pip_(package_manager)):

```bash
pip install videohash
```

  - Install directly from GitHub:

```bash
pip install git+https://github.com/akamhy/videohash.git
```

### Usage

```python
>>> from videohash import VideoHash
>>> hash1 = VideoHash(url="https://www.youtube.com/watch?v=PapBjpzRhnA")
>>> str(hash1)
'0b0011010000011111111011111111111110001111011110000000000000000000'
>>> hash1.hash
'0b0011010000011111111011111111111110001111011110000000000000000000'
>>> hash1.hash_hex
'0x341fefff8f780000'
>>> repr(hash1)
'VideoHash(hash=0b0011010000011111111011111111111110001111011110000000000000000000, hash_hex=0x341fefff8f780000, collage_path=/tmp/tmp3kzva948/temp_storage_dir/kyci5lleck1z/collage/collage.jpg, bits_in_hash=64)'
>>> hash1.collage_path
'/tmp/tmp3kzva948/temp_storage_dir/kyci5lleck1z/collage/collage.jpg'
>>> hash1.bits_in_hash
64
>>> len(hash1)
66
>>> hash2 = VideoHash(url="https://raw.githubusercontent.com/akamhy/videohash/main/assets/rocket.mkv")
>>> hash2.hash
'0b0011010000011111111011111111111110001111011110000000000000000000'
>>> hash2.hash_hex
'0x341fefff8f780000'
>>> hash1.hash_hex
'0x341fefff8f780000'
>>> hash1 - hash2
0
>>> hash2 - "0x341fefff8f780000"
0
>>> hash1 - "0b0011010000011111111011111111111110001111011110000000000000000000"0
>>> hash1 == hash2
True
>>> hash1 != hash2
False
>>> hash3 = VideoHash(path="/home/akamhy/Downloads/rocket.mkv")
>>> hash3.hash_hex
'0x341fefff8f780000'
>>> hash3.hash
'0b0011010000011111111011111111111110001111011110000000000000000000'
>>> hash3 - hash2
0
>>> hash3 == hash1
True
>>> hash4 = VideoHash(url="https://www.youtube.com/watch?v=_T8cn2J13-4")
>>> hash4.hash_hex
'0x7cffff000000eff0'
>>> hash4.hash
'0b0111110011111111111111110000000000000000000000001110111111110000'
>>> hash4 == hash3
False
>>> hash4 - hash2
34
>>> hash4 != hash2
True
>>> hash4 - "0b0011010000011111111011111111111110001111011110000000000000000000"34
>>> hash4 - "0b0111110011111111111111110000000000000000000000001110111111110000"0
>>> hash4 - "0x7cffff000000eff0"
0
>>>
```
<sub>Run the above code @ </sub>





## License
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/akamhy/videohash/blob/master/LICENSE)


Released under the MIT License. See
[license](https://github.com/akamhy/videohash/blob/master/LICENSE) for details.

------------------------------------------------------------------------------------
