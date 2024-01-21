---
description: Pydantic-factories - создание фиктивных данных для pydantic_models
title: Pydantic-factories
tags: pydantic pip tests python
---
Эта библиотека предлагает мощные возможности создания фиктивных данных для моделей и классов данных на основе pydantic. Можно использовать с другими библиотеками, использующими pydantic в качестве основы, например SQLModel и Beanie.

```python
from datetime import date, datetime
from typing import List, Union

from pydantic import BaseModel, UUID4

from pydantic_factories import ModelFactory


class Person(BaseModel):
    id: UUID4
    name: str
    hobbies: List[str]
    age: Union[float, int]
    birthday: Union[datetime, date]


class PersonFactory(ModelFactory):
    __model__ = Person


result = PersonFactory.build()
```

Мы можем создать фиктивный объект данных, соответствующий определению модели класса Person. Это возможно из-за информации о типизации, доступной в модели pydantic и полях модели, которые используются в качестве источника истины для генерации данных. Фабрика анализирует информацию, хранящуюся в модели pydantic, и создает словарь kwargs, который передается методу init класса Person.

Возможности:

- поддерживает как встроенные, так и [[pydantic]] типы.
- поддерживает ограничения поля pydantic
- поддерживает сложные типы полей
- поддерживает настраиваемые поля модели

## Методы

Класс `ModelFactory` предоставляет два метода сборки:

`.build(**kwargs)` — строит один экземпляр модели фабрики
`.batch(size: int, **kwargs)` — построить список размером n экземпляров

```python
result = PersonFactory.build()  # a single Person instance

result = PersonFactory.batch(size=5)  # list[Person, Person, Person, Person, Person]
```

Любые kwargs, которые вы передаете в `.build`, `.batch` или любой из методов, будут иметь приоритет над любыми значениями по умолчанию, определенными в самом фабричном классе.

По умолчанию при создании класса pydantic проверяются kwargs. Чтобы избежать проверки ввода, вы можете использовать параметр `factory_use_construct`.

```python
result = PersonFactory.build(id=5)  # Raises a validation error

result = PersonFactory.build(
    factory_use_construct=True, id=5
)  # Build a Person with invalid id
```

## Поддерживаются встроенные и сконструированные типы

```python
from datetime import date, datetime
from enum import Enum
from pydantic import BaseModel, UUID4
from typing import Any, Dict, List, Union

from pydantic_factories import ModelFactory


class Species(str, Enum):
    CAT = "Cat"
    DOG = "Dog"
    PIG = "Pig"
    MONKEY = "Monkey"


class Pet(BaseModel):
    name: str
    sound: str
    species: Species


class Person(BaseModel):
    id: UUID4
    name: str
    hobbies: List[str]
    age: Union[float, int]
    birthday: Union[datetime, date]
    pets: List[Pet]
    assets: List[Dict[str, Dict[str, Any]]]


class PersonFactory(ModelFactory):
    __model__ = Person


result = PersonFactory.build()
```

Этот пример также будет работать, хотя для класса Pet не была определена фабрика, это не проблема — фабрика будет динамически сгенерирована для него на лету.

Сложная типизация под атрибутом assets немного сложнее, но фабрика сгенерирует объект python, соответствующий этой сигнатуре, поэтому пройдет проверку.

Обратите внимание: единственное, что фабрики не могут обработать, — это модели, ссылающиеся на самих себя, потому что это может привести к ошибкам рекурсии. В этом случае вам нужно будет обработать конкретное поле, установив для него значения по умолчанию.

## Датаклассы

Эта библиотека работает с любым классом, который наследует класс pydantic BaseModel, включая GenericModel и классы из сторонних библиотек, а также с классами данных — как из стандартной библиотеки python, так и из классов данных pydantic. Фактически, вы можете использовать их взаимозаменяемо.

```python
import dataclasses
from typing import Dict, List

import pydantic
from pydantic_factories import ModelFactory


@pydantic.dataclasses.dataclass
class MyPydanticDataClass:
    name: str


class MyFirstModel(pydantic.BaseModel):
    dataclass: MyPydanticDataClass


@dataclasses.dataclass()
class MyPythonDataClass:
    id: str
    complex_type: Dict[str, Dict[int, List[MyFirstModel]]]


class MySecondModel(pydantic.BaseModel):
    dataclasses: List[MyPythonDataClass]


class MyFactory(ModelFactory):
    __model__ = MySecondModel


result = MyFactory.build()
```

При создании фиктивных значений для полей с типом optional, если фабрика определена с `__allow_none_Options__ = True`, значение поля будет либо значением, либо `None` — в зависимости от случайного решения. Это работает, даже если необязательное типирование глубоко вложено, за исключением классов данных — типизация только поверхностно оценивается для классов данных, и поэтому всегда предполагается, что они требуют значения. Если вы хотите иметь значение `None`, в данном конкретном случае вы должны сделать это вручную, настроив обратный вызов Use для конкретного поля.

## Конфигурирование фабрики

Конфигурация `ModelFactory` выполняется с использованием переменных класса:

`__model__`: обязательная переменная, определяющая модель фабрики. Он принимает любой класс, который расширяет `BaseModel` pydantic, включая классы из других библиотек. Если эта переменная не установлена, будет возбуждено исключение `ConfigurationException.`

`__faker__`: необязательная переменная, указывающая настроенный пользователем экземпляр фиктивных данных. Если эта переменная не установлена, фабрика по умолчанию будет использовать ванильный фейкер.

`__sync_persistence__`: необязательная переменная, указывающая обработчик для синхронно сохраняемых данных. Если эта переменная не установлена, методы фабрики `.create_sync` и `.create_batch_sync` использовать нельзя.

`__async_persistence__`: необязательная переменная, определяющая обработчик асинхронно сохраняемых данных. Если эта переменная не задана, методы фабрики `.create_async` и `.create_batch_async` использовать нельзя.

`__allow_none_optionals__`: необязательная переменная, определяющая, должна ли фабрика случайным образом устанавливать значения `None` для необязательных полей или всегда устанавливать для них значения. Это `True` по умолчанию.

```python
from faker import Faker
from pydantic_factories import ModelFactory

from app.models import Person
from .persistence import AsyncPersistenceHandler, SyncPersistenceHandler

Faker.seed(5)
my_faker = Faker("en-EN")


class PersonFactory(ModelFactory):
    __model__ = Person
    __faker__ = my_faker
    __sync_persistence__ = SyncPersistenceHandler
    __async_persistence__ = AsyncPersistenceHandler
    __allow_none_optionals__ = False
    ...
```

Для генерации детерменистических данных используйте метод `ModelFactory.seed_random`. Это передаст начальное значение как `Faker`, так и вызову случайного метода, гарантируя, что данные будут одинаковыми между вызовами. Особенно полезно для тестирования.

## Определение атрибутов

```python
from datetime import date, datetime
from enum import Enum
from pydantic import BaseModel, UUID4
from typing import Any, Dict, List, Union


class Species(str, Enum):
    CAT = "Cat"
    DOG = "Dog"


class Pet(BaseModel):
    name: str
    species: Species


class Person(BaseModel):
    id: UUID4
    name: str
    hobbies: List[str]
    age: Union[float, int]
    birthday: Union[datetime, date]
    pets: List[Pet]
    assets: List[Dict[str, Dict[str, Any]]]
```

Первый способ - непосредственно при создании

```python
pet = Pet(name="Roxy", sound="woof woof", species=Species.DOG)


class PersonFactory(ModelFactory):
    __model__ = Person

    pets = [pet]
```

В этом случае, когда мы вызываем `PersonFactory.build()`, результат будет сгенерирован случайным образом, за исключением списка питомцев, который будет жестко запрограммированным значением по умолчанию, которое мы определили.

### Поле Use

Другой вариант - определить фабрику для Pet, где мы ограничиваем выбор диапазоном, который нам нравится.

```python
from enum import Enum
from pydantic_factories import ModelFactory, Use
from random import choice

from .models import Pet, Person


class Species(str, Enum):
    CAT = "Cat"
    DOG = "Dog"


class PetFactory(ModelFactory):
    __model__ = Pet

    name = Use(choice, ["Ralph", "Roxy"])
    species = Use(choice, list(Species))


class PersonFactory(ModelFactory):
    __model__ = Person

    pets = Use(PetFactory.batch, size=2)
```

или так (не используя Use):

```python
class PetFactory(ModelFactory):
    __model__ = Pet

    name = lambda: choice(["Ralph", "Roxy"])
    species = lambda: choice(list(Species))
```

### Поле PostGenerated

Позволяет создавать поля на основе уже сгенерированных значений других (не созданных таким способом) полей. В большинстве случаев этого шаблона лучше избегать.

```python
from pydantic import BaseModel
from pydantic_factories import ModelFactory, PostGenerated
from random import randint


def add_timedelta(name: str, values: dict, *args, **kwds):
    delta = timedelta(days=randint(0, 12), seconds=randint(13, 13000))
    return values["from_dt"] + delta


class MyModel(BaseModel):
    from_dt: datetime
    to_dt: datetime


class MyFactory(ModelFactory):
    __model__ = MyModel

    to_dt = PostGenerated(add_timedelta)
```

### Поле Ignore

Используется для обозначения данного атрибута как игнорируемого.

```python
from typing import TypeVar

from odmantic import EmbeddedModel, Model
from pydantic_factories import ModelFactory, Ignore

T = TypeVar("T", Model, EmbeddedModel)


class OdmanticModelFactory(ModelFactory[T]):
    id = Ignore()
```

### Поле Require

Указывает, что конкретный атрибут является обязательным kwarg. То есть, если kwarg со значением для этого конкретного атрибута не передается при вызове `factory.build()`, будет поднята ошибка `MissingBuildKwargError`.

Каков вариант использования для этого? Например, предположим, что у нас есть документ под названием Article, который мы храним в какой-либо БД и который представлен с использованием не-pydantic модели, скажем, документа с эластичной DSL. Затем нам нужно сохранить в нашем объекте pydantic ссылку на идентификатор этой статьи. Это значение не должно быть каким-то фиктивным значением, а должно быть фактическим идентификатором, переданным на фабрику. Таким образом, мы можем определить этот атрибут по мере необходимости:

```python
from pydantic import BaseModel
from pydantic_factories import ModelFactory, Require
from uuid import UUID


class ArticleProxy(BaseModel):
    article_id: UUID
    ...


class ArticleProxyFactory(ModelFactory):
    __model__ = ArticleProxy

    article_id = Require()
```

### Persistence

ModelFactory имеет четыре метода сохранения:

- `.create_sync(**kwargs)` — синхронно создает и сохраняет один экземпляр модели фабрики.
- `.create_batch_sync(size: int, **kwargs)` — синхронно создает и сохраняет список размером n экземпляров.
- `.create_async(**kwargs)` — асинхронно создает и сохраняет один экземпляр модели фабрики.
- `.create_batch_async(size: int, **kwargs)` — асинхронно создает и сохраняет список размером n экземпляров.

Чтобы использовать эти методы, вы должны сначала указать синнные и/или асинхронные обработчики для фабрики:

```python
# persistence.py
from typing import TypeVar, List

from pydantic import BaseModel
from pydantic_factories import SyncPersistenceProtocol

T = TypeVar("T", bound=BaseModel)


class SyncPersistenceHandler(SyncPersistenceProtocol[T]):
    def save(self, data: T) -> T:
        ...  # do stuff

    def save_many(self, data: List[T]) -> List[T]:
        ...  # do stuff


class AsyncPersistenceHandler(AsyncPersistenceProtocol[T]):
    async def save(self, data: T) -> T:
        ...  # do stuff

    async def save_many(self, data: List[T]) -> List[T]:
        ...  # do stuff
```

Затем вы можете указать один или оба этих обработчика в вашей фабрике:

```python
from pydantic_factories import ModelFactory

from app.models import Person
from .persistence import AsyncPersistenceHandler, SyncPersistenceHandler


class PersonFactory(ModelFactory):
    __model__ = Person
    __sync_persistence__ = SyncPersistenceHandler
    __async_persistence__ = AsyncPersistenceHandler
```

Или создайте свою собственную базовую фабрику и повторно используйте ее в различных фабриках:

```python
from pydantic_factories import ModelFactory

from app.models import Person
from .persistence import AsyncPersistenceHandler, SyncPersistenceHandler


class BaseModelFactory(ModelFactory):
    __sync_persistence__ = SyncPersistenceHandler
    __async_persistence__ = AsyncPersistenceHandler


class PersonFactory(BaseModelFactory):
    __model__ = Person
```

Обратите внимание: вам не нужно определять какой-либо или оба обработчика сохранения. Если вы будете использовать только синхронное или асинхронное сохранение, вам нужно только определить соответствующий обработчик для использования этих методов.

## Дополнительно - [создание фабричных методов](https://github.com/Goldziher/pydantic-factories#create-factory-method)

Если вы предпочитаете императивное создание фабрики, вы можете сделать это с помощью метода `ModelFactory.create_factory`. Этот метод получает следующие аргументы:

- `model` - модель для фабрики.
- `base` - необязательный базовый класс фабрики. По умолчанию используется фабричный класс, для которого вызывается метод.
- `kwargs` - словарь аргументов, соответствующих переменным класса, принятым `ModelFactory`.
Вы также можете переопределить атрибут `__model__` дочерней фабрики, чтобы указать используемую модель и `kwargs`

Пример

```python
from datetime import date, datetime
from enum import Enum
from pydantic import BaseModel, UUID4
from typing import Any, Dict, List, TypeVar, Union, Generic, Optional
from pydantic_factories import ModelFactory


class Species(str, Enum):
    CAT = "Cat"
    DOG = "Dog"


class PetBase(BaseModel):
    name: str
    species: Species


class Pet(PetBase):
    id: UUID4


class PetCreate(PetBase):
    pass


class PetUpdate(PetBase):
    pass


class PersonBase(BaseModel):

    name: str
    hobbies: List[str]
    age: Union[float, int]
    birthday: Union[datetime, date]
    pets: List[Pet]
    assets: List[Dict[str, Dict[str, Any]]]


class PersonCreate(PersonBase):
    pass


class Person(PersonBase):
    id: UUID4


class PersonUpdate(PersonBase):
    pass


def test_factory():
    class PersonFactory(ModelFactory):
        __model__ = Person

    person = PersonFactory.build()

    assert person.pets != []


ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BUILDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(
        self,
        model: ModelType = None,
        create_schema: Optional[CreateSchemaType] = None,
        update_schema: Optional[UpdateSchemaType] = None,
    ):
        self.model = model
        self.create_model = create_schema
        self.update_model = update_schema

    def build_object(self) -> ModelType:
        object_Factory = ModelFactory.create_factory(self.model)
        return object_Factory.build()

    def build_create_object(self) -> CreateSchemaType:
        object_Factory = ModelFactory.create_factory(self.create_model)
        return object_Factory.build()

    def build_update_object(self) -> UpdateSchemaType:
        object_Factory = ModelFactory.create_factory(self.update_model)
        return object_Factory.build()


class BUILDPet(BUILDBase[Pet, PetCreate, PetUpdate]):
    def build_object(self) -> Pet:
        object_Factory = ModelFactory.create_factory(self.model, name="Fido")
        return object_Factory.build()

    def build_create_object(self) -> PetCreate:
        object_Factory = ModelFactory.create_factory(self.create_model, name="Rover")
        return object_Factory.build()

    def build_update_object(self) -> PetUpdate:
        object_Factory = ModelFactory.create_factory(self.update_model, name="Spot")
        return object_Factory.build()


def test_factory_create():

    person_factory = BUILDBase(Person, PersonCreate, PersonUpdate)

    pet_factory = BUILDPet(Pet, PetCreate, PetUpdate)

    create_person = person_factory.build_create_object()
    update_person = person_factory.build_update_object()

    pet = pet_factory.build_object()
    create_pet = pet_factory.build_create_object()
    update_pet = pet_factory.build_update_object()

    assert create_person != None
    assert update_person != None

    assert pet.name == "Fido"
    assert create_pet.name == "Rover"
    assert update_pet.name == "Spot"
```

## Дополнительно

Любой класс, производный от `BaseModel` pydantic, может использоваться как `__model__` фабрики. Для большинства сторонних библиотек, например. `SQLModel`, эта библиотека будет работать как есть из коробки.

Есть API для [[ormar]]

Смотри еще:

- [гитхаб](https://github.com/Goldziher/pydantic-factories)
- [[pydantic]]
- [[pytest]]
- [[mock-libraries]]
- [[mock]]
- [[faker]]
- [[тестирование]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[pydantic]: pydantic "Pydantic"
[ormar]: ormar "Ormar"
[pytest]: pytest "Pytest"
[mock-libraries]: mock-libraries "Либы для создания моков"
[mock]: mock "Mock-тесты"
[faker]: faker "Faker - пакет для создания фейковых данных для тестов"
[тестирование]: ../lists/%D1%82%D0%B5%D1%81%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5 "Основные принципы тестровния"
[//end]: # "Autogenerated link references"
[//begin]: # "Autogenerated link references for markdown compatibility"
[pydantic]: pydantic "Pydantic"
[ormar]: ormar "Ormar"
[pydantic]: pydantic "Pydantic"
[pytest]: pytest "Pytest"
[mock-libraries]: mock-libraries "Либы для создания моков"
[mock]: mock "Mock-тесты"
[faker]: faker "Faker - пакет для создания фейковых данных для тестов"
[тестирование]: ../lists/тестирование "Основные принципы тестровния"
[//end]: # "Autogenerated link references"