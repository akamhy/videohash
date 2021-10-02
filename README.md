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

```
<sub>Run the above code @ </sub>





## License
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/akamhy/videohash/blob/master/LICENSE)


Released under the MIT License. See
[license](https://github.com/akamhy/videohash/blob/master/LICENSE) for details.

------------------------------------------------------------------------------------
