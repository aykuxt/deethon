"""
🎵 Deethon is a Python3 library to easily download music from Deezer and a
wrapper for the Deezer API with some extra features. 🎵
"""

from importlib import metadata

__version__ = metadata.version(__name__)

from . import types, utils, consts, errors, session
from .session import Session
from .types import Album, Track

__all__ = ["Session", "Album", "Track", "errors",
           "utils", "consts", "types", "session"]
