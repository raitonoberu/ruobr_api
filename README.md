# ruobr_api

Python модуль для доступа к API [электронного дневника Кемеровской области](https://cabinet.ruobr.ru/login/).

## Дисклеймер

Разработчик не имеет никакого отношения к ООО "МИРИТ". Исходный код находится в открытом доступе, автор не несёт ответственности за последствия его использования.

## Установка

```sh
pip install ruobr_api
```

## Использование

```python
>>> from ruobr_api import Ruobr
>>> r = Ruobr('username', 'password')
>>> r.getUser()
{'status': 'child', 'first_name': 'Иванов', 'last_name': 'Иван', 'middle_name': 'Иванович', 'school': 'Школа 1', 'school_is_tourniquet': False, 'readonly': False, 'school_is_food': True, 'group': '9В', 'id': 9999999, 'gps_tracker': False}
```

## Зависимости

[Python](https://www.python.org/) 3.6+

Модуль [httpx](https://github.com/encode/httpx) последней версии.

## Документация

Пользовательскую документацию можно получить по [ссылке](./docs/index.md).

## Примеры

Примеры можно найти по [ссылке](./examples/index.md).
