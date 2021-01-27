# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deethon']

package_data = \
{'': ['*']}

install_requires = \
['mutagen>=1.45.0,<2.0.0',
 'pycryptodome>=3.9.9,<4.0.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'deethon',
    'version': '0.5.0',
    'description': 'Python3 library to easily download music from Deezer',
    'long_description': '# Deethon\n\n[![Codacy Badge](https://app.codacy.com/project/badge/Grade/3a54b30586b941acb82079d0252e0320)](https://www.codacy.com/gh/deethon/deethon?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=deethon/deethon&amp;utm_campaign=Badge_Grade)\n[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/3a54b30586b941acb82079d0252e0320)](https://www.codacy.com/gh/deethon/deethon?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=deethon/deethon&amp;utm_campaign=Badge_Coverage)\n[![PyPI](https://img.shields.io/pypi/v/deethon)](https://pypi.org/project/deethon/)\n![PyPI - Status](https://img.shields.io/pypi/status/deethon)\n[![PyPI - Downloads](https://img.shields.io/pypi/dm/deethon)](https://pypi.org/project/deethon/)\n[![GitHub license](https://img.shields.io/github/license/deethon/deethon)](https://github.com/deethon/deethon/blob/master/LICENSE)\n\nDeethon is a lightweight Python library for downloading high quality music from Deezer.\n\n## Getting started\n\n### Installation\n\n```sh\npip install deethon\n```\n\n### Usage\n\n```python\nimport deethon\n\ndeezer = deethon.Session("YOUR ARL TOKEN")\n\ndeezer.download(\n    "https://www.deezer.com/track/1234567",\n    bitrate="FLAC"  # or MP3_320 / MP3_256 / MP3_128 (optional)\n)\n```\n',
    'author': 'Aykut Yilmaz',
    'author_email': 'aykuxt@gmail.com',
    'maintainer': 'Aykut Yilmaz',
    'maintainer_email': 'aykuxt@gmail.com',
    'url': 'https://github.com/deethon/deethon',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
