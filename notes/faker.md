---
description: Моки данных на python
tags: tests pip python
title: Faker - пакет для создания фейковых данных для тестов
---
`pip install Faker`

Доступны методы, генерирующие разные данные (имена, адреса, имейлы). Есть возможность уточнять локализацию.

Каждый вызов метода объекта добавляет новые рандомные результаты.

```python
from faker import Faker
fake = Faker(['it_IT', 'en_US', 'ja_JP'])
for _ in range(10):
    print(fake.name())

# 鈴木 陽一
# Leslie Moreno
# Emma Williams
# 渡辺 裕美子
# Marcantonio Galuppi
# Martha Davis
# Kristen Turner
# 中津川 春香
# Ashley Castillo
# 山田 桃子
```

## [Использование класса](https://faker.readthedocs.io/en/master/fakerclass.html) `Faker`

```python
from faker import Faker
fake = Faker()
Faker.seed(4321)

print(fake.name())
# 'Margaret Boehm'
```

Другой вариант - передать каждому экземпляру генератора свой `random.Random`:

```python
from faker import Faker
fake = Faker()
fake.seed_instance(4321)

print(fake.name())
# 'Margaret Boehm'
```

Пример использования множества локалей

```python
from collections import OrderedDict
from faker import Faker
locales = OrderedDict([
    ('en-US', 1),
    ('en-PH', 2),
    ('ja_JP', 3),
])
fake = Faker(locales)

# Get the list of locales specified during instantiation
fake.locales

# Get the list of internal generators of this `Faker` instance
fake.factories

# Get the internal generator for 'en_US' locale
fake['en_US']

# Get the internal generator for 'en_PH' locale
fake['en_PH']

# Get the internal generator for 'ja_JP' locale
fake['ja_JP']

# Will raise a KeyError as 'en_GB' was not included
fake['en_GB']

# Set the seed value of the shared `random.Random` object
# across all internal generators that will ever be created
Faker.seed(0)

# Creates and seeds a unique `random.Random` object for
# each internal generator of this `Faker` instance
fake.seed_instance(0)

# Creates and seeds a unique `random.Random` object for
# the en_US internal generator of this `Faker` instance
fake.seed_locale('en_US', 0)

# Generate a name based on the provided weights
# en_US - 16.67% of the time (1 / (1 + 2 + 3))
# en_PH - 33.33% of the time (2 / (1 + 2 + 3))
# ja_JP - 50.00% of the time (3 / (1 + 2 + 3))
fake.name()

# Generate a name under the en_US locale
fake['en-US'].name()

# Generate a zipcode based on the provided weights
# Note: en_PH does not support the zipcode provider method
# en_US - 25% of the time (1 / (1 + 3))
# ja_JP - 75% of the time (3 / (1 + 3))
fake.zipcode()

# Generate a zipcode under the ja_JP locale
fake['ja_JP'].zipcode()

# Will raise an AttributeError
fake['en_PH'].zipcode()

# Generate a Luzon province name
# Note: only en_PH out of the three supports this provider method
fake.luzon_province()

# Generate a Luzon province name
fake['en_PH'].luzon_province()

# Will raise an AttributeError
fake['ja_JP'].luzon_province()
```

Есть возможность создавать объекты, уникальные на всей протяженности жизни инстанса `Faker()`:

```python
import faker

fake = faker.Faker()

numbers = set(fake.unique.random_int() for i in range(1000))
assert len(numbers) == 1000
```

## [Провайдеры](https://faker.readthedocs.io/en/master/providers.html)

- faker.providers
- faker.providers.address
- faker.providers.automotive
- faker.providers.bank
- faker.providers.barcode
- faker.providers.color
- faker.providers.company
- faker.providers.credit_card
- faker.providers.currency
- faker.providers.date_time
- faker.providers.file
- faker.providers.geo
- faker.providers.internet
- faker.providers.isbn
- faker.providers.job
- faker.providers.lorem
- faker.providers.misc
- faker.providers.person
- faker.providers.phone_number
- faker.providers.profile
- faker.providers.python
- faker.providers.ssn
- faker.providers.user_agent

Так-же [комьюнити-бейст дополнение](https://faker.readthedocs.io/en/master/communityproviders.html):

- Airtravel
- Biology
- Credit Score
- Microservice
- Music
- Posts
- Vehicle
- WebProvider
- Wi-Fi
- Optional

Тут [информация о локализации провадеров](https://faker.readthedocs.io/en/master/locales.html)

Провайдеров [можно создавать и кастомизировать](https://faker.readthedocs.io/en/master/#how-to-create-a-provider)

## [[pytest]] [фикстуры](https://faker.readthedocs.io/en/master/pytest-fixtures.html)

Доступны фикстуры из коробки. По умолчанию фикстура faker возвращает экземпляр Faker с областью действия сеанса, который будет использоваться во всех тестах в наборе тестов. По умолчанию для этого экземпляра используется языковой стандарт en-US, он повторно заполняется с использованием начального значения 0 перед каждым тестом, а запомненные сгенерированные значения .unique очищаются. Чтобы изменить это поведение - надо переопределить фикстуры `faker_session_locale`, `autouse_faker_seed` в `conftest.py`

```python
import pytest

@pytest.fixture(scope='session', autouse=True)
def faker_session_locale():
    return ['it_IT']

@pytest.fixture(scope='session', autouse=True)
def faker_seed():
    return 12345
```

или так:

```python
import pytest

@pytest.fixture(scope='session', autouse=True)
def faker_session_locale():
    return ['it_IT', 'ja_JP', 'en_US']
```

[Подробнее о конфигурации](https://faker.readthedocs.io/en/master/pytest-fixtures.html#configuration-options)

Смотри еще:

- [документация](https://faker.readthedocs.io/en/master/)
- [[тестирование]]
- [[mock-libraries]]
- [[pytest]]
- [[pydantic-factories]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[pytest]: pytest "Pytest"
[тестирование]: ..%2Flists%2F%D1%82%D0%B5%D1%81%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5 "Основные принципы тестровния"
[mock-libraries]: mock-libraries "Либы для создания моков"
[pydantic-factories]: pydantic-factories "Pydantic-factories"
[//end]: # "Autogenerated link references"