---
description: Дескрипторы в python
tags: python-standart-library python
title: Python descriptors
---
В python существует три варианта доступа к атрибуту:

1. Получить значение атрибута, var = obj.a
2. Изменить значение, obj.a = 'new value'
3. Удалить атрибут, del obj.a

Python позволяет перехватить доступ к атрибуту и переопределить связанное с этим доступом поведение. Это реализуется через механизм протокола дескрипторов.

Чаще всего это используется для проверки данных, передаваемых в атрибут.

Дескриптор - это любой объект, который определяет методы `__get__()`, `__set__()` или `__delete__()`.

Исплементация дескрипторов описана [тут](https://docs.python.org/3/reference/datamodel.html#implementing-descriptors)

Пример реализации:

```python
>>> class NonNegative:

...     def __init__(self, name):
...         self.name = name

...     def __get__(self, instance, owner):
...         return instance.__dict__[self.name]

...     def __set__(self, instance, value):
...         if value < 0:
...             raise ValueError('Cannot be negative.')
...         instance.__dict__[self.name] = value

>>> class Order:

...     price = NonNegative('price')
...     quantity = NonNegative('quantity')

...     def __init__(self, name, price, quantity):
...         self._name = name
...         self.price = price
...         self.quantity = quantity

...     def total(self):
...         return self.price * self.quantity

>>> apple_order = Order('apple', 1, 10)
>>> apple_order.total()
10
>>> apple_order.price = -10
ValueError: Cannot be negative
>>> apple_order.quantity = -10
ValueError: Cannot be negative
```

Пример взят из [этой статьи](https://webdevblog.ru/chto-takoe-deskriptory-i-ih-ispolzovanie-v-python-3-6/). В данном случае мы определили класс дескриптора и класс владельца, в котором класс дескриптора используется для инициализации атрибутов. При попытке установить неприемлемое значение в атрибут будет вызван `ValueError`. Такая реализация является типичной для до python 3.6.

В настоящий момент это можно реализовать короче (измененеия отмечены #):

```python
>>> class NonNegative:

...     def __get__(self, instance, owner):
...         return instance.__dict__[self.name] #

...     def __set__(self, instance, value):
...         if value < 0:
...             raise ValueError('Cannot be negative.')
...         instance.__dict__[self.name] = value

...     def __set_name__(self, owner, name): #
...         self.name = name #

>>> class Order:

...     price = NonNegative() #
...     quantity = NonNegative() #

...     def __init__(self, name, price, quantity):
...         self._name = name
...         self.price = price
...         self.quantity = quantity

...     def total(self):
...         return self.price * self.quantity
```

`object.__get__(self, instance, owner=None)` вызывается для получения атрибута класса-владельца (доступ к атрибуту класса) или экземпляра этого класса (доступ к атрибуту экземпляра). Необязательный аргумент `owner` - это класс владельца, в то время как `instance` - это экземпляр, через который был осуществлен доступ к атрибуту, или `None`, если доступ к атрибуту осуществляется через владельца. Этот метод должен возвращать вычисленное значение атрибута или вызывать исключение `AttributeError`. PEP 252 указывает, что `__get __()` вызывается с одним или двумя аргументами. Собственные встроенные дескрипторы python поддерживают эту спецификацию; однако вполне вероятно, что некоторые сторонние инструменты имеют дескрипторы, требующие обоих аргументов. Собственная реализация Python `__getattribute __()` всегда передает оба аргумента независимо от того, требуются они или нет.

`object.__set__(self, instance, value)` вызывается для установки в экземпляре `instance` класса-владельца нового значения атрибута `value`. Добавление `__set __()` или `__delete __()` изменяет тип дескриптора на «дескриптор данных».

`object.__delete__(self, instance)` вызывается для удаления атрибута в экземпляре `instance` класса владельца. Атрибут `__objclass__` интерпретируется модулем проверки как указывающий класс, в котором был определен этот объект (соответствующая установка этого параметра может помочь в самоанализе динамических атрибутов класса во время выполнения). Для вызываемых объектов это может указывать на то, что экземпляр данного типа (или подкласса) ожидается или требуется в качестве первого позиционного аргумента (например, CPython устанавливает этот атрибут для несвязанных методов, реализованных в C).

Данные методы применяются только тогда, когда экземпляр класса, содержащего метод (так называемый класс дескриптора), появляется в классе владельца (дескриптор должен находиться либо в словаре класса владельца, либо в словаре классов для одного из его родителей).

Про порядок вызовов методов дескриптора в разных чулаях [читай подробнее тут](https://docs.python.org/3/reference/datamodel.html#invoking-descriptors)

Методы python (в том числе `@staticmethod` и `@classmethod`) реализованы как non-data дескрипторы. Соответственно, экземпляры могут переопределять декорированные таким образом методы. Это позволяет отдельным экземплярам приобретать поведение, которое отличается от поведения других экземпляров того же класса.

Функция `property()` реализована как дескриптор данных. Соответственно, экземпляры не могут переопределить поведение property.

## [Descriptor HowTo](https://docs.python.org/3/howto/descriptor.html#descriptorhowto)

В статье документации приводистя большое число примеров реализации и обьъясняются особенности констирукции.

Например здесь класс `Person` имеет два экземпляра дескриптора, `name` и `age`. Когда класс `Person` определяется, он выполняет обратный вызов `__set_name__()` в `LoggedAccess`, чтобы можно было определить имена полей, давая каждому дескриптору собственное имя `public_name` и `private_name`:

```python
>>> import logging

>>> logging.basicConfig(level=logging.INFO)

>>> class LoggedAccess:

...     def __set_name__(self, owner, name):
...         self.public_name = name
...         self.private_name = '_' + name

...     def __get__(self, obj, objtype=None):
...         value = getattr(obj, self.private_name)
...         logging.info('Accessing %r giving %r', self.public_name, value)
...         return value

...     def __set__(self, obj, value):
...         logging.info('Updating %r to %r', self.public_name, value)
...         setattr(obj, self.private_name, value)

>>> class Person:

...     name = LoggedAccess()                # First descriptor instance
...     age = LoggedAccess()                 # Second descriptor instance

...     def __init__(self, name, age):
...         self.name = name                 # Calls the first descriptor
...         self.age = age                   # Calls the second descriptor

...     def birthday(self):
...         self.age += 1

>>> vars(vars(Person)['name'])
{'public_name': 'name', 'private_name': '_name'}
>>> vars(vars(Person)['age'])
{'public_name': 'age', 'private_name': '_age'}
>>> pete = Person('Peter P', 10)
INFO:root:Updating 'name' to 'Peter P'
INFO:root:Updating 'age' to 10
>>> kate = Person('Catherine C', 20)
INFO:root:Updating 'name' to 'Catherine C'
INFO:root:Updating 'age' to 20
>>> vars(pete)
{'_name': 'Peter P', '_age': 10}
>>> vars(kate)
{'_name': 'Catherine C', '_age': 20}
```

[Более близкий к практике пример](https://docs.python.org/3/howto/descriptor.html#complete-practical-example) - определен дескриптор как абстрактный класс, наследующие классы обязаны определять ряд методов. Их инстансы используются в классе-владельце.

Тут рассматривается [вызов дескрипторов.](https://docs.python.org/3/howto/descriptor.html#overview-of-descriptor-invocation):

- из инстанса
- из класса
- с помощью `super()`

Общие принципы:

- Механизм дескрипторов встроен в методы `__getattribute__()` для `object`, `type` и `super() `
- Дескрипторы вызываются методом `__getattribute__()`
- Классы наследуют этот механизм от `object`, `type` или `super()`
- Переопределение предотвращает автоматические вызовы дескриптора, потому что вся логика дескриптора находится в этом методе
- `object.__ getattribute__()` и `type.__getattribute__()` по-разному вызывают `__get__()`. Первый включает экземпляр и может включать класс. Второй определяет `None` для экземпляра и всегда включает класс
- Дескрипторы данных всегда имеют приоритет над словарями экземпляров
- Дескрипторы, не относящиеся к данным, могут быть переопределены словарями экземпляров

[Пример для ОРМ](https://docs.python.org/3/howto/descriptor.html#orm-example)

Далее описываются [встроенные конструкции python на дескрипторах](https://docs.python.org/3/howto/descriptor.html#pure-python-equivalents)

Properties, bound methods, static methods, class methods и `__slots__` основаны на протоколе дескриптора:

- [property](https://docs.python.org/3/howto/descriptor.html#properties) Вызов `property()` - это краткий способ создания дескриптора данных, который запускает вызов функции при доступе к атрибуту. Встроенная функция `property()` помогает всякий раз, когда пользовательский интерфейс предоставляет доступ к атрибутам, а затем для последующих изменений требуется вмешательство метода
- [функции и методы](https://docs.python.org/3/howto/descriptor.html#functions-and-methods) Используя дескрипторы, не относящиеся к данным, эти два элемента легко объединяются. Функции, хранящиеся в словарях классов, при вызове превращаются в методы. Методы отличаются от обычных функций только тем, что экземпляр объекта добавляется к другим аргументам. По соглашению экземпляр называется self, но может называться этим или любым другим именем переменной
- [static methods](https://docs.python.org/3/howto/descriptor.html#static-methods) Возвращают возвращают базовую функцию без изменений. Хорошими кандидатами на статические методы являются методы, которые не ссылаются на переменную self.
- [class methods](https://docs.python.org/3/howto/descriptor.html#class-methods) В отличие от статических методов, методы класса добавляют ссылку на класс к списку аргументов перед вызовом функции. Этот формат одинаков для экземпляра или класса. Это поведение полезно, когда методу нужна только ссылка на класс, и он не полагается на данные, хранящиеся в конкретном экземпляре. Одно из применений методов класса - создание альтернативных конструкторов класса

Кроме того, дескрипторы [реализуют](https://docs.python.org/3/howto/descriptor.html#member-objects-and-slots) логику `__clots__`

Когда класс определяет `__slots__`, он заменяет словари экземпляров массивом значений слотов фиксированной длины. С точки зрения пользователя, это имеет несколько эффектов:

Во-первых обеспечивает немедленное обнаружение ошибок из-за неправильного написания атрибутов, т.к. разрешены только имена атрибутов, указанные в `__slots__`

```python
>>> class Vehicle:
...     __slots__ = ('id_number', 'make', 'model')

>>> auto = Vehicle()
>>> auto.id_nubmer = 'VYE483814LQEX'
Traceback (most recent call last):
    ...
AttributeError: 'Vehicle' object has no attribute 'id_nubmer'
```

Во-вторых помогает создавать неизменяемые объекты, в которых дескрипторы управляют доступом к закрытым атрибутам, хранящимся в `__slots__`

```python
>>> class Immutable:

...     __slots__ = ('_dept', '_name')          # Replace the instance dictionary

...     def __init__(self, dept, name):
...         self._dept = dept                   # Store to private attribute
...         self._name = name                   # Store to private attribute

...     @property                               # Read-only descriptor
...     def dept(self):
...         return self._dept

...     @property
...     def name(self):                         # Read-only descriptor
...         return self._name

>>> mark = Immutable('Botany', 'Mark Watney')
>>> mark.dept
'Botany'
>>> mark.dept = 'Space Pirate'
Traceback (most recent call last):
    ...
AttributeError: can't set attribute
>>> mark.location = 'Mars'
Traceback (most recent call last):
    ...
AttributeError: 'Immutable' object has no attribute 'location'
```

Кроме того, это `__slots__`:

- Экономит память. В 64-битной сборке Linux экземпляр с двумя атрибутами занимает 48 байтов с `__slots__` и 152 байта без. Этот шаблон проектирования легковесного проекта, вероятно, имеет значение только тогда, когда будет создано большое количество экземпляров.
- Повышает скорость. Чтение переменных экземпляра выполняется на 35% быстрее из `__slots__` (по измерениям с Python 3.10 на процессоре Apple M1)
- Но это блокирует такие инструменты, как `functools.cached_property()`, которым для правильной работы требуется словарь экземпляра

Смотри еще:

- [[python-standart-library]]
- [[python-datamodel]]
- [[sqlalchemy]]
- [[functools]]
- [[python-patterns]] паттерн strategy с дескриптором

[//begin]: # "Autogenerated link references for markdown compatibility"
[python-standart-library]: ..%2Flists%2Fpython-standart-library "Стандартная библиотека python и полезные ресурсы"
[python-datamodel]: ..%2Flists%2Fpython-datamodel "Python datamodel"
[sqlalchemy]: ..%2Flists%2Fsqlalchemy "Sqlalchemy"
[functools]: functools "Functools"
[python-patterns]: python-patterns "Python patterns programming"
[//end]: # "Autogenerated link references"