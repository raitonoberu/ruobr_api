# -*- coding: utf-8 -*-
"""
ruobr.ru/api
~~~~~~~~~~~~

Библиотека для доступа к API электронного дневника.
Пример:

   >>> from ruobr_api import Ruobr
   >>> r = Ruobr('username', 'password')
   >>> r.getUser()
   {'status': 'child', 'first_name': 'Иванов', 'last_name': 'Иван', 'middle_name': 'Иванович', 'school': 'Школа 1', 'school_is_tourniquet': False, 'readonly': False, 'school_is_food': True, 'group': '9В', 'id': 9999999, 'gps_tracker': False}

:authors: raitonoberu
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2020 raitonoberu
"""

from .ruobr_api import (
    Ruobr,
    AsyncRuobr,
    AuthenticationException,
    NoSuccessException,
)

__author__ = "raitonoberu"
__version__ = "1.0.2"
__email__ = "raitonoberu@mail.ru"
