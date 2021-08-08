# Starlette

ASGI асинхронный фреймворк на python. Используется в [[fastapi]]

[Документация](https://www.starlette.io/)

Его преимущества:

- Seriously impressive performance.
- WebSocket support.
- GraphQL support.
- In-process background tasks.
- Startup and shutdown events.
- Test client built on requests.
- CORS, GZip, Static Files, Streaming responses.
- Session and Cookie support.
- 100% test coverage.
- 100% type annotated codebase.
- Zero hard dependencies.

`pip3 install starlette`

Кроме того, нужен сервер, к примеру [[uvicorn]]

Пример реализации:

```python
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route


async def homepage(request):
    return JSONResponse({'hello': 'world'})


app = Starlette(debug=True, routes=[
    Route('/', homepage),
])
```

Это можно запустить через `uvicorn example:app`. [Более полный пример](https://github.com/encode/starlette-example)

## Зависимости (опциональные)

- `requests` - Required if you want to use the TestClient.
- `aiofiles` - Required if you want to use FileResponse or StaticFiles.
- `jinja2` - Required if you want to use Jinja2Templates.
- `python-multipart` - Required if you want to support form parsing, with request.form().
- `itsdangerous` - Required for SessionMiddleware support.
- `pyyaml` - Required for SchemaGenerator support.
- `graphene` - Required for GraphQLApp support.

[Работа с бд](https://www.starlette.io/database/)

## Создание приложения

Специальный класс `Starlette`. Описание и пример [тут](https://www.starlette.io/applications/)

```python
[...]

app = Starlette(debug=True, routes=routes, on_startup=[startup])
```

Параметры:

- debug - Boolean, индицирует следует ли возвращать трасер при ошибках
- routes - список путей для http и websocket
middleware - список middleware, запускается на каждом запросе. Старлетт всегда автоматически включает два мидлевейра - ServerErrorMiddleware и ExceptionMiddleware
- exception_handlers - словарь http-кодов и ошибок
- on_startup - список того, что запускается на старте приложения
- on_shutdown - на закрытии

Можно задавать дополнительные стейтменты, используя `state` атрибутам

```python
app.state.ADMIN_EMAIL = 'admin@example.org'
```

## [Requests](https://www.starlette.io/requests/)

`Request` class

```python
from starlette.requests import Request
from starlette.responses import Response


async def app(scope, receive, send):
    assert scope['type'] == 'http'
    request = Request(scope, receive)
    content = '%s %s' % (request.method, request.url.path)
    response = Response(content, media_type='text/plain')
    await response(scope, receive, send)
```

описание аттрибутов [в статье](https://www.starlette.io/requests/)

## [Responses](https://www.starlette.io/responses/)

`Response(content, status_code=200, headers=None, media_type=None)`

- content - A string or bytestring.
- status_code - An integer HTTP status code.
- headers - A dictionary of strings.
- media_type - A string giving the media type. eg. "text/html"

Доступен метод `Response.set_cookie(key, value, max_age=None, expires=None, path="/", domain=None, secure=False, httponly=False, samesite="lax")`. Описание аттрибутов [в статье.](https://www.starlette.io/responses/)

Еще методы:

- `Response.delete_cookie(key, path='/', domain=None)`
- `HTMLResponse('<html><body><h1>Hello, world!</h1></body></html>')`
- `PlainTextResponse('Hello, world!')`
- `JSONResponse({'hello': 'world'})`
- `RedirectResponse(url='/')`
- `StreamingResponse(generator, media_type='text/html')`
- `FileResponse('statics/favicon.ico')`

## [Websockets](https://www.starlette.io/websockets/)

Механизм такой-же, как и для http-запроса

```python
from starlette.websockets import WebSocket


async def app(scope, receive, send):
    websocket = WebSocket(scope=scope, receive=receive, send=send)
    await websocket.accept()
    await websocket.send_text('Hello, world!')
    await websocket.close()
```

## [Routing](https://www.starlette.io/routing/)

Пути прописываются в виде списка.

```python
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route


async def homepage(request):
    return PlainTextResponse("Homepage")

async def about(request):
    return PlainTextResponse("About")


routes = [
    Route("/", endpoint=homepage),
    Route("/about", endpoint=about),
]

app = Starlette(routes=routes)
```

В качестве эндпоинта принимается обычная или асинхронная функция с единственным креквестом или класс, реализующий #ASGI интерфейс.

Про переменные пути [читай статью](https://www.starlette.io/routing/). Допустима [[type-annotation]]

Допускаются следующие данные переменных:

- `str` returns a string, and is the default.
- `int` returns a Python integer.
- `float` returns a Python float.
- `uuid` return a Python uuid.UUID instance.
- `path` returns the rest of the path, including any additional / characters.

```python
Route('/users/{user_id:int}', user)
Route('/floating-point/{number:float}', floating_point)
Route('/uploaded/{rest_of_path:path}', uploaded)
````

Можно задавать тип #http запроса

```python
Route('/users/{user_id:int}', user, methods=["GET", "POST"])
```

Можно монтировать сабпути для больших проектов

```python
routes = [
    Route('/', homepage),
    Mount('/users', routes=[
        Route('/', users, methods=['GET', 'POST']),
        Route('/{username}', user),
    ])
]

# или так
from myproject import users, auth

routes = [
    Route('/', homepage),
    Mount('/users', routes=users.routes),
    Mount('/auth', routes=auth.routes),
]

# или испльзуя сабприложения
routes = [
    ...
    Mount("/static", app=StaticFiles(directory="static"), name="static")
]

app = Starlette(routes=routes)
```

Иак можно вернуть url из пути

```python
routes = [
    Route("/", homepage, name="homepage")
]

# We can use the following to return a URL...
url = request.url_for("homepage")
```

## [Endpoints](https://www.starlette.io/endpoints/)

Два класса - `HTTPEndpoint` and `WebSocketEndpoint`

HTTPEndpoint

```python
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.endpoints import HTTPEndpoint
from starlette.routing import Route


class Homepage(HTTPEndpoint):
    async def get(self, request):
        return PlainTextResponse(f"Hello, world!")


class User(HTTPEndpoint):
    async def get(self, request):
        username = request.path_params['username']
        return PlainTextResponse(f"Hello, {username}")

routes = [
    Route("/", Homepage),
    Route("/{username}", User)
]

app = Starlette(routes=routes)
```

WebSocketEndpoint

```python
from starlette.endpoints import WebSocketEndpoint


class App(WebSocketEndpoint):
    encoding = 'bytes'

    async def on_connect(self, websocket):
        await websocket.accept()

    async def on_receive(self, websocket, data):
        await websocket.send_bytes(b"Message: " + data)

    async def on_disconnect(self, websocket, close_code):
        pass
```

[Подробнее](https://www.starlette.io/endpoints/)

## [Middleware](https://www.starlette.io/middleware/)

В старлетте несколько миддлвейров, все они реализованы как #ASGI классы

```python
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

routes = ...

# Ensure that all requests include an 'example.com' or '*.example.com' host header,
# and strictly enforce https-only access.
middleware = [
  Middleware(TrustedHostMiddleware, allowed_hosts=['example.com', '*.example.com']),
  Middleware(HTTPSRedirectMiddleware)
]

app = Starlette(routes=routes, middleware=middleware)
```

Исполняются сверху вниз, поэтому приложение должно выглядеть так:

- Middleware
  - ServerErrorMiddleware
  - TrustedHostMiddleware
  - HTTPSRedirectMiddleware
  - ExceptionMiddleware
- Routing
- Endpoint

Доступно:

- CORSMiddleware - добавляет [CORS заголовки](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- SessionMiddleware - куки-бейсед http сессия
- HTTPSRedirectMiddleware - http или wss
- TrustedHostMiddleware
- GZipMiddleware
- BaseHTTPMiddleware

Доступна куча Third party middleware. [Подробнее](https://www.starlette.io/middleware/)

## [Static Files](https://www.starlette.io/staticfiles/)

## [Templates](https://www.starlette.io/templates/)

## [Database](https://www.starlette.io/database/)

Можно использовать как обычные ОРМ, типа [[sqlalchemy]]. Можно ассинхронные, типа [[gino]]

Используется пакет [[databases]]

Пример

```.env
DATABASE_URL=sqlite:///test.db
```

```python
import databases
import sqlalchemy
from starlette.applications import Starlette
from starlette.config import Config
from starlette.responses import JSONResponse
from starlette.routing import Route


# Configuration from environment variables or '.env' file.
config = Config('.env')
DATABASE_URL = config('DATABASE_URL')


# Database table definitions.
metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)

database = databases.Database(DATABASE_URL)


# Main application code.
async def list_notes(request):
    query = notes.select()
    results = await database.fetch_all(query)
    content = [
        {
            "text": result["text"],
            "completed": result["completed"]
        }
        for result in results
    ]
    return JSONResponse(content)

async def add_note(request):
    data = await request.json()
    query = notes.insert().values(
       text=data["text"],
       completed=data["completed"]
    )
    await database.execute(query)
    return JSONResponse({
        "text": data["text"],
        "completed": data["completed"]
    })

routes = [
    Route("/notes", endpoint=list_notes, methods=["GET"]),
    Route("/notes", endpoint=add_note, methods=["POST"]),
]

app = Starlette(
    routes=routes,
    on_startup=[database.connect],
    on_shutdown=[database.disconnect]
)
```

Параметры запросов задаются с помощью [[sqlalchemy]] [стандартных методов запроса](https://docs.sqlalchemy.org/en/14/core/)

- rows = await database.fetch_all(query)
- row = await database.fetch_one(query)
- async for row in database.iterate(query)
- await database.execute(query)
- await database.execute_many(query)

Транзакции доступны через декоратор, контекстный менеджер или низкоуровневый апи апи

```python
# decorator
@database.transaction()
async def populate_note(request):
    # This database insert occurs within a transaction.
    # It will be rolled back by the `RuntimeError`.
    query = notes.insert().values(text="you won't see me", completed=True)
    await database.execute(query)
    raise RuntimeError()

# manager
async def populate_note(request):
    async with database.transaction():
        # This database insert occurs within a transaction.
        # It will be rolled back by the `RuntimeError`.
        query = notes.insert().values(text="you won't see me", completed=True)
        await request.database.execute(query)
        raise RuntimeError()

# applicationasync def populate_note(request):
transaction = await database.transaction()
try:
    # This database insert occurs within a transaction.
    # It will be rolled back by the `RuntimeError`.
    query = notes.insert().values(text="you won't see me", completed=True)
    await database.execute(query)
    raise RuntimeError()
except:
    transaction.rollback()
    raise
else:
    transaction.commit()
```

### Изоляция для тестов

```python
from starlette.applications import Starlette
from starlette.config import Config
import databases

config = Config(".env")

TESTING = config('TESTING', cast=bool, default=False)
DATABASE_URL = config('DATABASE_URL', cast=databases.DatabaseURL)
TEST_DATABASE_URL = DATABASE_URL.replace(database='test_' + DATABASE_URL.database)

# Use 'force_rollback' during testing, to ensure we do not persist database changes
# between each test case.
if TESTING:
    database = databases.Database(TEST_DATABASE_URL, force_rollback=True)
else:
    database = databases.Database(DATABASE_URL)

[...]

import pytest
from starlette.config import environ
from starlette.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database

# This sets `os.environ`, but provides some additional protection.
# If we placed it below the application import, it would raise an error
# informing us that 'TESTING' had already been read from the environment.
environ['TESTING'] = 'True'

import app


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
  """
  Create a clean database on every test case.
  For safety, we should abort if a database already exists.

  We use the `sqlalchemy_utils` package here for a few helpers in consistently
  creating and dropping the database.
  """
  url = str(app.TEST_DATABASE_URL)
  engine = create_engine(url)
  assert not database_exists(url), 'Test database already exists. Aborting tests.'
  create_database(url)             # Create the test database.
  metadata.create_all(engine)      # Create the tables.
  yield                            # Run the tests.
  drop_database(url)               # Drop the test database.


@pytest.fixture()
def client():
    """
    When using the 'client' fixture in test cases, we'll get full database
    rollbacks between test cases:

    def test_homepage(client):
        url = app.url_path_for('homepage')
        response = client.get(url)
        assert response.status_code == 200
    """
    with TestClient(app) as client:
        yield client
```

### миграции

Для миграций используется [[alembic]]

`$ pip install alembic`
`$ alembic init migrations`

в `alembic.ini`:

```python
sqlalchemy.url = driver://user:pass@localhost/dbname
```

в `migrations/env.py`:

```python
# The Alembic Config object.
config = context.config

# Configure Alembic to use our DATABASE_URL and our table definitions...
import app
config.set_main_option('sqlalchemy.url', str(app.DATABASE_URL))
target_metadata = app.metadata
```

теперь можно создавать ревизию

`alembic revision -m "Create notes table"`

и наконец популяцию в `migrations/versions`

```python
def upgrade():
    op.create_table(
      'notes',
      sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
      sqlalchemy.Column("text", sqlalchemy.String),
      sqlalchemy.Column("completed", sqlalchemy.Boolean),
    )

def downgrade():
    op.drop_table('notes')
```

и миграциб

`alembic upgrade head`

Вариант с тестированием и базой данныъ (создаем миграцию каждый запуск теста вместе с созданием БД)

```python
from alembic import command
from alembic.config import Config
import app

...

@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    url = str(app.DATABASE_URL)
    engine = create_engine(url)
    assert not database_exists(url), 'Test database already exists. Aborting tests.'
    create_database(url)             # Create the test database.
    config = Config("alembic.ini")   # Run the migrations.
    command.upgrade(config, "head")
    yield                            # Run the tests.
    drop_database(url)               # Drop the test database.
```

## [[graphQL]] [ссылка на статью](https://www.starlette.io/graphql/)

## [authentication](https://www.starlette.io/authentication/)

## [API schemas](https://www.starlette.io/schemas/)'

## [Events](https://www.starlette.io/events/)

Могут быть ассинхронные корутины или обычные функции.

```python
from starlette.applications import Starlette


async def some_startup_task():
    pass

async def some_shutdown_task():
    pass

routes = [
    ...
]

app = Starlette(
    routes=routes,
    on_startup=[some_startup_task],
    on_shutdown=[some_shutdown_task]
```

Вариант запуска тестового клиента вручную, без сетапов или тирдаун кода

```python
from example import app
from starlette.testclient import TestClient


def test_homepage():
    with TestClient(app) as client:
        # Application 'on_startup' handlers are called on entering the block.
        response = client.get("/")
        assert response.status_code == 200

    # Application 'on_shutdown' handlers are called on exiting the block.
```

## [Background tasks](https://www.starlette.io/background/)

Бекграунд таски прикреплены к запросам и запускаются, только, если запрос отправлен. В старлетт два класса - для единственного таска и для множества `BackgroundTask` и `BackgroundTasks`. Все это нужно, чтобы отправить что-то не сильно актуальное (например имейлы или внести какие-то второстепенные данные в какую-то БД), что не требует остановки процесса.

```python
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.background import BackgroundTask


...

async def signup(request):
    data = await request.json()
    username = data['username']
    email = data['email']
    task = BackgroundTask(send_welcome_email, to_address=email)
    message = {'status': 'Signup successful'}
    return JSONResponse(message, background=task)

async def send_welcome_email(to_address):

routes = [
    ...
    Route('/user/signup', endpoint=signup, methods=['POST'])
]

app = Starlette(routes=routes)
```

несколько

```python
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.background import BackgroundTasks

async def signup(request):
    data = await request.json()
    username = data['username']
    email = data['email']
    tasks = BackgroundTasks()
    tasks.add_task(send_welcome_email, to_address=email)
    tasks.add_task(send_admin_notification, username=username)
    message = {'status': 'Signup successful'}
    return JSONResponse(message, background=tasks)

async def send_welcome_email(to_address):
    ...

async def send_admin_notification(username):
    ...

routes = [
    Route('/user/signup', endpoint=signup, methods=['POST'])
]

app = Starlette(routes=routes)
```

## [Серверные пуши](https://www.starlette.io/server-push/)

## [Эксепшены и http-ошибки](https://www.starlette.io/exceptions/)

## [Конфигурирование](https://www.starlette.io/config/)

пример конфигурации

```python
import databases

from starlette.applications import Starlette
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

# Config will be read from environment variables and/or ".env" files.
config = Config(".env")

DEBUG = config('DEBUG', cast=bool, default=False)
DATABASE_URL = config('DATABASE_URL', cast=databases.DatabaseURL)
SECRET_KEY = config('SECRET_KEY', cast=Secret)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=CommaSeparatedStrings)

app = Starlette(debug=DEBUG)
```

```,env
# Don't commit this to source control.
# Eg. Include ".env" in your `.gitignore` file.
DEBUG=True
DATABASE_URL=postgresql://localhost/myproject
SECRET_KEY=43n080musdfjt54t-09sdgr
ALLOWED_HOSTS=127.0.0.1, localhost
```

Варианты конфигурирования:

- из переменных окружения
- из `.env`
- из дефолтных значений, предоставленных в конфиге

Класс `secret` используется для сокрытия информации из логов. Мы задаем только число значений и словарь

```python
>>> from myproject import settings
>>> settings.SECRET_KEY
Secret('**********')
>>> str(settings.SECRET_KEY)
'98n349$%8b8-7yjn0n8y93T$23r'
```

```python
>>> from myproject import settings
>>> settings.DATABASE_URL
DatabaseURL('postgresql://admin:**********@192.168.0.8/my-application')
>>> str(settings.DATABASE_URL)
'postgresql://admin:Fkjh348htGee4t3@192.168.0.8/my-application'
```

```python
>>> from myproject import settings
>>> print(settings.ALLOWED_HOSTS)
CommaSeparatedStrings(['127.0.0.1', 'localhost'])
>>> print(list(settings.ALLOWED_HOSTS))
['127.0.0.1', 'localhost']
>>> print(len(settings.ALLOWED_HOSTS))
2
>>> print(settings.ALLOWED_HOSTS[0])
'127.0.0.1'
```

Для тестирвоания можно переписать переменные окружения через специальный инстанс старлета

```python
from starlette.config import environ

environ['TESTING'] = 'TRUE'
```

[Полный пример тут](https://www.starlette.io/config/)

## [Тестовый клиент](https://www.starlette.io/testclient/)

[[starlette-testclient]]

Можно тестировать как ассинхронные функции так и вебсокеты. Можно использовать стандартное API запроса. Клиент подымает [[http-requests-errors]], но это можно отключить `client = TestClient(app, raise_server_exceptions=False)`

Пример для вебсокетов смотри по ссылке. Важно: с вебсокетом работать через `width`

## [Third Party Packages](https://www.starlette.io/third-party-packages/)

[[starlete-список-кодов]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[fastapi]: ../lists/fastapi "Аastapi"
[uvicorn]: uvicorn "Uvicorn"
[type-annotation]: type-annotation "Анотация типов в python"
[sqlalchemy]: ../lists/sqlalchemy "Sqlalchemy"
[gino]: gino "Gino"
[databases]: databases "Databases"
[sqlalchemy]: ../lists/sqlalchemy "Sqlalchemy"
[alembic]: alembic "Alembic"
[starlette-testclient]: starlette-testclient "Starlette test client"
[http-requests-errors]: http-requests-errors "Http-requests"
[starlete-список-кодов]: starlete-список-кодов "Starlete-список-кодов"
[//end]: # "Autogenerated link references"