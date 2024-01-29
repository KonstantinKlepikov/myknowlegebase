---
description: Библиотека внедрения зависимостей dependency-injector на python
title: Dependency injection
tags: python
---
Первоначально шаблон внедрения зависимостей стал популярным в языках со статической типизацией, таких как Java. Внедрение зависимостей — это принцип, который помогает добиться инверсии управления.

Python — интерпретируемый язык с динамической типизацией. Существует мнение, что внедрение зависимостей для него работает не так хорошо, как для Java. Большая часть гибкости уже встроена. Также существует мнение, что фреймворк внедрения зависимостей — это то, что редко нужно разработчику Python. Разработчики Python говорят, что внедрение зависимостей можно легко реализовать, используя основы языка.

Внедрение зависимостей — это принцип, который помогает уменьшить связанность и повысить связность.

Как реализовать внедрение зависимостей?

Объекты больше не создают друг друга. Вместо этого они предоставляют способ внедрения зависимостей.

```python
# before
import os


class ApiClient:

    def __init__(self) -> None:
        self.api_key = os.getenv("API_KEY")  # <-- dependency
        self.timeout = int(os.getenv("TIMEOUT"))  # <-- dependency


class Service:

    def __init__(self) -> None:
        self.api_client = ApiClient()  # <-- dependency


def main() -> None:
    service = Service()  # <-- dependency
    ...


if __name__ == "__main__":
    main()

# after
import os


class ApiClient:

    def __init__(self, api_key: str, timeout: int) -> None:
        self.api_key = api_key  # <-- dependency is injected
        self.timeout = timeout  # <-- dependency is injected


class Service:

    def __init__(self, api_client: ApiClient) -> None:
        self.api_client = api_client  # <-- dependency is injected


def main(service: Service) -> None:  # <-- dependency is injected
    ...


if __name__ == "__main__":
    main(
        service=Service(
            api_client=ApiClient(
                api_key=os.getenv("API_KEY"),
                timeout=int(os.getenv("TIMEOUT")),
            ),
        ),
    )
```

## Что делает Dependency Injector?

Dependency Injector помогает собрать и внедрить зависимости. Он предоставляет контейнер и поставщиков, которые помогут вам со сборкой объектов. Когда вам нужен объект, вы помещаете `Provide` маркер в качестве значения по умолчанию аргумента функции. Когда вы вызываете эту функцию, фреймворк собирает и внедряет зависимости.

```python
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    api_client = providers.Singleton(
        ApiClient,
        api_key=config.api_key,
        timeout=config.timeout,
    )

    service = providers.Factory(
        Service,
        api_client=api_client,
    )


@inject
def main(service: Service = Provide[Container.service]) -> None:
    ...


if __name__ == "__main__":
    container = Container()
    container.config.api_key.from_env("API_KEY", required=True)
    container.config.timeout.from_env("TIMEOUT", as_=int, default=5)
    container.wire(modules=[__name__])

    main()  # <-- dependency is injected automatically

    with container.api_client.override(mock.Mock()):
        main()  # <-- overridden dependency is injected automatically
```

Когда вы вызываете `main()` функцию из примера, `Service` зависимость собирается и внедряется автоматически.

Когда вы проводите тестирование, вы вызываете `container.api_client.override()` метод, чтобы заменить реальный клиент API моком. Когда вы вызываете `main()`, вводится мок.

Вы можете заменить любого провайдера другим провайдером.

Это также поможет вам переконфигурировать проект для различных сред: замените клиент API заглушкой на стадии разработки.

Сборка объектов объединена в контейнер. Внедрение зависимостей определяется явно. Это облегчает понимание и изменение работы приложения.

## Ключевые фичи dependency injector

- **Провайдеры**. Предоставляет `Factory`, `Singleton`, `Callable`, `Coroutine`, `Object`, `List`, `Dict`, `Configuration`, `Resource`, `Dependency`, и `Selector` поставщиков, которые помогают собирать объекты.
- **Переопределение**. Может на лету переопределить любого провайдера другим провайдером. Это помогает в тестировании и настройке среды разработки/этапа для замены клиентов API заглушками и т. д.
- **Конфигурация**. Считывает конфигурацию из yaml, ini, json, настроек pydantic, переменных среды и словарей.
- **Ресурсы**. Помогает при инициализации и настройке ведения журнала, цикла событий, пула потоков или процессов и т. д. Может использоваться для выполнения каждой функции в тандеме с подключением.
- **Контейнеры**. Предоставляет декларативные и динамические контейнеры.
- **Проводка**. Внедряет зависимости в функции и методы. Помогает интегрироваться с другими фреймворками: Django, Flask, Aiohttp, Sanic, [[fastapi]].
- **Асинхронный**. Поддерживает асинхронные инъекции и [[asyncio]].
- **Типизация**. Поддерживает [[mypy]].
- **Производительность**. Быстрый. Написано на Cython.
- **Зрелость**. Зрелый и готовый к производству. Хорошо протестировано, документировано и поддерживается.

## Установка

`pip install dependency-injector`

## [Примеры](https://python-dependency-injector.ets-labs.org/examples/index.html)

- [FastAPI example](https://python-dependency-injector.ets-labs.org/examples/fastapi.html)
- [FastAPI + Redis example](https://python-dependency-injector.ets-labs.org/examples/fastapi-redis.html)
- [FastAPI + SQLAlchemy example](https://python-dependency-injector.ets-labs.org/examples/fastapi-sqlalchemy.html)

## API

### [Providers](https://python-dependency-injector.ets-labs.org/providers/index.html)

Провайдеры помогают собирать объекты. Они создают объекты и внедряют зависимости.

Каждый провайдер является вызываемым объектом. Поставщик извлекает базовые зависимости и внедряет их в созданный объект. Это вызывает каскадный эффект, который помогает собирать графы объектов.

```sh
provider1()
│
├──> provider2()
│
├──> provider3()
│    │
│    └──> provider4()
│
└──> provider5()
     │
     └──> provider6()
```

Еще одна особенность провайдеров — переопределение. Вы можете заменить любого провайдера другим провайдером. Это помогает в тестировании. Это также помогает переопределить клиенты API с помощью заглушек для среды разработки или промежуточной среды.

- [Документация АПИ провайдеров](https://python-dependency-injector.ets-labs.org/api/providers.html#module-dependency_injector.providers)
- [Factory provider](https://python-dependency-injector.ets-labs.org/providers/factory.html)
- [Singleton provider](https://python-dependency-injector.ets-labs.org/providers/singleton.html)
- [Callable provider](https://python-dependency-injector.ets-labs.org/providers/callable.html)
- [Coroutine provider](https://python-dependency-injector.ets-labs.org/providers/coroutine.html)
- [Object provider](https://python-dependency-injector.ets-labs.org/providers/object.html) возвращает объект как есть
- [List provider](https://python-dependency-injector.ets-labs.org/providers/list.html)
- [Dict provider](https://python-dependency-injector.ets-labs.org/providers/dict.html)
- [Configuration provider](https://python-dependency-injector.ets-labs.org/providers/configuration.html)
- [Resource provider](https://python-dependency-injector.ets-labs.org/providers/resource.html) объекты с логикой инициализации и шотдауна
- [Selector provider](https://python-dependency-injector.ets-labs.org/providers/selector.html)
- [Dependency provider](https://python-dependency-injector.ets-labs.org/providers/dependency.html) плейсхолдер для зависимостей ожидаемого типа

### [Containers](https://python-dependency-injector.ets-labs.org/containers/index.html)

Контейнеры — это коллекции провайдеров.

Существует несколько вариантов использования контейнеров:

- Хранение всех провайдеров в одном контейнере (чаще всего).
- Группировка провайдеров из одного архитектурного уровня (например, провайдеров Services и Models контейнеров Forms).
- Группировка провайдеров из одних функциональных групп (например, контейнер Users, содержащий все функциональные части пакета users).

- [Declarative container](https://python-dependency-injector.ets-labs.org/containers/declarative.html) определение контейнера, базирующееся на классе
- [Dynamic container](https://python-dependency-injector.ets-labs.org/containers/dynamic.html) контейнеры. определяемые в рантайм

### [Wiring](https://python-dependency-injector.ets-labs.org/wiring.html)

Функция подключения обеспечивает возможность внедрения поставщиков контейнеров в функции и методы.

- Поместите декоратор `@inject`.
- Разместите маркеры. Маркер связи указывает, какую зависимость следует внедрить, например `Provide[Container.bar]`. Это помогает контейнеру найти инъекции.
- Подключите контейнер с помощью маркеров в коде. Вызовите `container.wire()`, указав модули и пакеты, с которыми вы хотите его связать.
- Используйте функции и классы, как обычно. Framework обеспечит указанные инъекции.

```python
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject


class Service:
    ...


class Container(containers.DeclarativeContainer):

    service = providers.Factory(Service)


@inject
def main(service: Service = Provide[Container.service]) -> None:
    ...


if __name__ == "__main__":
    container = Container()
    container.wire(modules=[__name__])

    main()
```

Смотри еще:

- [[python-standart-library]]
- [[fastapi]]
- [python-dependency-injector](https://python-dependency-injector.ets-labs.org/) framework

[//begin]: # "Autogenerated link references for markdown compatibility"
[fastapi]: fastapi "Fastapi"
[asyncio]: asyncio "Asyncio"
[mypy]: mypy "Mypy"
[python-standart-library]: ../lists/python-standart-library "Стандартная библиотека python и полезные ресурсы"
[//end]: # "Autogenerated link references"