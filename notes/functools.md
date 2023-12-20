---
description: Высокоуровневые функции и операции над объектами в стандартной библиотке python
tags: python-standart-library python
title: Functools
---
Модуль [functools](https://docs.python.org/3/library/functools.html) предоставляют АПИ для адаптации и расширения функций и вызываемых объектов без их измененеия. Включает в себя функции декораторы, реализующие аспектно-ориентирвоанное программирование и повторное использование кода.

## [cache](https://docs.python.org/3/library/functools.html#functools.cache)

Аналог `lru_cache(maxsize=None)`

## [cached_property](https://docs.python.org/3/library/functools.html#functools.cached_property)

Преобразует метод класса в свойство, значение которого считается только один раз, а затем кешируется как обычный атрибут

```python
class DataSet:

    def __init__(self, sequence_of_numbers):
        self._data = tuple(sequence_of_numbers)

    @cached_property
    def stdev(self):
        return statistics.stdev(self._data)
```

У декоратора есть отличия в реализации по сравнению со стандартным `@property`. Смотри документацию.

Чего-то аналогичного можно достигнуть так:

```python
class DataSet:

    def __init__(self, sequence_of_numbers):
        self._data = tuple(sequence_of_numbers)
    self.__stdev = None

    @property
    def stdev(self):
        if self.__stdew is None:
            self.__stdew = statistics.stdev(self._data)
        return self.__stdew
```

Значение кеэша можно очистить, удалив атрибут. Декоратор будет работать, только если атрибут с таким же именем, как декорируемое свойство, отсутствует.

## [cmp_to_key](https://docs.python.org/3/library/functools.html#functools.cmp_to_key)

Интерфыейс сравнения объектов для покрытия методов, сконверченных из python2

## [lru_cache](https://docs.python.org/3/library/functools.html#functools.lru_cache)

Декоратор, задающий кэш возврата функции. Работает по принципу вытеснения из кэша последнего использовавшегося объекта. Декоратор требует хэшируемых атррибутов функции и предоставляет методы проверки состояния кэша. Есть возможность задать длину кэша.

```python
@lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)

[fib(n) for n in range(16)]
>>> [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]

>>> fib.cache_info()
>>> CacheInfo(hits=28, misses=16, maxsize=None, currsize=16)
```

## [total_ordering](https://docs.python.org/3/library/functools.html#functools.total_ordering)

Реализует расширенное сравнение объектов. Данный декоратор получает класс, который предоставляет лишь часть методов сравнения (`__lt__()`, `__le__()`, `__eq__()`, `__ne__()`, `__gt__()`, `__ge__()`) и добавляет остальные.

```python
import functools
import inspect
from pprint import pprint


@functools.total_ordering
class MyObject:

    def __init__(self, val):
        self.val = val

    def __eq__(self, other):
        print('  testing __eq__({}, {})'.format(
            self.val, other.val))
        return self.val == other.val

    def __gt__(self, other):
        print('  testing __gt__({}, {})'.format(
            self.val, other.val))
        return self.val > other.val
```

Если сравнение не может быть выполнено - вернется `NotImplemented`

## [partial](https://docs.python.org/3/library/functools.html#functools.partial)

Используется в качестве обертки вокруг вызываемого объекта, задавая значения по умолчанию для части или всех его аругментов. С результирующим объектом можно работать как с исходным.

`partial` не имеет `__doc__` и `__name__`. Их можно задать.

```python
from functools import partial

basetwo = partial(int, base=2)
basetwo.__doc__ = 'Convert base 2 string to an int.'
basetwo('10010')
>>> 18
```

Или передать из оборачиваемой функции при помощи `ipdate_wrapper()` (см. дальше)

## [partialmethod](https://docs.python.org/3/library/functools.html#functools.partialmethod)

Реализует тоже самое, но только для определения методов

```python
class Cell:
    def __init__(self):
        self._alive = False
    @property
    def alive(self):
        return self._alive
    def set_state(self, state):
        self._alive = bool(state)
    set_alive = partialmethod(set_state, True)
    set_dead = partialmethod(set_state, False)

c = Cell()
c.alive
>>> False
c.set_alive()
c.alive
>>> True
```

## [reduce](https://docs.python.org/3/library/functools.html#functools.reduce)

Получает вызываемый объект и последовательность данных в качестве аргументов. Результат работы функции - последовательный вызов объекта с накоплением результата.

```python
import functools

def do_reduce(a, b):
    print('do_reduce({}, {})'.format(a, b))
    return a + b

data = range(1, 5)
result = functools.reduce(do_reduce, data)
print('result: {}'.format(result))
>>> do_reduce(1, 2)
>>> do_reduce(3, 3)
>>> do_reduce(6, 4)
>>> result: 10
```

При этом можно задать инициализирующее значение через `initializer` - с него будет начинаться операция редуцирования. Если функция получила пустой список и инциализатор - она редуцирует к иницализирующему значению. Если в списке только одно значение и нет иницализатора - произойдет редукция к значению в списке. Если передан только пустой список, будет поднята ошибка `TypeError`

## [singledispatch](https://docs.python.org/3/library/functools.html#functools.singledispatch)

Декоратор позволяет реализовать обобщенную функцию - функция, которая ведет себя по разному, в зависимости от типа переданного аргумента

```python
import functools


@functools.singledispatch
def myfunc(arg):
    print('default myfunc({!r})'.format(arg))


@myfunc.register(int)
def myfunc_int(arg):
    print('myfunc_int({})'.format(arg))


@myfunc.register(list)
def myfunc_list(arg):
    print('myfunc_list()')
    for item in arg:
        print('  {}'.format(item))
```

Можно регистрировать лямбда-функции. Можно стакать регистрации над функциями. Если для специфичного типа ничего не зарегистрировано - будет предпринята попытка найти более подходящую имплементацию по дереву наследования. Смотри доку

## [singledispatchmethod](https://docs.python.org/3/library/functools.html#functools.singledispatchmethod)

Аналогично реализует дженерик-методы классов

## [update_wrapper](https://docs.python.org/3/library/functools.html#functools.update_wrapper)

Релизует передачу свойств оборачиваемого объекта оберачивающей функции. [wraps](https://docs.python.org/3/library/functools.html#functools.wraps) реализует это же на уровне декоратора. Это позволяет получить имя обернутого объекта и его докстринги

```python
from functools import wraps
def my_decorator(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        print('Calling decorated function')
        return f(*args, **kwds)
    return wrapper

@my_decorator
def example():
    """Docstring"""
    print('Called example function')

example()
>>> Calling decorated function
>>> Called example function
example.__name__
>>> example
example.__doc__
>>> Docstring
```

[[python-standart-library]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[python-standart-library]: ..%2Flists%2Fpython-standart-library "Стандартная библиотека python и полезные ресурсы"
[//end]: # "Autogenerated link references"