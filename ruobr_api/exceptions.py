# -*- coding: utf-8 -*-
"""
:authors: raitonoberu
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2021 raitonoberu
"""


class AuthenticationException(Exception):
    def __init__(self, text):
        self.text = text


class NoChildrenException(Exception):
    def __init__(self, text):
        self.text = text


class NoSuccessException(Exception):
    def __init__(self, text):
        self.text = text
