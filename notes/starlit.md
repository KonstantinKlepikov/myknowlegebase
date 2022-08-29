---
description: ООП-ориентированный http-фреймворк Starlit
tags: starlit http
title: Starlit
---
Starlite is a light, opinionated and flexible ASGI API framework built on top of [[pydantic]] and [[starlette]].

Минимальный пример

```python
# datamodel
# my_app/models/user.py
from pydantic import BaseModel, UUID4

class User(BaseModel):
    first_name: str
    last_name: str
    id: UUID4

# controller
# my_app/controllers/user.py
from typing import List

from pydantic import UUID4
from starlite import Controller, Partial, get, post, put, patch, delete

from my_app.models import User

class UserController(Controller):
    path = "/users"

    @post()
    async def create_user(self, data: User) -> User:
        ...

    @get()
    async def list_users(self) -> List[User]:
        ...

    @patch(path="/{user_id:uuid}")
    async def partial_update_user(self, user_id: UUID4, data: Partial[User]) -> User:
        ...

    @put(path="/{user_id:uuid}")
    async def update_user(self, user_id: UUID4, data: User) -> User:
        ...

    @get(path="/{user_id:uuid}")
    async def get_user(self, user_id: UUID4) -> User:
        ...

    @delete(path="/{user_id:uuid}")
    async def delete_user(self, user_id: UUID4) -> User:
        ...

# entrypoint
# my_app/main.py

from starlite import Starlite

from my_app.controllers.user import UserController

app = Starlite(route_handlers=[UserController])
```

ASQI-server  run: `uvicorn my_app.main:app --reload`

Этот проект основан на наборе инструментов [[starlette]] и моделировании [[pydantic]] для создания высокоуровневой концептуальной структуры. Идея взять за основу эти две библиотеки конечно не нова — это было впервые сделано в [[fastapi]], который в этом плане (и некоторых других) послужил источником вдохновения для этого фреймворка.

Тем не менее, Starlite — это не FastAPI — у него другой дизайн, другие цели проекта и совершенно другая кодовая база. Цель этого проекта — стать общественным проектом. То есть иметь не одного «владельца», а основную команду сопровождающих, которая ведет проект, а также участников сообщества.

Starlite черпает вдохновение из NestJS — современного фреймворка TypeScript, в основе которого лежит ядро и шаблоны. Таким образом, дизайн API отличается от дизайна Starlette. Наконец, Python OOP чрезвычайно мощен и универсален. По-прежнему допуская эндпоинты на основе функций, Starlite стремится опираться на это, помещая контроллеры на основе классов в свое ядро.

## [App](https://starlite-api.github.io/starlite/usage/0-the-starlite-app/0-the-starlite-app/)

В основе каждого приложения Starlite лежит экземпляр класса `Starlite` или его подкласса. Обычно этот код помещается в файл с именем `main.py` в корневом каталоге проекта.

```python
from starlite import Starlite, get

@get(path="/")
def health_check() -> str:
    return "healthy"

app = Starlite(route_handlers=[health_check])
```

Экземпляр приложения является корневым уровнем приложения — он имеет базовый путь «/», и все контроллеры корневого уровня, маршрутизаторы и обработчики маршрутов должны быть зарегистрированы на нем

Конструктор Starlite принимает следующие дополнительные аргументы:

- `after_request`: обработчик жизненного цикла после запроса
- `after_response`: обработчик жизненного цикла после ответа
- `allowed_hosts`: Список разрешенных хостов
- `before_request`: обработчик жизненного цикла перед запросом
- `cache_config`: Позволяет указывать параметры кэша, такие как серверная часть, срок действия и т.д.
- `compression_config`: строенная поддержка сжатия Gzip и Brotli
- `cors_config`: Если установлено, это включает CORSMiddleware
- `debug`: Логический флаг, включающий и выключающий режим отладки. Если значение равно True, ошибки 404 будут отображаться как HTML с трассировкой стека. Этот параметр не следует использовать в производстве. По умолчанию False.
- `dependencies`: зависимости
- `exception_handlers`: словарь, отображающий исключения или коды исключений в функции обработчика
- `guards`: Список вызываемых гуардсов
- `middleware`: список промежуточного программного обеспечения
- `on_shutdown`: список вызываемых объектов, которые вызываются во время закрытия приложения
- `on_startup`: список вызываемых объектов, которые вызываются при запуске приложения
- `openapi_config`: По умолчанию используется базовая конфигурация
- `parameters`: сопоставление определения параметров, которое будет доступно во всех путях приложения
- `response_class`: пользовательский класс ответа, который будет использоваться приложением по умолчанию
- `response_cookies`: список Cookie
- `response_headers`: заголовки ответов
- `static_files_config`: статические файлы
- `tags`: список тегов для добавления к определениям путей openapi для всех путей приложений

Классический вариант использования `on_startup` / `on_shutdown` — подключение к базе данных. Часто мы хотим установить соединение с базой данных один раз при запуске приложения, а затем корректно закрыть его после завершения работы.

```python
from typing import cast
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from starlite import Starlite, State
from pydantic import BaseSettings

class AppSettings(BaseSettings):
    POSTGRES_CONNECTION_STRING: str

settings = AppSettings()

def get_postgres_connection(state: State) -> AsyncEngine:
    """Returns the Postgres connection. If it doesn't exist,
    creates it and saves it in on the application state object"""
    if not state.postgres_connection:
        state.postgres_connection = create_async_engine(
            settings.POSTGRES_CONNECTION_STRING
        )
    return cast("AsyncEngine", state.postgres_connection)

async def close_postgres_connection(state: State) -> None:
    """Closes the postgres connection stored in the application State object"""
    if state.postgres_connection:
        await cast("AsyncEngine", state.postgres_connection).engine.dispose()
    return None

app = Starlite(
    on_startup=[get_postgres_connection], on_shutdown=[close_postgres_connection]
)
```

Как тут видно, вызываемые объекты могут получить необязательный аргумент с именем `state`, который является объектом состояния приложения. Это тот же объект, который доступен в экземпляре `Starlite`, `.state`. Преимущество использования application state заключается в том, что к нему можно получить доступ на нескольких этапах соединения, а также его можно внедрить в зависимости и обработчики маршрутов

```python
from starlite import State, Provide, get

def my_dependency(state: State) -> None:
    # application state is injected
    ...

@get("/some-path")
def my_handler(dep: Provide(my_dependency)) -> None:
    ...
```

Статические файлы обслуживаются приложением из предопределенных мест. Чтобы настроить раздачу статических файлов, передайте экземпляр `starlite.config.StaticFilesConfig` или их список конструктору Starlite с помощью параметра `static_files_config`.

Например, предположим, что наше приложение Starlite будет обслуживать обычные файлы из папки «my_app/static» и html-документы из папки «my_app/html», и мы хотели бы обслуживать статические файлы по пути «/files». и html-файлы по пути «/html»:

```python
from starlite import Starlite, StaticFilesConfig

app = Starlite(
    route_handlers=[...],
    static_files_config=[
        StaticFilesConfig(directories=["static"], path="/files"),
        StaticFilesConfig(directories=["html"], path="/html", html_mode=True),
    ],
)
```

Логгирование (можно использовать и любое другое решение, например [[loguru]])

```python
from starlite import Starlite, LoggingConfig

my_app_logging_config = LoggingConfig(
    loggers={
        "my_app": {
            "level": "INFO",
            "handlers": ["queue_listener"],
        }
    }
)

app = Starlite(on_startup=[my_app_logging_config.configure])
```

## [Routes](https://starlite-api.github.io/starlite/usage/1-routing/0-routing/)

Хотя он Starlite основан на Starlette наборе инструментов ASGI в качестве основы, он не использует систему Starletteмаршрутизации, которая использует сопоставление регулярных выражений, а вместо этого реализует собственное решение, основанное на концепции radix-дерева или trie.

Сопоставление регулярных выражений, используемое Starlette (и FastAPI), Очень хорошо подходит для быстрого разрешения параметров пути, что дает ему преимущество, когда URL-адрес имеет много параметров пути - то, что мы можем рассматривать как вертикальное масштабирование. С другой стороны, он плохо масштабируется по горизонтали — чем больше маршрутов, тем менее производительным он становится. Таким образом, существует обратная зависимость между производительностью и размером приложения при таком подходе, который явно поддерживает очень маленькие микросервисы. Используемый подход на основе дерева Starlite не зависит от количества маршрутов приложения, что дает ему лучшие характеристики горизонтального масштабирования за счет несколько более медленного разрешения параметров пути.

В корне каждого Starlite приложения есть экземпляр класса `starlite.app.Starlite`, на котором контроллеры корневого уровня, маршрутизаторы и функции обработчика маршрутов зарегистрированы с помощью `route_handlerskwarg`

```python
from starlite import Starlite, get


@get("/sub-path")
def sub_path_handler() -> None:
    ...

@get()
def root_handler() -> None:
    ...

app = Starlite(route_handlers=[root_handler, sub_path_handler])
```

Компоненты, зарегистрированные в приложении, добавляются к корневому пути. Таким образом, root_handler функция будет вызываться для пути "/", тогда как функция будет вызываться sub_path_handlerдля "/подпути". Вы также можете объявить функцию для обработки нескольких путей, например:

```python
from starlite import get, Starlite

@get(["/", "/sub-path"])
def handler() -> None:
    ...

app = Starlite(route_handlers=[handler])
```

Иногда возникает необходимость динамической регистрации маршрута. Starlite поддерживает это с помощью `.register` метода, предоставляемого экземпляром приложения Starlite:

```python
from starlite import Starlite, get


@get()
def root_handler() -> None:
    ...

app = Starlite(route_handlers=[root_handler])

@get("/sub-path")
def sub_path_handler() -> None:
    ...

app.register(sub_path_handler)
```

Для обработки сложных схем используются маршрутизаторы и контроллеры.

Маршрутизаторы — это экземпляры класса `starlite.router.Router`, который является базовым классом для самого Starlite приложения. Маршрутизатор может регистрировать контроллеры, функции обработчика маршрутов и другие маршрутизаторы, аналогично конструктору Starlite:

```python
from starlite import Starlite, Router, get

@get("/{order_id:int}")
def order_handler(order_id: int) -> None:
    ...

order_router = Router(path="/orders", route_handlers=[order_handler])
base_router = Router(path="/base", route_handlers=[order_router])
app = Starlite(route_handlers=[base_router])
```

После `order_router` регистрации в `base_router`, функция обработчика, зарегистрированная в `order_router`, станет доступной в `/base/orders/{order_id}`.

Контроллеры являются подклассами класса `starlite.controller.Controller`. Они используются для организации конечных точек по определенному подпути, которое является путем контроллера. Их цель — позволить пользователям использовать ООП Python для лучшей организации кода и организации кода по логическим соображениям.

```python
from pydantic import BaseModel, UUID4
from starlite.controller import Controller
from starlite.handlers import get, post, patch, delete
from starlite.types import Partial

class UserOrder(BaseModel):
    user_id: int
    order: str

class UserOrderController(Controller):
    path = "/user-order"

    @post()
    async def create_user_order(self, data: UserOrder) -> UserOrder:
        ...

    @get(path="/{order_id:uuid}")
    async def retrieve_user_order(self, order_id: UUID4) -> UserOrder:
        ...

    @patch(path="/{order_id:uuid}")
    async def update_user_order(
        self, order_id: UUID4, data: Partial[UserOrder]
    ) -> UserOrder:
        ...

    @delete(path="/{order_id:uuid}")
    async def delete_user_order(self, order_id: UUID4) -> UserOrder:
        ...
```

Выше приведен простой пример контроллера «CRUD» для модели с именем `UserOrder`. Вы можете разместить столько методов обработчика маршрута на контроллере, сколько есть уникальных path+http.

Тот path, который определен в контроллере, добавляется перед путем, который определен для объявленных на нем обработчиков маршрутов. Таким образом, в приведенном выше примере `create_user_order` имеет путь к контроллеру - `/user-order/`, а `retrieve_user_order` имеет путь `/user-order/{order_id:uuid}`.

Вы можете многократно регистрировать как автономные функции обработчика маршрутов, так и контроллеры.

```python
from starlite import Router, Controller, get

class MyController(Controller):
    path = "/controller"

    @get()
    def handler(self) -> None:
        ...

internal_router = Router(path="/internal", route_handlers=[MyController])
partner_router = Router(path="/partner", route_handlers=[MyController])
consumer_router = Router(path="/consumer", route_handlers=[MyController])
```

В приведенном выше примере один и тот же `MyController` класс был зарегистрирован на трех разных маршрутизаторах. Это возможно, потому что маршрутизатору передается не экземпляр класса, а сам класс. Маршрутизатор создает собственный экземпляр контроллера, что обеспечивает инкапсуляцию.

Следовательно, в приведенном выше примере `MyController` будут созданы три разных экземпляра, каждый из которых будет смонтирован на своем подпути, например `/internal/controller`, `/partner/controller` и `/consumer/controller`.

Вы также можете зарегистрировать автономные обработчики маршрутов несколько раз:

```python
from starlite import Starlite, Router, get

@get(path="/handler")
def my_route_handler() -> None:
    ...

internal_router = Router(path="/internal", route_handlers=[my_route_handler])
partner_router = Router(path="/partner", route_handlers=[my_route_handler])
consumer_router = Router(path="/consumer", route_handlers=[my_route_handler])

Starlite(route_handlers=[internal_router, partner_router, consumer_router])
```

Когда функция-обработчик зарегистрирована, она фактически копируется. Таким образом, у каждого маршрутизатора есть свой уникальный экземпляр обработчика маршрута. Поведение пути идентично поведению контроллеров выше, а именно функция обработчика маршрута будет доступна по следующим путям: `/internal/handler`, `/partner/handler` и `/consumer/handler`.

## [Route Handlers](https://starlite-api.github.io/starlite/usage/2-route-handlers/0_route_handlers_concept/)

Обработчики маршрутов являются ядром Starlite. Они создаются путем декорирования функции или метода класса одним из декораторов-обработчиков, экспортированных из Starlite. Все декораторы обработчиков маршрутов принимают необязательный аргумент пути.

```python
from starlite import MediaType, get

@get("/", media_type=MediaType.TEXT)
def greet() -> str:
    return "hello world"
```

Функции или методы обработчика маршрутов получают доступ к различным данным, объявляя их как аннотированные функции. Аннотированные аргументы проверяются Starlite, а затем вводятся в обработчик запросов.

```python
from typing import Any, Dict
from starlite import State, Request, get
from starlette.datastructures import Headers

@get(path="/")
def my_request_handler(
    state: State,
    request: Request,
    headers: Headers,
    query: Dict[str, Any],
    cookies: Dict[str, Any],
) -> None:
    ...
```

Наиболее часто используемые обработчики маршрутов — это те, которые обрабатывают HTTP-запросы и ответы. Все эти обработчики маршрутов наследуются от класса `starlite.handlers.http.HTTPRouteHandler`, псевдоним которого вызывается декоратором `route`

```python
from starlite import HttpMethod, route

@route(path="/some-path", http_method=[HttpMethod.GET, HttpMethod.POST])
def my_endpoint() -> None:
    ...
```

Starlite также включает в себя «семантические» декораторы, то есть декораторы, предварительно устанавливающие `http_method` на конкретный HTTP-глагол, который соотносится с их именем:

- delete
- get
- patch
- post
- put

Они используются точно так же, `route` за исключением того, что вы не можете настроить `http_method`

Вы можете использовать как синхронные, так и асинхронные функции в качестве основы для функций обработчика маршрутов, но что следует использовать и когда?

Если вашему обработчику маршрута необходимо выполнить операцию ввода-вывода (чтение или запись данных из или в службу/базу данных и т.д.), наиболее эффективным решением в рамках приложения ASGI, включая Starlite, будет использование асинхронное решение для этой цели.

Причина этого в том, что асинхронный код, если он написан правильно, является неблокирующим. То есть асинхронный код можно приостанавливать и возобновлять, и поэтому он не прерывает выполнение основного цикла событий (если он написан правильно). С другой стороны, синхронный ввод-вывод часто блокирует, и если вы используете такой код в своей функции, это может вызвать проблемы с производительностью.

В этом случае следует воспользоваться `sync_to_thread` опцией. Это означает, что Starlite запускает синхронную функцию в отдельном асинхронном потоке, где она может блокироваться, но не прерывать выполнение основного цикла событий.

Однако проблема заключается в том, что это значительно замедлит выполнение вашего синхронного кода — на 40-60%. Таким образом, вы должны использовать эту опцию только тогда, когда ваш синхронный код выполняет блокирующие операции ввода-вывода. Для остальных операций это использовать не следует.

Starlite поддерживает веб-сокеты через `websocket` декоратор

```python
from starlite import WebSocket, websocket

@websocket(path="/socket")
async def my_websocket_handler(socket: WebSocket) -> None:
    await socket.accept()
    await socket.send_json({...})
    await socket.close()
```

В отличие от обработчиков HTTP-маршрутов, к обработчикам веб-сокетов предъявляются следующие требования:

- они должны объявить socket-аргументы
- они должны иметь аннотацию для return `None`
- они должны быть асинхронными функциями

Наконец, если вам нужно написать собственное приложение ASGI, вы можете сделать это с помощью `asgi` декоратора.

## [Parameters](https://starlite-api.github.io/starlite/usage/3-parameters/0-path-parameters/)

Поддерживается типизация и проверка:

- параметры пути
- параметры запрсоа
- заголовки
- файлы куки
- функции параметров
- многоуровневые параметры

## [Запрос данных](https://starlite-api.github.io/starlite/usage/4-request-data/0-request-data/)

Для всех типов запроса кроме `GET` можно получить доступ к телу, указав соответствующий пайдантик тип в `data` аргументе

```python
from starlite import post
from pydantic import BaseModel

class User(BaseModel):
    ...

@post(path="/user")
async def create_user(data: User) -> User:
    ...
```

## [Ответы](https://starlite-api.github.io/starlite/usage/5-responses/0-responses-intro/)

## [Ingection dependencies](https://starlite-api.github.io/starlite/usage/6-dependency-injection/0-dependency-injection-intro/)

Starlite имеет простую, но мощную систему внедрения зависимостей, которая позволяет объявлять зависимости на всех уровнях приложения:

```python
from starlite import Controller, Router, Starlite, Provide, get


def bool_fn() -> bool:
    ...

def dict_fn() -> dict:
    ...

def list_fn() -> list:
    ...

def int_fn() -> int:
    ...

class MyController(Controller):
    path = "/controller"
    # on the controller
    dependencies = {"controller_dependency": Provide(list_fn)}

    # on the route handler
    @get(path="/handler", dependencies={"local_dependency": Provide(int_fn)})
    def my_route_handler(
        self,
        app_dependency: bool,
        router_dependency: dict,
        controller_dependency: list,
        local_dependency: int,
    ) -> None:
        ...

    # on the router

my_router = Router(
    path="/router",
    dependencies={"router_dependency": Provide(dict_fn)},
    route_handlers=[MyController],
)

# on the app
app = Starlite(
    route_handlers=[my_router], dependencies={"app_dependency": Provide(bool_fn)}
)
```

Предпосылки для внедрения зависимостей:

- зависимости должны быть вызываемыми
- зависимости могут получать kwargs и аргумент, self но не позиционные аргументы
- имя kwarg и ключ зависимости должны совпадать
- зависимость должна быть объявлена ​​с помощью Provide класса
- зависимость должна находиться в области действия функции-обработчика

Зависимости изолированы от контекста, в котором они объявлены. Таким образом, в приведенном выше примере к local_dependency объекту можно получить доступ только в рамках конкретного обработчика маршрута, для которого он был объявлен; controller_dependency доступен только для обработчиков маршрутов на этом конкретном контроллере; зависимости маршрутизатора доступны только для обработчиков маршрутов, зарегистрированных на этом конкретном маршрутизаторе. Только app_dependencies доступны для всех обработчиков маршрутов.

Как указано выше, зависимости могут получать kwargs, но не args. Причина этого в том, что зависимости анализируются с использованием того же механизма, который анализирует функции обработчика маршрутов, и они тоже, как и функции обработчика маршрутов, могут вводить в себя данные. По сути, вы можете внедрить те же данные, что и в обработчики маршрутов

```python
from starlite import Controller, Provide, Partial, patch
from pydantic import BaseModel, UUID4

class User(BaseModel):
    id: UUID4
    name: str

async def retrieve_db_user(user_id: UUID4) -> User:
    ...

class UserController(Controller):
    path = "/user"
    dependencies = {"user": Provide(retrieve_db_user)}

    @patch(path="/{user_id:uuid}")
    async def update_user(self, data: Partial[User], user: User) -> User:
        ...
```

Поскольку зависимости объявляются на каждом уровне приложения с помощью словаря со строковым ключом, переопределить зависимости очень просто

```python
from starlite import Controller, Provide, get

def bool_fn() -> bool:
    ...

def dict_fn() -> dict:
    ...

class MyController(Controller):
    path = "/controller"
    # on the controller
    dependencies = {"some_dependency": Provide(dict_fn)}

    # on the route handler
    @get(path="/handler", dependencies={"some_dependency": Provide(bool_fn)})
    def my_route_handler(
        self,
        some_dependency: bool,
    ) -> None:
        ...
```

Класс `starlite.provide.Provide` представляет собой оболочку, используемую для внедрения зависимостей. Чтобы внедрить вызываемый объект, вы должны обернуть его `Provide`:

```python
from starlite import Provide, get
from random import randint

def my_dependency() -> int:
    return randint(1, 10)

@get(
    "/some-path",
    dependencies={
        "my_dep": Provide(
            my_dependency,
        )
    },
)
def my_handler(my_dep: int) -> None:
    ...
```

Вы можете внедрять зависимости в другие зависимости точно так же, как и в обычные функции.

## [Middlewire](https://starlite-api.github.io/starlite/usage/7-middleware/#pre-requisites-and-scope)

Промежуточные программы — это мини-приложения ASGI, которые получают необработанный объект запроса и каким-либо образом проверяют или преобразовывают его. Starlite позволяет пользователям использовать промежуточное программное обеспечение Starlette и любое стороннее промежуточное программное обеспечение, созданное для него, а также предлагает собственный протокол промежуточного программного обеспечения. Пример собственнокго:

```python
import logging

from starlette.types import ASGIApp, Receive, Scope, Send
from starlite import MiddlewareProtocol, Request

logger = logging.getLogger(__name__)

class MyRequestLoggingMiddleware(MiddlewareProtocol):
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http":
            request = Request(scope)
            logger.info("%s - %s" % request.method, request.url)
        await self.app(scope, receive, send)
```

Метод `__init__` получает и устанавливает «приложение» — приложение не является экземпляром Starlite, а является следующим промежуточным программным обеспечением в стеке, которое также является приложением ASGI.

Метод `__call__` превращает этот класс в callable, т.е. после создания экземпляра этот класс действует как функция, имеющая сигнатуру приложения ASGI: три параметра `scope`, `receive`, `send` задаются спецификацией ASGI, а их значения исходят от сервера ASGI (например, uvicorn) используется для запуска Starlite.

Здесь важно отметить две вещи:

- Хотя `scope` используется для создания экземпляра запроса путем передачи его `Request` конструктору, что упрощает доступ к нему, поскольку он уже выполняет некоторый синтаксический анализ для вас, фактический источник истины остается `scope`, а не запрос. Если вам нужно изменить данные запроса, вы должны изменить словарь области действия, а не какие-либо эфемерные объекты запроса, созданные, как описано выше.
- Как только промежуточное ПО заканчивает делать то, что делает, оно должно передать `scope`, `receive` и `send` либо экземпляру, либо `self.app` экземпляру `Response` — в других архитектурах промежуточного ПО это эквивалентно вызову `next`, что и происходит в последней строке примера.

Доступны встроенные миддлвейры:

- CORS
- CSRF
- удостоверенные хосты
- сжатие

## [Authentication](https://starlite-api.github.io/starlite/usage/8-authentication/#pre-requisites-and-scope)

Starlite не зависит от того, какой механизм аутентификации должно использовать приложение — вы можете использовать файлы cookie, токены JWT, подключение OpenID в зависимости от вашего варианта использования. Он также не реализует для вас ни один из этих механизмов. Что он делает, так это предлагает мнение о том, где должна происходить аутентификация, а именно - как часть вашего стека промежуточного программного обеспечения. Это соответствует Starlette и многим другим фреймворкам (например, Django, NestJS и т.д.).

```python
from starlite import AuthenticationResult, Request

async def authenticate_request(request: Request) -> AuthenticationResult:
    ...
```

## [Guards](https://starlite-api.github.io/starlite/usage/9-guards/#csrf)

Guards — это вызываемые объекты, которые получают два аргумента — `request`, который является экземпляром запроса, и `route_handler`, который является копией `BaseRouteHandler` модели. Их роль заключается обработке запроса путем проверки того, что запросу разрешено достигать рассматриваемого обработчика конечной точки. Если проверка не удалась, guard должен вызвать `HTTPException`, обычно N`otAuthorizedException` со значением `status_code401`.

## [Plugins](https://starlite-api.github.io/starlite/usage/10-plugins/0-plugins-intro/#example-create-a-jwt-authentication-middleware)

Starlite поддерживает расширение через плагины, которые позволяют:

- Сериализация и десериализация сторонних классов, не основанных на pydantic
- Автоматическое создание схемы OpenAPI для сторонних классов.

Другими словами, плагины позволяют анализировать и проверять входящие данные с использованием не-pydantic классов, сохраняя при этом безопасность типов, анализ и проверку pydantic. Кроме того, они обеспечивают бесшовную сериализацию и создание схемы.

## [OpenAPI](https://starlite-api.github.io/starlite/usage/12-openapi/)

Поддерживается документация АПИ на Redox

## [Tests](https://starlite-api.github.io/starlite/usage/14-testing/#example-create-a-jwt-authentication-middleware)

## [Templates](https://starlite-api.github.io/starlite/usage/15-templating/#after-response)

Встроенная поддержка [[jinja2]] и mako

## [Response caching](https://starlite-api.github.io/starlite/usage/16-caching/)

## [Exceptions handling](https://starlite-api.github.io/starlite/usage/17-exceptions/)

## Переход на Старлайт

Миграция со Starlette или FastAPI на Starlite довольно несложна, потому что фреймворки по большей части совместимы друг с другом

### Декораторы маршрутизации

Starlite не включает декоратор как часть экземпляров `Router`. Все маршруты должны быть объявлены с использованием обработчиков маршрутов — в автономных функциях или методах контроллера. Затем вам необходимо зарегистрировать их в приложении, либо сначала зарегистрировав их на маршрутизаторе, а затем зарегистрировав маршрутизатор в приложении, либо зарегистрировав их непосредственно в приложении.

### Классы маршрутизации

Starlite не расширяет классы маршрутизации Starlette, а вместо этого реализует их собственные версии. Вам нужно будет использовать `Router` классы Starlite вместо их эквивалентов из других фреймворков. Есть некоторые отличия класса Starlite от других фреймворков:

- Версия Starlite не является приложением ASGI, единственным приложением ASGI является приложение Starlite и любые промежуточные программы, которые вы ему передаете.
- Версия Starlite не включает декораторы, вместо этого вы должны использовать обработчики маршрутов.
- Версия Starlite не поддерживает хуки жизненного цикла, вместо этого вы должны управлять всем своим жизненным циклом на уровне приложения.

Если вы используете экземпляры Starlette `Route` напрямую, вам нужно будет заменить их обработчиками маршрутов.

Класс Starlette `Mount` заменен на Starlite `Router`. Класс `Host` намеренно не поддерживается. Если ваше приложение зависит от `Host`, вам придется разделить логику на разные микросервисы, а не использовать этот тип маршрутизации.

### Внедрение зависимости

Система внедрения зависимостей Starlite отличается от той, что используется [[fastapi]]. В FastAPI вы объявляете зависимости либо как список функций, передаваемых экземплярам `Router` или FastAPI, либо как значение аргумента функции по умолчанию, заключенное в экземпляр `Depend` класса.

В Starlite зависимости всегда объявляются с помощью словаря со строковым ключом и значением, обернутым в экземпляр `Provide` класса.

### Аутентификация

FastAPI продвигает шаблон использования внедрения зависимостей для аутентификации. Вы можете сделать то же самое в Starlite, но предпочтительный способ справиться с этим — расширить класс `Starlite AbstractAuthenticationMiddleware`.

### Сторонние пакеты

Сторонние пакеты, созданные для Starlette и FastAPI , должны быть в целом совместимы со Starlite. Единственными исключениями являются пакеты, использующие в качестве основы систему внедрения зависимостей FastAPI — они не будут работать как таковые.

Смотри еще:

- [документация](https://starlite-api.github.io/starlite/)
- [github](https://github.com/starlite-api/starlite)
- [[fastapi]]
- [[http]]
- [[starlette]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[pydantic]: pydantic "Pydantic"
[starlette]: starlette "Starlette"
[starlette]: starlette "Starlette"
[pydantic]: pydantic "Pydantic"
[fastapi]: fastapi "Fastapi"
[loguru]: loguru "Loguru"
[jinja2]: jinja2 "Jinja2"
[fastapi]: fastapi "Fastapi"
[fastapi]: fastapi "Fastapi"
[http]: ../lists/http "Http"
[starlette]: starlette "Starlette"
[//end]: # "Autogenerated link references"
[//begin]: # "Autogenerated link references for markdown compatibility"
[pydantic]: pydantic "Pydantic"
[starlette]: starlette "Starlette"
[starlette]: starlette "Starlette"
[pydantic]: pydantic "Pydantic"
[fastapi]: fastapi "Fastapi"
[loguru]: loguru "Loguru"
[jinja2]: jinja2 "Jinja2"
[fastapi]: fastapi "Fastapi"
[fastapi]: fastapi "Fastapi"
[http]: ../lists/http "Http"
[starlette]: starlette "Starlette"
[//end]: # "Autogenerated link references"