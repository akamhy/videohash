# videohash

A simple Video Hashing Library.

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

```python
>>> import videohash
>>> hash1 = videohash.from_url("https://www.youtube.com/watch?v=PapBjpzRhnA")
>>> str(hash1)
'7c7e7ff9ffff0000'
>>> hash2 = videohash.from_url("https://www.youtube.com/watch?v=PapBjpzRhnA")
>>> diff = hash1 - hash2
>>> diff
0
>>> hash3 = videohash.from_url("https://www.youtube.com/watch?v=_T8cn2J13-4")
>>> diff = hash1 - hash3
>>> diff
31
>>> 

```
