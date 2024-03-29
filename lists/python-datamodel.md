---
description: Модель данных в python
tags: python-standart-library python
title: Python datamodel
---
## Объекты, значения и типы

У каждого объекта в python есть id, имя и значение. Объект можно представить через адрес в памяти - его идентичность никогда не меняется после создания - `is` сравнивает идентичность, а `id()` возвращает айдишник объекта (в CPython это представление адреса в памяти).

Тип объекта определяет операции, которые поддерживаются объектом и возможные значения объекта. `type()` возвращает тип объекта. Значение типа может меняться после создания объекта - объекты с изменяемыми типами называются изменяемыми. При этом объекты-контейнеры с неизменяемым типом (к примеру кортежи) могут "содержать" объекты с изменяемым типом. Контейнеры содержат не сами объекты, а ссылки на них, поэтому при изменении объектов, на которые указывают ссылки контейнеров, следует ожидать изменения и при вызове контейнеров.

Объекты в python не уничтожаются явным способом, но при отсутствии ссылок на них, их может собрать сборщик мусора. CPython использует схему подсчета ссылок с отложенным подсчетом циклических ссылок, что обеспечивает удаление большинства объектов, на которые никто не ссылается... но не гарантирует удаление всех подобных объектов. Трассировка, отладка и перехват исключений с помощью `try... except` могут приводить к сохранению ссылок на объекты. Всегда следует явно закрывать открытые файлы через `close()` (если предоставлен), `try... finally` или менеджеры контекста `with...`

### Иерархия типов

#### `None`

Используется для обозначения отсутствия значения

#### `NotImplemented`

Численные методы и методы сравнения должны возвращать этот тип, если они не реализуют операцию для представленных операндов. Данный тип не следует использовать в логическом контексте

### `Ellipsis` многоточие `...`

#### [numbers.Number](https://docs.python.org/3/library/numbers.html#numbers.Number)

Все числовые типы неизменяемы

- Строковsе представление подчиняется следующим правилам:
  - это действительные числовые литералы, которые при передаче их конструктору класса создают объект, имеющий значение исходного числа
  - если возможно, представление выполняется в базе 10
  - начальные нули, за исключением одного нуля перед десятичной точкой, не отображаются
  - завершающие нули, за исключением одного нуля после десятичной точки, не отображаются
  - знак отображается только тогда, когда число отрицательное
- [numbers.Integral](https://docs.python.org/3/library/numbers.html#numbers.Integral) целые числа
  - [int](https://docs.python.org/3/library/functions.html#int) целые числа в неограниченном диапазоне (верхний предел ограничен памятью).
  - [bool](https://docs.python.org/3/library/functions.html#bool) логические числа `False/True`, ведут себя как 0 и 1 за исключением преобразования в строку
- [numbers.Real](https://docs.python.org/3/library/numbers.html#numbers.Real) реализуют [float](https://docs.python.org/3/library/functions.html#float) числа с плавающей точкой двойной точности машинного уровня, которая зависит от реализации интерпретатора.
- [numbers.Complex](https://docs.python.org/3/library/numbers.html#numbers.Complex) реализует [complex](https://docs.python.org/3/library/functions.html#complex) комплексные числа как пару float чисел. Обе части для числа z можно получить так: `z.real` и `z.imag`

#### Sequences

Конечные упорядоченные наборы объектов, индексированные неотрицательными числами. Последовательность имеет длину, поддерживает операцию нарезки (в т.ч. расширенную, с шагом).

- **Неизменяемые**
  - Strings последовательность значений Unicode символов
  - Tuples последовательность произвольных объектов python
  - Bytes последовательность состоящая из объектов байтов (неизменяемые объекты длиной 8 бит, состоящие из чисел в диапазоне 0<X<=256)
- **Изменяемые**
  - Lists
  - Byte Arrays

#### Sets

Конечные неупорядоченные наборы уникальных неизменяемых объектов. Не индексируются. Имеют длину

- Sets изменяемый тип
- Frozen sets неизменяемые

#### Mappings (отображения)

Конечные наборы объектов, индексированные произвольным набором индексов. Имеют длину

- Dicts - для индекса словарей неприменимы объекты, содержащие изменяемые типы, которые сравниваются по значению, а не по хешу. Это связано с тем, что хеш ключа должен быть неимзенным. Начиная с 3.6 словари сохраняют порядок вставки, а замена ключа не меняет порядок, однако удаление и новая вставка добавляет ключ в конец.

Пример с использованием двух чисел, имеющих одинаковый хеш, провоцирующий неожиданное поведение.

```python
>>> d = {1: 100, 1.0: 200}
>>> print(d)

{1: 200}
```

#### Calable tipes

Типы, к которым можно применить [операцию вызова](https://docs.python.org/3/reference/expressions.html#calls). Это пользовательские функции, методы встроенных классов, объекты классов, методы экземпляров классов и все объекты, реализующие  метод `__call__()`.

Аргументы вызываемых типов оцениваются до вызова следующим образом: первым делом создается список незаполненных слотов для параметров. Если имеется N позиционных аргументов, они помещаются в первые N слотов. Если присутствуют ключевые аргументы, они преобразуются в позиционные аргументы. Для каждого ключевого аргумента его идентификатор используется для определения соответствующего слота (если идентификатор совпадает с именем первого формального параметра, используется первый слот и т. д.). Если слот уже заполнен, возникает исключение TypeError. В противном случае значение аргумента помещается в слот, заполняя его. Когда все аргументы обработаны, пустые слоты заполняются соответствующим значением по умолчанию из определения функции. Значения по умолчанию вычисляются один раз, когда функция определена; таким образом, изменяемые объекты, используемые в качестве значений по умолчанию, будут использованы всеми вызовами, что может привести к нежелательному поведению. Если есть какие-либо незаполненные слоты, для которых не указано значение по умолчанию, возникает исключение TypeError. В противном случае список заполненных слотов используется в качестве списка аргументов для вызова.

Попытка переопределить уже заполненный слот

```python
>>> def my(a, b, c=4):
...     print(a + b + c)

>>> my(1, 2, b=3)
Traceback (most recent call last):
  File "<string>", line 4, in <module>
TypeError: my() got multiple values for argument 'b'
```

Использование изменяемого объекта при повторных вызовах приводит к неожиданному поведению

```python
>>> def my(a, b=[]):
...     print(b)
...     b.append(a)
...     print(b)

>>> my(1)
[]
[1]
>>> my(2)
[1]
[1, 2]
```

Основные типы вызываемых объектов:

- **User-defined functions** (пользорвательские функции) создаются определением функции со списком аргументов, содержащим тоже кол-во аргументов, что и формальных параметров функции. Специфические атрибуты представлены ниже

| Атрибут | Значение | |
|-|-|-|
| `__doc__` | Строка документации функции или, `None` если она недоступна; не наследуется подклассами | запись/чтение |
| `__name__` | Имя функции | запись/чтение |
| `__qualname__` | [Квалифицированное имя](https://docs.python.org/3/glossary.html#term-qualified-name) - включающее путь от глобальной области видимости | запись/чтение |
| `__module__` | Имя модуля, в котором функция была определена, или `None` если он недоступен | запись/чтение |
| `__defaults__` | Кортеж, содержащий значения аргументов по умолчанию для тех аргументов, которые имеют значения по умолчанию, или `None` если аргументы не имеют значения по умолчанию | запись/чтение |
| `__code__` | Объект кода, представляющий тело скомпилированной функции | запись/чтение |
| `__globals__` | Ссылка на словарь, содержащий глобальные переменные функции - глобальное пространство имен модуля, в котором функция была определена | только чтение |
| `__dict__` | Пространство имен, поддерживающее атрибуты функции | запись/чтение |
| `__closure__` | `None` или кортеж, содержащий привязки замыканий | только чтение |
| `__annotations__` | Словарь с аннотациями параметров. Ключи - это имена параметров и 'return' для аннотации возврата, если она есть | запись/чтение |
| `__kwdefaults__` | Словарь, содержащий значения по умолчанию для ключевых параметров. Если мы не определим * между позиционными и ключевыми параметрами, то вместо словаря будет `None`... а если определим, то `None` будет в `__defaults__` | запись/чтение |

Пример

```python
>>> z = 3
>>> def my(a: int, *, b: int = 3) -> int:
...     """This is doc"""
...     def this():
...         return a + b + z
...     return this

>>> print(my.__doc__)
This is doc
>>> print(my.__name__)
my
>>> print(my.__qualname__)
my
>>> print(my.__module__)
__main__
>>> print(my.__defaults__)
None
>>> print(my.__code__)
<code object my at 0x7fae9a4883a0, file "<string>", line 2>
>>> print(my.__globals__)
{'__name__': '__main__','__doc__': None, '__package__': None,
'__loader__': <class '_frozen_importlib.BuiltinImporter'>,
'__spec__': None, '__annotations__': {},
'__builtins__': <module 'builtins' (built-in)>, 'z': 3,
'my': <function my at 0x7fee736c9d30>}
>>> my.n = 4
>>> print(my.__dict__)
{'n': 4}
>>> print(my.__closure__)
None
>>> print(my.__annotations__)
{'a': <class 'int'>, 'b': <class 'int'>, 'return': <class 'int'>}
>>> print(my.__kwdefaults__)
{'b': 3}

>>> f = my(1)
>>> print(f.__closure__)
(<cell at 0x7fee738214c0: int object at 0x955e40>,
 <cell at 0x7fee7372cd90: int object at 0x955e80>)
```

- Instance methods - объект метода экземпляра объединяет класс, инстанс класса и вызываемый объект (обычно пользовательскую функцию).

Специальные атрибуты только для чтения: `__self__` это объект экземпляра класса, `__func__` это объект функции; `__doc__` документация метода (то же, что и `__func__.__doc__`); `__name__` это имя метода (то же, что и `__func__.__name__`); `__module__`- это имя модуля, в котором был определен метод, или None если он недоступен.

Пример

```python
>>> class My():

...     def my(self):
...         """This is the doc"""
...         pass

>>> m = My()

>>> print(m.my.__self__)
<__main__.My object at 0x7fb701ba44c0>
>>> print(m.my.__doc__)
This is the doc
>>> print(m.my.__func__)
<function My.my at 0x7fb701a4cdc0>
>>> print(m.my.__name__)
my
>>> print(m.my.__module__)
__main__
```

Объект создается при получении атрибута класса. если этот атрибут является функцией или методом класса.

Когда объект метода экземпляра создается путем извлечения функции из экземпляра класса `__self__` является экземпляром, а объект метода называется связанным (bound method). `__func__` - это исходный объект функции.

Когда объект метода экземпляра создается путем извлечения объекта метода класса из класса, его `__self__` атрибутом является сам класс, а его `__func__` атрибутом является объект функции, лежащий в основе метода класса.

```python
>>> class My:
...     def foo(self):
...         pass

>>> def this():
...     pass

>>> def that():
...     pass

>>> My.this = this
>>> m = My()
>>> m.that = that

>>> if __name__ == '__main__':
...     print(this)
<function this at 0x7fdc845c9a60>
...     print(My.this)
<function this at 0x7fdc845c9a60>
...     print(m.this)
<bound method this of <__main__.My object at 0x7fdc84698400>>
...     print(m.this.__func__)
<function this at 0x7fdc845c9a60>
...     print(m.this.__self__)
<__main__.My object at 0x7fdc84698400>
...     print(m.that)
<function that at 0x7fdc845c9af0>
```

Преобразование объекта функции в объект метода экземпляра происходит каждый раз, когда атрибут извлекается из экземпляра. В некоторых случаях хорошей оптимизацией является присвоение атрибута локальной переменной и вызов этой локальной переменной. Это преобразование происходит только для пользовательских функций; другие вызываемые объекты (и все невызываемые объекты) извлекаются без преобразования. Определяемые пользователем функции, которые являются атрибутами экземпляра класса, не преобразуются в связанные методы; это происходит только тогда, когда функция является атрибутом класса.

- **Generator functions** - функция или метод, использующий `yield` оператор. Такая функция при вызове всегда возвращает объект-итератор, который можно использовать для выполнения тела функции: вызов `iterator.__next__()` метода итератора приведет к выполнению функции до тех пор, пока она не предоставит значение с помощью `yield` оператора. Когда функция выполняет `return` оператор или добегает до конца своего тела, возникает `StopIteration` исключение, и итератор достигает конца набора возвращаемых значений.

Пример `yield` и `return`

```python
>>> def that():
...     this = [1, 2, 3, 4]
...     for i in this:
...         if i == 3:
...             return 'this is madness'
...         else:
...             yield i

>>> t = that()

>>> print(t)
<generator object that at 0x7f8468a1f580>
>>> print(next(t))
1
>>> print(next(t))
2

>>> try:
...     print(next(t))
>>> except StopIteration as s:
...     print(s)
this is madness

>>> print(list(t))
[]
```

Пример с подъемом ошибки

```python
>>> def that():
...     this = [1, 2, 3, 4]
...     for i in this:
...         try:
...             raise StopIteration
...         except:
...             yield i

>>> t = that()

>>> print(t)
<generator object that at 0x7fa53bbb1580>
>>> for i in range(5):
...     print(next(t))
1
2
3
4
Traceback (most recent call last):
  File "<string>", line 16, in <module>
StopIteration
```

Смотри пример с итератором: [[python-iterators-example]]

- **Coroutine functions** - функции определенные с `async def` возвращает экземпляр сопрограммы. Может содержать выражения `await`, `async with`, `async for`. Подробнее в [[asyncio]]
- **Asynchronous generator functions** - асинхорнные генераторные функции - это функции, определенные с `async def` и `yield` в теле. При вызове возвращает объект асинхронного итератора, который можно использовать для выполнения `async for`. Вызов через [`aiterator.__anext__`](https://docs.python.org/3/reference/datamodel.html#object.__anext__) вернет awaitable объект. Аналогично обычному генератору, при достижении конца тела или при выполнении `return` будет поднеята ошибка `StopAsyncIteration`
- **Built-in functions** объекты встроенных функций интерпретатора (обертка над c-реализациями).
- **Built-in methods** - объекты встроенных методов (пример `alist.append()` при условии, что alist - это соответствующий условиям метода список)
- **Classes** объекты классов. Передача аргументов реализуется через `__new__()` и `__init__()`
- **Class Instances** экземпляры классов, для которых определен `__call__()` в их классе

#### Modules

Объект модуля имеет пространство имен, реализованное объектом словаря, на котоырй будут ссылаться все функции модуля через свой атрибут `__globals__`. Ссылки на атрибуты модуля транслируются в поиск по данному словарю. Подробнее о пространствах имен [[python-namespaces]].

Дефолтно определено и доступно для записи:

- `__name__` имя модуля
- `__doc__` строка документации модуля или, None если она недоступна
- `__file__` путь к файлу, из которого был загружен модуль, если он был загружен из файла. Атрибут может отсутствовать для некоторых типов модулей, таких как модули C, которые статически связаны к интерпретатору. Для модулей расширений, динамически загружаемых из общей библиотеки, это путь к файлу общей библиотеки
- `__annotations__` словарь, содержащий аннотации переменных, собранных во время выполнения тела модуля
- `__dict__` специальный атрибут только для чтения - пространство имен модуля

В CPython словарь модуля будет очищен, когда модуль уйдет из области видимости функции, даже если в словаре все еще есть активные ссылки. Можно скопировать словарь или держать ссылку на модуль в пространстве видимости модуля.

#### Custom classes

Типы пользовательских классов создаются определениями классов. У класса есть пространство имен, реализованное объектом словаря. Ссылки на атрибуты классов переводятся в поисковые запросы в этом словаре. Если имя атрибута там не найдено, поиск атрибута продолжается в родительских классах используя специальную схему разрешения поиска MRO.

Когда ссылка на атрибут класса приводит к объекту метода класса, он преобразуется в объект метода экземпляра, `__self__` атрибут которого принимает сам класс. Если это статический метод, то происходит преобразование в объект статического метода.

Назначения атрибутов класса обновляют словарь текущего класса, а не словарь родительского класса.

Особые атрибуты:

- `__name__` имя класса
- `__module__` имя модуля, в котором был определен класс
- `__dict__` словарь, содержащий пространство имен класса
- `__bases__` кортеж, содержащий родительские классы, в порядке их появления
- `__doc__` строка документации класса или, None если она не определена
- `__annotations__` словарь, содержащий аннотации переменных класса, собранные во время выполнения тела класса

#### Class instances

Экземпляр класса имеет пространство имен, реализованное как словарь. При поиске ссылок на атрибуты этот словарь опрашивается в первую очередь. Если атрибут не найден, а класс экземпляра имеет атрибут с таким именем, поиск продолжается уже в словаре самого класса. Если обнаружен атрибут класса, который является объектом определяемой пользователем функции, он преобразуется в объект метода экземпляра (см.выше), `__self__` атрибут которого является экземпляром. Также преобразуются объекты статических методов и методов класса. Если атрибут класса не найден, а у класса объекта есть `__getattr__()`, для поиска вызывается данный метод.

Назначение и удаление атрибутов обновляют словарь экземпляра, но не словарь класса. Если в классе есть метод `__setattr__()` или `__delattr__()` - они вызываются вместо непосредственного обновления словаря экземпляра.

Экземпляры классов могут выполнять роль чисел, последовательностей или отображений, если у них есть методы с определенными специальными именами. [Смотри список методов](https://docs.python.org/3/reference/datamodel.html#specialnames)

Специальные атрибуты: `__dict__` словарь атрибутов; `__class__` это класс экземпляра.

#### I/O objects - объекты ввода/вывода

Представляют из мебя открытые файлы.

#### Internal types

Некоторые типы, используемые внутри интерпретатора, доступны пользователю. Их определения могут измениться в будущих версиях интерпретатора

- **Code objects**. Объекты кода представляют байт-скомпилированный исполняемый код Python или байт-код. Разница между объектом кода и объектом функции состоит в том, что объект функции содержит явную ссылку на глобальные объекты функции (модуль, в котором он был определен), в то время как объект кода не содержит контекста; также значения аргументов по умолчанию хранятся в объекте функции, а не в объекте кода (поскольку они представляют значения, вычисленные во время выполнения). В отличие от объектов функций, объекты кода неизменяемы и не содержат ссылок (прямо или косвенно) на изменяемые объекты
- **Frame objects**. Представляют собой фреймы исполнения. Они могут встречаться в объектах трассировки ([[traceback]]), а также передаются зарегистрированным функциям трассировки
- **Traceback objects**. Объекты трассировки представляют собой трассировку стека исключения. Объект трассировки неявно создается при возникновении исключения, а также может быть создан явно путем вызова `types.TracebackType`
- **Slice objects**. Объекты среза используются для представления срезов для `__getitem__()` методов. Они также создаются встроенной `slice()` функцией
- **Static method objects**. Объекты статических методов позволяют предотвратить преобразование объектов функций в объекты методов. Объект статического метода - это оболочка вокруг любого другого объекта, обычно объекта метода, определенного пользователем. Когда объект статического метода извлекается из класса или экземпляра класса, фактически возвращаемый объект является обернутым объектом, который не подлежит дальнейшему преобразованию. Эти объекты являются вызываемыми. Можно создавать встроенным `staticmethod()` конструктором
- **Class method objects**. Объект метода класса, как и объект статического метода, представляет собой оболочку вокруг другого объекта, которая изменяет способ получения этого объекта из классов и экземпляров классов. Объекты метода класса создаются встроенным `classmethod()` конструктором.

## Специальные методы

Класс может реализовывать определенные операции, которые вызываются специальным синтаксисом (например, арифметические операции или индексирование и разрезание), определяя методы со специальными именами. Это позволяет классам определять собственное поведение по отношению к операторам языка.

Установка специального метода в значение `None` указывает, что соответствующая операция недоступна. Например, если для класса установлено `__iter__()` значение `None`, итерация этого класса невозможна, поэтому вызов `iter()` его экземпляров вызовет `TypeError` (без возврата к `__getitem__()`).

При реализации класса, который эмулирует любой встроенный тип, важно, чтобы эмуляция была реализована только в той степени, в которой это имеет смысл для моделируемого объекта.

### [Базовые спец.методы](https://docs.python.org/3/reference/datamodel.html#basic-customization)

- [`__new__`](https://docs.python.org/3/reference/datamodel.html#object.__new__) Используется для создания нового экземплояра класса. В основном предназначен для того, чтобы подклассы неизменяемых типов (например, `int`, `str` или `tuple`) могли настраивать создание экземпляров. Он также обычно переопределяется в настраиваемых метаклассах, чтобы настроить создание класса.
- [`__init__`](https://docs.python.org/3/reference/datamodel.html#object.__init__) Конструктор класса. Вызывается после того, как экземпляр был создан `__new__()`, но до того, как он будет возвращен вызывающей стороне. В `self` передается экземпляр, возвращенный в `__new__()`. Если `__new__()` не возвращал `cls`, то и `__init__()` вызван не будет. Аргументы передаются выражению конструктора класса. Если базовый класс имеет `__init__()` метод, метод производного класса `__init__()`, если таковой имеется, должен явно вызывать его, чтобы гарантировать правильную инициализацию части экземпляра базового класса
- [`__del__`](https://docs.python.org/3/reference/datamodel.html#object.__del__). Вызывается при уничтожении инстанса. Если базовый класс имеет `__del__()` метод, метод производного класса `__del__()`, если таковой имеется, должен явно вызывать его, чтобы гарантировать правильное удаление части экземпляра базового класса. Не гарантируется, что `__del__()` методы вызываются для объектов, которые все еще существуют, когда интерпретатор завершает работу. См. [нюансы реализации для cpython](https://docs.python.org/3/reference/datamodel.html#object.__del__)
- [__repr__](https://docs.python.org/3/reference/datamodel.html#object.__repr__) Предоставляет строкове представление объекта. Обычно используется для дебага
- [`__str__`](https://docs.python.org/3/reference/datamodel.html#object.__str__) Человекочитаемое строкове представление. Будет вызван `__repr__()` по умолчанию, если не задан
- [`__bytes__`](https://docs.python.org/3/reference/datamodel.html#object.__bytes__) Представление объекта в виде байт-кода
- [`__format__`](https://docs.python.org/3/reference/datamodel.html#object.__format__) [f-строковое](https://docs.python.org/3/reference/lexical_analysis.html#f-strings) представление. Смотри подробнее [[2021-12-21-daily-note]]
- [`__lt__`, `__le__`, `__eq__`, `__ne__`, `__gt__`, `__ge__`](https://docs.python.org/3/reference/datamodel.html#object.__lt__) Реализуют сравнение объектов
- [`__hash__`](https://docs.python.org/3/reference/datamodel.html#object.__hash__) Вызов встроенной функции `hash()`. Используется так-же для сранвнения
- [`__bool__`](https://docs.python.org/3/reference/datamodel.html#object.__bool__). Реализует проверку истинности. Если этот метод не определен, то вызывается `__len__()`. Если `__len__()` не определен, то все элементы класса считаются истинными.

### [Доступ к атрибутам](https://docs.python.org/3/reference/datamodel.html#customizing-attribute-access)

- [`__getattr__`](https://docs.python.org/3/reference/datamodel.html#object.__getattr__). Этот метод вернет вычисленное значение атрибута, если при попытке доступа поднято исключение `AttributeError`
- [`__getattribute__`](https://docs.python.org/3/reference/datamodel.html#object.__getattribute__). Вызывается безоговорочно для реализации доступа к атрибутам для экземпляров класса. Если класс также определяет `__getattr__()`, последний не будет вызываться, пока `__getattribute__()` не вызовет его явно или пока не будет поднят `AttributeError`. Метод должен вернуть вычисленное значени либо поднять `AttributeError`
- [`__setattr__`](https://docs.python.org/3/reference/datamodel.html#object.__setattr__) Вызывается при попытке присвоения атрибута
- [`__delattr__`](https://docs.python.org/3/reference/datamodel.html#object.__delattr__) Вызывается при попытке удалить атрибут
- [`__dir__`](https://docs.python.org/3/reference/datamodel.html#object.__dir__) Работает, когда мы вызываем объект через `dir()`

[Читай про доступ к атрибутам модуля](https://docs.python.org/3/reference/datamodel.html#customizing-module-attribute-access)

### [Дескрипторы](https://docs.python.org/3/reference/datamodel.html#implementing-descriptors)

Методы применяются только тогда, когда экземпляр класса, содержащего метод (класс дескриптора), появляется в классе владельца `owner` (дескриптор должен находиться либо в словаре класса владельца, либо в словаре классов для одного из его родителей)

- [`__get__(self, instance, owner=None)`](https://docs.python.org/3/reference/datamodel.html#object.__get__) Вызывается для получения атрибута класса-владельца (доступ к атрибуту класса) или экземпляра этого класса (доступ к атрибуту экземпляра). Этот метод должен возвращать вычисленное значение атрибута или вызывать `AttributeError`.
- [`__set__(self, instance, value)`](https://docs.python.org/3/reference/datamodel.html#object.__set__). Вызывается для установки атрибута экземпляра `instance` класса-владельца нового значения.
- [`__delete__(self, instance)`](https://docs.python.org/3/reference/datamodel.html#object.__delete__) Вызывается для удаления атрибута в экземпляре `instance` класса владельца.

Дескриптор является атрибутом объекта со «связыванным поведением», один атрибут доступа которого был изменен с помощью методов в протоколе дескриптора: `__get__()`, `__set__()` и `__delete__()`. Если какой-либо из этих методов определен для объекта, он называется дескриптором.

Поведение по умолчанию для доступа к атрибуту заключается в получении, установке или удалении атрибута из словаря объекта. Если искомое в словаре значение является объектом, определяющим один из методов дескриптора, тогда Python может переопределить поведение по умолчанию и вместо этого вызвать метод дескриптора. То, где это происходит в цепочке приоритетов, зависит от того, какие методы дескриптора были определены и как они были вызваны.

- **Direct Call**. Наиболее простой и распространенный вызов , когда код пользователя непосредственно вызывает метод дескриптора: `x.__get__(a)`
- **Instance Binding**. Если привязка к объекту инстанса, `a.x` трансформируется в вызов: `type(a).__dict__['x'].__get__(a, type(a))`
- **Class Binding**. Если привязка к объекту класса, то `A.x` трансформируется в вызов: `A.__dict__['x'].__get__(None, A)`
- **Super Binding**. Если используется объект, возвращаемый [super](https://docs.python.org/3/library/functions.html#super), тогда связка `super(B, obj).m()` ищет в `obj.__class__.__mro__` родительский класс `A` сразу после `B` и затем вызывает: `A.__dict__['m'].__get__(obj, obj.__class__)`.

Методы Python (в том числе отмеченные символами `@staticmethod` и `@classmethod`) реализованы как дескрипторы, не являющиеся дескрипторами данных. Соответственно, экземпляры могут переопределять методы. Это позволяет отдельным экземплярам приобретать поведение, которое отличается от поведения других экземпляров того же класса.

Функция `property()` реализована в виде дескриптора данных. Соответственно, экземпляры не могут переопределить поведение свойства. Смотри [[python-buildin-functions]]

Подробнее читай тут [[python-descriptors]]

### [`__slots__`](https://docs.python.org/3/reference/datamodel.html#slots)

`__slots__` позволяют явно объявлять данные класса (например, свойства) и запрещать создание `__dict__` и `__weakref__`. Это гарантирует экономию ресурсов при частых вызовах.

[Data model](https://docs.python.org/3/reference/datamodel.html#implementing-descriptors)

### [Настройки при создании класса и метаклассы](https://docs.python.org/3/reference/datamodel.html#customizing-class-creation)

### [Эмуляция универсальных типов](https://docs.python.org/3/reference/datamodel.html#emulating-generic-types)

При использовании аннотации типа, часто бывает полезно использовать параметризацию универсального типа с помощью квадратных скобок. Класс можно параметризовать, только если он определяет специальный метод класса `__class_getitem__()`

Смотри [[typing]]

### [Эмуляция вызываемых объектов](https://docs.python.org/3/reference/datamodel.html#emulating-callable-objects)

`__call__` вызывается, когда инстанс вызывается как функция, если этот метод определен

### [Эмуляция поведения контейнеров](https://docs.python.org/3/reference/datamodel.html#emulating-container-types)

Эта группа методов может быть определена для реализации контейнерных объектов.

Контейнеры обычно представляют собой последовательности (например, lists или tuples) или отображения (например dictionaries), но могут также представлять другие контейнеры.

Первый набор методов используется либо для имитации последовательности, либо для имитации отображения; разница в том, что для последовательности, допустимые ключи должны быть целыми числами `к`, для которых `0 <= k < N`, где `N` представляет собой длину последовательности, или `slice` объектов, которые определяют диапазон элементов.

Рекомендуется, чтобы отображения обеспечивали методы `keys()`, `values()`, `items()`, `get()`, `clear()`, `setdefault()`, `pop()`, `popitem(`), `copy()`, и `update()` что обеспечивает поведение, подобное словарям. `collections.abc` предоставляет абстрактный базовый класс для этих целей.

Изменяемые последовательности должны обеспечивать методы `append()`, `count()`, `index()`, `extend()`, `insert()`, `pop()`, `remove()`, `reverse()` и `sort()` аналогично python спискам.

Последовательности так-же должны реализовывать  `__add__()`, `__radd__()`, `__iadd__()`, `__mul__()`, `__rmul__()` и `__imul__()` методы и другие численные операции.

Рекомендуется реализовать `__contains__()` как для отображений так и для последовательностей, чтобы использовать `in` оператор, а так-же `__iter__()` для итерации.

[Методы, которые так-же могут быть реализованы для контейнеров](https://docs.python.org/3/reference/datamodel.html#emulating-container-types):

- `__len__(self)` вызывается для реализации встроенной функции `len()` и должен возвращать `int` >=0
- `__length_hint__(self)` возвращает оценочную длину объекта (обычно требуется только для оптимизации)
- `__getitem__(self, key)` Вызывается для реализации возврата значения `self[key]`. Для типов последовательностей допустимыми ключами являются целые числа и объекты-срезы
- `__setitem__(self, key, value)` Вызывается для реализации присваивания `self[key]` (только для отображений)
- `__delitem__(self, key)` удаление по ключу (только для отображений)
- `__missing__(self, key)` реализует возврат дефолта, когда ключа нет в словаре
- `__iter__(self)` вызывается, когда для контейнера требуется итератор. Должен возвращать новый объект итератора, который может перебирать все объекты в контейнере. Для отображений он должен перебирать ключи контейнера.
- `__reversed__(self)` реализует встроенную функцию `reversed()`
- `__contains__(self, item)` реализует проверку `in self`

### Эмуляция численных методов

Весь список дефолтных методов [смотри тут](https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types)

### [Контекстные менеджеры](https://docs.python.org/3/reference/datamodel.html#with-statement-context-managers)

Менеджер контекста является объектом, который определяет контекст выполнения. Диспетчер контекста обрабатывает вход и выход из желаемого контекста для выполнения блока кода. Менеджеры контекста обычно вызываются с помощью `with` оператора, но также могут использоваться путем прямого вызова их методов.

Типичные применения диспетчеров контекста включают сохранение и восстановление различных видов глобального состояния, блокировку и разблокировку ресурсов, закрытие открытых файлов и т.д.

- [`__enter__(self)`](https://docs.python.org/3/reference/datamodel.html#object.__enter__) Оператор `with` свяжет возвращаемое значение этого метода с целью (целями), указанными в `as` оператора, если таковые имеются.
- [`__exit__(self, exc_type, exc_value, traceback)`](https://docs.python.org/3/reference/datamodel.html#object.__exit__) Параметры описывают исключение, вызвавшее выход из контекста. Если контекст был закрыт без исключения, все три аргумента будут равны None. Если предоставляется исключение, и метод желает подавить исключение (т. е. предотвратить его распространение), он должен вернуть истинное значение. В противном случае исключение будет обработано нормально при выходе из этого метода.

### [Pattern matching](https://docs.python.org/3/reference/datamodel.html#customizing-positional-arguments-in-class-pattern-matching)

### [Сопрограммы](https://docs.python.org/3/reference/datamodel.html#coroutines)

Реализация `__await__` делает объект awaitable.

Объекты сопрограмм - это awaitable объекты. Выполнением сопрограммы можно управлять путем вызова`__await__()` и повторения результата. Когда сопрограмма завершает выполнение и возвращает управление, итератор поднимает `StopIteration`, а значение атрибута `value` ошибки содержит возвращаемое значение. Если сопрограмма вызывает исключение, оно распространяется итератором. Сопрограммы не должны напрямую вызывать необработанные `StopIteration`.

У сопрограмм также есть методы, которые аналогичны методам генераторов. [Подробнее о методах](https://docs.python.org/3/reference/datamodel.html#coroutine-objects)

Смотри подробнее [[asyncio]]

### [Асинхронные итераторы](https://docs.python.org/3/reference/datamodel.html#asynchronous-iterators)

Асинхронный итератор может вызвать асинхронный код в `__anext__` методе

- [`__aiter__(self)`](https://docs.python.org/3/reference/datamodel.html#object.__aiter__) возвращает объект асинхронного итератора
- [`__anext__(self)`](https://docs.python.org/3/reference/datamodel.html#object.__anext__) возвращает awaitable значение. Должен вызывать `StopAsyncIteration` исключение по окончании итерации.

Пример

```python
class Reader:
    async def readline(self):
        ...

    def __aiter__(self):
        return self

    async def __anext__(self):
        val = await self.readline()
        if val == b'':
            raise StopAsyncIteration
        return val
```

### [Асинхронные менеджеры контекста](https://docs.python.org/3/reference/datamodel.html#asynchronous-context-managers)

Асинхронный менеджер контекста - это контекстный менеджер, способный приостанавливать выполнение. Используется с оператором `await width`

- [`__aenter__(self)`](https://docs.python.org/3/reference/datamodel.html#object.__aenter__) должен возвращать ожидаемый объект
- [`__aexit__(self, exc_type, exc_value, traceback)`](https://docs.python.org/3/reference/datamodel.html#object.__aexit__) аналогично `__exit__`

Пример

```python
class AsyncContextManager:
    async def __aenter__(self):
        await log('entering context')

    async def __aexit__(self, exc_type, exc, tb):
        await log('exiting context')
```

Смотри еще:

- [[python-standart-library]]
- [[python-descriptors]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[python-iterators-example]: ../notes/python-iterators-example "Python iterators"
[asyncio]: ../notes/asyncio "Asyncio"
[python-namespaces]: ../notes/python-namespaces "Python namespaces"
[traceback]: ../notes/traceback "Traceback"
[2021-12-21-daily-note]: ../posts/2021-12-21-daily-note "Formatted string literals specificators"
[python-buildin-functions]: ../notes/python-buildin-functions "Python build-in functions"
[python-descriptors]: ../notes/python-descriptors "Python descriptors"
[typing]: ../notes/typing "Typing"
[python-standart-library]: python-standart-library "Стандартная библиотека python и полезные ресурсы"
[//end]: # "Autogenerated link references"
[//begin]: # "Autogenerated link references for markdown compatibility"
[python-iterators-example]: ../notes/python-iterators-example "Python iterators"
[asyncio]: ../notes/asyncio "Asyncio"
[python-namespaces]: ../notes/python-namespaces "Python namespaces"
[traceback]: ../notes/traceback "Traceback"
[2021-12-21-daily-note]: ../posts/2021-12-21-daily-note "Formatted string literals specificators"
[python-buildin-functions]: ../notes/python-buildin-functions "Python build-in functions"
[python-descriptors]: ../notes/python-descriptors "Python descriptors"
[typing]: ../notes/typing "Typing"
[asyncio]: ../notes/asyncio "Asyncio"
[python-standart-library]: python-standart-library "Стандартная библиотека python и полезные ресурсы"
[python-descriptors]: ../notes/python-descriptors "Python descriptors"
[//end]: # "Autogenerated link references"