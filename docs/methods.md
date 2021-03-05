## ruobr-api

class ruobr_api.**Ruobr**(username, password, raw_data=False)

*   username (str) - имя пользователя
*   password (str) - пароль
*   raw_data (bool) - возвращать данные в виде словаря

class ruobr_api.**AsyncRuobr**(username, password, raw_data=False)

Асинхронная версия ruobr_api.**Ruobr**. Методы идентичны.

*   username (str) - имя пользователя
*   password (str) - пароль
*   raw_data (bool) - возвращать данные в виде словаря

**Методы**

**getUser**() -> [User](#user)

Авторизует и возвращает информацию об ученике. После авторизации информация доступна в свойстве user. Если профиль родительский, используйте метод setChild() для выбора ребёнка

**getChildren**() -> list[[User](#user)]

Возвращает список детей текущего аккаунта (для обработки родительских аккаунтов)

**setChild**(id) -> None

Установить номер ребёнка (для обработки родительских аккаунтов)

*   id(int) - порядковый номер (с нуля)

**getMail**() -> list[[Message](#message)]

Возвращает почту

**readMessage**(id) -> None

Помечает сообщение как прочитанное

*   id(int/str) - ID сообщения, полученный с помощью getMail()

**getControlmarks**() -> list[[ControlmarksPeriod](#controlmarksperiod)]

Возвращает итоговые оценки

**getTimetable**(start, end) -> list[[Lesson](#lesson)]

Возвращает дневник целиком. Пример даты: '2020-04-27'

*   start(str/date/datetime) - начальная дата
*   end(str/date/datetime) - конечная дата

**getHomework**(start, end) -> list[[Lesson](#lesson)]

Возвращает список домашних заданий (выборка из дневника). Пример даты: '2020-04-27'

*   start(str) - начальная дата
*   end(str) - конечная дата

**getProgress**(date=datetime.now()) -> [Progress](#progress)

Возвращает статистику ученика (дата - обычно сегодня). Пример даты: '2020-04-27'

*   date(str/date/datetime) - дата

**getMarks**(start, end) -> dict[str, list[[Mark](#mark)]]

Возвращает оценки за указанный период. Пример даты: '2020-04-27'

*   start(str/date/datetime) - начальная дата
*   end(str/date/datetime) - конечная дата

**getAttendance**(start, end) -> dict[str, list[str]]

Возвращает пропуски за указанный период. Пример даты: '2020-04-27'

*   start(str) - начальная дата
*   end(str) - конечная дата

**getFoodInfo**() -> [FoodInfo](#foodinfo)

Возвращает информацию о счёте питания

**getFoodHistory**(start=None, end=None) -> list[[FoodHistoryDay](#foodhistoryday)]

Возвращает историю питания. Пример даты: '2020-04-27'

*   start(str) - начальная дата (обычно первый день года)
*   end(str) - конечная дата (обычно последний день года)

**getNews**() -> list[[NewsItem](#newsitem)]

Возвращает новости

**getHomeworkById**(id, type="group") -> str

Возвращает ссылку на страницу с подробной информацией о домашнем задании. Не требует авторизации

*   id(int/str) - ID домашнего задания, полученный с помощью getTimetable() или getHomework()
*   type(str) - тип домашнего задания (?)

Пример вывода:
 `https://ruobr.ru/api/homework/?homework=123456&type=group`

## Модели

### User

* id: int
* status: str
* first_name: str
* last_name: str
* middle_name: str
* school: str
* school_is_tourniquet: bool
* readonly: bool
* school_is_food: bool
* group: str
* gps_tracker: bool

### Message

* id: int
* post_date: datetime
* author: str
* read: bool
* text: str
* clean_text: str
* subject: str

### ControlmarksPeriod

* marks: Dict[str, str]
* rom: str
* period: int
* title: str

### Task

* id: int
* title: str
* doc: bool
* requires_solutions: bool
* deadline: date
* test_id: int = None
* type: str

### Lesson

* id: int
* topic: str = None
* task: Task = None
* time_start: time
* date: date
* subject: str
* time_end: time
* staff: str

### ProgressSubject

* subject: str
* place_count: int
* place: int
* group_avg: float
* child_avg: float
* parallels_avg: float

### Progress

* period_name: str
* place_count: str
* subjects: List[ProgressSubject]
* place: int
* group_avg: float
* child_avg: float
* parallels_avg: float

### Mark

* question_name: str
* question_id: int
* number: int
* question_type: str
* mark: int

### FoodInfo

* subsidy: int
* account: int
* total_take_off: int
* total_add: int
* balance_on_start_year: int
* balance: int
* default_complex: str

### FoodHistoryDay

* id: int
* date: date
* state: int
* complex__code: str
* complex__uid: str
* state_str: str
* complex__name: str

### NewsItem

* id: int
* title: str
* clean_text: str
* author: str
* school_name: str
* school_id: int
* text: str
* date: date
* pub_date: datetime

## Исключения

### AuthenticationException

ruobr_api.**AuthenticationException**

Вызывается при неудачной аутентификации

### NoSuccessException

ruobr_api.**NoSuccessException**

Вызывается, если сервер вернул ложный параметр success или при ошибке в расшифровке JSON

### NoChildrenException

ruobr_api.**NoChildrenException**

Вызывается в случае, если на родительском аккаунте нет детей