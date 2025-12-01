---
description: Структуры данных в python - Enum
tags: python-standart-library python
title: Enum
---
Enum определяет перечислимый тип данных с возможностями итерации и сравнения элементов. Позволяет создавать символические имена для элементов (альтернатива строковым литералам словарей и индексам списков)

[Сссылка на ст.библиотеку](https://docs.python.org/3/library/enum.html?highlight=enum#module-enum)

```python
import enum

class BugStatus(enum.Enum):

    new: int = 7
    incomplete = 6
    invalid = 5
    wont_fix = 4
    in_progress = 3
    fix_committed = 2
    fix_released = 1

print('Member name: {}'.format(BugStatus.wont_fix.name))
>>> Member name: wont_fix
print('Member value: {}'.format(BugStatus.wont_fix.value))
>>> Member value: 4
print(BugStatus(1))
>>> Member value: 7
```

При этом элементы преобразуются в экземпляры классов, которые имеют свойство `name` и `value`

По `Enum` можно итерировать. Элементы будут предоставлены в порядке, в котором они объявлены в классе

```python
for status in BugStatus:
    print(status.name, status.value)
```

Так как элементы неупорядочены, то доступно только сравнение `==` или `is`. При попытке сравнить больше/меньше будет выброшено исключение `TypeError`. Чтобы сравнить элементы или использовать другое поведение, эквивалентное поведению "как числа", надо использовать `IntEnum`

```python
class Shape(enum.IntEnum):
    circle: int = 1
    squire: int = 2

print(['a', 'b', 'c'][Shape.circle])
>>> b
```

Элементы перечисления, которым соответствют одинаковые значения, ведут себя как алиасные ссылки на этот объект - повторяющиеся объекты в итератор Enum не добавляются. Каноническим является то имя, которое было первым связано со значением.

Уникальность значений можно "требовать" с помощью декоратора `@enumunic` - в случае нахождения неуникальных значений будет поднято исключение `ValueError`

```python
@enum.unique
class Shape(enum.IntEnum):
    circle: int = 1
    squire: int = 2
    triangle: int = 3
```

Перечисление можно создавать [программным способом](https://docs.python.org/3/library/enum.html?highlight=enum#programmatic-access-to-enumeration-members-and-their-attributes). Доступен также [функциональный апи](https://docs.python.org/3/library/enum.html?highlight=enum#functional-api)

```python
Enum(value='NewEnumName', names=<...>, *, module='...',
    qualname='...', type=<mixed-in class>, start=1)

# names API
'RED GREEN BLUE' | 'RED,GREEN,BLUE' | 'RED, GREEN, BLUE'
['RED', 'GREEN', 'BLUE']
[('CYAN', 4), ('MAGENTA', 5), ('YELLOW', 6)]
{'CHARTREUSE': 7, 'SEA_GREEN': 11, 'ROSEMARY': 42}
```

Перечисление может быть сериализовано и для них доступны сабклассы только, если в родительском классе не реализовано ни одного члена. Для классов `Enum` доступно создание собственных методлов, включая `__init__`

## Производные

### Flag и IntFlag

Может быть скомбинирован с побитовыми операторами (&, |, ^, ~). IntFlag позволяет оперировать как с числами.

```python
class Color(enum.Flag):
    RED = enum.auto()
    BLUE = enum.auto()
    GREEN = enum.auto()
    WHITE = RED | BLUE | GREEN

print(Color.WHITE.value)
>>> 7
```

В предыдущем примере реализован `auto()` обеспечивающий автоматическое присваивание номеров.

```python
class Perm(enum.IntFlag):
    R = 4
    W = 2
    X = 1

RW = Perm.R | Perm.W
print(Perm.R in RW)
>>> True
```

Для большинства нового кода настоятельно рекомендуются `Enum` и `Flag`, поскольку `IntEnum` и `IntFlag` нарушают некоторые семантические соглашения перечислений (будучи сопоставимыми с целыми числами). `IntEnum` и `IntFlag` следует использовать только в тех случаях, когда `Enum` и `Flag` не подходят; например, когда целочисленные константы заменяются перечислениями, или для взаимодействия с другими объектами.

В целом значения `Enum` не ограничены числами, а сам класс может включать любые методы.

```python
class BugStatus(enum.Enum):
    new = (7, ['incomplete',
               'invalid',
               'wont_fix',
               'in_progress'])
    incomplete = (6, ['new', 'wont_fix'])
    invalid = (5, ['new'])
    wont_fix = (4, ['new'])
    in_progress = (3, ['new', 'fix_committed'])
    fix_committed = (2, ['in_progress', 'fix_released'])
    fix_released = (1, ['new'])

    def __init__(self, num, transitions):
        self.num = num
        self.transitions = transitions

    def can_transition(self, new_state):
        return new_state.name in self.transitions

print(BugStatus.in_progress)
>>> BugStatus.in_progress
print('Value:', BugStatus.in_progress.value)
>>> Value: (3, ['new', 'fix_committed'])
print('Custom attribute:', BugStatus.in_progress.transitions)
>>> Custom attribute: ['new', 'fix_committed']
print('Using attribute:',
      BugStatus.in_progress.can_transition(BugStatus.new))
>>> Using attribute: True
```

## [How do I test if int value exists in Python Enum without using try/catch?](https://stackoverflow.com/questions/43634618/how-do-i-test-if-int-value-exists-in-python-enum-without-using-try-catch)

```python
from enum import Enum

class Fruit(Enum):
    Apple = 4
    Orange = 5
    Pear = 6

5 in Fruit._value2member_map_  # True
7 in Fruit._value2member_map_  # False

'Apple' in Fruit._member_names_  # True
'Mango' in Fruit._member_names_  # False
```

[Подробнее](https://stackoverflow.com/a/43634746/15966204)

## [Enum HOWTO](https://docs.python.org/3/howto/enum.html)

```python
>>> from enum import Enum
>>> class Weekday(Enum):
...    MONDAY = 1
...    TUESDAY = 2
...    WEDNESDAY = 3
...    THURSDAY = 4
...    FRIDAY = 5
...    SATURDAY = 6
...    SUNDAY = 7

...    @classmethod
...    def from_date(cls, date):
...        return cls(date.isoweekday())

>>> Weekday(3)
<Weekday.WEDNESDAY: 3>

>>> Weekday['MONDAY']
<Weekday.WEDNESDAY: 3>

>>> print(Weekday.THURSDAY)
Weekday.THURSDAY

>>> type(Weekday.MONDAY)
<enum 'Weekday'>

>>> isinstance(Weekday.FRIDAY, Weekday)
True

>>> print(Weekday.TUESDAY.name)
TUESDAY

>>> Weekday.WEDNESDAY.value
3

>>> from datetime import date
>>> Weekday.from_date(date.today())
<Weekday.TUESDAY: 2>

>>> for i in Weekday:
...     print(i)
```

В случаях, когда фактические значения вхождений не имеют значения, вы можете сэкономить немного времени и использовать auto() для значений. [Flag](https://docs.python.org/3/library/enum.html#enum.Flag) поддерживает побитовые операторы & (AND), | (OR), ^ (XOR), and ~ (INVERT); результаты этих операторов являются членами перечисления. Использование auto с флагом приводит к получению целых чисел, являющихся степенью двойки, начиная с 1.

```python
>>> from enum import auto

>>> class Weekday(Flag):
...     MONDAY = auto()
...     TUESDAY = auto()
...     WEDNESDAY = auto()
...     THURSDAY = auto()
...     FRIDAY = auto()
...     SATURDAY = auto()
...     SUNDAY = auto()
...     WEEKEND = SATURDAY | SUNDAY

>>> print(Weekday.WEEKEND.value)
96
```

Поведение auto() может быть переопределено. Для этого метод _generate_next_value_() должен быть определен до любых членов.

```python
>>> class AutoName(Enum):
...     def _generate_next_value_(name, start, count, last_values):
...         return name

>>> class Ordinal(AutoName):
...     NORTH = auto()
...     SOUTH = auto()
...     EAST = auto()
...     WEST = auto()

>>> [member.value for member in Ordinal]
['NORTH', 'SOUTH', 'EAST', 'WEST']
```

Наличие двух элементов перечисления с одинаковым именем недопустимо.

```python
>>> class Shape(Enum):
...     SQUARE = 2
...     SQUARE = 3

Traceback (most recent call last):
...
TypeError: 'SQUARE' already defined as 2
```

Однако член перечисления может иметь другие связанные с ним имена... если не установлено, что членство уникально с помощью [unique()](https://docs.python.org/3/library/enum.html#enum.unique)

```python
from enum import Enum, unique

>>> class Shape(Enum):
...     SQUARE = 2
...     DIAMOND = 1
...     CIRCLE = 3
...     ALIAS_FOR_SQUARE = 2

>>> Shape.SQUARE
<Shape.SQUARE: 2>
>>> Shape.ALIAS_FOR_SQUARE
<Shape.SQUARE: 2>
>>> Shape(2)
<Shape.SQUARE: 2>

>>> @unique
>>> class Mistake(Enum):
...     ONE = 1
...     TWO = 2
...     THREE = 3
...     FOUR = 3

Traceback (most recent call last):
...
ValueError: duplicate values found in <enum 'Mistake'>: FOUR -> THREE
```

Специальный атрибут `__members__` представляет собой упорядоченное сопоставление имен с членами, доступное только для чтения.

```python
>>> for name, member in Shape.__members__.items():
...     name, member

('SQUARE', <Shape.SQUARE: 2>)
('DIAMOND', <Shape.DIAMOND: 1>)
('CIRCLE', <Shape.CIRCLE: 3>)
('ALIAS_FOR_SQUARE', <Shape.SQUARE: 2>)
```

Доступно сравнение на идентичность и эквивалентность

```python
>>> Color.RED is Color.RED
True
>>> Color.RED is Color.BLUE
False
>>> Color.RED is not Color.BLUE
True
>>> Color.BLUE == Color.RED
False
>>> Color.BLUE != Color.RED
True
>>> Color.BLUE == Color.BLUE
True
```

Однако порядковые сравнения не доступны - надо использовать [IntEnum](https://docs.python.org/3/library/enum.html#enum.IntEnum)

```python
>>> Color.RED < Color.BLUE
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: '<' not supported between instances of 'Color' and 'Color'
```

IntEnum аналогичен Enum, но его члены также являются целыми числами и могут использоваться везде, где могут использоваться целые числа. Если с элементом IntEnum выполняется какая-либо целочисленная операция, результирующее значение теряет свой статус перечисления.

```python
>>> from enum import IntEnum

>>> class Numbers(IntEnum):
...     ONE = 1
...     TWO = 2
...     THREE = 3
>>> Numbers.THREE
<Numbers.THREE: 3>
>>> Numbers.ONE + Numbers.TWO
3
>>> Numbers.THREE + 5
8
>>> Numbers.THREE == 3
True
>>> Numbers.ONE > Numbers.TWO
False
```

Перечисления — это классы Python, которые, как обычно, могут иметь методы и специальные методы. Перечисления могут иметь сабклассы, только если не содержат членов. Перечисления могут быть сериализованы и десериализованы.

Кроме IntEnum доступны StrEnum, IntFlag. Другие типы можно конструировать миксуя:

```python
>>> from enum import Enum

>>> class FloatNumbers(float, Enum):
...     pass
```

При этом:

- При создании подкласса Enum смешанные типы должны стоять перед самим Enum в последовательности оснований.
- Смешанные типы должны иметь разрешение на подклассы. Например, bool и range не могут иметь подклассы и вызовут ошибку во время создания Enum, если они используются в качестве типа микширования.
- Хотя Enum может иметь элементы любого типа, после добавления дополнительного типа все члены должны иметь значения этого типа. Это ограничение не распространяется на примеси, которые только добавляют методы и не указывают другой тип.
- Когда вмешивается другой тип данных, атрибут value не совпадает с самим членом перечисления, хотя он и будет сравниваться с эквивалентным.
- форматирование в стиле %: `%s` и `%r` вызывают `__str__()` и `__repr__()` класса Enum соответственно; другие коды (например, `%i` или `%h` для `IntEnum`) рассматривают член перечисления как смешанный тип.
- Форматированные строковые литералы, `str.format()` и `format()` будут использовать метод перечисления `__str__()`.

Смотри еще:

- [примеры](https://docs.python.org/3/howto/enum.html#enum-cookbook)
- [больше примеров](https://docs.python.org/3/library/enum.html?highlight=enum#interesting-examples)
- [Enum HOWTO](https://docs.python.org/3/howto/enum.html)
- [[python-standart-library]]


[python-standart-library]: ../lists/python-standart-library "Стандартная библиотека python и полезные ресурсы"
