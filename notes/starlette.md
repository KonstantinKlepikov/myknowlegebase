# starlette

ASGI асинхронный фреймворк на #python. Используется в [[fastapi]]

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

[[starlette-testclient]]
