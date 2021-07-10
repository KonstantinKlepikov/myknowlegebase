# Fastapi testing dependencies with owerride

[Статья](https://fastapi.tiangolo.com/pt/advanced/testing-dependencies/)

Иногда надо переписать зависимости, к примеру когда используется внешняя аутентикация юзера. Чтобы тест не зависил от реализации, для теста можно переписать зависимости. Для этого используется атрибут `app.dependency_overrides`

```python
from typing import Optional

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


async def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return {"message": "Hello Items!", "params": commons}


@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return {"message": "Hello Users!", "params": commons}


client = TestClient(app)


async def override_dependency(q: Optional[str] = None):
    return {"q": q, "skip": 5, "limit": 10}


app.dependency_overrides[common_parameters] = override_dependency


def test_override_in_items():
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": None, "skip": 5, "limit": 10},
    }


def test_override_in_items_with_q():
    response = client.get("/items/?q=foo")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": "foo", "skip": 5, "limit": 10},
    }


def test_override_in_items_with_params():
    response = client.get("/items/?q=foo&skip=100&limit=200")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": "foo", "skip": 5, "limit": 10},
    }
```

После выполнение действий с переопределенными зависимостями, можно сбросить словарь переопределенных зависимостей вот так `app.dependency_overrides = {}`

Если нужно переопределить зависимости только для тест, то можно переопределить их на старте теста [[fastapi-setup-teardown]]

Вот так метод применен в [[fastapi-тестирование-базы-данных]]

[[fastapi]]
[[тестирование]]
[[fastapi-setting-environment-variables]]