## Ruobr (основной класс)

class ruobr_api.**Ruobr**(username, password)

-   username (str) - имя пользователя
-   password (str) - пароль

**Методы:**

**getUser**() -> dict

Авторизует и возвращает информацию об ученике. После авторизации информация доступна в переменной user.

Пример вывода:
`{'status': 'child', 'first_name': 'Иванов', 'last_name': 'Иван', 'middle_name': 'Иванович', 'school': 'Школа 1', 'school_is_tourniquet': False, 'readonly': False, 'school_is_food': True, 'group': '9В', 'id': 9999999, 'gps_tracker': False}`

**getChildren**() -> list

Возвращает список детей текущего аккаунта (для обработки родительских профилей)

Пример вывода:
`[{'first_name': 'first_name1', 'last_name': 'last_name1', 'middle_name': 'middle_name1', 'school': 'school1', 'school_is_tourniquet': False, 'school_is_food': True, 'group': 'group1', 'id': 9999999, 'readonly': False}, ...]`

**setChild**(id) -> None

Установить номер ребёнка (для обработки родительских профилей)

-   id(int) - порядковый номер (с нуля)

**getMail**() -> list

Возвращает почту

Пример вывода:
`[{'post_date': '2020-04-26 22:36:11', 'author': 'Author', 'read': True, 'text': 'text', 'clean_text': 'clean_text', 'id': 7777777, 'subject': 'TITLE'}, ...]`

**readMessage**(id) -> None

Помечает сообщение как прочитанное

-   id(int/str) - ID сообщения, полученный с помощью getMail()

**getControlmarks**() -> dict

Возвращает итоговые оценки

Пример вывода:
`[{'marks': {'Subject': 'Mark', ...}, 'rom': 'I', 'period': 1, 'title': '1-я четверть'}, ...]`

**getTimetable**(start, end) -> list

Возвращает дневник целиком. Пример даты: '2020-04-27' (дата также может быть объектом datetime.datetime)

-   start(str/datetime) - начальная дата
-   end(str/datetime) - конечная дата

Пример вывода:
`[{'topic': (опц)'Topic', 'task': (опц){'title': 'Task_title', 'doc': False, 'requires_solutions': False, 'deadline': '2020-04-24', 'test_id': None, 'type': 'group', 'id': 99999999}, 'time_start': '08:30:00', 'date': '2020-04-24', 'id': 175197390, 'subject': 'Subject', 'time_end': '09:15:00', 'staff': 'Teacher's Name}, ...]`

**getHomework**(start, end) -> list

Возвращает список домашнего задания (выборка из дневника). Пример даты: '2020-04-27' (дата также может быть объектом datetime.datetime)

-   start(str) - начальная дата
-   end(str) - конечная дата

Пример вывода:
`[{'topic': (опц)'Topic', 'task': {'title': 'Task_title', 'doc': False, 'requires_solutions': False, 'deadline': '2020-04-24', 'test_id': None, 'type': 'group', 'id': 99999999}, 'time_start': '08:30:00', 'date': '2020-04-24', 'id': 175197390, 'subject': 'Subject', 'time_end': '09:15:00', 'staff': 'Teacher's Name}, ...]`

**getProgress**(date) -> dict

Возвращает статистику ученика. Пример даты: '2020-04-27' (дата также может быть объектом datetime.datetime)

-   date(str/datetime) - дата

Пример вывода:
`{'period_name': '4-я четверть', 'place_count': 23, 'subjects': [{'place_count': 17, 'place': 3, 'group_avg': 3.69, 'child_avg': 4.29, 'parallels_avg': 3.56, 'subject': 'Русский язык'}, ...], 'place': 7, 'group_avg': 4.05, 'child_avg': 4.28, 'parallels_avg': 3.84}`

**getMarks**(start, end) -> dict

Возвращает оценки за указанный период. Пример даты: '2020-04-27' (дата также может быть объектом datetime.datetime)

-   start(str/datetime) - начальная дата
-   end(str/datetime) - конечная дата

Пример вывода:
`{'Русский язык': [{'question_name': 'Ответ на уроке', 'question_id': 104552170, 'number': 1, 'question_type': 'Ответ на уроке', 'mark': '4'}, ...], ...}`

**getAttendance**(start, end) -> dict

Возвращает пропуски за указанный период. Пример даты: '2020-04-27' (дата также может быть объектом datetime.datetime)

-   start(str) - начальная дата
-   end(str) - конечная дата

Пример вывода:
`{'Русский язык': ['УП', 'Н', ...], ...}`

**getFoodInfo**() -> dict

Возвращает информацию о счёте питания

Пример вывода:
`{'subsidy': 0, 'account': 999999999, 'total_take_off': 372423, 'total_add': 363000, 'balance_on_start_year': 17113, 'balance': 7690, 'default_complex': 'default_complex'}`

**getFoodHistory**(start, end) -> list

Возвращает историю питания. Пример даты: '2020-04-27' (дата также может быть объектом datetime.datetime)

-   start(str) - начальная дата (обычно первый день года)
-   end(str) - конечная дата (обычно последний день года)

Пример вывода:
`[{'date': '2020-01-13', 'state': 30, 'complex__code': 'А', 'complex__uid': 'dacd83e5-2dd6-11e8-a63a-00155d039800', 'state_str': 'Заказ подтверждён', 'complex__name': 'Альтернативно-молочный', 'id': 63217607}, ...]`

**getNews**() -> list

Возвращает новости

Пример вывода:
`[{'title': 'title', 'clean_text': 'text without html tags', 'author': 'author', 'school_name': 'school num 1', 'school_id': 10, 'text': '<p>text</p>', 'date': '2020-11-03', 'pub_date': '2020-11-03 15:50:270', 'id': 100001}...]`

**getHomeworkById**(id, type="group") -> str

Возвращает ссылку на страницу с подробной информацией о домашнем задании. Не требует авторизации

-   id(int/str) - ID домашнего задания, полученный с помощью getTimetable() или getHomework()
-   type(str) - тип домашнего задания (?)

Пример вывода:
`https://ruobr.ru/api/homework/?homework=123456&type=group`


## AsyncRuobr (асинхронная версия)

class ruobr_api.**AsyncRuobr**(username, password)

-   username (str) - имя пользователя
-   password (str) - пароль

**Методы идентичны классу ruobr_api.Ruobr**


## Исключения


### AuthenticationException

ruobr_api.**AuthenticationException**

Вызывается при неудачной аутентификации

### NoSuccessException

ruobr_api.**NoSuccessException**

Вызывается, если сервер вернул ложный параметр success или при ошибке в расшифровке JSON
