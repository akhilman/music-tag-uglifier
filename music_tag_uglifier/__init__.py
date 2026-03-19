import dataclasses
import pprint
import re
from pathlib import Path
from typing import Iterable, Iterator, List

import mutagen
import tqdm

SUPPORTED_EXTENSIONS = [".mp3", ".ogg", ".flac"]


@dataclasses.dataclass(frozen=True)
class Album:
    artist: str
    album: str


@dataclasses.dataclass(frozen=True)
class AlbumNameAndDiscNumber:
    name: str
    disc: int | None


def find_music(music_dir: Path) -> Iterator[Path]:
    return (
        p
        for p in music_dir.rglob("*")
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def get_first[T](values: Iterable[T] | None) -> T | None:
    if not values:
        return None
    return next(iter(values), None)


def separate_album_name_and_disc_number(album_name: str) -> AlbumNameAndDiscNumber:
    match = re.search(
        r"(?i)(.*?)(?:(?:\s|\s-\s|\s?:\s)\(?\[?(?:cd|disc):?\s*([0-9]+)\]?\)?)?$",
        album_name,
    )
    assert match
    name, disc = match.groups()
    if disc is not None:
        disc = int(disc)
    return AlbumNameAndDiscNumber(name=name, disc=disc)


def get_album(audio: mutagen.FileType) -> Album | None:
    artist = get_first(audio.get("albumartist")) or get_first(audio.get("artist"))
    album = get_first(audio.get("album"))
    if artist and album:
        return Album(artist, separate_album_name_and_disc_number(album).name)
    return None


def get_disc_number(audio: mutagen.FileType) -> int:
    raw_disc_number: List[str] | None = audio.get("discnumber") or None
    disc_number = 1
    if raw_disc_number:
        disc_number = max(int(n.split("/")[0]) for n in raw_disc_number)
    return disc_number


def find_multi_disk_albums(music_files: Iterable[Path]) -> Iterator[Album]:
    last_album = None
    for f in music_files:
        audio = mutagen.File(f, easy=True)
        album = get_album(audio)

        if not album or album == last_album:
            continue

        last_album = album

        if get_disc_number(audio) > 1:
            yield album


def normalise(
    music_file: Path,
    multi_disc_albums: set[Album] = set(),
    dry_run: bool = False,
    set_artist: bool = False,
):
    audio = mutagen.File(music_file, easy=True)
    new_tags = {}
    if set_artist and audio.get("albumartist"):
        if audio.get("artist") != audio.get("albumartist"):
            new_tags["artist"] = audio.get("albumartist")

    if get_album(audio) in multi_disc_albums:
        disk_number = get_disc_number(audio)
        album_names = []
        for name in audio["album"]:
            if separate_album_name_and_disc_number(name).disc is None:
                name = f"{name} CD{disk_number}"
            album_names.append(name)
        if audio["album"] != album_names:
            new_tags["album"] = album_names

    if new_tags:
        if dry_run:
            # TODO: Make better formatting.
            tqdm.tqdm.write(str(music_file))
            tqdm.tqdm.write(pprint.pformat(new_tags))
        else:
            audio.update(new_tags)
            audio.save()


def uglify(
    music_dir: Path,
    dry_run: bool = False,
    set_artist: bool = False,
    album_disk_number: bool = False,
):

    if not set_artist and not album_disk_number:
        print("Nothing to do")
        return

    music_files = list(find_music(music_dir))

    multi_disk_albums: set[Album] = set()
    if album_disk_number:
        multi_disk_albums = set(
            find_multi_disk_albums(
                tqdm.tqdm(music_files, desc="Searching multi-disc albums")
            )
        )

    for f in tqdm.tqdm(music_files, desc="Updating tags"):
        normalise(
            f,
            multi_disc_albums=multi_disk_albums,
            dry_run=dry_run,
            set_artist=set_artist,
        )
