# -*- coding: utf-8 -*-
"""
:authors: raitonoberu
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2021 raitonoberu
"""
from ruobr_api.exceptions import (
    AuthenticationException,
    NoChildrenException,
    NoSuccessException,
)
import httpx
import base64
from datetime import date, datetime
from typing import List, Union


class Ruobr(object):
    """Класс для доступа к API электронного дневника"""

    def __init__(self, username: str, password: str):
        # Логин и пароль должны быть закодированы в base64
        self.username = base64.b64encode(username.upper().encode("UTF-8")).decode(
            "UTF-8"
        )
        self.password = base64.b64encode(password.encode("UTF-8")).decode("UTF-8")

        self.is_applicant = None  # Является ли профиль родительским
        self.is_authorized = False  # Авторизован ли профиль
        self.is_empty = None  # Является ли профиль пустым (без детей)
        self.child = 0  # Номер ребёнка, если профиль родительский
        self._children = None

    def _check_authorized(self):
        if not self.is_authorized:
            self.get_user()

    def _check_empty(self):
        if self.is_empty:
            raise NoChildrenException("На аккаунте нет детей")

    @property
    def user(self) -> dict:
        if self.is_authorized and not self.is_empty:
            return self._children[self.child]
        return None

    def _get(self, target: str) -> dict:
        """Метод для получения данных"""

        response = httpx.get(
            f"https://api3d.ruobr.ru/{target}",
            headers={"password": self.password, "username": self.username},
        )
        try:
            response = response.json()
        except:
            raise NoSuccessException(response.text)
        if isinstance(response, dict):
            if "success" in response.keys():
                if not (response["success"]):
                    if "error" in response.keys():
                        raise NoSuccessException(response["error"])
                    if "error_type" in response.keys():
                        # не уверен, что это всё ещё работает
                        if response["error_type"] == "auth":
                            raise AuthenticationException(
                                "Проверьте логин и/или пароль"
                            )
                        raise NoSuccessException(response["error_type"])
                    raise NoSuccessException(response)
        return response

    def get_user(self) -> dict:
        """Авторизует и возвращает информацию об ученике
        После авторизации информация доступна в поле user
        Если профиль родительский, измените поле child для выбора ребёнка"""

        if self.user is not None:
            return self.user

        user = self._get("user/")
        if not user:
            raise AuthenticationException("Проверьте логин и/или пароль")
        if user["status"] == "applicant":
            self.is_applicant = True
            self._children = user["childs"]
        else:
            self.is_applicant = False
            self._children = [user]

        self.is_authorized = True
        self.is_empty = len(self._children) == 0

        return self.user

    def get_children(self) -> List[dict]:
        """Возвращает список детей текущего аккаунта (для обработки родительских аккаунтов)"""

        self._check_authorized()

        return self._children

    def get_mail(self) -> List[dict]:
        """Возвращает почту
        Если в сообщении type_id == 2, то last_msg_text содержит HTML-разметку"""

        self._check_authorized()

        return self._get("mail/")["messages"]

    def get_message(self, message_id: int) -> dict:
        """Возвращает подробную информацию о сообщении
        Падает c ошибкой 502 Bad Gateway, если в сообщении type_id == 2"""

        self._check_authorized()
        self._check_empty()

        return self._get(f"mail/{message_id}/?child={self.user['id']}")["data"]

    def get_recipients(self) -> List[dict]:
        """Возвращает доступных получателей сообщения"""

        self._check_authorized()

        return self._get("mail/new/")["data"]

    def get_achievements(self) -> dict:
        """Возвращает список достижений"""

        self._check_authorized()
        self._check_empty()

        return self._get(f"achievements/?child={self.user['id']}")["data"]

    def get_control_marks(self) -> List[dict]:
        """Возвращает итоговые оценки"""

        self._check_authorized()
        self._check_empty()

        return self._get(f"controlmark/?child={self.user['id']}")

    def get_all_marks(self, period: int, subject_id: int) -> dict:
        """Возвращает все оценки по предмету за период. Может быть пустым"""

        self._check_authorized()
        self._check_empty()

        return self._get(f"all_marks/{period}/{subject_id}/?child={self.user['id']}")[
            "data"
        ]

    def get_events(self) -> dict:
        """Возвращает события"""

        self._check_authorized()
        self._check_empty()

        return self._get(f"btm/?child={self.user['id']}")

    def get_certificate(self) -> dict:
        """Возвращает информацию о сертификате"""

        self._check_authorized()
        self._check_empty()

        return self._get(f"do/cert/?child={self.user['id']}")["data"]

    def get_birthdays(self) -> List[dict]:
        """Возвращает дни рождения"""

        self._check_authorized()
        self._check_empty()

        return self._get(f"birthday/?child={self.user['id']}")["data"]

    def get_food_info(self, _date: Union[str, date, datetime] = None) -> dict:
        """Возвращает информацию о питании. Может быть пустым"""

        self._check_authorized()
        self._check_empty()

        if _date is None:
            _date = datetime.now()

        if isinstance(_date, (date, datetime)):
            _date = _date.strftime("%Y-%m-%d")

        return self._get(
            f"food/calendary/?child={self.user['id']}&food_type={self.user['school_is_food']}&selected_date={_date}"
        )["data"]

    def get_classmates(self) -> List[dict]:
        """Возвращает информацию об одноклассниках"""

        self._check_authorized()
        self._check_empty()

        return self._get(f"odnoklassniki/?child={self.user['id']}")["data"]

    def get_books(self) -> List[dict]:
        """Возвращает информацию о взятых книгах"""

        self._check_authorized()
        self._check_empty()

        return self._get(f"book/?child={self.user['id']}")["data"]

    def get_useful_links(self) -> dict:
        """Возвращает полезные ссылки"""

        self._check_authorized()
        self._check_empty()

        return self._get(f"ios/?child={self.user['id']}")["data"]

    def get_guide(self) -> dict:
        """Возвращает информацию об учебном заведении"""

        self._check_authorized()
        self._check_empty()

        return self._get(f"guide/?child={self.user['id']}")["data"]

    def get_timetable(
        self, start: Union[str, date, datetime], end: Union[str, date, datetime]
    ) -> List[dict]:
        """Возвращает дневник целиком
        Пример даты: '2020-04-27'"""

        self._check_authorized()
        self._check_empty()

        if isinstance(start, (date, datetime)):
            start = start.strftime("%Y-%m-%d")
        if isinstance(end, (date, datetime)):
            end = end.strftime("%Y-%m-%d")

        return self._get(
            f"timetable2/?start={start}&end={end}&child={self.user['id']}"
        )["lessons"]


class AsyncRuobr(Ruobr):
    """Класс для доступа к новому API электронного дневника"""

    async def _check_authorized(self):
        if not self.is_authorized:
            await self.get_user()

    async def _get(self, target: str) -> dict:
        """Метод для получения данных"""

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api3d.ruobr.ru/{target}",
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

    async def get_user(self) -> dict:
        """Авторизует и возвращает информацию об ученике
        После авторизации информация доступна в поле user
        Если профиль родительский, измените поле child для выбора ребёнка"""

        if self.user is not None:
            return self.user

        user = await self._get("user/")
        if not user:
            raise AuthenticationException("Проверьте логин и/или пароль")
        if user["status"] == "applicant":
            self.is_applicant = True
            self._children = user["childs"]
        else:
            self.is_applicant = False
            self._children = [user]

        self.is_authorized = True
        self.is_empty = len(self._children) == 0

        return self.user

    async def get_children(self) -> List[dict]:
        """Возвращает список детей текущего аккаунта (для обработки родительских аккаунтов)"""

        await self._check_authorized()

        return self._children

    async def get_mail(self) -> List[dict]:
        """Возвращает почту
        Если в сообщении type_id == 2, то last_msg_text содержит HTML-разметку"""

        await self._check_authorized()

        result = await self._get("mail/")
        return result["messages"]

    async def get_message(self, message_id: int) -> dict:
        """Возвращает подробную информацию о сообщении
        Падает, если в сообщении type_id == 2"""

        await self._check_authorized()
        self._check_empty()

        result = await self._get(f"mail/{message_id}/?child={self.user['id']}")
        return result["data"]

    async def get_recipients(self) -> List[dict]:
        """Возвращает доступных получателей сообщения"""
        # TODO: возможность отправки сообщений

        await self._check_authorized()

        result = await self._get("mail/new/")
        return result["data"]

    async def get_achievements(self) -> dict:
        """Возвращает список достижений"""

        await self._check_authorized()
        self._check_empty()

        result = await self._get(f"achievements/?child={self.user['id']}")
        return result["data"]

    async def get_control_marks(self) -> List[dict]:
        """Возвращает итоговые оценки"""

        await self._check_authorized()
        self._check_empty()

        return await self._get(f"controlmark/?child={self.user['id']}")

    async def get_all_marks(self, period: int, subject_id: int) -> dict:
        """Возвращает все оценки по предмету за период. Может быть пустым"""

        await self._check_authorized()
        self._check_empty()

        result = await self._get(
            f"all_marks/{period}/{subject_id}/?child={self.user['id']}"
        )
        return result["data"]

    async def get_events(self) -> dict:
        """Возвращает события"""

        await self._check_authorized()
        self._check_empty()

        return await self._get(f"btm/?child={self.user['id']}")

    async def get_certificate(self) -> dict:
        """Возвращает информацию о сертификате"""

        await self._check_authorized()
        self._check_empty()

        result = await self._get(f"do/cert/?child={self.user['id']}")
        return result["data"]

    async def get_birthdays(self) -> List[dict]:
        """Возвращает дни рождения"""

        await self._check_authorized()
        self._check_empty()

        result = await self._get(f"birthday/?child={self.user['id']}")
        return result["data"]

    async def get_food_info(self, _date: Union[str, date, datetime] = None) -> dict:
        """Возвращает информацию о питании. None если пусто"""

        await self._check_authorized()
        self._check_empty()

        if _date is None:
            _date = datetime.now()

        if isinstance(_date, (date, datetime)):
            _date = _date.strftime("%Y-%m-%d")

        result = await self._get(
            f"food/calendary/?child={self.user['id']}&food_type={self.user['school_is_food']}&selected_date={_date}"
        )
        return result["data"]

    async def get_classmates(self) -> List[dict]:
        """Возвращает информацию об одноклассниках"""

        await self._check_authorized()
        self._check_empty()

        result = await self._get(f"odnoklassniki/?child={self.user['id']}")
        return result["data"]

    async def get_books(self) -> List[dict]:
        """Возвращает информацию о взятых книгах"""

        await self._check_authorized()
        self._check_empty()

        result = await self._get(f"book/?child={self.user['id']}")
        return result["data"]

    async def get_useful_links(self) -> dict:
        """Возвращает полезные ссылки"""

        await self._check_authorized()
        self._check_empty()

        result = await self._get(f"ios/?child={self.user['id']}")
        return result["data"]

    async def get_guide(self) -> dict:
        """Возвращает информацию об учебном заведении"""

        await self._check_authorized()
        self._check_empty()

        result = await self._get(f"guide/?child={self.user['id']}")
        return result["data"]

    async def get_timetable(
        self, start: Union[str, date, datetime], end: Union[str, date, datetime]
    ) -> List[dict]:
        """Возвращает дневник целиком
        Пример даты: '2020-04-27'"""

        await self._check_authorized()
        self._check_empty()

        if isinstance(start, (date, datetime)):
            start = start.strftime("%Y-%m-%d")
        if isinstance(end, (date, datetime)):
            end = end.strftime("%Y-%m-%d")

        result = await self._get(
            f"timetable2/?start={start}&end={end}&child={self.user['id']}"
        )
        return result["lessons"]
