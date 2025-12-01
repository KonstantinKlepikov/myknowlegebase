---
description: События в fastapi
tags: fastapi python
title: Fastapi events
---
Вы можете определить эту логику запуска и завершения работы, используя параметр lifespan приложения FastAPI и «менеджер контекста».

```python
from contextlib import asynccontextmanager

from fastapi import FastAPI


def fake_answer_to_everything_ml_model(x: float):
    return x * 42


ml_models = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    ml_models["answer_to_everything"] = fake_answer_to_everything_ml_model
    yield
    # Clean up the ML models and release the resources
    ml_models.clear()


app = FastAPI(lifespan=lifespan)


@app.get("/predict")
async def predict(x: float):
    result = ml_models["answer_to_everything"](x)
    return {"result": result}
```

Здесь мы имитируем дорогостоящую операцию запуска загрузки модели, помещая (фальшивую) функцию в словарь с моделями машинного обучения перед `yield`. Этот код будет выполнен до того, как приложение начнет принимать запросы, во время запуска. А потом, сразу после выхода, выгружаем модель.

Этот код будет выполняться после того, как приложение завершит обработку запросов, прямо перед завершением работы. Это может, например, высвободить такие ресурсы, как память или процессорное время.

В данном контексте используется концепция [[fastapi-зависимости-с-yield]]

## [[starlette]] events style

[Статья](https://www.starlette.io/events/)

```python
# in starlette
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
)
```

## Old fastapi events (deprecated)

Startup

```python
from fastapi import FastAPI

app = FastAPI()

items = {}


@app.on_event("startup")
async def startup_event():
    items["foo"] = {"name": "Fighters"}
    items["bar"] = {"name": "Tenders"}


@app.get("/items/{item_id}")
async def read_items(item_id: str):
    return items[item_id]
```

Shutdown

```python
from fastapi import FastAPI

app = FastAPI()


@app.on_event("shutdown")
def shutdown_event():
    with open("log.txt", mode="a") as log:
        log.write("Application shutdown")


@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]
```

Смотри еще:

- [[fastapi-зависимости-с-yield]]
- [fastapi-events lib](https://github.com/melvinkcx/fastapi-events/) Asynchronous event dispatching/handling library for FastAPI and Starlette
- [[fastapi]]
- [[starlette]]


[fastapi-зависимости-с-yield]: fastapi-%D0%B7%D0%B0%D0%B2%D0%B8%D1%81%D0%B8%D0%BC%D0%BE%D1%81%D1%82%D0%B8-%D1%81-yield "Fastapi зависимости с yield"
[starlette]: starlette "Starlette"
[fastapi]: fastapi "Fastapi"


[fastapi-зависимости-с-yield]: fastapi-зависимости-с-yield "Fastapi зависимости с yield"
[starlette]: starlette "Starlette"
[fastapi-зависимости-с-yield]: fastapi-зависимости-с-yield "Fastapi зависимости с yield"
[fastapi]: fastapi "Fastapi"
[starlette]: starlette "Starlette"
