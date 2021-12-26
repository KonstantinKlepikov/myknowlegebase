---
description: Pydantic - библиотека для валидации типов в python
---
# Pydantic

Типизация для python [Документация](https://pydantic-docs.helpmanual.io/). Использует [[type-annotation]] на базе [[mypy]]

```python
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name = 'John Doe'
    signup_ts: Optional[datetime] = None
    friends: List[int] = []


external_data = {
    'id': '123',
    'signup_ts': '2019-06-01 12:22',
    'friends': [1, 2, '3'],
}
user = User(**external_data)
print(user.id)
#> 123
print(repr(user.signup_ts))
#> datetime.datetime(2019, 6, 1, 12, 22)
print(user.friends)
#> [1, 2, 3]
print(user.dict())
"""
{
    'id': 123,
    'signup_ts': datetime.datetime(2019, 6, 1, 12, 22),
    'friends': [1, 2, 3],
    'name': 'John Doe',
}
"""
```

## Установка

`pip install pydantic`

Три варианта

`pip install pydantic[email]` [валидация имейлов](https://github.com/JoshData/python-email-validator)
`pip install pydantic[dotenv]` [.env support](https://pydantic-docs.helpmanual.io/usage/settings/#dotenv-env-support) - [[.env-переменные-окружения]]
`pip install pydantic[email,dotenv]`

## Использование

### Модели

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name = 'Jane Doe'
```

Каждый класс модели наследует базовой модели pydantic. В данном случае тип name инферится из типа строки. Это поле не обязательно, так как установлено дефолтное значение. Тогда создавая инстанс класса, мы получим аттрибуты:

```python
user = User(id='123')

assert user.id == 123
assert user.name == 'Jane Doe'

# name не создается при инициализации, т.к. имеет дефолтное значение
assert user.__fields_set__ == {'id'}

# поля полученные, при инициализации
assert user.dict() == dict(user) == {'id': 123, 'name': 'Jane Doe'}

# наконец, у нас есть полный доступ к атрибутам
user.id = 321
assert user.id == 321
```

[Свойства модели](https://pydantic-docs.helpmanual.io/usage/models/#model-properties):

- `dict()` словарь полей и значений модели
- `json()` тоже вамое в виде json
- `copy()` копия модели (по дефолту shallow)
- `parse_obj()` метод для парсинга и лоада объекта в модель с выдачей ошибки, если объект не похож на fict
- `parse_raw()` тоже самое из json
- `parse_file()` из файла
- `from_orm()` из класса ОРМ
- `schema()` возвращает json-схему в виде словаря
- `schema_json()` в виде json
- `construct()` создание модели без валидации (когда данные из проверенногно источника - на в 30 раз быстрее)
- `_fields_set__` имена полей в виде множества
- `__fields__` словарь полей
- `__config__` конфиг

#### Можно выстраивать модели иерархически

```python
from typing import List
from pydantic import BaseModel


class Foo(BaseModel):
    count: int
    size: float = None


class Bar(BaseModel):
    apple = 'x'
    banana = 'y'


class Spam(BaseModel):
    foo: Foo
    bars: List[Bar]

m = Spam(foo={'count': 4}, bars=[{'apple': 'x1'}, {'apple': 'x2'}])
print(m)
#> foo=Foo(count=4, size=None) bars=[Bar(apple='x1', banana='y'),
#> Bar(apple='x2', banana='y')]
print(m.dict())
"""
{
    'foo': {'count': 4, 'size': None},
    'bars': [
        {'apple': 'x1', 'banana': 'y'},
        {'apple': 'x2', 'banana': 'y'},
    ],
}
"""
```

#### ORM модели

```python
from typing import List
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, constr

Base = declarative_base()


class CompanyOrm(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True, nullable=False)
    public_key = Column(String(20), index=True, nullable=False, unique=True)
    name = Column(String(63), unique=True)
    domains = Column(ARRAY(String(255)))


class CompanyModel(BaseModel):
    id: int
    public_key: constr(max_length=20)
    name: constr(max_length=63)
    domains: List[constr(max_length=255)]

    class Config:
        orm_mode = True


co_orm = CompanyOrm(
    id=123,
    public_key='foobar',
    name='Testing',
    domains=['example.com', 'foobar.com'],
)
print(co_orm)
#> <models_orm_mode.CompanyOrm object at 0x7fb266c7ef40>
co_model = CompanyModel.from_orm(co_orm)
print(co_model)
#> id=123 public_key='foobar' name='Testing' domains=['example.com',
#> 'foobar.com']
```

Иногда нужно дать название колонке, после того, как зарезервирвоано название поля.

```python
import typing

from pydantic import BaseModel, Field
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base


class MyModel(BaseModel):
    metadata: typing.Dict[str, str] = Field(alias='metadata_')

    class Config:
        orm_mode = True


BaseModel = declarative_base()


class SQLModel(BaseModel):
    __tablename__ = 'my_table'
    id = sa.Column('id', sa.Integer, primary_key=True)
    # 'metadata' is reserved by SQLAlchemy, hence the '_'
    metadata_ = sa.Column('metadata', sa.JSON)


sql_model = SQLModel(metadata_={'key': 'val'}, id=1)

pydantic_model = MyModel.from_orm(sql_model)

print(pydantic_model.dict())
#> {'metadata': {'key': 'val'}}
print(pydantic_model.dict(by_alias=True))
#> {'metadata_': {'key': 'val'}}
```

ORM модели [могут быть рекурсивными](https://pydantic-docs.helpmanual.io/usage/models/#recursive-orm-models)

### Доступ к ошибкам

[Осуществляется через ValidationError](https://pydantic-docs.helpmanual.io/usage/models/#error-handling). Поднимается один эксепшен вне зависимости от кол-ва ошибок, с информацией по которому можно работать через несколько методов. Кроме того, можно реализовать кастомные ошибки.

### Поддерживаются дополнительные методы создания моделей (см. в models)

Например [можно сделать даныне модели неизменяемыми](https://pydantic-docs.helpmanual.io/usage/models/#faux-immutability). Можно создавать [дженерик модели](https://pydantic-docs.helpmanual.io/usage/models/#generic-models) для последующего использования в качестве "шаблона". Можно [использовать абстрактные базовы классы](https://pydantic-docs.helpmanual.io/usage/models/#abstract-base-classes), [устанавливать строгий порядок полей](https://pydantic-docs.helpmanual.io/usage/models/#field-ordering) (поля должны оставаться в том порядке, в котором они были заданы в модели)

### [Обязательные поля](https://pydantic-docs.helpmanual.io/usage/models/#required-fields)

```python
from pydantic import BaseModel, Field

class Model(BaseModel):
    a: int
    b: int = ...
    c: int = Field(...)
```

вариант рекуаред поля с опциональным значением

```python
class Model(BaseModel):
    a: Optional[int]
    b: Optional[int] = ...
    c: Optional[int] = Field(...)
```

### [Поля с динамическим required значением](https://pydantic-docs.helpmanual.io/usage/models/#field-with-dynamic-default-value)

С помощью `default_factory`

```python
from datetime import datetime
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class Model(BaseModel):
    uid: UUID = Field(default_factory=uuid4)
    updated: datetime = Field(default_factory=datetime.utcnow)
```

### Автоматическая конфертация

Пайдантик автоматически конвертирует некотоыре типы данных, что может привести к потере информации

```python
from pydantic import BaseModel


class Model(BaseModel):
    a: int
    b: float
    c: str

print(Model(a=3.1415, b=' 2.72 ', c=123).dict())
#> {'a': 3, 'b': 2.72, 'c': '123'}
```

## [Типы полей](https://pydantic-docs.helpmanual.io/usage/types/)

Поддерживает все стандартные типы #python

- [strict types](https://pydantic-docs.helpmanual.io/usage/types/#strict-types)
- [constrained types](https://pydantic-docs.helpmanual.io/usage/types/#constrained-types)

Типы:

- `None` or `type(None)` or `Literal[None]`
- `bool`
- `int`
- `float`
- `str`
- `bytes`
- `list` (принимает list, tuple, set, frozenset, deque и генераторы)
- `tuple` (принимает list, tuple, set, frozenset, deque и генераторы)
- `dict`
- `set` (принимает list, tuple, set, frozenset, deque и генераторы)
- `frozenset` (принимает list, tuple, set, frozenset, deque и генераторы)
- `deque` (принимает list, tuple, set, frozenset, deque и генераторы)
- `datetime.date`
- `datetime.time`
- `datetime.datetime`
- `datetime.timedelta`
- `typing.Any` любое значение
- `typing.Annotated` анотированное значение
- `typing.TypeVar` константа, базирующаяся на [этом](https://pydantic-docs.helpmanual.io/usage/types/#typevar)
- `typing.Union` [несколько разных типов](https://pydantic-docs.helpmanual.io/usage/types/)
- `typing.Optional` обертка над `Union[x, None]`
- `typing.List`
- `typing.Tuple`
- subclass of `typing.NamedTuple`
- subclass of `collections.namedtuple`
- `typing.Dict` и subclass
- `typing.Set`
- `typing.FrozenSet`
- `typing.Deque`
- `typing.Sequence`
- `typing.Iterable` зарезевировано под другие итераторы
- `typing.Type`
- `typing.Callable`
- `typing.Pattern` для regex
- `ipaddress.IPv4Address` и другие ip...
- `enum.Enum` и subclass of `enum.Enum`
- `enum.IntEnum` и subclass
- `decimal.Decimal` конвертит в строку, затем в decimal
- `pathlib.Path`
- `uuid.UUID`
- `ByteSize`

Пример с итераторами

```python
from typing import (
    Deque, Dict, FrozenSet, List, Optional, Sequence, Set, Tuple, Union
)

from pydantic import BaseModel


class Model(BaseModel):
    simple_list: list = None
    list_of_ints: List[int] = None

    simple_tuple: tuple = None
    tuple_of_different_types: Tuple[int, float, str, bool] = None

    simple_dict: dict = None
    dict_str_float: Dict[str, float] = None

    simple_set: set = None
    set_bytes: Set[bytes] = None
    frozen_set: FrozenSet[int] = None

    str_or_bytes: Union[str, bytes] = None
    none_or_str: Optional[str] = None

    sequence_of_ints: Sequence[int] = None

    compound: Dict[Union[str, bytes], List[Set[int]]] = None

    deque: Deque[int] = None
```

### DateTime типы

- datetime fields can be:
  - datetime, existing datetime object
  - int or float, assumed as Unix time, i.e. seconds (if >= -2e10 or <= 2e10) or milliseconds (if < -2e10or > 2e10) since 1 January 1970
  - str, following formats work:
    - YYYY-MM-DD[T]HH:MM[:SS[.ffffff]][Z or [±]HH[:]MM]]]
    - int or float as a string (assumed as Unix time)
- date fields can be:
  - date, existing date object
  - int or float, see datetime
  - str, following formats work:
    - YYYY-MM-DD
    - int or float, see datetime
- time fields can be:
  - time, existing time object
  - str, following formats work:
    - HH:MM[:SS[.ffffff]][Z or [±]HH[:]MM]]]
- timedelta fields can be:
  - timedelta, existing timedelta object
  - int or float, assumed as seconds
  - str, following formats work:
    - [-][DD ][HH:MM]SS[.ffffff]
    - [±]P[DD]DT[HH]H[MM]M[SS]S (ISO 8601 format for timedelta)

### Boolean

Будет ошибка валидации, если значение не одно из;

- True or False
- 0 or 1
- a str which when converted to lower case is one of '0', 'off', 'f', 'false', 'n', 'no', '1', 'on', 't', 'true', 'y', 'yes'
- a bytes which is valid (per the previous rule) when decoded to str

### [Calable](https://pydantic-docs.helpmanual.io/usage/types/#callable)

Позволяет передавать функцию и указывать, какой выход в ней ожидается. Валидация не проверяте типы аргументов функции, только то, что этот объект вызываемый.

### [Type](https://pydantic-docs.helpmanual.io/usage/types/#type)

Когда мы должны проверить, что объект является производным от  `tyoe`, т.е. классом, не инстансом.

### [Literal Type](https://pydantic-docs.helpmanual.io/usage/types/#literal-type)

Появился в #python 3.8 `typing.Literal` (или `typing_extensions.Literal` для 3.8). позволяет определить только специфичные значения литералов. Позволяет проверять одно или больше специфичных значений без использования валидаторов.

```python
from typing import Literal

from pydantic import BaseModel, ValidationError


class Pie(BaseModel):
    flavor: Literal['apple', 'pumpkin']


Pie(flavor='apple')
Pie(flavor='pumpkin')
try:
    Pie(flavor='cherry')
except ValidationError as e:
    print(str(e))
```

Пример с Union

```python
from typing import Optional, Union

from typing import Literal

from pydantic import BaseModel


class Dessert(BaseModel):
    kind: str


class Pie(Dessert):
    kind: Literal['pie']
    flavor: Optional[str]


class ApplePie(Pie):
    flavor: Literal['apple']


class PumpkinPie(Pie):
    flavor: Literal['pumpkin']


class Meal(BaseModel):
    dessert: Union[ApplePie, PumpkinPie, Pie, Dessert]

print(type(Meal(dessert={'kind': 'pie', 'flavor': 'apple'}).dessert).__name__)
#> ApplePie
print(type(Meal(dessert={'kind': 'pie', 'flavor': 'pumpkin'}).dessert).__name__)
#> PumpkinPie
print(type(Meal(dessert={'kind': 'pie'}).dessert).__name__)
#> Pie
print(type(Meal(dessert={'kind': 'cake'}).dessert).__name__)
#> Dessert
```

### [Анотированные типы](https://pydantic-docs.helpmanual.io/usage/types/#annotated-types)

Пример с NamedTuple

```python
from typing import NamedTuple

from pydantic import BaseModel, ValidationError


class Point(NamedTuple):
    x: int
    y: int


class Model(BaseModel):
    p: Point


print(Model(p=('1', '2')))
#> p=Point(x=1, y=2)
```

### [pydantic types](https://pydantic-docs.helpmanual.io/usage/types/#pydantic-types)

- `FilePath`
- `DirectoryPath`
- `EmailStr`
- `NameEmail`
- `PyObject`
- `Color` html/css цвет вот [в таком формате](https://pydantic-docs.helpmanual.io/usage/types/#color-type). Поддерживается несколько методов конвертации.
- `Json` [Пример](https://pydantic-docs.helpmanual.io/usage/types/#json-type)
- `PaymentCardNumber` [Пример](https://pydantic-docs.helpmanual.io/usage/types/#payment-card-numbers)
- `AnyUrl` [описание про урлы](https://pydantic-docs.helpmanual.io/usage/types/#urls)
- `AnyHttpUrl`
- `HttpUrl`
- `PostgresDsn`
- `RedisDsn`
- `stricturl`
- `UUID1` и 2, 3, 4, 5
- `SecretBytes` и т.д. [если нужно скрыт часть инфы из логирования](https://pydantic-docs.helpmanual.io/usage/types/#secret-types)
- `IPvAnyAddress` и т.д.
- `NegativeFloat` и т.д.
- несколько методов, которые принимают методы, содержащие другие типы

### [Constrained types](https://pydantic-docs.helpmanual.io/usage/types/#constrained-types)

Ограничение типов по форматам, диапазонам и т.д. через приставку con*

```python
from decimal import Decimal

from pydantic import (
    BaseModel,
    NegativeFloat,
    NegativeInt,
    PositiveFloat,
    PositiveInt,
    NonNegativeFloat,
    NonNegativeInt,
    NonPositiveFloat,
    NonPositiveInt,
    conbytes,
    condecimal,
    confloat,
    conint,
    conlist,
    conset,
    constr,
    Field,
)


class Model(BaseModel):
    lower_bytes: conbytes(to_lower=True)
    short_bytes: conbytes(min_length=2, max_length=10)
    strip_bytes: conbytes(strip_whitespace=True)

    lower_str: constr(to_lower=True)
    short_str: constr(min_length=2, max_length=10)
    regex_str: constr(regex=r'^apple (pie|tart|sandwich)$')
    strip_str: constr(strip_whitespace=True)

    big_int: conint(gt=1000, lt=1024)
    mod_int: conint(multiple_of=5)
    pos_int: PositiveInt
    neg_int: NegativeInt
    non_neg_int: NonNegativeInt
    non_pos_int: NonPositiveInt

    big_float: confloat(gt=1000, lt=1024)
    unit_interval: confloat(ge=0, le=1)
    mod_float: confloat(multiple_of=0.5)
    pos_float: PositiveFloat
    neg_float: NegativeFloat
    non_neg_float: NonNegativeFloat
    non_pos_float: NonPositiveFloat

    short_list: conlist(int, min_items=1, max_items=4)
    short_set: conset(int, min_items=1, max_items=4)

    decimal_positive: condecimal(gt=0)
    decimal_negative: condecimal(lt=0)
    decimal_max_digits_and_places: condecimal(max_digits=2, decimal_places=2)
    mod_decimal: condecimal(multiple_of=Decimal('0.25'))

    bigger_int: int = Field(..., gt=10000)
```

Описание всех аргументов (методов) [смотри там же](https://pydantic-docs.helpmanual.io/usage/types/#constrained-types)

Есть еще несколько специфичных случаев и можно задавать свои типы.

## Validators

[Использование классметода для валидации данных в модели](https://pydantic-docs.helpmanual.io/usage/validators/)

Это позволяет возвращать определенные данные, после валидации

```python
from pydantic import BaseModel, ValidationError, validator


class UserModel(BaseModel):
    name: str
    username: str
    password1: str
    password2: str

    @validator('name')
    def name_must_contain_space(cls, v):
        if ' ' not in v:
            raise ValueError('must contain a space')
        return v.title()

    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        if 'password1' in values and v != values['password1']:
            raise ValueError('passwords do not match')
        return v

    @validator('username')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        return v


user = UserModel(
    name='samuel colvin',
    username='scolvin',
    password1='zxcvbn',
    password2='zxcvbn',
)
print(user)
#> name='Samuel Colvin' username='scolvin' password1='zxcvbn' password2='zxcvbn'

try:
    UserModel(
        name='samuel',
        username='scolvin',
        password1='zxcvbn',
        password2='zxcvbn2',
    )
except ValidationError as e:
    print(e)
    """
    2 validation errors for UserModel
    name
      must contain a space (type=value_error)
    password2
      passwords do not match (type=value_error)
    """
```

В разделе примеры как использовать кастом валидацию.

## [Config](https://pydantic-docs.helpmanual.io/usage/model_config/)

```python
class Sprints(BaseModel):
    user: User
    sprints: List[Sprint]
    
    class Config:
        orm_mode = True
```

- `title` заголовко json схемы
- `anystr_strip_whitespace` и т.д.
- `validate_all`
- `extra` забыть, применить или игнорировать экстра атрибуты при инциализации
- `allow_mutation` для неизменяемых типов
- `frozen` открывает дорогу к хешированию инстансов модели
- ...
- `orm_mode` использовать как модель для ORM
- `alias_generator`
- `schema_extra`
- `json_loads` кастомные ф-ии для json
- `json_dumps`
- `json_encoders`

Сконфигурировать можно глобально, вот так:

```python
class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True
```

## [Alias](https://pydantic-docs.helpmanual.io/usage/model_config/#alias-precedence)

Пример алиас-генератора, чтобы перегнать все змеиные имена в верблюжьи

```python
from pydantic import BaseModel


def to_camel(string: str) -> str:
    return ''.join(word.capitalize() for word in string.split('_'))


class Voice(BaseModel):
    name: str
    language_code: str

    class Config:
        alias_generator = to_camel


voice = Voice(Name='Filiz', LanguageCode='tr-TR')
print(voice.language_code)
#> tr-TR
print(voice.dict(by_alias=True))
#> {'Name': 'Filiz', 'LanguageCode': 'tr-TR'}
```

## [SCHEMA](https://pydantic-docs.helpmanual.io/usage/schema/)

Возвращается json-схема, в т.ч. можно в [[openapi-specification]]

[Смотри статью](https://pydantic-docs.helpmanual.io/usage/schema/) про данные, которые попадают в схему, анотированные типы в схеме, валидацию схемы и кастомизацию:

## [Экспорт моделей](https://pydantic-docs.helpmanual.io/usage/exporting_models/) в другие форматы данных

## [Dataclasses](https://pydantic-docs.helpmanual.io/usage/dataclasses/)

## Использование [validate_arguments](https://pydantic-docs.helpmanual.io/usage/validation_decorator/)

Находится в бете с версии 1.5. Пример использования:

```python
from pydantic import validate_arguments, ValidationError


@validate_arguments
def repeat(s: str, count: int, *, separator: bytes = b'') -> bytes:
    b = s.encode()
    return separator.join(b for _ in range(count))


a = repeat('hello', 3)
print(a)
#> b'hellohellohello'

b = repeat('x', '4', separator=' ')
print(b)
#> b'x x x x'

try:
    c = repeat('hello', 'wrong')
except ValidationError as exc:
    print(exc)
    """
    1 validation error for Repeat
    count
      value is not a valid integer (type=type_error.integer)
    """
```

Аргументы для валидации инфирятся из аннотации типов функции. Если тип не анотирован, он инферится как `any`

## [Settings managements](https://pydantic-docs.helpmanual.io/usage/settings/)

Если создать модель и унаследовать ее от `BaseSettings`, эта модель позволит определить значения любых полей, которые не определены ключевым аргументом, из переменных окружения. Это позволяет сделать следующее:

- сделать понятный класс конфигураций для приложения
- автоматически чиать конфигурации из переменных окружения
- в ручную переписывать специфические настройки, к примеру для тестов

```python
from typing import Set

from pydantic import (
    BaseModel,
    BaseSettings,
    PyObject,
    RedisDsn,
    PostgresDsn,
    Field,
)


class SubModel(BaseModel):
    foo = 'bar'
    apple = 1


class Settings(BaseSettings):
    auth_key: str
    api_key: str = Field(..., env='my_api_key')

    redis_dsn: RedisDsn = 'redis://user:pass@localhost:6379/1'
    pg_dsn: PostgresDsn = 'postgres://user:pass@localhost:5432/foobar'

    special_function: PyObject = 'math.cos'

    # to override domains:
    # export my_prefix_domains='["foo.com", "bar.com"]'
    domains: Set[str] = set()

    # to override more_settings:
    # export my_prefix_more_settings='{"foo": "x", "apple": 1}'
    more_settings: SubModel = SubModel()

    class Config:
        env_prefix = 'my_prefix_'  # defaults to no prefix, i.e. ""
        fields = {
            'auth_key': {
                'env': 'my_auth_key',
            },
            'redis_dsn': {
                'env': ['service_redis_dsn', 'redis_url']
            }
        }


print(Settings().dict())
"""
{
    'auth_key': 'xxx',
    'api_key': 'xxx',
    'redis_dsn': RedisDsn('redis://user:pass@localhost:6379/1',
scheme='redis', user='user', password='pass', host='localhost',
host_type='int_domain', port='6379', path='/1'),
    'pg_dsn': PostgresDsn('postgres://user:pass@localhost:5432/foobar',
scheme='postgres', user='user', password='pass', host='localhost',
host_type='int_domain', port='5432', path='/foobar'),
    'special_function': <built-in function cos>,
    'domains': set(),
    'more_settings': {'foo': 'bar', 'apple': 1},
}
"""
```

Есть [.env поддержка](https://pydantic-docs.helpmanual.io/usage/settings/#dotenv-env-support)

.env файл

```.env
# ignore comment
ENVIRONMENT="production"
REDIS_ADDRESS=localhost:6379
MEANING_OF_LIFE=42
MY_VAR='Hello world'
```

создание модели настроек

```python
class Settings(BaseSettings):
    ...

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
```

Создание инстанса настроек

```python
settings = Settings(_env_file='prod.env', _env_file_encoding='utf-8')
```

## [Postponed annotations](https://pydantic-docs.helpmanual.io/usage/postponed_annotations/)

## [Использование devtools](https://pydantic-docs.helpmanual.io/usage/devtools/)

- [[devtools]]
- [[pydantic-validation-custom]]
- [[fastapi-setting-environment-variables]] про поддержку .env

[//begin]: # "Autogenerated link references for markdown compatibility"
[type-annotation]: type-annotation "Анотация типов в python"
[mypy]: mypy "Mypy"
[openapi-specification]: openapi-specification "Open-api v3 спецификация"
[devtools]: devtools "Python devtools"
[pydantic-validation-custom]: pydantic-validation-custom "Pydantic-validation-custom"
[fastapi-setting-environment-variables]: fastapi-setting-environment-variables "Fastapi environment variables"
[//end]: # "Autogenerated link references"