---
description: Структуры данных в python - Enum
tags: python-standart-library
---
# Enum

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

Больше примеров [тут](https://docs.python.org/3/library/enum.html?highlight=enum#interesting-examples)

[[python-standart-library]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[python-standart-library]: ../lists/python-standart-library "Стандартная библиотека python - список заметок"
[//end]: # "Autogenerated link references"