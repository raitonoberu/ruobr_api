# -*- coding: utf-8 -*-
"""
api3d.ruobr.ru
~~~~~~~~~~~~

Библиотека для доступа к API электронного дневника.
Пример:

   >>> from ruobr_api import Ruobr
   >>> r = Ruobr('username', 'password')
   >>> r.get_user()
   {'status': 'child', 'last_name': 'Зубенко', 'school_terrirtory_id': 1, 'user_img': 'https://ruobr.ru/mediac/avatars/48ba6326740e49d6a3c9ac01fedff9d7.JPEG', 'school_is_tourniquet': 0, 'user_id': 115654529, 'school_is_food': 5, 'school': 'МБОУ "СОШ №69"', 'group': '11А', 'success': True, 'push_settings': {'school_news': 0, 'attendance': 0, 'homework': 0, 'mau_balance': 0, 'tourniquet': 1, 'mark': 1}, 'middle_name': 'Петрович', 'id': 4694228, 'readonly': 0, 'first_name': 'Михаил', 'birth_date': '2004-10-10', 'gps_tracker': False}

:authors: raitonoberu
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2021 raitonoberu
"""

from ruobr_api.__main__ import Ruobr, AsyncRuobr
from ruobr_api.exceptions import (
    AuthenticationException,
    NoChildrenException,
    NoSuccessException,
)

__author__ = "raitonoberu"
__version__ = "2.0.1"
__email__ = "raitonoberu@mail.ru"
