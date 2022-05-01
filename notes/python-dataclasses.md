---
description: Датаклассы в python
tags: python-standart-library
title: Python dataclasses
---
Модуль `dataclasses` предоставляет [[python-decorator]] и функции для автоматического добавления сгенерированных специальных методов, таких как `__init__()` и `__repr__()`, в пользовательские классы.

`@dataclasses.dataclass(*, init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False, match_args=True, kw_only=False, slots=False` - декоратор, который используется для добавления сгенерированных специальных методов к классам. Декоратор `dataclass()` проверяет класс, чтобы найти поля. **Поле определяется как переменная класса, имеющая аннотацию типа**. За двумя исключениями, описанными ниже, в `dataclass()` ничто не проверяет тип, указанный в аннотации переменной. Порядок полей во всех сгенерированных методах соответствует порядку, в котором они появляются в определении класса. `dataclass()` так-же добавит в класс дандер-методы. Если какой-либо из добавленных методов уже существует в классе, поведение зависит от параметра декоратора. Декоратор возвращает тот же класс, для которого он был вызван - новый класс не создается. Если `dataclass()` используется просто как простой декоратор без параметров, он действует так, как если бы у него были значения по умолчанию, задокументированные в этой сигнатуре.

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
@dataclass
class Rectangle:
    height: float
    width: float

@dataclass
class Square(Rectangle):
    side: float

    def __post_init__(self):
        super().__init__(self.side, self.side)
```

Одним из двух мест, где `dataclass()` фактически проверяет тип поля, является определение того, является ли поле переменной класса. Он делает это, проверяя, является ли тип поля `typing.ClassVar`. Если поле является `ClassVar`, оно исключается из рассмотрения как поле и игнорируется механизмами класса данных. Такие псевдополя `ClassVar` не возвращаются функцией `fields()` уровня модуля.

Другое место, где `dataclass()` проверяет аннотацию типа — это определение того, является ли поле переменной только для инициализации. Он делает это, проверяя, относится ли тип поля к типу `dataclasses.InitVar`. Если поле является `InitVar`, оно считается псевдополем, называемым полем только для инициализации. Поскольку это не настоящее поле, оно не возвращается функцией `fields()` уровня модуля. Поля только для инициализации добавляются в качестве параметров в сгенерированный метод `__init__()` и передаются в необязательный метод `__post_init__()`. В противном случае они не используются классами данных. [Подробнее](https://docs.python.org/3/library/dataclasses.html#init-only-variables)

Можно инициализировать looks like неизменяемый инстанс датакласса - при попытке доступа через `__setattr__()` и `__delattr__()` будут подняты ошибки. [Подробнее](https://docs.python.org/3/library/dataclasses.html#frozen-instances)

Стандартная схема наследования python полностью реализована для dataclass

Смотри еще:

- [документация](https://docs.python.org/3/library/dataclasses.html#frozen-instances)
- [[python-decorator]]
- [[python-datamodel]]
- [[convert-dcit-to-dataclass]]
- [[python-standart-library]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[python-decorator]: python-decorator "Python decorator"
[python-decorator]: python-decorator "Python decorator"
[python-datamodel]: ../lists/python-datamodel "Python datamodel"
[convert-dcit-to-dataclass]: convert-dcit-to-dataclass "Convert dict to dataclass or namedtuple"
[python-standart-library]: ../lists/python-standart-library "Стандартная библиотека python и полезные ресурсы"
[//end]: # "Autogenerated link references"