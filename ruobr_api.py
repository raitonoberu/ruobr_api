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

:license: Apache 2.0, see LICENSE for more details.
"""

import requests
import base64
from datetime import datetime


class Ruobr(object):
    class AuthError(Exception):
        def __init__(self, text):
            self.text = text

    class noSuccess(Exception):
        def __init__(self, text):
            self.text = text

    def __init__(self, username, password):
        # Логин и пароль должны быть закодированы в base64
        self.username = base64.b64encode(
            username.upper().encode("UTF-8")).decode("UTF-8")
        self.password = base64.b64encode(
            password.encode("UTF-8")).decode("UTF-8")
        self.isApplicant = False  # Является ли профиль родительским
        self.child = 0  # Номер ребёнка, если профиль родительский

        self.getUser()

    def get(self, target):
        """Метод для получения данных"""
        response = requests.get(
            f'https://ruobr.ru/api/{target}',
            headers={"password": self.password, "username": self.username},
        )
        response = response.json()
        if isinstance(response, dict):  # В случае ошибки возвращается словарь
            if "success" in response.keys():
                if not(response['success']):
                    if "error" in response.keys():
                        raise Ruobr.noSuccess(response['error'])
                    if "error_type" in response.keys():
                        if response['error_type'] == "auth":
                            raise Ruobr.AuthError(
                                "Проверьте логин и/или пароль")
                        raise Ruobr.noSuccess(response['error_type'])
                    raise Ruobr.noSuccess(response)
        return response

    def getUser(self):
        """Возвращает информацию об ученике
        Если профиль родительский, используйте метод Ruobr.setChild() для выбора ребёнка

        {'status': 'child', 'first_name': 'first_name', 'last_name': 'last_name', 'middle_name': 'middle_name', 'school': 'school', 'school_is_tourniquet': False, 'readonly': False, 'school_is_food': True, 'group': 'group', 'id': 9999999, 'gps_tracker': False}"""
        user = self.get("user/")
        if user['status'] == "applicant":
            self.isApplicant = True
            user = user['childs'][self.child]
        self.user = user
        return user

    def getChildren(self):
        """Возвращает список детей текущего аккаунта (для обработки родительских профилей)

        [{'first_name': 'first_name1', 'last_name': 'last_name1', 'middle_name': 'middle_name1', 'school': 'school1', 'school_is_tourniquet': False, 'school_is_food': True, 'group': 'group1', 'id': 9999999, 'readonly': False}, ...]"""
        user = self.get("user/")
        if user['status'] == "applicant":
            self.isApplicant = True
            user = user['childs']
        else:
            user = [user]
        return user

    def setChild(self, id):
        """Установить номер ребёнка, если профиль родительский"""
        self.child = id
        self.getUser()


    def getMail(self):
        """Возвращает почту

        [{'post_date': '2020-04-26 22:36:11', 'author': 'Author', 'read': True, 'text': 'text', 'clean_text': 'clean_text', 'id': 7777777, 'subject': 'TITLE'}, ...]"""
        return self.get("mail/")['messages']

    def getControlmark(self):
        """Возвращает итоговые оценки

        [{'marks': {'Subject': 'Mark', ...}, 'rom': 'I', 'period': 1, 'title': '1-я четверть'}, ...]"""
        return self.get(f"controlmark/?child={self.user['id']}")

    def getTimetable(self, start, end):
        """Возвращает дневник целиком
        Пример даты: '2020-04-27'

        [{'topic': (опц)'Topic', 'task': (опц){'title': 'Task_title', 'doc': False, 'requires_solutions': False, 'deadline': '2020-04-24', 'test_id': None, 'type': 'group', 'id': 99999999}, 'time_start': '08:30:00', 'date': '2020-04-24', 'id': 175197390, 'subject': 'Subject', 'time_end': '09:15:00', 'staff': 'Teacher's Name}, ...]"""
        return self.get(f"timetable/?start={start}&end={end}&child={self.user['id']}")['lessons']

    def getHomework(self, start, end):
        """Возвращает список домашнего задания (выборка из дневника)
        Пример даты: '2020-04-27'

        [{'topic': (опц)'Topic', 'task': {'title': 'Task_title', 'doc': False, 'requires_solutions': False, 'deadline': '2020-04-24', 'test_id': None, 'type': 'group', 'id': 99999999}, 'time_start': '08:30:00', 'date': '2020-04-24', 'id': 175197390, 'subject': 'Subject', 'time_end': '09:15:00', 'staff': 'Teacher's Name}, ...]"""
        timetable = self.getTimetable(start, end)
        homework = []
        for lesssion in timetable:
            if "task" in lesssion.keys():
                homework.append(lesssion)

        return homework

    def getProgerss(self, date=None):
        """Возвращает статистику ученика (дата - обычно сегодня)
        Пример даты: '2020-04-27'

        {'period_name': '4-я четверть', 'place_count': 23, 'subjects': [{'place_count': 17, 'place': 3, 'group_avg': 3.69, 'child_avg': 4.29, 'parallels_avg': 3.56, 'subject': 'Русский язык'}, ...], 'place': 7, 'group_avg': 4.05, 'child_avg': 4.28, 'parallels_avg': 3.84}"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        return self.get(f"progress/?child={self.user['id']}&date={date}")

    def getMark(self, start, end):
        """Возвращает оценки по дням
        Пример даты: '2020-04-27'

        {'Русский язык': [{'question_name': 'Ответ на уроке', 'question_id': 104552170, 'number': 1, 'question_type': 'Ответ на уроке', 'mark': '4'}, ...], ...}"""

        return self.get(f"mark/?child={self.user['id']}&start={start}&end={end}")['subjects']

    def getFoodInfo(self):
        """Возвращает информацию о счёте питания

        {'subsidy': 0, 'account': 999999999, 'total_take_off': 372423, 'total_add': 363000, 'balance_on_start_year': 17113, 'balance': 7690, 'default_complex': 'default_complex'}"""
        return self.get(f"food/?child={self.user['id']}")['account']

    '''
    def getFoodComplex(self):
        """Судя по всему, это получение списка комплексов, но сейчас это не работает

        []"""
        return self.get(f"food/complex/?child={self.user['id']}")['complex_list']
    '''

    def getFoodHistory(self, start=None, end=None):
        """Возвращает историю питания (обыычно start - первый день года, end - последний)
        Пример даты: '2020-04-27'

        [{'date': '2020-01-13', 'state': 30, 'complex__code': 'А', 'complex__uid': 'dacd83e5-2dd6-11e8-a63a-00155d039800', 'state_str': 'Заказ подтверждён', 'complex__name': 'Альтернативно-молочный', 'id': 63217607}, ...]"""
        if start is None and end is None:
            year = datetime.now().year
            start = f"{year}-01-01"
            end = f"{year}-12-31"
        return self.get(f"food/history/?child={self.user['id']}&end={end}&start={start}")['events']
