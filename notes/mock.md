---
description: Как писать mock-тесты на python
tags: tests python
title: Mock-тесты
---
[unittest.mock](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.MagicMock)

[[unittest]] mock предоставляет базовый `Mock` class. После создания объекта, можно ассертить методы и аттрибуты класса, а так-же возвращать значения и устанавливать атрибуты, если это нужно.

Дополнительно предоставляется `patch()` декоратор который позволяет мокать тестируемые модули и атрибуты уровня класса. `MagicMock` - сабкласс `Mock`, который предоставляет множество магических методов.

```python
from unittest.mock import MagicMock
thing = ProductionClass()
thing.method = MagicMock(return_value=3)
thing.method(3, 4, 5, key='value')

thing.method.assert_called_with(3, 4, 5, key='value')
```

```pyjon
mock = Mock(side_effect=KeyError('foo'))
mock()

>>> Traceback (most recent call last):
 ...
KeyError: 'foo'
```

```python
values = {'a': 1, 'b': 2, 'c': 3}
def side_effect(arg):
    return values[arg]

mock.side_effect = side_effect
mock('a'), mock('b'), mock('c')

mock.side_effect = [5, 4, 3, 2, 1]
mock(), mock(), mock()
```

```python
from unittest.mock import patch
@patch('module.ClassName2')
@patch('module.ClassName1')
def test(MockClass1, MockClass2):
    module.ClassName1()
    module.ClassName2()
    assert MockClass1 is module.ClassName1
    assert MockClass2 is module.ClassName2
    assert MockClass1.called
    assert MockClass2.called

test()
```

```python
with patch.object(ProductionClass, 'method', return_value=None) as mock_method:
    thing = ProductionClass()
    thing.method(1, 2, 3)

mock_method.assert_called_once_with(1, 2, 3)
```

Оригинальное состояние мокируемого объекта будет возвращено, когда тест завершается

```python
foo = {'key': 'value'}
original = foo.copy()
with patch.dict(foo, {'newkey': 'newvalue'}, clear=True):
    assert foo == {'newkey': 'newvalue'}

assert foo == original
```

MagicMock мокирует все маг.методы #python

```python
mock = MagicMock()
mock.__str__.return_value = 'foobarbaz'
str(mock)

>>> 'foobarbaz'

mock.__str__.assert_called_with()
```

Маг.методам можно присваивать функции

```python
mock = Mock()
mock.__str__ = Mock(return_value='wheeeeee')
str(mock)

>>> 'wheeeeee'
```

Autospeck позволяет автоматически создавать моки всех атрибутов и методов функции

```python
from unittest.mock import create_autospec
def function(a, b, c):
    pass

mock_function = create_autospec(function, return_value='fishy')
mock_function(1, 2, 3)

'fishy'

mock_function.assert_called_once_with(1, 2, 3)
mock_function('wrong arguments')

"""Traceback (most recent call last):
 ...
TypeError: <lambda>() takes exactly 3 arguments (1 given)"""
```

## [MocK class](https://docs.python.org/3/library/unittest.mock.html#the-mock-class)

Mock создает вызываемый объект, который создает новые моки атрибутов, когда мы получаем к ним доступ. Атрибуты всегда возвращают одно и тоже значение моков.

```python
class unittest.mock.Mock(spec=None, side_effect=None, return_value=DEFAULT, wraps=None, name=None, spec_set=None, unsafe=False, **kwargs)
```

- specx - список строк или другой объект (например класс или инстанс) - это спецификация мока
- spec_set - список вариантов мока
- side_effect - функция, которая будет вызывана, когда вызван мок
- return_value - значение, которое вернет мок
- см.остальное в доке

Доступны такие ассерты:

- `assert_called()` проверка того, что мок был вызван хотябы однажды
- `assert_called_once()` вызван строго дин раз
- `assert_called_with(*args, **kwargs)` вызван с аргументами

```python
mock = Mock()
mock.method(1, 2, 3, test='wow')
<Mock name='mock.method()' id='...'>
mock.method.assert_called_with(1, 2, 3, test='wow')
```

- `assert_called_once_with(*args, **kwargs)`
- `assert_any_call(*args, **kwargs)` был вызов с любым из аргументов
- `assert_has_calls(calls, any_order=False)` были вызовы в определенном порядке

```python
mock = Mock(return_value=None)
mock(1)
mock(2)
mock(3)
mock(4)
calls = [call(2), call(3)]
mock.assert_has_calls(calls)
calls = [call(4), call(2), call(3)]
mock.assert_has_calls(calls, any_order=True)
```

- `assert_not_called()`

Остальные методы, начиная с [reset_mock()](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock.reset_mock) - различные методы, конфигурирующие моки.

Доступны [асинхронные моки](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.AsyncMock). [[asyncio]]

### [Вызов мока](https://docs.python.org/3/library/unittest.mock.html#calling)

Объект мока вызываемы и возвращает значение, указанное в return_value. Дефолтно мок возвращает новый мок-объект. Возвращаемый объект создается первый раз при первом ассерте, дальше возвращается все время одно и тоже.

Вызовы пишутся в атрибуты call_args and call_args_list. Если задан side_effect, он запускается после создание объекта мока, так что вызов все равно будет записан в атрибут.

```python
m = MagicMock(side_effect=IndexError)
m(1, 2, 3)
Traceback (most recent call last):
  ...
IndexError
m.mock_calls
[call(1, 2, 3)]
m.side_effect = KeyError('Bang!')
m('two', 'three', 'four')
Traceback (most recent call last):
  ...
KeyError: 'Bang!'
m.mock_calls
[call(1, 2, 3), call('two', 'three', 'four')]
```

Если использовать функцию в качестве объекта side_effect, то она принимает аргументы вызова - это позволяет поднимать ошибку или возвращать значения в зависимости от атрибутов мока

```python
def side_effect(value):
    return value + 1

m = MagicMock(side_effect=side_effect)
m(1)
2
m(2)
3
m.mock_calls
[call(1), call(2)]
```

Мы так-же в любой момент можем переопределить сайд эффект и возвращать дефолтно. Два способа как это сделать:

```python
m = MagicMock()
def side_effect(*args, **kwargs):
    return m.return_value

m.side_effect = side_effect
m.return_value = 3
m()
3
def side_effect(*args, **kwargs):
    return DEFAULT

m.side_effect = side_effect
m()
3
```

Чтобы возвращать дефолтное состояние, нужно установить side_effect в `None`

```python
m = MagicMock(return_value=6)
def side_effect(*args, **kwargs):
    return 3

m.side_effect = side_effect
m()
3
m.side_effect = None
m()
6
```

Крмое того, side_effect можно итерирровать

```python
m = MagicMock(side_effect=[1, 2, 3])
m()
1
m()
2
m()
3
m()
Traceback (most recent call last):
  ...
StopIteration
```

И поднимать эксепшены в процессе итерации

```python
iterable = (33, ValueError, 66)
m = MagicMock(side_effect=iterable)
m()
33
m()
Traceback (most recent call last):
 ...
ValueError
m()
66
```

### [Удаление атрибутов](https://docs.python.org/3/library/unittest.mock.html#deleting-attributes)

```python
mock = MagicMock()
hasattr(mock, 'm')
True
del mock.m
hasattr(mock, 'm')
False
del mock.f
mock.f
Traceback (most recent call last):
    ...
AttributeError: f
```

### [Название mocka (атрибут name)](https://docs.python.org/3/library/unittest.mock.html#mock-names-and-the-name-attribute)

### [Использование мока, как атрибута](https://docs.python.org/3/library/unittest.mock.html#attaching-mocks-as-attributes)

При присоединении мока, как атрибута к другому моку, он становится дочерним моком.

```python
parent = MagicMock()
child1 = MagicMock(return_value=None)
child2 = MagicMock(return_value=None)
parent.child1 = child1
parent.child2 = child2
child1(1)
child2(2)
parent.mock_calls
[call.child1(1), call.child2(2)]
```

Другие подробности в статье

## [The patchers](https://docs.python.org/3/library/unittest.mock.html#the-patchers)

Декораторы patch используются для исправления объектов только в рамках функции, которую они декорируют. Они автоматически обрабатывают распаковку, даже если возникают исключения. Все эти функции также могут использоваться в операторах with или в качестве декораторов классов.

```python
unittest.mock.patch(target, new=DEFAULT, spec=None, create=False, spec_set=None, autospec=None, new_callable=None, **kwargs)
```

Может использоваться как декоратор функции, класса или контекст-менеджер.

- target должен быть в формате `'package.module.ClassName'`, Target испортируется и специфицированный объект заменяется на новый
- spec и spec_set пеередается в MagicMock
- new_callable определяет какие новые объекты буду вызваны при создании нового объекта

Подробнее об остальном в статье

```python
>>> @patch('__main__.SomeClass')
... def function(normal_argument, mock_class):
...     print(mock_class is SomeClass)
...
>>> function(None)
True
```

```python
>>> class Class:
...     def method(self):
...         pass
...
>>> with patch('__main__.Class') as MockClass:
...     instance = MockClass.return_value
...     instance.method.return_value = 'foo'
...     assert Class() is instance
...     assert Class().method() == 'foo'
```

Пачт [может получать различные объекты](https://docs.python.org/3/library/unittest.mock.html#patch-object)

```python
@patch.object(SomeClass, 'class_method')
def test(mock_method):
    SomeClass.class_method(3)
    mock_method.assert_called_with(3)

test()
```

```python
foo = {}
@patch.dict(foo, {'newkey': 'newvalue'})
def test():
    assert foo == {'newkey': 'newvalue'}
test()
assert foo == {}
```

```python
with patch.multiple(settings, FIRST_PATCH='one', SECOND_PATCH='two'):
    ...
```

У патчей есть start() и stop() методы. Это упрощает setUp для теста

```python
patcher = patch('package.module.ClassName')
from package import module
original = module.ClassName
new_mock = patcher.start()
assert module.ClassName is not original
assert module.ClassName is new_mock
patcher.stop()
assert module.ClassName is original
assert module.ClassName is not new_mock
```

Пример с сетап-тирдаун

```python
class MyTest(unittest.TestCase):
    def setUp(self):
        self.patcher1 = patch('package.module.Class1')
        self.patcher2 = patch('package.module.Class2')
        self.MockClass1 = self.patcher1.start()
        self.MockClass2 = self.patcher2.start()

    def tearDown(self):
        self.patcher1.stop()
        self.patcher2.stop()

    def test_something(self):
        assert package.module.Class1 is self.MockClass1
        assert package.module.Class2 is self.MockClass2

MyTest('test_something').run()
```

Важно! Если setup вызовет ошибку - tearDown'а уже не будет. Проблему помогает решить [unittest.TestCase.addCleanup()](https://docs.python.org/3/library/unittest.html#unittest.TestCase.addCleanup)

```python
class MyTest(unittest.TestCase):
    def setUp(self):
        patcher = patch('package.module.Class')
        self.MockClass = patcher.start()
        self.addCleanup(patcher.stop)

    def test_something(self):
        assert package.module.Class is self.MockClass
```

Еще доступно вот это: `patch.stopall()`

### [Test prefix](https://docs.python.org/3/library/unittest.mock.html#test-prefix)

Это позволяет передать через декоратор что-то только специфическим методам класса, если декорируется класс. Аналог [unittest.TestLoader](https://docs.python.org/3/library/unittest.html#unittest.TestLoader)

```python
>>> patch.TEST_PREFIX = 'foo'
>>> value = 3
>>>
>>> @patch('__main__.value', 'not three')
... class Thing:
...     def foo_one(self):
...         print(value)
...     def foo_two(self):
...         print(value)
...
>>>
>>> Thing().foo_one()
not three
>>> Thing().foo_two()
not three
>>> value
3
```

### [Декораторы patch можно стакать](https://docs.python.org/3/library/unittest.mock.html#nesting-patch-decorators)

```python
@patch.object(SomeClass, 'class_method')
@patch.object(SomeClass, 'static_method')
def test(mock1, mock2):
    assert SomeClass.static_method is mock1
    assert SomeClass.class_method is mock2
    SomeClass.static_method('foo')
    SomeClass.class_method('bar')
    return mock1, mock2

mock1, mock2 = test()
mock1.assert_called_once_with('foo')
mock2.assert_called_once_with('bar')
```

Остальное смотир в доке

## [MagicMock](https://docs.python.org/3/library/unittest.mock.html#magicmock-and-magic-method-support)

Позволяет мокироват ьмагические методы #python. Если для мока используется функция, ей обязательно необходимо передать self

```python
def __str__(self):
    return 'fooble'
mock = Mock()
mock.__str__ = __str__
str(mock)


mock = Mock()
mock.__str__ = Mock()
mock.__str__.return_value = 'fooble'
str(mock)
'fooble'


mock = Mock()
mock.__iter__ = Mock(return_value=iter([]))
list(mock)
[]
```

Вот так можно замокать контекст-менеджер:

```python
mock = Mock()
mock.__enter__ = Mock(return_value='foo')
mock.__exit__ = Mock(return_value=False)
with mock as m:
    assert m == 'foo'

mock.__enter__.assert_called_with()
mock.__exit__.assert_called_with(None, None, None)
```

Полный список того, что можно замокать:

- \__hash__, \__sizeof__, \__repr__ and \__str__
- \__dir__, \__format__ and \__subclasses__
- \__round__, \__floor__, \__trunc__ and \__ceil__
- Comparisons: \__lt__, \__gt__, \__le__, \__ge__, \__eq__ and \__ne__
- Container methods: \__getitem__, \__setitem__, \__delitem__, \__contains__, \__len__, \__iter__, \__reversed__ and \__missing__
- Context manager: \__enter__, \__exit__, \__aenter__ and \__aexit__
- Unary numeric methods: \__neg__, \__pos__ and \__invert__
- The numeric methods (including right hand and in-place variants): \__add__, \__sub__, \__mul__, \__matmul__, \__div__, \__truediv__, \__floordiv__, \__mod__, \__divmod__, \__lshift__, \__rshift__, \__and__, \__xor__, \__or__, and \__pow__
- Numeric conversion methods: \__complex__, \__int__, \__float__ and \__index__
- Descriptor methods: \__get__, \__set__ and \__delete__
- Pickling: \__reduce__, \__reduce_ex__, \__getinitargs__, \__getnewargs__, \__getstate__ and \__setstate__
- File system path representation: \__fspath__
- Asynchronous iteration methods: \__aiter__ and \__anext__

Данные методы не поддерживаются либо могут вызывать проблемы:

- \__getattr__, \__setattr__, \__init__ and \__new__
- \__prepare__, \__instancecheck__, \__subclasscheck__, \__del__

### [MagicMock](https://docs.python.org/3/library/unittest.mock.html#magic-mock)

Два варианта `MagicMock` and `NonCallableMagicMock`. Первый - это сабкласс от `Mock`, реализующий большинство меджик методов. Второй - его невызываемый собрат. Его конструктор аналогичен первому за исключением того, что return_value и side_effect не имеют значения.

```python
mock = MagicMock()
mock[3] = 'fish'
mock.__setitem__.assert_called_with(3, 'fish')
mock.__getitem__.return_value = 'result'
mock[2]
'result'
```

Доступные методы и их дефолтные значения

- \__lt__: NotImplemented
- \__gt__: NotImplemented
- \__le__: NotImplemented
- \__ge__: NotImplemented
- \__int__: 1
- \__contains__: False
- \__len__: 0
- \__iter__: iter([])
- \__exit__: False
- \__aexit__: False
- \__complex__: 1j
- \__float__: 1.0
- \__bool__: True
- \__index__: 1
- \__hash__: default hash for the mock
- \__str__: default str for the mock
- \__sizeof__: default sizeof for the mock

```python
mock = MagicMock()
int(mock)
1
len(mock)
0
list(mock)
[]
object() in mock
False
```

Подробнее читай доку - есть нюансы. Так-же ест ьметоды, котоыре поддерживаются, но не определены дефолтные значения.

## [Helpers](https://docs.python.org/3/library/unittest.mock.html#helpers)

`unittest.mock.sentinel` простйо способ создавать уникальные объекты для тестов
`unittest.mock.DEFAULT` заранее созданный сентинел. Как используется - смотри выше, там где обсуждался вывод дефолтного значения в side_effect
`unittest.mock.call(*args, **kwargs)` хелпер для упрощения ассершена

```python
m = MagicMock(return_value=None)
m(1, 2, a='foo', b='bar')
m()
m.call_args_list == [call(1, 2, a='foo', b='bar'), call()]
True
```

Реализованы методы call_args, call_args_list, mock_calls и method_calls. [Подробнее](https://docs.python.org/3/library/unittest.mock.html#call)

- `unittest.mock.create_autospec(spec, spec_set=False, instance=False, **kwargs)` позволяет создать мок, используя другой объект в качестве спецификации. [Подробный пример тут](https://docs.python.org/3/library/unittest.mock.html#auto-speccing)
- `unittest.mock.ANY` позволяет создать аргумент с "абсолютно любым значением"

```python
mock = Mock(return_value=None)
mock('foo', bar=object())
mock.assert_called_once_with('foo', bar=ANY)
```

```python
m = MagicMock(return_value=None)
m(1)
m(1, 2)
m(object())
m.mock_calls == [call(1), call(1, 2), ANY]
True
```

- `unittest.mock.FILTER_DIR`
- `unittest.mock.mock_open(mock=None, read_data=None)`
- `unittest.mock.seal(mock)`

## [Monkeypatching/mocking modules and environments](https://docs.pytest.org/en/6.2.x/monkeypatch.html)

Моки модулей и окружений можно делать в [[pytest]]. The `monkeypatch` fixture helps you to safely set/delete an attribute, dictionary item or environment variable, or to modify sys.path for importing

```python
monkeypatch.setattr(obj, name, value, raising=True)
monkeypatch.delattr(obj, name, raising=True)
monkeypatch.setitem(mapping, name, value)
monkeypatch.delitem(obj, name, raising=True)
monkeypatch.setenv(name, value, prepend=False)
monkeypatch.delenv(name, raising=True)
monkeypatch.syspath_prepend(path)
monkeypatch.chdir(path)
```

Все модификации удаляются после того, как запрашиваемая функция в фикстуре выполняется. raising параметр определяет, что происходит при KeyError или AttributeError

Когда надо использовать?

- модифицировать методы API
- заменить значения словарей
- заменить переменные окружения
- заменить контекст, например текущие рабочие директории
- подменить `sys.path`

Простой пример

```python
# contents of test_module.py with source code and the test
from pathlib import Path


def getssh():
    """Simple function to return expanded homedir ssh path."""
    return Path.home() / ".ssh"


def test_getssh(monkeypatch):
    # mocked return function to replace Path.home
    # always return '/abc'
    def mockreturn():
        return Path("/abc")

    # Application of the monkeypatch to replace Path.home
    # with the behavior of mockreturn defined above.
    monkeypatch.setattr(Path, "home", mockreturn)

    # Calling getssh() will use mockreturn in place of Path.home
    # for this test with the monkeypatch.
    x = getssh()
    assert x == Path("/abc/.ssh")
```

Можно мокать возвращаемый объект, для этого надо [создать мок-класс](https://docs.pytest.org/en/6.2.x/monkeypatch.html#monkeypatching-returned-objects-building-mock-classes)

```python
# contents of app.py, a simple API retrieval example
import requests


def get_json(url):
    """Takes a URL, and returns the JSON."""
    r = requests.get(url)
    return r.json()
```

```python
# contents of test_app.py, a simple test for our API retrieval
# import requests for the purposes of monkeypatching
import requests

# our app.py that includes the get_json() function
# this is the previous code block example
import app

# custom class to be the mock return value
# will override the requests.Response returned from requests.get
class MockResponse:

    # mock json() method always returns a specific testing dictionary
    @staticmethod
    def json():
        return {"mock_key": "mock_response"}


def test_get_json(monkeypatch):

    # Any arguments may be passed and mock_get() will always return our
    # mocked object, which only has the .json() method.
    def mock_get(*args, **kwargs):
        return MockResponse()

    # apply the monkeypatch for requests.get to mock_get
    monkeypatch.setattr(requests, "get", mock_get)

    # app.get_json, which contains requests.get, uses the monkeypatch
    result = app.get_json("https://fakeurl")
    assert result["mock_key"] == "mock_response"
```

Как мокать другие объекты - читай в документации

Либа [pytest-mock](https://github.com/pytest-dev/pytest-mock/) предоставляет доп.апи для моков в pytest, напирмер позволяет работать с файловой системой

```python
import os

class UnixFS:

    @staticmethod
    def rm(filename):
        os.remove(filename)

def test_unix_fs(mocker):
    mocker.patch('os.remove')
    UnixFS.rm('file')
    os.remove.assert_called_once_with('file')
```

Смотри еще:

- [[pytest]]
- [pytest-mock](https://github.com/pytest-dev/pytest-mock/)

[//begin]: # "Autogenerated link references for markdown compatibility"
[unittest]: unittest "Unittest"
[asyncio]: asyncio "Asyncio"
[pytest]: pytest "Pytest"
[//end]: # "Autogenerated link references"