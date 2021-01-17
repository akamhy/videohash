<div align="center">

# VIDEOHASH

<h3>A simple Video Hashing Library</h3>

</div>

<p align="center">
<a href="https://pypi.org/project/videohash/"><img alt="pypi" src="https://img.shields.io/pypi/v/videohash.svg"></a>
<a href="https://pepy.tech/project/videohash?versions=1*&versions=2*"><img alt="Downloads" src="https://pepy.tech/badge/videohash/month"></a>
<a href="https://github.com/akamhy/videohash/commits/master"><img alt="GitHub lastest commit" src="https://img.shields.io/github/last-commit/akamhy/videohash?color=blue&style=flat-square"></a>
<a href="#"><img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/videohash?style=flat-square"></a>

--------------------------------------------------------------------------


### Installation

You must have [ffmpeg](https://ffmpeg.org/) installed to use this library.


  - Using [pip](https://en.wikipedia.org/wiki/Pip_(package_manager)):

```bash
pip install videohash
```

  - Install directly from GitHub:

```bash
pip install git+https://github.com/akamhy/videohash.git
```

### Usage

  - <https://raw.githubusercontent.com/akamhy/videohash/main/assets/rocket.webm> is copy of <https://www.youtube.com/watch?v=PapBjpzRhnA>, both of these files are about the [Artemis program](https://en.wikipedia.org/wiki/Artemis_program) and [SLS rocket](https://en.wikipedia.org/wiki/Space_Launch_System).
 
  - <https://www.youtube.com/watch?v=_T8cn2J13-4> is a completly different video also about the [Artemis program](https://en.wikipedia.org/wiki/Artemis_program).

```python
>>> import videohash
>>> hash1 = videohash.from_url("https://raw.githubusercontent.com/akamhy/videohash/main/assets/rocket.webm")
>>> str(hash1)
'7c7e7ff9ffff0000'
>>> hash2 = videohash.from_url("https://www.youtube.com/watch?v=PapBjpzRhnA")
>>> str(hash2)
'fc7e7ffbffff0000'
>>> 
>>> diff = hash1 - hash2
>>> diff
2
>>> 
>>> hash3 = videohash.from_url("https://www.youtube.com/watch?v=_T8cn2J13-4")
>>> diff = hash1 - hash3
>>> diff
37
>>> str(hash3)
'3cffff0000000eff'
>>> 
```

  - Notice that the difference of hash1 and hash2 is 2, but the difference between hash1 and hash3 is 37.
  
  - The difference of hash1 and hash2 is not 0 as the file in this repository is slightly modified.
  
  - You can hash local video using `videohash.from_path("<absolute path to video>")`.

  - Public domain files used. NASA copyright policy states that "NASA material is not protected by copyright unless noted".
  
  - We create collage of frames and actually are calculating image hashes under the hood.
  


<div align="center">

<img src="https://raw.githubusercontent.com/akamhy/videohash/main/assets/collage.jpeg"><br>

</div>


## License
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/akamhy/videohash/blob/master/LICENSE)

Released under the MIT License. See
[license](https://github.com/akamhy/videohash/blob/master/LICENSE) for details.

------------------------------------------------------------------------------------
