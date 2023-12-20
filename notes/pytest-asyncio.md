---
description: Асинхронное тестирование с использованием pytest
tags: tests pip python asyncio
title: Pytest-asyncio
---
pytest-asyncio запускает каждый тестовый элемент в своем собственном цикле событий [[asyncio]]. Доступ к циклу можно получить через фикстуру `event_loop`, которая автоматически запрашивается всеми асинхронными тестами.

```python
async def test_provided_loop_is_running_loop(event_loop):
    assert event_loop is asyncio.get_running_loop()
```

Pytest-asyncio предоставляет два режима обнаружения тестов: строгий и автоматический.

## Строгий режим

В строгом режиме pytest-asyncio будет запускать только тесты с маркером [[asyncio]] и оценивать только асинхронные фикстуры, декорированные @pytest_asyncio.fixture. Тестовые функции и фикстуры без этих маркеров и декораторов не будут обрабатываться pytest-asyncio.

Этот режим предназначен для проектов, которые хотят поддерживать несколько библиотек асинхронного программирования, поскольку он позволяет pytest-asyncio сосуществовать с другими плагинами для асинхронного тестирования в одной кодовой базе.

Pytest автоматически включает установленные плагины. В результате плагины [[pytest]] должны мирно сосуществовать в конфигурации по умолчанию. Вот почему строгий режим является режимом по умолчанию.

## Автоматический режим

В автоматическом режиме pytest-asyncio автоматически добавляет маркер asyncio ко всем функциям асинхронного тестирования. Он также станет владельцем всех асинхронных фикстур, независимо от того, декорированы ли они символами @pytest.fixture или @pytest_asyncio.fixture.

Этот режим предназначен для проектов, которые используют [[asyncio]] в качестве единственной библиотеки асинхронного программирования. Автоматический режим обеспечивает простейшую настройку теста и приспособления и является рекомендуемым значением по умолчанию.

Если вы собираетесь поддерживать несколько библиотек асинхронного программирования, например, [[asyncio]] и [[trio]], предпочтительным вариантом будет строгий режим.

## Конфиг

```yml
# pytest.ini
[pytest]
asyncio_mode = auto
```

`pytest tests --asyncio-mode=strict` для выбора режима

## [Fixtures](https://pytest-asyncio.readthedocs.io/en/latest/reference/fixtures.html)

`event_loop` создает новый асинхронный цикл событий на основе текущей политики цикла событий. Новый цикл доступен как возвращаемое значение этой фикстуры или через `asyncio.get_running_loop`. Цикл событий завершается, когда область действия фикстуры заканчивается. Область фикстуры по умолчанию ограничивается областью видимости функции.

```python
def test_http_client(event_loop):
    url = "http://httpbin.org/get"
    resp = event_loop.run_until_complete(http_client(url))
    assert b"HTTP/1.1 200 OK" in resp
```

Обратите внимание, что при использовании фикстуры `event_loop` вам необходимо взаимодействовать с циклом событий, используя такие методы, как `event_loop.run_until_complete`. Если вы хотите ожидать код внутри своей тестовой функции, вам нужно написать сопрограмму и использовать ее в качестве тестовой функции. Маркер asyncio используется для обозначения сопрограмм, которые следует рассматривать как тестовые функции. Фикстура `event_loop` может быть переопределена в любом из стандартных местоположений [[pytest]], например, непосредственно в тестовом файле или в `conftest.py`. Это позволяет переопределить область видимости:

```python
@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()
```

Если вам нужно изменить тип цикла событий, необходимо установить пользовательскую политику цикла событий, а не переопределять фикстуру `event_loop`.

Если декоратор `pytest.mark.asyncio` применяется к тестовой функции, фикстура `event_loop` будет автоматически запрашиваться тестовой функцией.

Другие готовые фикстуры: `unused_tcp_port`, `unused_tcp_port_factory`, `unused_udp_port` and `unused_udp_port_factory`.

## [Markers](https://pytest-asyncio.readthedocs.io/en/latest/reference/markers.html)

Сопрограмма или асинхронный генератор с маркером `pytest.mark.asyncio` будут рассматриваться [[pytest]] как тестовая функция. Отмеченная функция будет выполняться как асинхронная задача в цикле событий, предоставленном фикстурой `event_loop`. Чтобы сделать ваш тестовый код немного более лаконичным, можно использовать фичу [[pytest]] `pytestmark` для маркировки целых модулей или классов этим маркером. Будут затронуты только тестовые сопрограммы (по умолчанию сопрограммы с префиксом test_).

```python
import asyncio

import pytest

# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio


async def test_example(event_loop):
    """No marker!"""
    await asyncio.sleep(0, loop=event_loop)
```

В автоматическом режиме маркер `pytest.mark.asyncio` можно не указывать, маркер автоматически добавляется в функции асинхронного тестирования.

## [Decorators](https://pytest-asyncio.readthedocs.io/en/latest/reference/decorators.html)

Асинхронные фикстуры определяются так же, как и обычные фикстуры pytest, за исключением того, что они должны быть декорированы @pytest_asyncio.fixture.

```python
import pytest_asyncio


@pytest_asyncio.fixture
async def async_gen_fixture():
    await asyncio.sleep(0.1)
    yield "a value"


@pytest_asyncio.fixture(scope="module")
async def async_fixture():
    return await asyncio.sleep(0.1)
```

Поддерживаются все области, но если вы используете область за границами функции, вам потребуется переопределить фикстуру `event_loop`, чтобы она имела ту же или более широкую область. Для асинхронных фикстур требуется цикл обработки событий, поэтому они должны иметь ту же или более узкую область действия, чем фикстура `event_loop`. автоматический режим автоматически преобразует асинхронные фикстуры, объявленные с помощью стандартного декоратора @pytest.fixture, в асинхронные версии.

Смотир еще:

- [документация](https://pytest-asyncio.readthedocs.io/en/latest/concepts.html)
- [[pytest]]
- [[pytest-bdd]]
- [aioresponses](https://github.com/pnuckowski/aioresponses) is a helper to mock/fake web requests in python [[aiohttp]] package
- [[asyncio]]
- [[модульные-тесты]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[asyncio]: asyncio "Asyncio"
[pytest]: pytest "Pytest"
[trio]: trio "Trio асинхронный фреймворк"
[pytest-bdd]: pytest-bdd "pytest-bdd"
[aiohttp]: aiohttp "Aiohttp асинхронный клиент-свервер на python."
[модульные-тесты]: %D0%BC%D0%BE%D0%B4%D1%83%D0%BB%D1%8C%D0%BD%D1%8B%D0%B5-%D1%82%D0%B5%D1%81%D1%82%D1%8B "Модульные тесты"
[//end]: # "Autogenerated link references"
[//begin]: # "Autogenerated link references for markdown compatibility"
[asyncio]: asyncio "Asyncio"
[asyncio]: asyncio "Asyncio"
[pytest]: pytest "Pytest"
[asyncio]: asyncio "Asyncio"
[asyncio]: asyncio "Asyncio"
[trio]: trio "Trio асинхронный фреймворк"
[pytest]: pytest "Pytest"
[pytest]: pytest "Pytest"
[pytest]: pytest "Pytest"
[pytest]: pytest "Pytest"
[pytest-bdd]: pytest-bdd "pytest-bdd"
[aiohttp]: aiohttp "Aiohttp асинхронный клиент-свервер на python."
[asyncio]: asyncio "Asyncio"
[модульные-тесты]: модульные-тесты "Модульные тесты"
[//end]: # "Autogenerated link references"