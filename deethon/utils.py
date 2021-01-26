"""
The utils module contains several useful functions that are used within the package.
"""

from __future__ import annotations

import hashlib
from binascii import b2a_hex
from pathlib import Path
from typing import TYPE_CHECKING

from Crypto.Cipher import AES
from mutagen.flac import FLAC, Picture
from mutagen.id3 import ID3, Frames

if TYPE_CHECKING:
    from .types import Track


def md5hex(data: bytes) -> bytes:
    return hashlib.md5(data).hexdigest().encode()


def get_quality(bitrate: str) -> str:
    if bitrate == "FLAC":
        return "9"
    if bitrate == "MP3_320":
        return "3"
    if bitrate == "MP3_256":
        return "5"
    return "1"


def get_file_path(track: Track, ext: str) -> Path:
    """
    Generate a file path using a Track object.

    Args:
        track: A Track object.
        ext: The file extension to be used.

    Returns:
        A Path object containing the track path.
    """
    forbidden_chars = dict((ord(char), None) for char in r'\/*?:"<>|')
    album_artist = track.album.artist.translate(forbidden_chars)
    album_title = track.album.title.translate(forbidden_chars)

    std_dir = "Songs"
    dir_path = Path(std_dir, album_artist, album_title)
    dir_path.mkdir(parents=True, exist_ok=True)
    file_name = f"{track.number:02} {track.title}{ext}"
    return dir_path / file_name.translate(forbidden_chars)


def get_stream_url(track: Track, quality: str) -> str:
    """
    Get the direct download url for the encrypted track.

    Args:
        track: A [Track][deethon.types.Track] instance.
        quality: The preferred quality.

    Returns:
        The direct download url.
    """
    data = b"\xa4".join(
        a.encode() for a in [track.md5_origin, quality,
                             str(track.id), track.media_version]
    )
    data = b"\xa4".join([md5hex(data), data]) + b"\xa4"
    if len(data) % 16:
        data += b"\x00" * (16 - len(data) % 16)
    c = AES.new("jo6aey6haid2Teih".encode(), AES.MODE_ECB)
    hashs = b2a_hex(c.encrypt(data)).decode()
    return f"http://e-cdn-proxy-{track.md5_origin[0]}.dzcdn.net/api/1/{hashs}"


def tag(file_path: Path, track: Track) -> None:
    """
    Tag the music file at the given file path using the specified
    [Track][deethon.types.Track] instance.

    Args:
        file_path (Path): The music file to be tagged
        track: The [Track][deethon.types.Track] instance to be used for tagging.
    """
    ext = file_path.suffix

    if ext == ".mp3":
        tags = ID3()
        tags.clear()

        tags.add(Frames["TALB"](encoding=3, text=track.album.title))
        tags.add(Frames["TBPM"](encoding=3, text=str(track.bpm)))
        tags.add(Frames["TCON"](encoding=3, text=track.album.genres))
        tags.add(Frames["TCOP"](encoding=3, text=track.copyright))
        tags.add(Frames["TDAT"](encoding=3,
                                text=track.release_date.strftime("%d%m")))
        tags.add(Frames["TIT2"](encoding=3, text=track.title))
        tags.add(Frames["TPE1"](encoding=3, text=track.artist))
        tags.add(Frames["TPE2"](encoding=3, text=track.album.artist))
        tags.add(Frames["TPOS"](encoding=3, text=str(track.disk_number)))
        tags.add(Frames["TPUB"](encoding=3, text=track.album.label))
        tags.add(Frames["TRCK"](encoding=3,
                                text=f"{track.number}/{track.album.total_tracks}"))
        tags.add(Frames["TSRC"](encoding=3, text=track.isrc))
        tags.add(Frames["TYER"](encoding=3, text=str(track.release_date.year)))

        tags.add(Frames["TXXX"](encoding=3,
                                desc="replaygain_track_gain",
                                text=str(track.replaygain_track_gain)))

        if track.lyrics:
            tags.add(Frames["USLT"](encoding=3,
                                    text=track.lyrics))

        tags.add(Frames["APIC"](encoding=3,
                                mime="image/jpeg",
                                type=3,
                                desc="Cover",
                                data=track.album.cover_xl))

        tags.save(file_path, v2_version=3)

    else:
        tags = FLAC(file_path)
        tags.clear()
        tags["album"] = track.album.title
        tags["albumartist"] = track.album.artist
        tags["artist"] = track.artist
        tags["bpm"] = str(track.bpm)
        tags["copyright"] = track.copyright
        tags["date"] = track.release_date.strftime("%Y-%m-%d")
        tags["genre"] = track.album.genres
        tags["isrc"] = track.isrc
        if track.lyrics:
            tags["lyrics"] = track.lyrics
        tags["replaygain_track_gain"] = str(track.replaygain_track_gain)
        tags["title"] = track.title
        tags["tracknumber"] = str(track.number)
        tags["year"] = str(track.release_date.year)

        cover = Picture()
        cover.type = 3
        cover.data = track.album.cover_xl
        cover.width = 1000
        cover.height = 1000
        tags.clear_pictures()
        tags.add_picture(cover)
        tags.save(deleteid3=True)
