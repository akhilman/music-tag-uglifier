from pathlib import Path
import click

import music_tag_uglifier


@click.command(help="Music Tag Normalizer for Portable DAPs.")
@click.option(
    "--set-artist",
    "-a",
    type=click.BOOL,
    is_flag=True,
    help="Copy albumartist tag to artist.",
)
@click.option(
    "--disc-number",
    "-d",
    type=click.BOOL,
    is_flag=True,
    help="Add disc number to album name.",
)
@click.option(
    "--dry-run", "-n", type=click.BOOL, is_flag=True, help="Do not update tags."
)
@click.argument(
    "music_dir",
    type=click.Path(
        exists=True, file_okay=False, dir_okay=True, writable=True, path_type=Path
    ),
    nargs=1,
)
@click.version_option()
def main(music_dir: Path, set_artist: bool, disc_number: bool, dry_run: bool):
    music_tag_uglifier.uglify(
        music_dir,
        set_artist=set_artist,
        album_disk_number=disc_number,
        dry_run=dry_run,
    )


if __name__ == "__main__":
    main()
