import hashlib
from binascii import a2b_hex, b2a_hex
from pathlib import Path

from Crypto.Cipher import AES, Blowfish


def md5hex(data: bytes) -> bytes:
    hashed = hashlib.md5(data).hexdigest().encode()
    return hashed


def get_quality(bitrate: str) -> str:
    if bitrate == "FLAC":
        return "9"
    elif bitrate == "MP3_320":
        return "3"
    elif bitrate == "MP3_256":
        return "5"
    elif bitrate == "MP3_128":
        return "1"


def get_file_path(track, ext) -> Path:
    std_dir = "Songs/"
    dir_path = Path(f"{std_dir}{track.album.artist}/{track.album.title}")
    dir_path.mkdir(parents=True, exist_ok=True)
    file_name = f"{track.number} - {track.title}{ext}"
    return dir_path / file_name


def get_stream_url(md5: str, quality: str, track_id: int, media) -> str:
    data = b"\xa4".join(a.encode() for a in [md5, quality, str(track_id), str(media)])
    data = b"\xa4".join([md5hex(data), data]) + b"\xa4"
    if len(data) % 16:
        data += b"\x00" * (16 - len(data) % 16)
    c = AES.new("jo6aey6haid2Teih".encode(), AES.MODE_ECB)
    hashs = b2a_hex(c.encrypt(data)).decode()
    return f"https://e-cdns-proxy-{md5[0]}.dzcdn.net/mobile/1/{hashs}"


def decrypt_file(crypt, trackid: int, output: Path) -> None:
    h = md5hex(str(trackid).encode())
    key = "".join(chr(h[i] ^ h[i + 16] ^ b"g4el58wc0zvf9na1"[i]) for i in range(16))
    seg = 0
    with output.open("wb") as f:
        for data in crypt:
            if not data:
                break
            if (seg % 3) == 0 and len(data) == 2048:
                data = Blowfish.new(key.encode(), Blowfish.MODE_CBC,
                                    a2b_hex("0001020304050607")).decrypt(data)
            f.write(data)
            seg += 1