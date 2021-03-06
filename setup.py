#!/usr/bin/env python
# -*- coding: utf-8 -*-
from io import open
from setuptools import setup

"""
:authors: raitonoberu
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2021 raitonoberu
"""


version = "1.1.1"

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="ruobr_api",
    version=version,
    author="raitonoberu",
    author_email="raitonoberu@mail.ru",
    description=(
        u"Python модуль для доступа к API электронного дневника "
        u"Кемеровской области (cabinet.ruobr.ru API wrapper)"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/raitonoberu/ruobr_api",
    download_url="https://github.com/raitonoberu/ruobr_api/archive/v{}.zip".format(
        version
    ),
    license="Apache License, Version 2.0, see LICENSE file",
    packages=["ruobr_api"],
    install_requires=["httpx", "pydantic"],
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
