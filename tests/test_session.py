"""This module contains tests for the [session][deethon.session] module."""
from pathlib import Path

import pytest

import deethon


def test_session():
    """
    Test if the [Session][deethon.session.Session] class raises a
    [DeezerLoginError][deethon.types.DeezerLoginError] when an invalid
    arl token is passed.
    """
    with pytest.raises(deethon.errors.DeezerLoginError):
        session = deethon.Session('wrongarltoken')
        session._refresh_session()


def test_download():
    """Test if the download method returns a Path object."""
    deezer = deethon.Session(
        '38975b6cb1831c523d8163adac2aadb847f86aff1643ba0e6edb87d93658fd6bc12b313b328165c6f9091c969baef5f5f46381c3f2f59b443a9b906221a77eaa98c95598cf7692a9e695350f847b60dd1affff14145c15a3542de8186b74943f')
    assert isinstance(
        deezer.download('https://www.deezer.com/track/2104162', 'MP3_320'), Path)
    assert isinstance(
        deezer.download('https://www.deezer.com/track/2104162'), Path)

    with pytest.raises(deethon.errors.InvalidUrlError):
        deezer.download('https://www.google.com')

    with pytest.raises(deethon.errors.ActionNotSupported):
        deezer.download('https://www.deezer.com/unsuppoted/123456')

    with pytest.raises(deethon.errors.DownloadError):
        deezer.download('https://www.deezer.com/track/101399924')
