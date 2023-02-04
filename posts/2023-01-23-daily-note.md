---
title: Some pydantic tricks-1. Закрытые атрибуты, женерики, корневые типы, корневые валидаторы, заполнение полей и ошибки в mypy
description: Несколько трюков с pydantic - закрытые атрибуты, женерики, корневые типы, корневые валидаторы, заполнение полей и ошибки в mypy
category: post
tags: pydantic python
---
## [Private model attributes](https://docs.pydantic.dev/usage/models/#private-model-attributes)

Если вам нужно изменить или манипулировать внутренними атрибутами экземпляров модели, вы можете объявить их с помощью `PrivateAttr`. Имена частных атрибутов должны начинаться с подчеркивания, чтобы предотвратить конфликты с полями модели: поддерживаются как `_attr`, так и `__attr__`. Если `Config`.`underscore_attrs_are_private` имеет значение `True`, любой атрибут с дандером, не относящийся к `ClassVar`, будет рассматриваться как приватный.

```python
from typing import ClassVar
from datetime import datetime
from random import randint
from pydantic import BaseModel, PrivateAttr

class TimeAwareModel(BaseModel):
    _processed_at: datetime = PrivateAttr(default_factory=datetime.now)
    _secret_value: str = PrivateAttr()

    def __init__(self, **data):
        super().__init__(**data)
        # this could also be done with default_factory
        self._secret_value = randint(1, 5)


class Model(BaseModel):
    _class_var: ClassVar[str] = 'class var value'
    _private_attr: str = 'private attr value'

    class Config:
        underscore_attrs_are_private = True
```

## [Model and field level include and exclude](https://docs.pydantic.dev/usage/exporting_models/#advanced-include-and-exclude)

В дополнение к явным аргументам `exclude` и `include`, передаваемым в методы `dict`, `json` и `copy`, мы также можем передать аргументы `include/exclude` непосредственно конструктору `Field` или эквивалентной записи поля в классе `Config` моделей.

```python
from pydantic import BaseModel, Field, SecretStr


class User(BaseModel):
    id: int
    username: str
    password: SecretStr = Field(..., exclude=True)


class Transaction(BaseModel):
    id: str
    user: User = Field(..., exclude={'username'})
    value: int

    class Config:
        fields = {'value': {'exclude': True}}


t = Transaction(
    id='1234567890',
    user=User(
        id=42,
        username='JohnDoe',
        password='hashedpassword'
    ),
    value=9876543210,
)

print(t.dict())
#> {'id': '1234567890', 'user': {'id': 42}}
```

[Остальные примеры](https://docs.pydantic.dev/usage/exporting_models/#advanced-include-and-exclude)

## [Generic Models](https://docs.pydantic.dev/usage/models/#generic-models)

В [[pydantic]] поддерживается создание универсальных моделей, чтобы упростить повторное использование общей структуры модели.

Чтобы объявить универсальную модель, выполните следующие шаги:

- Объявите один или несколько экземпляров `typing.TypeVar` для использования для параметризации вашей модели.
- Объявите модель `pydantic`, которая наследуется от `pydantic.generics.GenericModel` и `typing.Generic,` где вы передаете экземпляры `TypeVar` в качестве параметров в `typing.Generic`.
- Используйте экземпляры `TypeVar` в качестве аннотаций, когда вы захотите заменить их другими типами или моделями `pydantic`.

[Примеры тут](https://docs.pydantic.dev/usage/models/#generic-models)

## [How does Pydantic implement overriding defaults in the Config class?](https://stackoverflow.com/a/72724820/15966204)

```python
class Person(BasePerson):
    class Config(BasePerson.Config):
        n_arms = 1
```

## [How can I create a MappingModel using pydantic?](https://stackoverflow.com/a/66255455/15966204)

Можно использовать [Custom Root Types](https://docs.pydantic.dev/usage/models/#custom-root-types). Модели Pydantic можно определить с пользовательским корневым типом, объявив поле `__root__`. Корневой тип может быть любым типом, поддерживаемым `pydantic`, и указывается подсказкой типа в поле `__root__`. Корневое значение может быть передано в модель `__init__` через ключевой аргумент `__root__` или в качестве первого и единственного аргумента для `parse_obj`. [Подробнее тут](https://docs.pydantic.dev/usage/models/#custom-root-types).

```python
from typing import Dict, Any
from pydantic import BaseModel


class Model(BaseModel):
    __root__: Dict[str, Any]

    def __iter__(self):
        return iter(self.__root__)

    def __getattr__(self, item):
        return self.__root__[item]


m = Model.parse_obj({'key1': 'val1', 'key2': 'val2'})
assert m.key1 == "val1"
```

Dictlike объект должен реализовывать [такие методы](https://stackoverflow.com/a/23976949/15966204):

```python
class Mapping(dict):

    def __setitem__(self, key, item):
        self.__dict__[key] = item

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        return repr(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __delitem__(self, key):
        del self.__dict__[key]

    def clear(self):
        return self.__dict__.clear()

    def copy(self):
        return self.__dict__.copy()

    def has_key(self, k):
        return k in self.__dict__

    def update(self, *args, **kwargs):
        return self.__dict__.update(*args, **kwargs)

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()
```

[[2022-11-07-daily-note]] кастомные классы от python-словаря

## How Serialize a property?

Можно использовать женерики [[pydantic]], создав сабкласс, поддерживающий сериализацию свойств.

```python
class PropertyBaseModel(BaseModel):
    """
    Workaround for serializing properties with pydantic until
    https://github.com/samuelcolvin/pydantic/issues/935
    is solved
    """
    @classmethod
    def get_properties(cls):
        return [
            prop for prop
            in dir(cls)
            if isinstance(getattr(cls, prop), property)
            and prop not in ("__values__", "fields")
                ]

    def dict(
        self,
        *,
        include: Union['AbstractSetIntStr', 'MappingIntStrAny'] = None,
        exclude: Union['AbstractSetIntStr', 'MappingIntStrAny'] = None,
        by_alias: bool = False,
        skip_defaults: bool = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> 'DictStrAny':
        attribs = super().dict(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none
        )
        props = self.get_properties()
        # Include and exclude properties
        if include:
            props = [prop for prop in props if prop in include]
        if exclude:
            props = [prop for prop in props if prop not in exclude]

        # Update the attribute dict with the properties
        if props:
            attribs.update({prop: getattr(self, prop) for prop in props})

        return attribs
```

Это (и другие) - неофициальная реализация. Читай [обсуждение тут](https://github.com/pydantic/pydantic/issues/935#issuecomment-641175527).

Еще решение для заполнения: [pydantic-computed](https://pypi.org/project/pydantic-computed/)

```python
from pydantic import BaseModel
from pydantic_computed import Computed, computed

class ExampleModel(BaseModel):
    a: int
    b: int
    c: Computed[int]

    @computed('c')
    def calculate_c(a: int, **kwargs):
        return a + 1

model = ExampleModel(a=1, b=2)
print(model.c) # Outputs 2
```

## [Required fields format](https://docs.pydantic.dev/usage/models/#field-ordering)

Чтобы объявить поле обязательным, вы можете объявить его, используя только аннотацию, или вы можете использовать многоточие `(...)` в качестве значения:

```python
from pydantic import BaseModel, Field


class Model(BaseModel):
    a: int
    b: int = ...
    c: int = Field(...)
```

Тот же подход для опциональных обязательных полей, которые могут принимать значение `None` если не заполнены:

```python
from typing import Optional
from pydantic import BaseModel, Field, ValidationError


class Model(BaseModel):
    a: Optional[int]
    b: Optional[int] = ...
    c: Optional[int] = Field(...)
```

## [Root Validators](https://docs.pydantic.dev/usage/validators/#root-validators)

Root-валидаторы используются для валидации всех данных модели. Один из вариантов примененеия - это заполнение полей перед или после примененеия (что бывает полезно, когда входящая модель определяет поля, для которых вы не хотите назначать алиасы). [Пример со stackoweflow](https://stackoverflow.com/questions/63676411/pydantic-how-to-use-one-fields-value-to-set-values-for-other-fields):

```python

class User(BaseModel):
    account_type: Optional[str] = 'user'
    field1: Optional[str] = ''
    field1: Optional[str] = ''

    @root_validator(pre=False)
    def _set_fields(cls, values: dict) -> dict:
        """This is a validator that sets the field values based on the
        the user's account type.

        Args:
            values (dict): Stores the attributes of the User object.

        Returns:
            dict: The attributes of the user object with the user's fields.
        """
        values["field1"] = user_dict[values["account_type"]]["field1"]
        values["field2"] = user_dict[values["account_type"]]["field2"]
        return values
```

Как и в случае с валидаторами полей, корневые валидаторы могут иметь `pre=True`, и в этом случае они вызываются до того, как происходит проверка поля (и предоставляются с необработанными входными данными), или `pre=False` (по умолчанию), и в этом случае они вызывается после проверки поля. Проверка поля не будет выполняться, если корневые валидаторы `pre=True` выдают ошибку. Как и в случае с валидаторами полей, корневые валидаторы с `pre=False` по умолчанию будут вызываться, даже если предыдущие валидаторы терпят неудачу; это поведение можно изменить, установив аргумент ключевого слова `skip_on_failure=True` для валидатора. Аргумент значений будет представлять собой словарь, содержащий значения, прошедшие проверку поля, и поля по умолчанию, там где это применимо.

## MyPy error with custom pydantic fields

Вот это будет выдавать ошибку:

```python
from pydantic import BaseModel, conint

class MyPyProblem(BaseModel):
    big_int: conint(gt=1000, lt=1024) = None
```

Решение ([обсуждалось тут](https://github.com/pydantic/pydantic/issues/239)):

```python
from typing import cast
from pydantic import BaseModel, ConstrainedInt

class BigInt(ConstrainedInt):
    gt = 1000
    lt = 1024

class MyModel(BaseModel):
    foo: BigInt  # required
    bar: BigInt = cast(BigInt, 1001)  # with a default

m = MyModel(foo=1011)
print(m.dict())
```

Смотри еще:

- [[pydantic]]
- [[python-standart-library]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[pydantic]: ../notes/pydantic "Pydantic"
[2022-11-07-daily-note]: 2022-11-07-daily-note "Кастомные классы от python-словаря"
[pydantic]: ../notes/pydantic "Pydantic"
[pydantic]: ../notes/pydantic "Pydantic"
[python-standart-library]: ../lists/python-standart-library "Стандартная библиотека python и полезные ресурсы"
[//end]: # "Autogenerated link references"
[//begin]: # "Autogenerated link references for markdown compatibility"
[pydantic]: ../notes/pydantic "Pydantic"
[2022-11-07-daily-note]: 2022-11-07-daily-note "Кастомные классы от python-словаря"
[pydantic]: ../notes/pydantic "Pydantic"
[pydantic]: ../notes/pydantic "Pydantic"
[python-standart-library]: ../lists/python-standart-library "Стандартная библиотека python и полезные ресурсы"
[//end]: # "Autogenerated link references"