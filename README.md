<div align="center">
<img src="https://raw.githubusercontent.com/akamhy/videohash/main/assets/logo/logo-optimized.svg"><br>
</div>

<h2 align="center"> The Python package for near duplicate video detection </h2>

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

## ⭐️ Introduction

Videohash is a [Python package](https://www.udacity.com/blog/2021/01/what-is-a-python-package.html) for **detecting near-duplicate videos (Perceptual Video Hashing)**.
It can take any input video and generate a 64-bit equivalent hash value. Videohash is way more faster than comparing the imagehash values of individual [frames](https://en.wikipedia.org/wiki/Film_frame) of the video and more reliable than hashing [keyframes](https://en.wikipedia.org/wiki/Key_frame).

The video-hash-values for identical or near-duplicate videos are the same or similar, implying that if the video is resized (upscaled/downscaled), [transcoded](https://medium.com/videocoin/what-is-video-transcoding-and-why-do-you-do-it-348a2610cefc), [watermark](https://en.wikipedia.org/wiki/Digital_watermarking) added/removed, [stabilized](https://link.springer.com/referenceworkentry/10.1007%2F978-0-387-78414-4_76), [color changed](https://en.wikipedia.org/wiki/Chrominance), [frame rate](https://www.techsmith.com/blog/frame-rate-beginners-guide/) changed, changed [aspect ratio](https://en.wikipedia.org/wiki/Aspect_ratio_(image)),  [cropped](https://www.avs4you.com/blog/trim-cut-crop-avs4you/), [black-bars](https://en.wikipedia.org/wiki/Letterboxing_(filming)) added or removed, the hash-value should remain unchanged or not vary substantially.

### How the hash values are calculated

> - In layman's terms : Every one second, a frame from the input video is extracted, the frames are shrunk to a 144x144 pixel square, a collage is constructed that contains all of the resized frames(square-shaped), the collage's [wavelet hash](https://fullstackml.com/wavelet-image-hash-in-python-3504fdd282b5) is the video hash value for the original input video.

### When not to use Videohash

> - Videohash cannot be used to verify whether one video is a part of another (video fingerprinting). If the video is reversed or rotated by a substantial angle (greater than 10 degrees), Videohash will not provide the same or similar hash result, but you can always reverse the video manually and generate the hash value for reversed video.

### How to compare the video hash values stored in a database

> - Read [Hamming Distance / Similarity searches in a database - Stack Overflow](https://stackoverflow.com/questions/9606492/hamming-distance-similarity-searches-in-a-database) [(Archive link)](https://web.archive.org/web/20211015120052/https://stackoverflow.com/questions/9606492/hamming-distance-similarity-searches-in-a-database)

--------------------------------------------------------------------------

### 🏗 Installation

To use this software, you must have [FFmpeg](https://ffmpeg.org/) installed. Please read [how to install FFmpeg](https://github.com/akamhy/videohash/wiki/Install-FFmpeg,-but-how%3F) if you don't already know how.

#### Install videohash

Upgrade pip
```bash
python3 -m pip install --upgrade pip
```
If you do not want to upgrade pip and the installation fails try appending `--prefer-binary` to the following installation command(s).

- Install from the [PyPi](https://pypi.org/) (recommended):

```bash
pip install videohash
```

- Install directly from [the](https://github.com/akamhy/videohash) GitHub repository (NOT recommended):

```bash
pip install git+https://github.com/akamhy/videohash.git
```

--------------------------------------------------------------------------

### 🌱 Features

- It is fast!
- Generate videohash of a video directly from its URL(uses [yt-dlp](https://github.com/yt-dlp/yt-dlp)) or its path.
- Can be used as the core of a scalable Near Duplicate Video Retrieval (NDVR) system.
- The end-user can access the image representation(the collage) of the video.
- A videohash instance can be compared to a 64-bit stored hash, its hex representation, bitlist, and other videohash instances.

--------------------------------------------------------------------------

### 🚀 Usage

In the following usage example the first three instance of VideoHash class are computing the hash for the same video(not same as in checksum) and the last one is a different video.

- videohash1 is the video at <https://www.youtube.com/watch?v=PapBjpzRhnA>.

- videohash2 is downscaled copy of <https://www.youtube.com/watch?v=PapBjpzRhnA> contained in [Matroska Multimedia Container](https://www.matroska.org/index.html).

- videohash3 is the same video as videohash2 but on local storage.

- videohash4 uses a completely different video at <https://www.youtube.com/watch?v=_T8cn2J13-4>.

```python
>>> from videohash import VideoHash
>>> # video: Artemis I Hot Fire Test
>>> url1 = "https://www.youtube.com/watch?v=PapBjpzRhnA"
>>> videohash1 = VideoHash(url=url1)
>>>
>>> videohash1.hash # video hash value of the file, value is same as str(videohash1)
'0b0011010000011111111011111111111110001111011110000000000000000000'
>>>
>>> #VIDEO:Artemis I Hot Fire Test
>>> url2="https://raw.githubusercontent.com/akamhy/videohash/main/assets/rocket.mkv"
>>> videohash2 = VideoHash(url=url2)
>>> videohash2.hash
'0b0011010000011111111011111111111110001111011110000000000000000000'
>>> videohash2.hash_hex
'0x341fefff8f780000'
>>> videohash2.hash_hex
'0x341fefff8f780000'
>>> videohash1 - videohash2
0
>>> videohash1 == videohash2
True
>>> videohash1 == "0b0011010000011111111011111111111110001111011110000000000000000000"
True
>>> videohash1 != videohash2
False
>>> path3 = "/home/akamhy/Downloads/rocket.mkv" #VIDEO: Artemis I Hot Fire Test
>>> videohash3 = VideoHash(path=path3)
>>> videohash3.hash
'0b0011010000011111111011111111111110001111011110000000000000000000'
>>> videohash3 - videohash2
0
>>> videohash3 == videohash1
True
>>> url4 = "https://www.youtube.com/watch?v=_T8cn2J13-4" #VIDEO: How We Are Going to the Moon
>>> videohash4 = VideoHash(url=url4)
>>> videohash4.hash_hex
'0x7cffff000000eff0'
>>> videohash4 - "0x7cffff000000eff0"
0
>>> videohash4.hash
'0b0111110011111111111111110000000000000000000000001110111111110000'
>>> videohash4 - videohash2
34
>>> videohash4 != videohash2
True
```

<sub>Run the above code @ <https://replit.com/@akamhy/videohash-usage-2xx-example-code-for-video-hashing#main.py></sub>

**Extended Usage** : <https://github.com/akamhy/videohash/wiki/Extended-Usage>

**API Reference** : <https://github.com/akamhy/videohash/wiki/API-Reference>

--------------------------------------------------------------------------


### 🙏 Credits

  - [JohannesBuchner](https://github.com/JohannesBuchner) and [bunchesofdonald](https://github.com/bunchesofdonald) for [imagehash](https://github.com/JohannesBuchner/imagehash).
  - [Dmitry Petrov](https://medium.com/@fullstackml) for [implementing](https://fullstackml.com/wavelet-image-hash-in-python-3504fdd282b5) [discrete wavelet transform](https://en.wikipedia.org/wiki/Discrete_wavelet_transform) (DWT) based image hashing in Python.
  - [FFmpeg developers](https://ffmpeg.org/consulting.html).
  - [Eddievin](https://github.com/Eddievin) for README design.
  - [iconolocode](https://github.com/iconolocode) for the videohash logo.
 
--------------------------------------------------------------------------
  
### 🛡 License

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/akamhy/videohash/blob/master/LICENSE)

Copyright (c) 2021-2022 Akash Mahanty. See
[license](https://github.com/akamhy/videohash/blob/master/LICENSE) for details.

The VideoHash logo was created by [iconolocode](https://github.com/iconolocode). See [license](https://github.com/akamhy/videohash/blob/main/assets/logo/LICENSE-LOGO) for details.

Videos are from NASA and are in the public domain.
> NASA copyright policy states that "NASA material is not protected by copyright unless noted".
