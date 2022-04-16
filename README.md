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
>>> r.get_user()
{'status': 'child', 'last_name': 'Зубенко', 'school_terrirtory_id': 1, 'user_img': 'https://ruobr.ru/mediac/avatars/48ba6326740e49d6a3c9ac01fedff9d7.JPEG', 'school_is_tourniquet': 0, 'user_id': 115654529, 'school_is_food': 5, 'school': 'МБОУ "СОШ №69"', 'group': '11А', 'success': True, 'push_settings': {'school_news': 0, 'attendance': 0, 'homework': 0, 'mau_balance': 0, 'tourniquet': 1, 'mark': 1}, 'middle_name': 'Петрович', 'id': 4694228, 'readonly': 0, 'first_name': 'Михаил', 'birth_date': '2004-10-10', 'gps_tracker': False}
```

## Зависимости

[httpx](https://github.com/encode/httpx)

## Примеры

Примеры можно найти по [ссылке](./examples/index.md).
