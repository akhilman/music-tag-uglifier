**Music Tag Normalizer for Portable DAPs**

This tool is designed to make music tags more compatible with **portable digital audio players (DAPs)** that have poor or inconsistent tag handling (especially regarding Artist vs Album Artist distinctions and multi-disc album display).

It performs two independent normalization steps on MP3, FLAC, and Ogg Vorbis files:

- **Artist tag correction**  
  If an `albumartist` tag exists and differs from the regular `artist` tag, it overwrites the `artist` field with the value from `albumartist`.  
  This helps many DAPs that ignore or mishandle the `albumartist` field and only look at the standard `artist` tag.

- **Multi-disc album title enhancement**  
  For albums identified as multi-disc (files with `discnumber` > 1), if the album title does **not** already contain phrases like “CDx”, “Disc x”, “[x]”, “(x)”, etc., the script appends `CD<discnumber>` to the album title.  
  This prevents tracks from different discs being grouped incorrectly or displayed without disc separation on devices with limited multi-disc support.

For now it supports flac, mp3 and ogg. Open an issue if you need something else.

## Installation and usage

### Using [uv](https://docs.astral.sh/uv/) package manager

```sh
uv tool install https://github.com/akhilman/music-tag-uglifier.git
```

Run `uv tool run music-tag-uglifier -ad /music/directory` to change all tags in /music/directory recursively.

Run `uv tool run music-tag-uglifier --help` to get up to date list of options.

### Using git, venv and pip

Clone this repository and enter to the clone:

```sh
git clone https://github.com/akhilman/music-tag-uglifier.git
cd music-tag-uglifier/
```

Create virtual environment and activate it:

```sh
python3 -m venv .venv
. .venv/bin/activate
```

Install package to virtual environment:

```sh
pip install --editable ./
```

Run the script from virtual environment:

```sh
music-tag-uglifier -ad /music/directory
```

or

```sh
python3 -m music-tag-uglifier -ad /music/directory
```
