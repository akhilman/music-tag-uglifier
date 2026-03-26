from pathlib import Path
import click

import music_tag_uglifier


@click.command(help="Music Tag Normalizer for Portable DAPs.")
@click.option(
    "--album-artist",
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
def main(
    music_dir: Path,
    dry_run: bool,
    album_artist: bool,
    disc_number: bool,
):
    params = music_tag_uglifier.Params()
    params.album_artist_to_artist = album_artist
    params.disc_to_album = disc_number

    music_tag_uglifier.uglify(
        music_dir,
        params,
        dry_run=dry_run,
    )


if __name__ == "__main__":
    main()
