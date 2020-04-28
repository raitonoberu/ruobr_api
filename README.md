# ruobr_api

Библиотека для доступа к API [электронного дневника](https://cabinet.ruobr.ru/login/).

## Использование

```
>>> from ruobr_api import Ruobr
>>> r = Ruobr('username', 'password')
>>> r.getUser()
{'status': 'child', 'first_name': 'Иванов', 'last_name': 'Иван', 'middle_name': 'Иванович', 'school': 'Школа 1', 'school_is_tourniquet': False, 'readonly': False, 'school_is_food': True, 'group': '9В', 'id': 9999999, 'gps_tracker': False}
```
## Зависимости

Модуль [requests](https://github.com/psf/requests) последней версии.


## Документация

Пользовательскую документацию можно получить по [ссылке](./docs/index.md).

## Примеры

Примеры можно найти по [ссылке](./examples/index.md).
