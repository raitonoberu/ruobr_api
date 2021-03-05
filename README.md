# ruobr_api

Python модуль для доступа к API [электронного дневника Кемеровской области](https://cabinet.ruobr.ru/login/).

## Дисклеймер

Разработчик не имеет никакого отношения к ООО "МИРИТ". Исходный код находится в открытом доступе, автор не несёт ответственности за последствия его использования.

## Установка

```sh
pip install ruobr_api
```

## Использование

Python 3.6+

```python
>>> from ruobr_api import Ruobr
>>> r = Ruobr('username', 'password')
>>> r.getUser()
User(id=7592904, status='child', first_name='Иван', last_name='Иванов', middle_name='Иванович', school='69-МБОУ "СОШ №69"', school_is_tourniquet=False, readonly=False, school_is_food=True, group='10А', gps_tracker=False)
```

## Зависимости

[httpx](https://github.com/encode/httpx)

[pydantic](https://github.com/samuelcolvin/pydantic)

## Документация

Пользовательскую документацию можно получить по [ссылке](./docs/index.md).

## Примеры

Примеры можно найти по [ссылке](./examples/index.md).
