# pydantic

Типизация для #python [Документация](https://pydantic-docs.helpmanual.io/)

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

#### OEM модели

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

Иногда нужно дать название колонке, после того, как зарещервирвоано название поля.

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

```python
from datetime import datetime
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

class Model(BaseModel):
    uid: UUID = Field(default_factory=uuid4)
    updated: datetime = Field(default_factory=datetime.utcnow)
```
