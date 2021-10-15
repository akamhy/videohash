<div align="center">

<h1> VideoHash </h1>

<h2> Python package for Perceptual Video Hashing </h2>

</div>

<p align="center">
<a href="https://github.com/akamhy/videohash/actions?query=workflow%3AUbuntu"><img alt="Build Status" src="https://github.com/akamhy/videohash/workflows/Ubuntu/badge.svg"></a>
<a href="https://github.com/akamhy/videohash/actions?query=workflow%3AWindows"><img alt="Build Status" src="https://github.com/akamhy/videohash/workflows/Windows/badge.svg"></a>
<a href="https://github.com/akamhy/videohash/actions?query=workflow%3AmacOS"><img alt="Build Status" src="https://github.com/akamhy/videohash/workflows/macOS/badge.svg"></a>
<a href="https://codecov.io/gh/akamhy/videohash"><img alt="codecov" src="https://codecov.io/gh/akamhy/videohash/branch/main/graph/badge.svg"></a>
<a href="https://lgtm.com/projects/g/akamhy/videohash/alerts/"><img alt="Total alerts" src="https://img.shields.io/lgtm/alerts/g/akamhy/videohash.svg?logo=lgtm&logoWidth=18"></a>
<a href="https://lgtm.com/projects/g/akamhy/videohash/context:python"><img alt="Language grade: Python" src="https://img.shields.io/lgtm/grade/python/g/akamhy/videohash.svg?logo=lgtm&logoWidth=18"></a>
<a href="https://pypi.org/project/videohash/"><img alt="pypi" src="https://img.shields.io/pypi/v/videohash.svg"></a>
<a href="https://pepy.tech/project/videohash?versions=1*&versions=2*"><img alt="Downloads" src="https://pepy.tech/badge/videohash/month"></a>
<a href="https://github.com/akamhy/videohash/commits/main"><img alt="GitHub lastest commit" src="https://img.shields.io/github/last-commit/akamhy/videohash?color=blue&style=flat-square"></a>
<a href="#"><img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/videohash?style=flat-square"></a>
</p>

--------------------------------------------------------------------------

### Introduction

Videohash is a Python package for Perceptual Video Hashing (Near-Duplicate-Video-Detection). The package can be used to generate a 64-bit comparable hash-value for any video input. The hash-values are the same or similar for identical/near-duplicate videos, which implies that hash-value should remain unchanged or not change drastically for the video if it's resized (upscaled/downscaled), transcoded, slightly-cropped, or black-bars added/removed.

How the hash values are calculated?
>  - Every one second a frame of the input video is extracted, the frames are resized to a 144x144 pixel square, a collage is created that embeds all the resized frames(square-shaped) in it, the wavelet hash value of the collage is computed, and it is the video hash value for the original input video.

When not to use Videohash?
>  - Videohash can not be used for verifying if one video is part of another video(video fingerprinting). Videohash doesn't produce the same or similar hash value if the video is reversed or rotated by a significant angle(more than 10 degrees), but you can always reverse the video yourself and generate the hash value for reversed video.

--------------------------------------------------------------------------

### Installation
You must have [FFmpeg](https://ffmpeg.org/) installed to use this software. If you don't know how to install FFmpeg, please read
[how to install FFmpeg](https://github.com/akamhy/videohash/wiki/Install-FFmpeg,-but-how%3F).


#### Install videohash

  - Using [pip](https://en.wikipedia.org/wiki/Pip_(package_manager)):

```bash
pip install videohash
```

  - Install directly from GitHub:

```bash
pip install git+https://github.com/akamhy/videohash.git
```
--------------------------------------------------------------------------

### Features

  - Generate videohash of a video directly from its URL or its path.
  - Can be used to implement scalable Near Duplicate Video Retrieval.
  - Image representation of the video is accessible by the end-user.
  - An instance of videohash can be compared with a stored hash(64-bit), its hex representation, and other instances of videohash.
  - Faster than the primitive process of comparing all the frames one by one. The videohash package produces a single 64-bit hash, a lot of database space is saved. And the number of comparisons required drops significantly.

--------------------------------------------------------------------------

### Usage

```python
>>> from videohash import VideoHash
>>> hash1 = VideoHash(url="https://www.youtube.com/watch?v=PapBjpzRhnA", download_worst=False)
>>> str(hash1)
'0b0011010000011111111011111111111110001111011110000000000000000000'
>>> hash1.hash
'0b0011010000011111111011111111111110001111011110000000000000000000'
>>> hash1.hash_hex
'0x341fefff8f780000'
>>> repr(hash1)
'VideoHash(hash=0b0011010000011111111011111111111110001111011110000000000000000000, hash_hex=0x341fefff8f780000, collage_path=/tmp/tmpe07d_b1g/temp_storage_dir/acn6zsdcb40q/collage/collage.jpg, bits_in_hash=64)'
>>> hash1.collage_path
'/tmp/tmpe07d_b1g/temp_storage_dir/acn6zsdcb40q/collage/collage.jpg'
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
'0x741fcfff8f780000'
>>> hash1 - hash2
0
>>> hash2 - "0x341fefff8f780000"
0
>>> hash1 - "0b0011010000011111111011111111111110001111011110000000000000000000"
2
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
False
>>> hash3 == hash2
True
>>> hash4 = VideoHash(url="https://www.youtube.com/watch?v=_T8cn2J13-4")
>>> hash4.hash_hex
'0x7cffff000000eff0'
>>> hash4 - "0x7cffff000000eff0"
0
>>> hash4.hash
'0b0111110011111111111111110000000000000000000000001110111111110000'
>>> hash4 - "0b0111110011111111111111110000000000000000000000001110111111110000"
0
>>> hash4 == hash3
False
>>> hash4 - hash2
34
>>> hash4 != hash2
True
>>> hash4 - "0b0011010000011111111011111111111110001111011110000000000000000000"
34
>>>
```
<sub>Run the above code @ <https://replit.com/@akamhy/videohash-usage-2xx-example-code-for-video-hashing#main.py></sub>
  
**Wiki/Extended Usage/Docs** : <https://github.com/akamhy/videohash/wiki>

--------------------------------------------------------------------------
  
### License
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/akamhy/videohash/blob/master/LICENSE)

Released under the MIT License. See
[license](https://github.com/akamhy/videohash/blob/master/LICENSE) for details.

Videos are from NASA and are in the public domain.
> NASA videos are in the public domain. NASA copyright policy states that "NASA material is not protected by copyright unless noted".

------------------------------------------------------------------------------------
