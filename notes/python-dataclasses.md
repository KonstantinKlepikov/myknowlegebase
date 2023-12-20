---
description: Датаклассы в python
tags: python-standart-library python
title: Python dataclasses
---
Модуль `dataclasses` предоставляет [[python-decorator]] и функции для автоматического добавления сгенерированных специальных методов, таких как `__init__()` и `__repr__()`, в пользовательские классы.

`@dataclasses.dataclass(*, init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False, match_args=True, kw_only=False, slots=False)` - декоратор, который используется для добавления сгенерированных специальных методов к классам. Декоратор `dataclass()` проверяет класс, чтобы найти поля. **Поле определяется как переменная класса, имеющая аннотацию типа**. За двумя исключениями, описанными ниже, в `dataclass()` ничто не проверяет тип, указанный в аннотации переменной. Порядок полей во всех сгенерированных методах соответствует порядку, в котором они появляются в определении класса. `dataclass()` так-же добавит в класс дандер-методы. Если какой-либо из добавленных методов уже существует в классе, поведение зависит от параметра декоратора. Декоратор возвращает тот же класс, для которого он был вызван - новый класс не создается. Если `dataclass()` используется просто как простой декоратор без параметров, он действует так, как если бы у него были значения по умолчанию, задокументированные в этой сигнатуре.

Три эквивалентных варианта использования `dataclass()`

```python
@dataclass
class C:
    ...

@dataclass()
class C:
    ...

@dataclass(init=True, repr=True, eq=True, order=False, unsafe_hash=False,
    frozen=False, match_args=True, kw_only=False, slots=False)
class C:
   ...
```

Параметры декоратора устанавливают какие специальные методы должны быть сгенерированы.

Если у класса уже определены `__init__()`, `__repr__()`, `__eq__()` то параметры декоратора будут проигнорированы. В случае других методов ожидается иное поведение, [смотри документацию](https://docs.python.org/3/library/dataclasses.html#dataclasses.dataclass).

Для переменных класса допускается указание дефолтных значений. При этом переменные с дефолтными значениями должны следовать после переменных без дефолта (в обычном порядке), иначе будет поднят `TypeError`.

Функция `dataclasses.field(*, default=MISSING, default_factory=MISSING, init=True, repr=True, hash=None, compare=True, metadata=None, kw_only=MISSING)` позволяет добавить дополнительную информацию о поле дата-класса.

```python
@dataclass
class C:
    mylist: list[int] = field(default_factory=list)

c = C()
c.mylist += [1, 2, 3]
```

- `default`: если указано, это будет значение по умолчанию для этого поля. Это необходимо, потому что сам вызов `field()` заменяет нзначения по умолчанию
- `default_factory`: если указано, это должна быть вызываемая функция без аргументов, которая будет вызываться, когда для этого поля требуется значение по умолчанию. Помимо прочего, это можно использовать для указания полей с изменяемыми значениями по умолчанию. Нельзя указывать и `default`, и `default_factory`
- `init`: если `True` (по умолчанию), это поле включается в качестве параметра в сгенерированный метод `__init__()`
- `repr`: аналогично
- см. [остальные параметры в доке](https://docs.python.org/3/library/dataclasses.html#dataclasses.field)

Следующие методы реализуют конвертацию в стандартные типы python:

- `dataclasses.asdict(obj, *, dict_factory=dict)` (по факту это глубокая копия)
- `dataclasses.astuple(obj, *, tuple_factory=tuple)` (аналогично)

Так-как используется глубокая копия, это может быть медленно. Если не нужен рекурсивный обход, дешевле может быть вызвать `dataclass_instance.__dict__`. [Ссылка на оверфлоу](https://stackoverflow.com/questions/52229521/why-is-dataclasses-asdictobj-10x-slower-than-obj-dict)

Предоставлен [метод для создания дата-класса](https://docs.python.org/3/library/dataclasses.html#dataclasses.make_dataclass) (это может быть полезно в каких-то фабриках)

```python
C = make_dataclass('C',
                   [('x', int),
                     'y',
                    ('z', int, field(default=5))],
                   namespace={'add_one': lambda self: self.x + 1})

# equal
@dataclass
class C:
    x: int
    y: 'typing.Any'
    z: int = 5

    def add_one(self):
        return self.x + 1
```

После генерации `__init__()` в датаклассе вызывается `__post_init__()`

```python
@dataclass
class C:
    a: float
    b: float
    c: float = field(init=False)

    def __post_init__(self):
        self.c = self.a + self.b
```

Сабклассы не вызывают унаследованный `__init__()`, поэтому хорошим кейсом будет вызывать `__init__()` из родителя через постинит дочернего класса

```python
from dataclasses import dataclass

@dataclass
class Rectangle:
    height: float
    width: float

@dataclass
class Square(Rectangle):
    side: float

    def __post_init__(self):
        super().__init__(self.side, self.side)


@dataclass
class SquareNoInit(Rectangle):
    side: float

one = Rectangle(3.0, 5.0)
print(one)
# Rectangle(height=3.0, width=5.0)

two = Square(1.0, 3.0, 4.0)
print(two)
# Square(height=4.0, width=4.0, side=4.0)

thre = SquareNoInit(1.0, 3.0, 4.0)
print(thre)
# SquareNoInit(height=1.0, width=3.0, side=4.0)
```

Одним из двух мест, где `dataclass()` фактически проверяет тип поля, является определение того, является ли поле переменной класса. Он делает это, проверяя, является ли тип поля `typing.ClassVar`. Если поле является `ClassVar`, оно исключается из рассмотрения как поле и игнорируется механизмами класса данных. Такие псевдополя `ClassVar` не возвращаются функцией `fields()` уровня модуля.

Другое место, где `dataclass()` проверяет аннотацию типа — это определение того, является ли поле переменной только для инициализации. Он делает это, проверяя, относится ли тип поля к типу `dataclasses.InitVar`. Если поле является `InitVar`, оно считается псевдополем, называемым полем только для инициализации. Поскольку это не настоящее поле, оно не возвращается функцией `fields()` уровня модуля. Поля только для инициализации добавляются в качестве параметров в сгенерированный метод `__init__()` и передаются в необязательный метод `__post_init__()`. В противном случае они не используются классами данных. [Подробнее](https://docs.python.org/3/library/dataclasses.html#init-only-variables)

Можно инициализировать looks like неизменяемый инстанс датакласса - при попытке доступа через `__setattr__()` и `__delattr__()` будут подняты ошибки. [Подробнее](https://docs.python.org/3/library/dataclasses.html#frozen-instances)

Стандартная схема наследования python полностью реализована для dataclass

### Известные проблемы

Существует проблема с наследованием от датаклоссов, в которых определены атрибуты с дефолтными значениями.

```python
@dataclass
class A:
    a: str
    aa: str

@dataclass
class B(A):
    b: str = 'b'  # <-- default value

@dataclass
class C(A):
    c: str

@dataclass
class D(B, C):
    d: str
```

В данном случае будет поднята ошибка: `Non-default argument(s) follows default argument(s) defined in B`

Проблема разрешена только в python 3.10 введением `kw_only`

```python
@dataclass
class A:
    a: str
    aa: str

@dataclass
class B(A):
    b: str = 'b'  # <-- default value

@dataclass(kw_only=True)
class C(A):
    c: str

@dataclass(kw_only=True)
class D(B, C):
    d: str
```

[Подробнее](https://medium.com/@aniscampos/python-dataclass-inheritance-finally-686eaf60fbb5)

## [dataclasses-json](https://github.com/lidatong/dataclasses-json)

Эта библиотека предоставляет простой API для кодирования и декодирования классов данных в JSON и обратно. [Docs](https://lidatong.github.io/dataclasses-json/)

Простой пример:

```python
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Person:
    name: str


person = Person(name='lidatong')
person.to_json()  # '{"name": "lidatong"}' <- this is a string
person.to_dict()  # {'name': 'lidatong'} <- this is a dict
Person.from_json('{"name": "lidatong"}')  # Person(1)
Person.from_dict({'name': 'lidatong'})  # Person(1)

# You can also apply _schema validation_ using an alternative API
# This can be useful for "typed" Python code

Person.from_json('{"name": 42}')  # This is ok. 42 is not a `str`, but
                                  # dataclass creation does not validate types
Person.schema().loads('{"name": 42}')  # Error! Raises `ValidationError`

# Another example
from typing import List


@dataclass_json
@dataclass(frozen=True)
class Minion:
    name: str


@dataclass_json
@dataclass(frozen=True)
class Boss:
    minions: List[Minion]


boss = Boss([Minion('evil minion'), Minion('very evil minion')])
boss_json = """
{
    "minions": [
        {
            "name": "evil minion"
        },
        {
            "name": "very evil minion"
        }
    ]
}
""".strip()

assert boss.to_json(indent=4) == boss_json
assert Boss.from_json(boss_json) == boss
```

### Что может пакет

Supported types:

- any arbitrary Collection type is supported. Mapping types are encoded as JSON objects and str types as JSON strings. Any other Collection types are encoded into JSON arrays, but decoded into the original collection types.
- datetime objects. datetime objects are encoded to float (JSON number) using timestamp. As specified in the datetime docs, if your datetime object is naive, it will assume your system local timezone when calling .timestamp(). JSON numbers corresponding to a datetime field in your dataclass are decoded into a datetime-aware object, with tzinfo set to your system local timezone. Thus, if you encode a datetime-naive object, you will decode into a datetime-aware object. This is important, because encoding and decoding won't strictly be inverses. See this section if you want to override this default behavior (for example, if you want to use ISO).
- UUID objects. They are encoded as str (JSON string).
- Decimal objects. They are also encoded as str

Два вида использования:

- декоратор класса
- наследования от миксина

Пример с вложенными датаклассами:

```python
import json
from typing import Set

from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Student:
    id: int = 0
    name: str = ""


@dataclass_json
@dataclass
class Professor:
    id: int
    name: str


@dataclass_json
@dataclass
class Course:
    id: int
    name: str
    professor: Professor
    students: Set[Student]


c_dict = {
    "id": 1, "name": "course",
    "professor": {"id": 1, "name": "professor"},
    "students": [{"id": 1, "name": "student"}]
}

# Using **kwargs to unpack arguments in the constructor
c_unpacked = Course(**c_dict)
# Non-keyword arguments that are already unpacked.
c_construct = Course(1, 'course', Professor(1, 'professor'), {Student(1, 'student')})
# Problem does not occur when loading from JSON
c_json = Course.from_json(json.dumps(c_dict))


assert c_unpacked.to_json() == c_construct.to_json()  # Pass

assert isinstance(c_unpacked.professor, Professor)  # Fail, type(c1.professor) is dict
assert isinstance(c_construct.professor, Professor)  # Pass
assert isinstance(c_json.professor, Professor)  # Pass

assert c_json == c_construct  # Pass
assert c_unpacked == c_construct  # Fail
```

[Источник](https://github.com/lidatong/dataclasses-json/issues/39#issuecomment-446046164)

Еще:

- Encode or decode from camelCase (or kebab-case)
- Encode or decode using a different name
- Handle missing or optional field values when decoding
- Handle unknown / extraneous fields in JSON
- Handle recursive dataclasses
- Using the dataclass_json decorator or mixing in DataClassJsonMixin will provide you with an additional method .schema()
- Overriding / Extending

Смотри еще:

- [документация](https://docs.python.org/3/library/dataclasses.html#frozen-instances)
- [[python-decorator]]
- [[python-datamodel]]
- [[convert-dcit-to-dataclass]]
- [[python-standart-library]]
- [dataclasses-json](https://github.com/lidatong/dataclasses-json)
- [marshmallow](https://marshmallow.readthedocs.io/en/stable/api_reference.html#schema) A lightweight library for converting complex objects to and from simple Python datatypes. [on github](https://github.com/marshmallow-code/marshmallow)
- [[2022-10-23-daily-note]] dataclass literal and dataclass dynamic fields

[//begin]: # "Autogenerated link references for markdown compatibility"
[python-decorator]: python-decorator "Python decorator"
[python-datamodel]: ..%2Flists%2Fpython-datamodel "Python datamodel"
[convert-dcit-to-dataclass]: convert-dcit-to-dataclass "Convert dict to dataclass or namedtuple"
[python-standart-library]: ..%2Flists%2Fpython-standart-library "Стандартная библиотека python и полезные ресурсы"
[2022-10-23-daily-note]: ..%2Fposts%2F2022-10-23-daily-note "Screenshoots with pytests amd dataclass fields dynamicaly and literal choices"
[//end]: # "Autogenerated link references"