# -*- coding: utf-8 -*-
"""
:authors: raitonoberu
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2021 raitonoberu
"""
from . import models
import httpx
import base64
from datetime import datetime, date
from typing import Dict, List, Union


class AuthenticationException(Exception):
    def __init__(self, text):
        self.text = text


class NoSuccessException(Exception):
    def __init__(self, text):
        self.text = text


class NoChildrenException(Exception):
    def __init__(self, text):
        self.text = text


class Ruobr(object):
    """Класс для доступа к API электронного дневника"""

    def __init__(self, username: str, password: str, raw_data: bool = False):
        # Логин и пароль должны быть закодированы в base64
        self.username = base64.b64encode(username.upper().encode("UTF-8")).decode(
            "UTF-8"
        )
        self.password = base64.b64encode(password.encode("UTF-8")).decode("UTF-8")
        self.raw_data = raw_data

        self.isApplicant = None  # Является ли профиль родительским
        self.isAuthorized = False  # Авторизован ли профиль
        self.isEmpty = None  # Является ли профиль пустым (без детей)
        self.child = 0  # Номер ребёнка, если профиль родительский
        self._children = None

    def _check_authorized(self):
        if not self.isAuthorized:
            self.getUser()

    def _check_empty(self):
        if self.isEmpty:
            raise NoChildrenException("На аккаунте нет детей")

    @property
    def user(self) -> Union[models.User, dict]:
        if self.isAuthorized and not self.isEmpty:
            return self._children[self.child]
        return None

    def _get(self, target: str) -> dict:
        """Метод для получения данных"""

        response = httpx.get(
            f"https://ruobr.ru/api/{target}",
            headers={"password": self.password, "username": self.username},
        )
        try:
            response = response.json()
        except:
            raise NoSuccessException(response.text)
        if isinstance(response, dict):  # В случае ошибки возвращается словарь
            if "success" in response.keys():
                if not (response["success"]):
                    if "error" in response.keys():
                        raise NoSuccessException(response["error"])
                    if "error_type" in response.keys():
                        if response["error_type"] == "auth":
                            raise AuthenticationException(
                                "Проверьте логин и/или пароль"
                            )
                        raise NoSuccessException(response["error_type"])
                    raise NoSuccessException(response)
        return response

    def getUser(self) -> Union[models.User, dict]:
        """Авторизует и возвращает информацию об ученике
        После авторизации информация доступна в свойстве user
        Если профиль родительский, используйте метод setChild() для выбора ребёнка

        {'status': 'child', 'first_name': 'first_name', 'last_name': 'last_name', 'middle_name': 'middle_name', 'school': 'school', 'school_is_tourniquet': False, 'readonly': False, 'school_is_food': True, 'group': 'group', 'id': 9999999, 'gps_tracker': False}"""

        if self.user is not None:
            return self.user

        user = self._get("user/")
        if user["status"] == "applicant":
            self.isApplicant = True
            if self.raw_data:
                self._children = user["childs"]
            else:
                self._children = []
                for child in user["childs"]:
                    self._children.append(
                        models.User(
                            **child, status="applicant", gps_tracker=user["gps_tracker"]
                        )
                    )
        else:
            self.isApplicant = False
            if self.raw_data:
                self._children = [user]
            else:
                self._children = [models.User(**user)]

        self.isAuthorized = True
        self.isEmpty = len(self._children) == 0

        return self.user

    def getChildren(self) -> List[Union[models.User, dict]]:
        """Возвращает список детей текущего аккаунта (для обработки родительских аккаунтов)

        [{'first_name': 'first_name1', 'last_name': 'last_name1', 'middle_name': 'middle_name1', 'school': 'school1', 'school_is_tourniquet': False, 'school_is_food': True, 'group': 'group1', 'id': 9999999, 'readonly': False}, ...]"""

        self._check_authorized()

        return self._children

    def setChild(self, id: int) -> None:
        """Установить номер ребёнка (для обработки родительских аккаунтов)"""

        self.child = id

    def getMail(self) -> List[Union[models.Message, dict]]:
        """Возвращает почту

        [{'post_date': '2020-04-26 22:36:11', 'author': 'Author', 'read': True, 'text': 'text', 'clean_text': 'clean_text', 'id': 7777777, 'subject': 'TITLE'}, ...]"""

        self._check_authorized()

        result = self._get("mail/")["messages"]
        if self.raw_data:
            return result
        return [models.Message(**i) for i in result]

    def readMessage(self, id: Union[int, str]) -> None:
        """Помечает сообщение как прочитанное"""

        self._check_authorized()

        self._get(f"mail/read/?message={id}")

    def getControlmarks(self) -> List[Union[models.ControlmarksPeriod, dict]]:
        """Возвращает итоговые оценки

        [{'marks': {'Subject': 'Mark', ...}, 'rom': 'I', 'period': 1, 'title': '1-я четверть'}, ...]"""

        self._check_authorized()
        self._check_empty()

        result = self._get(f"controlmark/?child={self.user['id']}")
        if self.raw_data:
            return result
        return [models.ControlmarksPeriod(**i) for i in result]

    def getTimetable(
        self, start: Union[str, date, datetime], end: Union[str, date, datetime]
    ) -> List[Union[models.Lesson, dict]]:
        """Возвращает дневник целиком
        Пример даты: '2020-04-27'

        [{'topic': (опц)'Topic', 'task': (опц){'title': 'Task_title', 'doc': False, 'requires_solutions': False, 'deadline': '2020-04-24', 'test_id': None, 'type': 'group', 'id': 99999999}, 'time_start': '08:30:00', 'date': '2020-04-24', 'id': 175197390, 'subject': 'Subject', 'time_end': '09:15:00', 'staff': 'Teachers Name'}, ...]"""

        self._check_authorized()
        self._check_empty()

        if isinstance(start, (date, datetime)):
            start = start.strftime("%Y-%m-%d")
        if isinstance(end, (date, datetime)):
            end = end.strftime("%Y-%m-%d")

        result = self._get(
            f"timetable/?start={start}&end={end}&child={self.user['id']}"
        )["lessons"]
        if self.raw_data:
            return result
        return [models.Lesson(**i) for i in result]

    def getHomework(
        self, start: Union[str, date, datetime], end: Union[str, date, datetime]
    ) -> List[Union[models.Lesson, dict]]:
        """Возвращает список домашних заданий (выборка из дневника)
        Пример даты: '2020-04-27'

        [{'topic': (опц)'Topic', 'task': {'title': 'Task_title', 'doc': False, 'requires_solutions': False, 'deadline': '2020-04-24', 'test_id': None, 'type': 'group', 'id': 99999999}, 'time_start': '08:30:00', 'date': '2020-04-24', 'id': 175197390, 'subject': 'Subject', 'time_end': '09:15:00', 'staff': 'Teacher's Name}, ...]"""

        timetable = self.getTimetable(start, end)
        homework = [i for i in timetable if i["task"] is not None]

        return homework

    def getProgress(
        self, _date: Union[str, date, datetime] = datetime.now()
    ) -> Union[models.Progress, dict]:
        """Возвращает статистику ученика (дата - обычно сегодня)
        Пример даты: '2020-04-27'

        {'period_name': '4-я четверть', 'place_count': 23, 'subjects': [{'place_count': 17, 'place': 3, 'group_avg': 3.69, 'child_avg': 4.29, 'parallels_avg': 3.56, 'subject': 'Русский язык'}, ...], 'place': 7, 'group_avg': 4.05, 'child_avg': 4.28, 'parallels_avg': 3.84}"""

        self._check_authorized()
        self._check_empty()

        if isinstance(_date, (date, datetime)):
            _date = _date.strftime("%Y-%m-%d")

        result = self._get(f"progress/?child={self.user['id']}&date={_date}")
        if self.raw_data:
            return result
        return models.Progress(**result)

    def getMarks(
        self, start: Union[str, date, datetime], end: Union[str, date, datetime]
    ) -> Dict[str, List[Union[models.Mark, dict]]]:
        """Возвращает оценки за указанный период
        Пример даты: '2020-04-27'

        {'Русский язык': [{'question_name': 'Ответ на уроке', 'question_id': 104552170, 'number': 1, 'question_type': 'Ответ на уроке', 'mark': '4'}, ...], ...}"""

        self._check_authorized()
        self._check_empty()

        if isinstance(start, (date, datetime)):
            start = start.strftime("%Y-%m-%d")
        if isinstance(end, (date, datetime)):
            end = end.strftime("%Y-%m-%d")
        marks = self._get(f"mark/?child={self.user['id']}&start={start}&end={end}")[
            "subjects"
        ]
        if self.raw_data:
            return marks
        for key, value in marks.items():
            marks[key] = [models.Mark(**i) for i in value]
        return marks

    def getAttendance(
        self, start: Union[str, date, datetime], end: Union[str, date, datetime]
    ) -> Dict[str, List[str]]:
        """Возвращает пропуски за указанный период
        Пример даты: '2020-04-27'

        {'Русский язык': ['УП', 'Н', ...], ...}"""

        self._check_authorized()
        self._check_empty()

        if isinstance(start, (date, datetime)):
            start = start.strftime("%Y-%m-%d")
        if isinstance(end, (date, datetime)):
            end = end.strftime("%Y-%m-%d")
        return self._get(
            f"attendance/?child={self.user['id']}&start={start}&end={end}"
        )["subjects"]

    def getFoodInfo(self) -> Union[models.FoodInfo, dict]:
        """Возвращает информацию о счёте питания

        {'subsidy': 0, 'account': 999999999, 'total_take_off': 372423, 'total_add': 363000, 'balance_on_start_year': 17113, 'balance': 7690, 'default_complex': 'default_complex'}"""

        self._check_authorized()
        self._check_empty()

        result = self._get(f"food/?child={self.user['id']}")["account"]
        if self.raw_data:
            return result
        return models.FoodInfo(**result)

    def getFoodHistory(
        self,
        start: Union[str, date, datetime] = None,
        end: Union[str, date, datetime] = None,
    ) -> List[Union[models.FoodHistoryDay, dict]]:
        """Возвращает историю питания (обычно start - первый день года, end - последний)
        Пример даты: '2020-04-27'

        [{'date': '2020-01-13', 'state': 30, 'complex__code': 'А', 'complex__uid': 'dacd83e5-2dd6-11e8-a63a-00155d039800', 'state_str': 'Заказ подтверждён', 'complex__name': 'Альтернативно-молочный', 'id': 63217607}, ...]"""

        self._check_authorized()
        self._check_empty()

        if start is None or end is None:
            now = datetime.now()
            if start is None:
                start = datetime(now.year, 1, 1)
            if end is None:
                end = datetime(now.year, 12, 31)

        if isinstance(start, (date, datetime)):
            start = start.strftime("%Y-%m-%d")
        if isinstance(end, (date, datetime)):
            end = end.strftime("%Y-%m-%d")

        result = self._get(
            f"food/history/?child={self.user['id']}&end={end}&start={start}"
        )["events"]
        if self.raw_data:
            return result
        return [models.FoodHistoryDay(**i) for i in result]

    def getNews(self) -> List[Union[models.NewsItem, dict]]:
        """Возвращает новости

        [{'title': 'title', 'clean_text': 'text without html tags', 'author': 'author', 'school_name': 'school num 1', 'school_id': 10, 'text': '<p>text</p>', 'date': '2020-11-03', 'pub_date': '2020-11-03 15:50:270', 'id': 100001}...]"""

        self._check_authorized()

        result = self._get("news/")
        if self.raw_data:
            return result
        return [models.NewsItem(**i) for i in result]

    @staticmethod
    def getHomeworkById(id: Union[int, str], type: str = "group") -> str:
        """Возвращает ссылку на страницу с подробной информацией о домашнем задании.
        Не требует авторизации"""

        return f"https://ruobr.ru/api/homework/?homework={id}&type={type}"


class AsyncRuobr(Ruobr):
    async def _check_authorized(self):
        if not self.isAuthorized:
            await self.getUser()

    async def _get(self, target: str) -> dict:
        """Метод для получения данных"""

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://ruobr.ru/api/{target}",
                headers={"password": self.password, "username": self.username},
            )
        try:
            response = response.json()
        except:
            raise NoSuccessException(
                f"Произошла ошибка на сервере: {response.status_code}"
            )
        if isinstance(response, dict):  # В случае ошибки возвращается словарь
            if "success" in response.keys():
                if not (response["success"]):
                    if "error" in response.keys():
                        raise NoSuccessException(response["error"])
                    if "error_type" in response.keys():
                        if response["error_type"] == "auth":
                            raise AuthenticationException(
                                "Проверьте логин и/или пароль"
                            )
                        raise NoSuccessException(response["error_type"])
                    raise NoSuccessException(response)
        return response

    async def getUser(self) -> Union[models.User, dict]:
        """Авторизует и возвращает информацию об ученике
        После авторизации информация доступна в свойстве user
        Если профиль родительский, используйте метод setChild() для выбора ребёнка

        {'status': 'child', 'first_name': 'first_name', 'last_name': 'last_name', 'middle_name': 'middle_name', 'school': 'school', 'school_is_tourniquet': False, 'readonly': False, 'school_is_food': True, 'group': 'group', 'id': 9999999, 'gps_tracker': False}"""

        if self.user is not None:
            return self.user

        user = await self._get("user/")
        if user["status"] == "applicant":
            self.isApplicant = True
            if self.raw_data:
                self._children = user["childs"]
            else:
                self._children = []
                for child in user["childs"]:
                    self._children.append(
                        models.User(
                            **child, status="applicant", gps_tracker=user["gps_tracker"]
                        )
                    )
        else:
            self.isApplicant = False
            if self.raw_data:
                self._children = [user]
            else:
                self._children = [models.User(**user)]

        self.isAuthorized = True
        self.isEmpty = len(self._children) == 0

        return self.user

    async def getChildren(self) -> List[Union[models.User, dict]]:
        """Возвращает список детей текущего аккаунта (для обработки родительских аккаунтов)

        [{'first_name': 'first_name1', 'last_name': 'last_name1', 'middle_name': 'middle_name1', 'school': 'school1', 'school_is_tourniquet': False, 'school_is_food': True, 'group': 'group1', 'id': 9999999, 'readonly': False}, ...]"""

        if not self.isAuthorized:
            await self.getUser()
        return self._children

    async def setChild(self, id: int) -> None:
        """Установить номер ребёнка (для обработки родительских аккаунтов)"""

        self.child = id

    async def getMail(self) -> List[Union[models.Message, dict]]:
        """Возвращает почту

        [{'post_date': '2020-04-26 22:36:11', 'author': 'Author', 'read': True, 'text': 'text', 'clean_text': 'clean_text', 'id': 7777777, 'subject': 'TITLE'}, ...]"""

        await self._check_authorized()

        result = (await self._get("mail/"))["messages"]
        if self.raw_data:
            return result
        return [models.Message(**i) for i in result]

    async def readMessage(self, id: Union[int, str]) -> None:
        """Помечает сообщение как прочитанное"""

        await self._check_authorized()

        await self._get(f"mail/read/?message={id}")

    async def getControlmarks(self) -> List[Union[models.ControlmarksPeriod, dict]]:
        """Возвращает итоговые оценки

        [{'marks': {'Subject': 'Mark', ...}, 'rom': 'I', 'period': 1, 'title': '1-я четверть'}, ...]"""

        await self._check_authorized()
        self._check_empty()

        result = await self._get(f"controlmark/?child={self.user['id']}")
        if self.raw_data:
            return result
        return [models.ControlmarksPeriod(**i) for i in result]

    async def getTimetable(
        self, start: Union[str, date, datetime], end: Union[str, date, datetime]
    ) -> List[Union[models.Lesson, dict]]:
        """Возвращает дневник целиком
        Пример даты: '2020-04-27'

        [{'topic': (опц)'Topic', 'task': (опц){'title': 'Task_title', 'doc': False, 'requires_solutions': False, 'deadline': '2020-04-24', 'test_id': None, 'type': 'group', 'id': 99999999}, 'time_start': '08:30:00', 'date': '2020-04-24', 'id': 175197390, 'subject': 'Subject', 'time_end': '09:15:00', 'staff': 'Teachers Name'}, ...]"""

        await self._check_authorized()
        self._check_empty()

        if isinstance(start, (date, datetime)):
            start = start.strftime("%Y-%m-%d")
        if isinstance(end, (date, datetime)):
            end = end.strftime("%Y-%m-%d")

        result = (
            await self._get(
                f"timetable/?start={start}&end={end}&child={self.user['id']}"
            )
        )["lessons"]
        if self.raw_data:
            return result
        return [models.Lesson(**i) for i in result]

    async def getHomework(
        self, start: Union[str, date, datetime], end: Union[str, date, datetime]
    ) -> List[Union[models.Lesson, dict]]:
        """Возвращает список домашних заданий (выборка из дневника)
        Пример даты: '2020-04-27'

        [{'topic': (опц)'Topic', 'task': {'title': 'Task_title', 'doc': False, 'requires_solutions': False, 'deadline': '2020-04-24', 'test_id': None, 'type': 'group', 'id': 99999999}, 'time_start': '08:30:00', 'date': '2020-04-24', 'id': 175197390, 'subject': 'Subject', 'time_end': '09:15:00', 'staff': 'Teacher's Name}, ...]"""

        timetable = await self.getTimetable(start, end)
        homework = [i for i in timetable if i["task"] is not None]

        return homework

    async def getProgress(
        self, _date: Union[str, date, datetime] = datetime.now()
    ) -> Union[models.Progress, dict]:
        """Возвращает статистику ученика (дата - обычно сегодня)
        Пример даты: '2020-04-27'

        {'period_name': '4-я четверть', 'place_count': 23, 'subjects': [{'place_count': 17, 'place': 3, 'group_avg': 3.69, 'child_avg': 4.29, 'parallels_avg': 3.56, 'subject': 'Русский язык'}, ...], 'place': 7, 'group_avg': 4.05, 'child_avg': 4.28, 'parallels_avg': 3.84}"""

        await self._check_authorized()
        self._check_empty()

        if isinstance(_date, (date, datetime)):
            _date = _date.strftime("%Y-%m-%d")

        result = await self._get(f"progress/?child={self.user['id']}&date={_date}")
        if self.raw_data:
            return result
        return models.Progress(**result)

    async def getMarks(
        self, start: Union[str, date, datetime], end: Union[str, date, datetime]
    ) -> Dict[str, List[Union[models.Mark, dict]]]:
        """Возвращает оценки за указанный период
        Пример даты: '2020-04-27'

        {'Русский язык': [{'question_name': 'Ответ на уроке', 'question_id': 104552170, 'number': 1, 'question_type': 'Ответ на уроке', 'mark': '4'}, ...], ...}"""

        await self._check_authorized()
        self._check_empty()

        if isinstance(start, (date, datetime)):
            start = start.strftime("%Y-%m-%d")
        if isinstance(end, (date, datetime)):
            end = end.strftime("%Y-%m-%d")
        marks = (
            await self._get(f"mark/?child={self.user['id']}&start={start}&end={end}")
        )["subjects"]
        if self.raw_data:
            return marks
        for key, value in marks.items():
            marks[key] = [models.Mark(**i) for i in value]
        return marks

    async def getAttendance(
        self, start: Union[str, date, datetime], end: Union[str, date, datetime]
    ) -> Dict[str, List[str]]:
        """Возвращает пропуски за указанный период
        Пример даты: '2020-04-27'

        {'Русский язык': ['УП', 'Н', ...], ...}"""

        await self._check_authorized()
        self._check_empty()

        if isinstance(start, (date, datetime)):
            start = start.strftime("%Y-%m-%d")
        if isinstance(end, (date, datetime)):
            end = end.strftime("%Y-%m-%d")
        return (
            await self._get(
                f"attendance/?child={self.user['id']}&start={start}&end={end}"
            )
        )["subjects"]

    async def getFoodInfo(self) -> Union[models.FoodInfo, dict]:
        """Возвращает информацию о счёте питания

        {'subsidy': 0, 'account': 999999999, 'total_take_off': 372423, 'total_add': 363000, 'balance_on_start_year': 17113, 'balance': 7690, 'default_complex': 'default_complex'}"""

        await self._check_authorized()
        self._check_empty()

        result = (await self._get(f"food/?child={self.user['id']}"))["account"]
        if self.raw_data:
            return result
        return models.FoodInfo(**result)

    async def getFoodHistory(
        self,
        start: Union[str, date, datetime] = None,
        end: Union[str, date, datetime] = None,
    ) -> List[Union[models.FoodHistoryDay, dict]]:
        """Возвращает историю питания (обычно start - первый день года, end - последний)
        Пример даты: '2020-04-27'

        [{'date': '2020-01-13', 'state': 30, 'complex__code': 'А', 'complex__uid': 'dacd83e5-2dd6-11e8-a63a-00155d039800', 'state_str': 'Заказ подтверждён', 'complex__name': 'Альтернативно-молочный', 'id': 63217607}, ...]"""

        await self._check_authorized()
        self._check_empty()

        if start is None or end is None:
            now = datetime.now()
            if start is None:
                start = datetime(now.year, 1, 1)
            if end is None:
                end = datetime(now.year, 12, 31)

        if isinstance(start, (date, datetime)):
            start = start.strftime("%Y-%m-%d")
        if isinstance(end, (date, datetime)):
            end = end.strftime("%Y-%m-%d")
        result = (
            await self._get(
                f"food/history/?child={self.user['id']}&end={end}&start={start}"
            )
        )["events"]
        if self.raw_data:
            return result
        return [models.FoodHistoryDay(**i) for i in result]

    async def getNews(self) -> List[Union[models.NewsItem, dict]]:
        """Возвращает новости

        [{'title': 'title', 'clean_text': 'text without html tags', 'author': 'author', 'school_name': 'school num 1', 'school_id': 10, 'text': '<p>text</p>', 'date': '2020-11-03', 'pub_date': '2020-11-03 15:50:270', 'id': 100001}...]"""

        await self._check_authorized()

        result = await self._get("news/")
        if self.raw_data:
            return result
        return [models.NewsItem(**i) for i in result]
