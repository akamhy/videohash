<div align="center">

<h1> VideoHash </h1>

<h3>A simple Video Hashing Library</h3>

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
Steps are [Based on video.stackexchange.com/a/20496](https://video.stackexchange.com/a/20496), but note that the download site is outdated as of January 2021.
  - Download the `release full` variant from <https://www.gyan.dev/ffmpeg/builds/>. You can download any variant you want, but I prefer the full release.
  - Decompress the archive.
  - Copy the bin directory from the decompressed folder, and paste inside `C:\Program Files\ffmpeg\`.
  - Right click on "This PC" and navigate to `Properties > Advanced System Settings > Advanced tab > Environment Variables`.
  - In the Environment Variables window, click the "Path" row under the "Variable" column, then click Edit.
  - Click New and add `C:\Program Files\ffmpeg\bin\`to the list.
  - Click Ok on all the windows we just opened up. (Answer postive)
  
If you still have doubts read the answer <https://video.stackexchange.com/a/20496>, it has images to guide you. 

Prefer video? <https://www.youtube.com/watch?v=qjtmgCb8NcE>
  


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
>>> import videohash
>>> hash1 = videohash.from_url("https://raw.githubusercontent.com/akamhy/videohash/main/assets/rocket.mkv")
>>> str(hash1)
'be1fffff9ffc0000'
>>> hash2 = videohash.from_url("https://www.youtube.com/watch?v=PapBjpzRhnA")
>>> str(hash2)
'fe3fffff9ffc0000'
>>>
>>> diff = hash1 - hash2
>>> diff
2
>>>
>>> hash3 = videohash.from_url("https://www.youtube.com/watch?v=_T8cn2J13-4")
>>> diff = hash1 - hash3
>>> diff
31
>>> str(hash3)
'3cffff00000081f0'
>>>
>>> #hash4 file is hash1 file downloaded locally. Use absolute path
>>> hash4 = videohash.from_path("/home/akamhy/Downloads/rocket.mkv")
>>> diff = hash4 - hash1
>>> diff
0
>>>
```
<sub>Run the above code @ <https://repl.it/@akamhy/video-hash-example#main.py></sub>


  - <https://raw.githubusercontent.com/akamhy/videohash/main/assets/rocket.mkv> is copy of <https://www.youtube.com/watch?v=PapBjpzRhnA>, and are about the [Artemis program](https://en.wikipedia.org/wiki/Artemis_program) and [SLS rocket](https://en.wikipedia.org/wiki/Space_Launch_System).

  - <https://www.youtube.com/watch?v=_T8cn2J13-4> is an entirely distinct video also about the [Artemis program](https://en.wikipedia.org/wiki/Artemis_program).

  - Notice that the difference of hash1 and hash2 is 2, but the difference between hash1 and hash3 is 37.

  - The difference of hash1 and hash2 is not 0 as the file in this repository is slightly modified and downscaled.

  - A collage of frames is generated and imagehash(Average hashing) of this collage is videohash for the full video.

<div align="center">
<img src="https://raw.githubusercontent.com/akamhy/videohash/main/assets/collage.jpeg"><br>
</div>



You can change the algorithm used to generate the hash of the collage via the `image_hash` argument. The default algorithm is `average_hash`.

```python
>>> hash = videohash.from_url("https://www.youtube.com/watch?v=PapBjpzRhnA", image_hash="crop_resistant_hash")
>>> hash = videohash.from_path("/home/akamhy/Downloads/rocket.mkv", image_hash="phash")
```
<details><summary>➤ Algorithms supported</summary>

<p>

- `average_hash`
- `phash`
- `dhash`
- `whash`
- `colorhash`
- `crop_resistant_hash`

</p>

</details>

videohash is using <https://github.com/JohannesBuchner/imagehash> to use these image-hashing algorithms.



## License
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/akamhy/videohash/blob/master/LICENSE)

NASA videos are in the public domain. NASA copyright policy states that "NASA material is not protected by copyright unless noted".

Released under the MIT License. See
[license](https://github.com/akamhy/videohash/blob/master/LICENSE) for details.

------------------------------------------------------------------------------------
