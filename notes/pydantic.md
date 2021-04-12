# pydantic

Типизация для #python [Документация](https://pydantic-docs.helpmanual.io/)

```python
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name = 'John Doe'
    signup_ts: Optional[datetime] = None
    friends: List[int] = []


external_data = {
    'id': '123',
    'signup_ts': '2019-06-01 12:22',
    'friends': [1, 2, '3'],
}
user = User(**external_data)
print(user.id)
#> 123
print(repr(user.signup_ts))
#> datetime.datetime(2019, 6, 1, 12, 22)
print(user.friends)
#> [1, 2, 3]
print(user.dict())
"""
{
    'id': 123,
    'signup_ts': datetime.datetime(2019, 6, 1, 12, 22),
    'friends': [1, 2, 3],
    'name': 'John Doe',
}
"""
```

## Установка

`pip install pydantic`

Три варианта

`pip install pydantic[email]` [валидация имейлов](https://github.com/JoshData/python-email-validator)
`pip install pydantic[dotenv]` [.env support](https://pydantic-docs.helpmanual.io/usage/settings/#dotenv-env-support) - [[.env-переменные-окружения]]
`pip install pydantic[email,dotenv]`

## Использование

## Модели

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name = 'Jane Doe'
```

Каждый класс модели наследует базовой модели pydantic. В данном случае тип name инферится из типа строки. Это поле не обязательно, так как установлено дефолтное значение. Тогда создавая инстанс класса, мы получим аттрибуты:

```python
user = User(id='123')

assert user.id == 123
assert user.name == 'Jane Doe'

# name не создается при инициализации, т.к. имеет дефолтное значение
assert user.__fields_set__ == {'id'}

# поля полученные, при инициализации
assert user.dict() == dict(user) == {'id': 123, 'name': 'Jane Doe'}

# наконец, у нас есть полный доступ к атрибутам
user.id = 321
assert user.id == 321
```

[Свойства модели](https://pydantic-docs.helpmanual.io/usage/models/#model-properties):

- `dict()` словарь полей и значений модели
- `json()` тоже вамое в виде json
- `copy()` копия модели (по дефолту shallow)
- `parse_obj()` метод для парсинга и лоада объекта в модель с выдачей ошибки, если объект не похож на fict
- `parse_raw()` тоже самое из json
- `parse_file()` из файла
- `from_orm()` из класса ОРМ
- `schema()` возвращает json-схему в виде словаря
- `schema_json()` в виде json
- `construct()` создание модели без валидации
- `_fields_set__` имена полей в виде множества
- `__fields__` словарь полей
- `__config__` сонфиг
