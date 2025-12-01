---
description: Typing - анотация типов в python
tags: python-standart-library python
title: Typing
---
Компонент стандартной библиотеки, используемый для [[type-annotation]] сложных объектов. Используется в [[mypy]]

[Ссылка на документацию](https://docs.python.org/3/library/typing.html#module-typing)

## Основные принципы

### [Aliaces](https://docs.python.org/3/library/typing.html#type-aliases)

Псевдонимы служат для сокращения аннотирующих конструкций

```python
Vector = list[float]

def scale(scalar: float, vector: Vector) -> Vector:
    return [scalar * num for num in vector]
```

### [New Type](https://docs.python.org/3/library/typing.html#newtype)

Специальная обертка, необходимая когда требуется новый тип, без затрат на создание класса

```python
from typing import NewType

UserId = NewType('UserId', int)

def get_user(x: UserId): ...

get_user(UserId(123456)) # this is fine
get_user(123456) # that's an int, not a UserId

UserId(123456) + 123456 # fine, because UserId is a subclass of int
```

[Смотри подробнее на оверфло](https://stackoverflow.com/a/58775376/15966204)

### [Callable](https://docs.python.org/3/library/typing.html#callable)

Аннотация вызываемых объектов

`Callable[[Arg1Type, Arg2Type], ReturnType]` или так `Callable[..., ReturnType]`

Вызываемые объекты, которые принимают другие вызываемые объекты в качестве аргументов, могут указывать, что их типы параметров зависят друг от друга, используя [ParamSpec](https://docs.python.org/3/library/typing.html#typing.ParamSpec). Кроме того, если этот вызываемый объект добавляет или удаляет аргументы из других вызываемых объектов, может использоваться оператор [Concatenate](https://docs.python.org/3/library/typing.html#typing.Concatenate). Они принимают форму `Callable[ParamSpecVariable, ReturnType]` и `Callable[Concatenate[Arg1Type, Arg2Type, ..., ParamSpecVariable], ReturnType]` соответственно.

### [Generics](https://docs.python.org/3/library/typing.html#generics)

Поскольку информация о типах объектов, хранящихся в контейнерах, не может быть статически выведена универсальным способом, абстрактные базовые классы были расширены для поддержки обозначения ожидаемых типов для элементов контейнеров.

```python
from collections.abc import Mapping, Sequence

def notify_by_email(employees: Sequence[Employee],
                    overrides: Mapping[str, str]) -> None: ...
```

[Пользователи могут определять собственные дженерики](https://docs.python.org/3/library/typing.html#user-defined-generic-types), наследуясь от `Generic` с помощью `TypeVar`

### [TypeVar](https://docs.python.org/3/library/typing.html#typing.TypeVar)

Переменные типа позволяют ссылаться на один и тот же тип более одного раза, не указывая точно, какой это тип.

У `TypeVar` есть еще несколько вариантов. Вы можете ограничить возможные значения, передав больше типов (например, `TypeVar(name, int, str)`), или вы можете указать граничное состояние, чтобы каждое значение переменной типа было подтипом этого типа (например, `TypeVar(name, bound=int)`). Кроме того, вы можете решить, является ли переменная типа ковариантной, контравариантной или ни той, ни другой при ее объявлении. По сути, это решает, когда подклассы или суперклассы могут использоваться вместо универсального типа.

Без `TypeVar` не было бы хорошего способа реализовать следующий пример

```python
from typing import TypeVar, Generic, List, Tuple

# Two type variables, named T and R
T = TypeVar('T')
R = TypeVar('R')

# Put in a list of Ts and get out one T
def get_one(x: List[T]) -> T: ...

# Put in a T and an R, get back an R and a T
def swap(x: T, y: R) -> Tuple[R, T]:
    return y, x

# A simple generic class that holds a value of type T
class ValueHolder(Generic[T]):
    def __init__(self, value: T):
        self.value = value
    def get(self) -> T:
        return self.value

x: ValueHolder[int] = ValueHolder(123)
y: ValueHolder[str] = ValueHolder('abc')
```

Типичный пример

```python
T = TypeVar('T')  # Can be anything
A = TypeVar('A', str, bytes)  # Must be str or bytes
```

### [The Any type](https://docs.python.org/3/library/typing.html#the-any-type)

Особым типом является `Any`. Средство проверки статического типа будет рассматривать каждый тип как совместимый с `Any`, а `Any` — как совместимый со всеми типами.

### [Duck typing](https://docs.python.org/3/library/typing.html#nominal-vs-structural-subtyping)

`typing` поддерживает утиную типизацию, что означает, что классы реализующие соответствующее поведение не обязаны наследоваться от всех классов, подразумеваемых в типизируемом.

## [Специальные типы и примитивы](https://docs.python.org/3/library/typing.html#special-typing-primitives)

- `Any`
- `NoReturn` специальный тип, указывающий, что функция никогда не возвращает значение

```python
from typing import NoReturn

def stop() -> NoReturn:
    raise RuntimeError('no way')
```

- `TypeAlias` Специальная аннотация для явного объявления алиаса

```python
from typing import TypeAlias

Factors: TypeAlias = list[int]
```

- `Tuple` (`Tuple[int, float, str]`, `Tuple[()]`, `Tuple[int, ...].`)
- `Union` эквивалент `X | Y` (последний вариант рекомендуем)

Нюансы реализации:

```python
Union[Union[int, str], float] == Union[int, str, float]
Union[int] == int
Union[int, str, int] == Union[int, str] == int | str
Union[int, str] == Union[str, int]
```

- `Optional` эквивалент `X | None` или `Union[X, None]`
- `Callable`
- `Concatenate`
- `Type(Generic[CT_co])`  Переменная, аннотированная с помощью C, может принимать значение типа C.

```python
a = 3         # Has type 'int'
b = int       # Has type 'Type[int]'
c = type(a)   # Also has type 'Type[int]'
```

- `Literal` указывает на один или несколько литералов

```python
def validate_simple(data: Any) -> Literal[True]:  # always returns True
    ...

MODE = Literal['r', 'rb', 'w', 'wb']
def open_helper(file: str, mode: MODE) -> str:
    ...

open_helper('/some/path', 'r')  # Passes type check
open_helper('/other/path', 'typo')  # Error in type checker
```

- `ClassVar` Разметка переменных класса

```python
class Starship:
    stats: ClassVar[dict[str, int]] = {} # class variable
    damage: int = 10                     # instance variable
```

- `Final` указывает на то. что переменная не может быть переопределена в сабклассах

```python
MAX_SIZE: Final = 9000
MAX_SIZE += 1  # Error reported by type checker

class Connection:
    TIMEOUT: Final[int] = 10

class FastConnector(Connection):
    TIMEOUT = 1  # Error reported by type checker
```

- `Annotated` анотация с помощью метаданных, например так: `Annotated[int, ValueRange(3, 10), ctype("char")]`
- `TypeGuard` Используется для аннотации возвращаемого типа с помощью определяемой пользователем guard функции, когда тип нельзя установить корректно на этапе объявления. `TypeGuard` принимает только один аргумент. Во время выполнения функции, помеченные таким образом, должны возвращать логическое значение. Добавлен в 3.10

```python
def is_str_list(val: List[object]) -> TypeGuard[List[str]]:
    '''Determines whether all objects in the list are strings'''
    return all(isinstance(x, str) for x in val)

def func1(val: List[object]):
    if is_str_list(val):
        # Type of ``val`` is narrowed to ``List[str]``.
        print(" ".join(val))
    else:
        # Type of ``val`` remains as ``List[object]``.
        print("Not a list of strings!")
```

## [Дженерики](https://docs.python.org/3/library/typing.html#building-generic-types)

- `Generic`
- `TypeVar`
- `ParamSpec`
- `ParamSpecArgs`
- `ParamSpecKwargs`
- `AnyStr` эквивалент `TypeVar('AnyStr', str, bytes)`
- `Protocol(Generic)` аннотирует проткол классов (поддерживает утиную типизацию в т.ч.)

```python
class Proto(Protocol):
    def meth(self) -> int:
        ...

class C:
    def meth(self) -> int:
        return 0

def func(x: Proto) -> int:
    return x.meth()

func(C())  # Passes static type check
```

- `runtime_checkable` рантайм проктол

## [Другие спец.директивы](https://docs.python.org/3/library/typing.html#other-special-directives)

В данном разделе не конструкции аннотации, а специальные типы, использующие аннотацию.

- `NamedTuple` поддерживающий аннотацию вариант `namedtuple`
- `NewType`
- `TypedDict` тип, поддерживающий аннотацию для словаря

## [Коллекция дженериков](https://docs.python.org/3/library/typing.html#generic-concrete-collections)

Основные типы: `List`, `Dict`, `FrozenSet`, `Set`

Типы, поддерживающие модуль `collections`: `DefaultDict`, `OrderedDict`, `ChainMap`, `Counter`, `Deque` (смотри [[deque]], [[chainmap]], [[counter]], [[ordereddict]], [[defaultdict]])

[Другие типы](https://docs.python.org/3/library/typing.html#other-concrete-types) (в основном депрекейтед)

## [ABC](https://docs.python.org/3/library/typing.html#abstract-base-classes)

- [связанные](https://docs.python.org/3/library/typing.html#corresponding-to-collections-in-collections-abc) с `collections.abc`
- [асинхронные объекты](https://docs.python.org/3/library/typing.html#asynchronous-programming)
- [контекстные менеджеры](https://docs.python.org/3/library/typing.html#context-manager-types)

## [Протоколы](https://docs.python.org/3/library/typing.html#protocols)

## [Функции и декораторы](https://docs.python.org/3/library/typing.html#functions-and-decorators)

- cast(typ, val) приводит переменную к типу, без изменеения значения
- @overload Декоратор @overload позволяет описывать функции и методы, поддерживающие различные комбинации типов аргументов. За серией декорированных @overload определений должно следовать ровно одно недекорированное @overload определение

```python
@overload
def process(response: None) -> None:
    ...
@overload
def process(response: int) -> tuple[int, str]:
    ...
@overload
def process(response: bytes) -> str:
    ...
def process(response):
    <actual implementation>
```

- @final запрет переопределения
- @no_type_check указание на то, что анотации не определяют тип
- @no_type_check_decorator декоратор декоратора
- @type_check_only определяет, что функция или класс не доступны в рантайм

## [Хелперы интроспекции](https://docs.python.org/3/library/typing.html#introspection-helpers)

## [TYPE_CHECKING](https://docs.python.org/3/library/typing.html#constant)

`True` на првоерке и `False` в рантайм

```python
if TYPE_CHECKING:
    import expensive_mod

def fun(arg: 'expensive_mod.SomeType') -> None:
    local_var: expensive_mod.AnotherType = other_fun()
```

Смотри еще:

- [[python-standart-library]]
- [[type-annotation]]
- [[python-datamodel]]
- [[python-patterns]]
- [[from-future-import-annotations]]


[type-annotation]: type-annotation "Аннотация типов в python"
[mypy]: mypy "Mypy"
[deque]: deque "Deque - двухсторонние очереди"
[chainmap]: chainmap "ChainMap"
[counter]: counter "Counter - счетчик хешируемых объектов"
[ordereddict]: ordereddict "OrderedDict упорядоченный словарь с опцией сравнения по порядку"
[defaultdict]: defaultdict "Defaultdict словарь с возвратом значения по умолчанию"
[python-standart-library]: ../lists/python-standart-library "Стандартная библиотека python и полезные ресурсы"
[python-datamodel]: ../lists/python-datamodel "Python datamodel"
[python-patterns]: python-patterns "Python patterns programming"
[from-future-import-annotations]: from-future-import-annotations "From future import annotations"
