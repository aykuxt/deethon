# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] - 2021-01-27
### Changed
- The library is now using the unencrypted streaming endpoint (5512f6eb132a2427cad6788f623c97418fbc54d5).
- Updated dependencies

### Removed
- Support for Python 3.7 (fb443c6b6b735f0b37cd5e2dbbf19fdf7271e919)

## [0.4.3] - 2020-07-15
### Added
- Additional tags to the track object and the downloaded tracks (lyrics, copyright, etc.) (880511be8726b80333c67f9280f80b654a7f7106).

### Fixed
- The session on Deezer will not be renewed after the expiration (a82cb4a910d5ab195791d0789a0e6811d2548824).
- The ReplayGain tag had a wrong value (880511be8726b80333c67f9280f80b654a7f7106).

## [0.4.2] - 2020-06-18
### Changed
- Return absolute file path (c6825373bbdc6f4fb0dd3b3dc9e5191d7ac6e1d1).

### Fixed
- Forbidden file name characters on Windows were not escaped
(487393e808b4e6152cb3cf73612451d74a1b8446). 

## [0.4.1] - 2020-06-08
### Added
- Fallback to lower quality if the track cannot be downloaded
(ffe271ee159972ff6969dd9ebccb0b55c0864e12).
- `pytest-cov` in dev-dependencies (56da09d2d385a82c91da0d2011e4cbb7e4244d2d).

### Changed
- Exclude python files from `.editorconfig` as it causes code style errors
(88e7708218e99ed8cd21bacf07fdc9a1cce68371).

### Fixed
- Obsolete type annotations in docstrings (fab7a84a19fc4ce07112d5ff2f046460dd850547).
- Some layout bugs in the documentation.

## [0.4.0] - 2020-06-02
### Added
- API documentation (!9).
- Support for Python 3.7+ (again) (09f16e3cb2ba766ddb0239a39f425bcedf3d9611).
- Raise [`DeezerLoginError`][deethon.errors.DeezerLoginError] when the
specified arl token is invalid. (c5b36935c83194ea3f2b745924c4370f16bc495a)
- More tests (52c29e954ee50721565e1b884fc78992aa92a631).
- `.editorconfig` file (2a9aff181b84717615e46e486b482acf8e083c2e).

### Changed
- Only accept an integer for the ID parameter of the album and track class.
(f33533372d031c677b22c41fec76338c2f6152db)

### Fixed
- Invalid all-object (cbb1e5d38e9e08c3c4a5c71bc8e56fa1bc3ecdb3).
- Useless object inheritance of Album class (05cb61e3fc63a2ef57bd060f28b1264e6f698fc1).
- Code style issues (ab13d39e17bc8a98483a00bed053052f538961f9).
- `__init__` method from base class `Exception` is not called
(094d15a8c7000f94b96accbc583785a16f9d8229).

## [0.3.3] - 2020-05-29
### Added
- Raise [DeezerApiError][deethon.errors.DeezerApiError] when the specified album
is not found (04580121bade63f8079d05142817ebaa8649bee2).
- Stream option for album download (c3168140f5fc5c530fd89b12cedf461af2fef67c).

## [0.3.2] - 2020-05-27
### Fixed
- `ID3NoHeaderError` when tagging MP3 files (5c79b5cc1749e54d0379575ed01ccf02ab10bc21).

## [0.3.1] - 2020-05-27
### Fixed
- The type of total bytes count should be int (0ebfd823514611fcfa28e139cebf4a1ecef9b764).
- Stream the download while decrypting the track (0ebfd823514611fcfa28e139cebf4a1ecef9b764)

## [0.3.0] - 2020-05-27
### Added
- Optional progress callback (29df0e9d3ef7b1cf2fa8c21ba112e23bf786f327)
- More type hints (04e67f4cf3be2e4292843150fc715db5b5841de8).

## [0.2.0] - 2020-05-27
### Added
- Support for album download (276ce7ce595ec000834dd7daf77bf55cfee9d5a7).
- Caching of tracks and albums (c69d8a39446d9fe668bbc4856f86948633a0206e).
- More album cover options (783f8b39e8b84b95ae95d3d805ef4807cdc2ff8e).

### Removed
- Support for Python 3.7 and earlier (3009e5fe5af4426325a2da17e7f9c5ddb3f90fd1).

## [0.1.1] - 2020-05-06
### Changed
- Use regex for the download url (0cf6739460a9ee51256dba9f17ca6d7e83bd2aa7).

### Fixed
- Wrong name of quality variable (399c1eb460a4cd59c9273513ba1fd7a37169a551).

## [0.1.0] - 2020-05-05
### Added
- Initial release! 🎉

[Unreleased]: https://github.com/deethon/deethon/compare/v0.5.0...HEAD
[0.5.0]: https://github.com/deethon/deethon/compare/v0.4.3...v0.5.0
[0.4.3]: https://github.com/deethon/deethon/compare/v0.4.2...v0.4.3
[0.4.2]: https://github.com/deethon/deethon/compare/v0.4.1...v0.4.2
[0.4.1]: https://github.com/deethon/deethon/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/deethon/deethon/compare/v0.3.3...v0.4.0
[0.3.3]: https://github.com/deethon/deethon/compare/v0.3.2...v0.3.3
[0.3.2]: https://github.com/deethon/deethon/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/deethon/deethon/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/deethon/deethon/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/deethon/deethon/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/deethon/deethon/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/deethon/deethon/releases/tag/v0.1.0
