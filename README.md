**Music Tag Normalizer for Portable DAPs**

This tool is designed to make music tags more compatible with **portable digital audio players (DAPs)** that have poor or inconsistent tag handling (especially regarding Artist vs Album Artist distinctions and multi-disc album display).

It performs two independent normalization steps on MP3, FLAC, and Ogg Vorbis files:

- **Artist tag correction**  
  If an `albumartist` tag exists and differs from the regular `artist` tag, it overwrites the `artist` field with the value from `albumartist`.  
  This helps many DAPs that ignore or mishandle the `albumartist` field and only look at the standard `artist` tag.

- **Multi-disc album title enhancement**  
  For albums identified as multi-disc (files with `discnumber` > 1), if the album title does **not** already contain phrases like “CDx”, “Disc x”, “[x]”, “(x)”, etc., the script appends `CD<discnumber>` to the album title.  
  This prevents tracks from different discs being grouped incorrectly or displayed without disc separation on devices with limited multi-disc support.

## Installation
Using [uv](https://docs.astral.sh/uv/)
```
uv tool install https://github.com/akhilman/music-tag-uglifier.git
```

## Usage
Run `music-tag-uglifier --help` to get up to date list of options.
