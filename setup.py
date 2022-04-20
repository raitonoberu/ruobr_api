#!/usr/bin/env python
# -*- coding: utf-8 -*-
from io import open
from setuptools import setup

__version__ = "2.0.1"
__author__ = "raitonoberu"
__email__ = "raitonoberu@mail.ru"

"""
:authors: raitonoberu
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2021 raitonoberu
"""

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="ruobr_api",
    version=__version__,
    author=__author__,
    author_email=__email__,
    description=(
        "Python модуль для доступа к API электронного дневника "
        "Кемеровской области (cabinet.ruobr.ru API wrapper)"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/raitonoberu/ruobr_api",
    download_url="https://github.com/raitonoberu/ruobr_api/archive/{}.zip".format(
        __version__
    ),
    license="Apache License, Version 2.0, see LICENSE file",
    packages=["ruobr_api"],
    install_requires=["httpx"],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
