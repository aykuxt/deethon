"""This module contains the Session class."""
import time
import re
from pathlib import Path
from typing import Union, Generator, Any, Tuple, Optional, Callable

import requests

from . import errors, consts, utils, types


class Session:
    """A session is required to connect to Deezer's unofficial API."""

    def __init__(self, arl_token: str):
        """
        Creates a new Deezer session instance.

        Args:
            arl_token (str): The arl token is used to make API requests
                on Deezer's unofficial API

        Raises:
            DeezerLoginError: The specified arl token is not valid.
        """
        self._arl_token: str = arl_token
        self._req = requests.Session()
        self._req.cookies["arl"] = self._arl_token
        self._csrf_token = ""
        self._session_expires = 0

    def _refresh_session(self) -> None:
        user = self.get_api(consts.METHOD_GET_USER)
        if user["USER"]["USER_ID"] == 0:
            raise errors.DeezerLoginError
        self._csrf_token = user["checkForm"]
        self._session_expires = time.time() + 3600

    def get_api(self, method: str, json: dict = None) -> dict:
        if not method == consts.METHOD_GET_USER and \
                (not self._csrf_token or self._session_expires > time.time()):
            self._refresh_session()

        params = {
            "api_version": "1.0",
            "api_token": self._csrf_token,
            "input": "3",
            "method": method,
        }
        return self._req.post(
            consts.API_URL,
            params=params,
            json=json
        ).json()["results"]

    def download(self,
                 url: str,
                 bitrate: str = "FLAC",
                 progress_callback: Optional[Callable] = None):
        """
        Downloads the given Deezer url if possible.

        Args:
            url: The URL of the track or album to download.
            bitrate: The preferred bitrate to download
                (`FLAC`, `MP3_320`, `MP3_256`, `MP3_128`).
            progress_callback (callable): A callable that accepts
                `current` and `bytes` arguments.

        Raises:
            ActionNotSupported: The specified URL is not (yet)
                supported for download.
            InvalidUrlError: The specified URL is not a valid deezer link.
        """
        match = re.match(
            r"https?://(?:www\.)?deezer\.com/(?:\w+/)?(\w+)/(\d+)", url)
        if match:
            mode = match.group(1)
            content_id = int(match.group(2))
            if mode == "track":
                return self.download_track(types.Track(content_id), bitrate,
                                           progress_callback)
            if mode == "album":
                return self.download_album(types.Album(content_id), bitrate)
            raise errors.ActionNotSupported(mode)
        raise errors.InvalidUrlError(url)

    def download_track(self,
                       track: types.Track,
                       bitrate: str = "FLAC",
                       progress_callback: Optional[Callable] = None) -> Path:
        """
        Downloads the given [Track][deethon.types.Track] object.

        Args:
            track: A [Track][deethon.types.Track] instance.
            bitrate: The preferred bitrate to download
                (`FLAC`, `MP3_320`, `MP3_256`, `MP3_128`).
            progress_callback: A callable that accepts
                `current` and `bytes` arguments.

        Returns:
            The file path of the downloaded track.

        Raises:
            DownloadError: The track is not downloadable.
        """
        track.add_more_tags(self)
        quality = utils.get_quality(bitrate)
        download_url = utils.get_stream_url(track, quality)
        res = self._req.get(download_url, stream=True)

        total = int(res.headers["Content-Length"])
        if not total:
            if bitrate == "FLAC":
                fallback_bitrate = "MP3_320"
            elif bitrate == "MP3_320":
                fallback_bitrate = "MP3_256"
            elif bitrate == "MP3_256":
                fallback_bitrate = "MP3_128"
            else:
                raise errors.DownloadError(track.id)
            return self.download_track(track, fallback_bitrate, progress_callback)
        current = 0

        ext = ".flac" if quality == "9" else ".mp3"
        file_path = utils.get_file_path(track, ext)

        with file_path.open("wb") as f:
            for data in res.iter_content(4096):
                current += len(data)
                f.write(data)
                if progress_callback:
                    progress_callback(current, total)

        utils.tag(file_path, track)

        return file_path.absolute()

    def download_album(
            self,
            album: types.Album,
            bitrate: str = None,
            stream: bool = False
    ) -> Union[Generator[Path, Any, None], Tuple[Path, ...]]:
        """
        Downloads an album from Deezer using the specified Album object.

        Args:
            album: An [Album][deethon.types.Album] instance.
            bitrate: The preferred bitrate to download
                (`FLAC`, `MP3_320`, `MP3_256`, `MP3_128`).
            stream: If `true`, this method returns a generator object,
                otherwise the downloaded files are returned as a tuple
                that contains the file paths.

        Returns:
            The file paths.
        """
        tracks = (self.download_track(track, bitrate)
                  for track in album.tracks)
        if stream:
            return tracks
        return tuple(tracks)
