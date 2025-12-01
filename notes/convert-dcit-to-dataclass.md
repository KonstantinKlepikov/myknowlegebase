---
description: Преобразовавние словаря в dataclass или namedtuple
tags: python-standart-library python
title: Convert dict to dataclass or namedtuple
---
## Распаковка словаря для создания экземпляра

```python
>>> from dataclasses import dataclass
>>> @dataclass
... class MyData:
...   prop1: int
...   prop2: str
...   prop3: int
...
>>> d = {'prop1': 5, 'prop2': 'hi', 'prop3': 100}
>>> my_data = MyData(**d)
>>> my_data
MyData(prop1=5, prop2='hi', prop3=100)
```

Тоже самое можно сделать с `namedtuple`

```python
>>> from collections import namedtuple
>>> MyTuple = namedtuple('MyTuple', 'field1, field2, field3')
>>> d = {'field1': 5, 'field2': 'hi', 'field3': 100}
>>> my_tuple = MyTuple(**d)
>>> my_tuple
MyTuple(field1=5, field2='hi', field3=100)
```

## Через __annotation__

Можно воспользоваться этим:

```python
class Foo:
    foo: str
    bar: int
    baz: list

Foo.__annotations__ = {'foo': str, 'bar': int, 'baz': list}
```

Тогда так:

```python
d_dataclass = dataclass(type('d_dataclass', (), {'__annotations__': {k: type(v) for k, v in d.items()}}))
```

Наконец можно так:

```python
def make_dc(d, name='d_dataclass'):
    @dataclass
    class Wrapped:
        __annotations__ = {k: type(v) for k, v in d.items()}

    Wrapped.__qualname__ = Wrapped.__name__ = name

    return Wrapped
```

[Источник](https://www.reddit.com/r/learnpython/comments/9h74no/convert_dict_to_dataclass/)

## Создание инстанса с помощью dacite

[Библиотека dacite](https://github.com/konradhalas/dacite)

```python
from dataclasses import dataclass
from dacite import from_dict

@dataclass
class User:
    name: str
    age: int
    is_active: bool

data = {
    'name': 'John',
    'age': 30,
    'is_active': True,
}

user = from_dict(data_class=User, data=data)

assert user == User(name='John', age=30, is_active=True)
```

Смотри ещеЖ
- [[python-dataclasses]]
- [[python-standart-library]]


[python-dataclasses]: python-dataclasses "Python dataclasses"
[python-standart-library]: ../lists/python-standart-library "Стандартная библиотека python и полезные ресурсы"
