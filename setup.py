try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Premiere Pro Extract File Names',
    'author': 'Frank Giraffe',
    'url': 'https://github.com/fgiraffe/pp_parse',
    'download_url': 'https://github.com/fgiraffe/pp_parse',
    'author_email': 'fgiraffe@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['NAME'],
    'scripts': [],
    'name': 'pp_parse'
}

setup(**config)
