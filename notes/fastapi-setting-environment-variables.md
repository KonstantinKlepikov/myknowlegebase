# fastapi environment variables

[Основная статья](https://fastapi.tiangolo.com/pt/advanced/settings/)

Прочитать переменные окружения в #python можно так

```python
import os

name = os.getenv("MY_NAME", "World")
print(f"Hello {name} from Python")
```

Переменные окружения - это всегда строго строки. Валидировать их можно в [[pydantic]] через импорт `BaseSettings`

```python
from fastapi import FastAPI
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str
    items_per_user: int = 50


settings = Settings()
app = FastAPI()


@app.get("/info")
async def info():
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }
```

Теперь мы можем создать инстанс этого класса и читать переменные окружения, валидируя их. Для этого надо запустить сервер с нужно конфигурацией:

```shell
ADMIN_EMAIL="deadpool@example.com" APP_NAME="ChimichangApp" uvicorn main:app

INFO: Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Теперь `admin_email` установлен в "deadpool@example.com" ну и т.д.

Кроме того мы можем создать сеттинги как зависимость, импортировать их в другой модуль и использовать в функции

```python
from functools import lru_cache

from fastapi import Depends, FastAPI

from . import config

app = FastAPI()


@lru_cache()
def get_settings():
    return config.Settings()


@app.get("/info")
async def info(settings: config.Settings = Depends(get_settings)):
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }
```

В дапнном случае мы внедрили зависимость от get_settings(), которая в свою очередь возвращает переменные окружения.

Наконец мы можем переопределить [[fastapi-testing-dependencies-with-override]] зависимости и в них переменные для [[тестирование]]

```python
from fastapi.testclient import TestClient

from . import config, main

client = TestClient(main.app)


def get_settings_override():
    return config.Settings(admin_email="testing_admin@example.com")


main.app.dependency_overrides[main.get_settings] = get_settings_override


def test_app():

    response = client.get("/info")
    data = response.json()
    assert data == {
        "app_name": "Awesome API",
        "admin_email": "testing_admin@example.com",
        "items_per_user": 50,
    }
```

## [Reading a .env file](https://fastapi.tiangolo.com/pt/advanced/settings/#reading-a-env-file)

В [[pydantic]] есть [поддержка .env](https://pydantic-docs.helpmanual.io/usage/settings/#dotenv-env-support). Нужно поставить `pip install dotenv` и добавить .env в конфиги

```python
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str
    items_per_user: int = 50

    class Config:
        env_file = ".env"
```

## lru_cash()

Все переменные можно задать один раз для всего

```python
from functools import lru_cache

from fastapi import Depends, FastAPI

from . import config

app = FastAPI()


@lru_cache()
def get_settings():
    return config.Settings()


@app.get("/info")
async def info(settings: config.Settings = Depends(get_settings)):
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }
```

`lru_cash()` модифицирует декорируемую функцию так, чтобы при последующих вычислениях возвращать результат первого вычисления при условии, что входные данные или функция не обновились.

[Подробнее про lru_cashe()](https://docs.python.org/3/library/functools.html#functools.lru_cache)

[[fastapi]]
[[fastapi-testing-dependencies-with-override]]