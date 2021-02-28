# -*- coding: utf-8 -*-
"""
ruobr.ru/api
~~~~~~~~~~~~

Библиотека для доступа к API электронного дневника.
Пример:

   >>> from ruobr_api import Ruobr
   >>> r = Ruobr('username', 'password')
   >>> r.getUser()
   User(id=7592904, status='child', first_name='Иван', last_name='Иванов', middle_name='Иванович', school='69-МБОУ "СОШ №69"', school_is_tourniquet=False, readonly=False, school_is_food=True, group='10А', gps_tracker=False)

:authors: raitonoberu
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2021 raitonoberu
"""

from .__main__ import (
    Ruobr,
    AsyncRuobr,
    NotAuthorizedException,
    AuthenticationException,
    NoSuccessException,
    NoChildrenException,
)

__author__ = "raitonoberu"
__version__ = "1.0.2"
__email__ = "raitonoberu@mail.ru"
