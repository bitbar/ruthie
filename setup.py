#!/usr/bin/env python3

"""The setup file."""


from setuptools import setup, find_packages
from ruthie import __version__


setup(
    name='ruthie',
    version=__version__,
    description='Run Unit Tests Harmoniously Incredibly Easy',
    url='https://github.com/bitbar/ruthie',
    install_requires=['docopt'],
    packages=find_packages(),
    entry_points={
        'console_scripts': ['ruthie=ruthie.cli:main'],
    }
)
