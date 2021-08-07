# -*- coding: utf-8 -*-
"""
:authors: raitonoberu
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2021 raitonoberu
"""
from ruobr_api.new import models
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
    """Класс для доступа к новому API электронного дневника"""

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

    def getUser(self) -> Union[models.User, dict]:
        """Авторизует и возвращает информацию об ученике
        После авторизации информация доступна в свойстве user
        Если профиль родительский, используйте метод setChild() для выбора ребёнка"""

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
        """Возвращает список детей текущего аккаунта (для обработки родительских аккаунтов)"""

        self._check_authorized()

        return self._children

    def setChild(self, id: int) -> None:
        """Установить номер ребёнка (для обработки родительских аккаунтов)"""

        self.child = id

    def getMail(self) -> List[Union[models.Message, dict]]:
        """Возвращает почту"""

        self._check_authorized()

        result = self._get("mail/")["messages"]
        if self.raw_data:
            return result
        return [models.Message(**i) for i in result]

    def getMessage(
        self, message: Union[int, models.Message]
    ) -> List[Union[models.MessageDetail, dict]]:
        """Возвращает подробную информацию о сообщении"""

        self._check_authorized()
        self._check_empty()

        if isinstance(message, models.Message):
            message = message.id

        result = self._get(f"mail/{message}/?child={self.user['id']}")["data"]
        if self.raw_data:
            return result
        return models.MessageDetail(**result)

    def getRecipients(self) -> List[Union[models.Recipient, dict]]:
        """Возвращает доступных получателей сообщения"""
        # TODO: возможность отправки сообщений

        self._check_authorized()

        result = self._get("mail/new/")["data"]
        if self.raw_data:
            return result
        return [models.Recipient(**i) for i in result]

    def getAchievements(self) -> dict:
        """Возвращает список достижений"""
        # TODO: узнать возвращаемые данные и добавить модели

        self._check_authorized()
        self._check_empty()

        result = self._get(f"achievements/?child={self.user['id']}")["data"]
        # if self.raw_data:
        #     return result
        # return models.Achievements(**result)
        return result

    def getControlmarks(self) -> List[Union[models.ControlmarksPeriod, dict]]:
        """Возвращает итоговые оценки"""

        self._check_authorized()
        self._check_empty()

        result = self._get(f"controlmark/?child={self.user['id']}")
        if self.raw_data:
            return result
        return [models.ControlmarksPeriod(**i) for i in result]

    def getAllMarks(
        self,
        period: Union[int, models.ControlmarksPeriod],
        subject: Union[int, models.ControlMark],
    ) -> Union[models.AllMarks, dict]:
        """Возвращает все оценки по предмету за период"""

        self._check_authorized()
        self._check_empty()

        if isinstance(period, models.ControlmarksPeriod):
            period = period.period
        if isinstance(subject, models.ControlMark):
            subject = subject.subject_id

        result = self._get(f"all_marks/{period}/{subject}/?child={self.user['id']}")[
            "data"
        ]
        if self.raw_data:
            return result
        return models.AllMarks(**result)

    def getEvents(self) -> dict:
        """Возвращает события"""
        # TODO: узнать возвращаемые данные и добавить модели

        self._check_authorized()
        self._check_empty()

        result = self._get(f"btm/?child={self.user['id']}")
        # if self.raw_data:
        #     return result
        # return models.Events(**result)
        return result

    def getCertificate(self) -> Union[models.Certificate, dict]:
        """Возвращает информацию о сертификате"""

        self._check_authorized()
        self._check_empty()

        result = self._get(f"do/cert/?child={self.user['id']}")["data"]
        if self.raw_data:
            return result
        return models.Certificate(**result)

    def getBirthdays(self) -> List[Union[models.Birthday, dict]]:
        """Возвращает дни рождения"""

        self._check_authorized()
        self._check_empty()

        result = self._get(f"birthday/?child={self.user['id']}")["data"]
        if self.raw_data:
            return result
        return [models.Birthday(**i) for i in result]

    def getFoodInfo(
        self, _date: Union[str, date, datetime] = None
    ) -> Union[models.FoodInfo, dict]:
        """Возвращает информацию о питании"""

        self._check_authorized()
        self._check_empty()

        if _date is None:
            _date = datetime.now()

        if isinstance(_date, (date, datetime)):
            _date = _date.strftime("%Y-%m-%d")

        result = self._get(
            f"food/calendary/?child={self.user['id']}&food_type={self.user['school_is_food']}&selected_date={_date}"
        )["data"]
        if self.raw_data:
            return result
        return models.FoodInfo(**result)

    def getClassmates(self) -> List[Union[models.Classmate, dict]]:
        """Возвращает информацию об одноклассниках"""

        self._check_authorized()
        self._check_empty()

        result = self._get(f"odnoklassniki/?child={self.user['id']}")["data"]
        if self.raw_data:
            return result
        return [models.Classmate(**i) for i in result]

    def getBooks(self) -> List:
        """Возвращает информацию о взятых книгах"""
        # TODO: узнать возвращаемые данные и добавить модели

        self._check_authorized()
        self._check_empty()

        result = self._get(f"book/?child={self.user['id']}")["data"]
        # if self.raw_data:
        #     return result
        # return models.Food(**result)
        return result

    def getIos(self) -> dict:
        """Возвращает информацию о ..."""
        # TODO: узнать возвращаемые данные и добавить модели

        self._check_authorized()
        self._check_empty()

        result = self._get(f"ios/?child={self.user['id']}")["data"]
        # if self.raw_data:
        #     return result
        # return models.Ios(**result)
        return result

    def getGuide(self) -> Union[models.Guide, dict]:
        """Возвращает информацию об учебном заведении"""

        self._check_authorized()
        self._check_empty()

        result = self._get(f"guide/?child={self.user['id']}")["data"]
        if self.raw_data:
            return result
        return models.Guide(**result)

    def getTimetable(
        self, start: Union[str, date, datetime], end: Union[str, date, datetime]
    ) -> List[Union[models.Lesson, dict]]:
        """Возвращает дневник целиком
        Пример даты: '2020-04-27'"""

        self._check_authorized()
        self._check_empty()

        if isinstance(start, (date, datetime)):
            start = start.strftime("%Y-%m-%d")
        if isinstance(end, (date, datetime)):
            end = end.strftime("%Y-%m-%d")

        result = self._get(
            f"timetable2/?start={start}&end={end}&child={self.user['id']}"
        )["lessons"]
        if self.raw_data:
            return result
        return [models.Lesson(**i) for i in result]


class AsyncRuobr(Ruobr):
    """Класс для доступа к новому API электронного дневника"""

    async def _check_authorized(self):
        if not self.isAuthorized:
            await self.getUser()

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

    async def getUser(self) -> Union[models.User, dict]:
        """Авторизует и возвращает информацию об ученике
        После авторизации информация доступна в свойстве user
        Если профиль родительский, используйте метод setChild() для выбора ребёнка"""

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
        """Возвращает список детей текущего аккаунта (для обработки родительских аккаунтов)"""

        await self._check_authorized()

        return self._children

    async def getMail(self) -> List[Union[models.Message, dict]]:
        """Возвращает почту"""

        await self._check_authorized()

        result = await self._get("mail/")
        if self.raw_data:
            return result["messages"]
        return [models.Message(**i) for i in result["messages"]]

    async def getMessage(
        self, message: Union[int, models.Message]
    ) -> List[Union[models.MessageDetail, dict]]:
        """Возвращает подробную информацию о сообщении"""

        await self._check_authorized()
        self._check_empty()

        if isinstance(message, models.Message):
            message = message.id

        result = await self._get(f"mail/{message}/?child={self.user['id']}")
        if self.raw_data:
            return result["data"]
        return models.MessageDetail(**result["data"])

    async def getRecipients(self) -> List[Union[models.Recipient, dict]]:
        """Возвращает доступных получателей сообщения"""
        # TODO: возможность отправки сообщений

        await self._check_authorized()

        result = await self._get("mail/new/")
        if self.raw_data:
            return result["data"]
        return [models.Recipient(**i) for i in result["data"]]

    async def getAchievements(self) -> dict:
        """Возвращает список достижений"""
        # TODO: узнать возвращаемые данные и добавить модели

        await self._check_authorized()
        self._check_empty()

        result = await self._get(f"achievements/?child={self.user['id']}")
        # if self.raw_data:
        #     return result
        # return models.Achievements(**result)
        return result["data"]

    async def getControlmarks(self) -> List[Union[models.ControlmarksPeriod, dict]]:
        """Возвращает итоговые оценки"""

        await self._check_authorized()
        self._check_empty()

        result = await self._get(f"controlmark/?child={self.user['id']}")
        if self.raw_data:
            return result
        return [models.ControlmarksPeriod(**i) for i in result]

    async def getAllMarks(
        self,
        period: Union[int, models.ControlmarksPeriod],
        subject: Union[int, models.ControlMark],
    ) -> Union[models.AllMarks, dict]:
        """Возвращает все оценки по предмету за период"""

        await self._check_authorized()
        self._check_empty()

        if isinstance(period, models.ControlmarksPeriod):
            period = period.period
        if isinstance(subject, models.ControlMark):
            subject = subject.subject_id

        result = await self._get(
            f"all_marks/{period}/{subject}/?child={self.user['id']}"
        )
        if self.raw_data:
            return result["data"]
        return models.AllMarks(**result["data"])

    async def getEvents(self) -> dict:
        """Возвращает события"""
        # TODO: узнать возвращаемые данные и добавить модели

        await self._check_authorized()
        self._check_empty()

        result = await self._get(f"btm/?child={self.user['id']}")
        # if self.raw_data:
        #     return result
        # return models.Events(**result)
        return result

    async def getCertificate(self) -> Union[models.Certificate, dict]:
        """Возвращает информацию о сертификате"""

        await self._check_authorized()
        self._check_empty()

        result = await self._get(f"do/cert/?child={self.user['id']}")
        if self.raw_data:
            return result["data"]
        return models.Certificate(**result["data"])

    async def getBirthdays(self) -> List[Union[models.Birthday, dict]]:
        """Возвращает дни рождения"""

        await self._check_authorized()
        self._check_empty()

        result = await self._get(f"birthday/?child={self.user['id']}")
        if self.raw_data:
            return result["data"]
        return [models.Birthday(**i) for i in result["data"]]

    async def getFoodInfo(
        self, _date: Union[str, date, datetime] = None
    ) -> Union[models.FoodInfo, dict]:
        """Возвращает информацию о питании"""

        await self._check_authorized()
        self._check_empty()

        if _date is None:
            _date = datetime.now()

        if isinstance(_date, (date, datetime)):
            _date = _date.strftime("%Y-%m-%d")

        result = await self._get(
            f"food/calendary/?child={self.user['id']}&food_type={self.user['school_is_food']}&selected_date={_date}"
        )
        if self.raw_data:
            return result["data"]
        return models.FoodInfo(**result["data"])

    async def getClassmates(self) -> List[Union[models.Classmate, dict]]:
        """Возвращает информацию об одноклассниках"""

        await self._check_authorized()
        self._check_empty()

        result = await self._get(f"odnoklassniki/?child={self.user['id']}")
        if self.raw_data:
            return result["data"]
        return [models.Classmate(**i) for i in result["data"]]

    async def getBooks(self) -> List:
        """Возвращает информацию о взятых книгах"""
        # TODO: узнать возвращаемые данные и добавить модели

        await self._check_authorized()
        self._check_empty()

        result = await self._get(f"book/?child={self.user['id']}")
        # if self.raw_data:
        #     return result
        # return models.Food(**result)
        return result["data"]

    async def getIos(self) -> dict:
        """Возвращает информацию о ..."""
        # TODO: узнать возвращаемые данные и добавить модели

        await self._check_authorized()
        self._check_empty()

        result = await self._get(f"ios/?child={self.user['id']}")
        # if self.raw_data:
        #     return result
        # return models.Ios(**result)
        return result["data"]

    async def getGuide(self) -> Union[models.Guide, dict]:
        """Возвращает информацию об учебном заведении"""

        await self._check_authorized()
        self._check_empty()

        result = await self._get(f"guide/?child={self.user['id']}")
        if self.raw_data:
            return result["data"]
        return models.Guide(**result["data"])

    async def getTimetable(
        self, start: Union[str, date, datetime], end: Union[str, date, datetime]
    ) -> List[Union[models.Lesson, dict]]:
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
        if self.raw_data:
            return result["lessons"]
        return [models.Lesson(**i) for i in result["lessons"]]
