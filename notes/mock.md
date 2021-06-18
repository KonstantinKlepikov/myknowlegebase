# mock-тесты

[unittest.mock](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.MagicMock)

[[unittest]] mock предоставляет базовый `Mock` class. После создания объекта, можно ассертить методы и аттрибуты класса, а так-же возвращать значения и устанавливать атрибуты, если это нужно.

Дополнительно предоставляется `patch()` декоратор который обрабатывает тестируемые модули и атрибуты уровня класса. `MagicMock` - сабкласс `Mock`, который предоставляет множество магических методов.

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
