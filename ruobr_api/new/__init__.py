# -*- coding: utf-8 -*-
"""
api3d.ruobr.ru
~~~~~~~~~~~~

Библиотека для доступа к новому API электронного дневника.
Пример:

   >>> from ruobr_api.new import Ruobr
   >>> r = Ruobr('username', 'password')
   >>> r.getUser()
   User(id=7694824, user_id=15543421, status='child', first_name='Иван', last_name='Иванов', middle_name='Иванович', birth_date=datetime.date(2004, 10, 10), user_img='https://ruobr.ru/mediac/avatars/123.JPEG', school='69-МБОУ "СОШ №69"', school_terrirtory_id=11, school_is_tourniquet=False, readonly=False, school_is_food=5, group='10А', gps_tracker=False)

:authors: raitonoberu
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2021 raitonoberu
"""

from ruobr_api.new.__main__ import Ruobr, AsyncRuobr

__author__ = "raitonoberu"
__version__ = "1.2.1"
__email__ = "raitonoberu@mail.ru"
