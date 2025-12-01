---
description: Тестирование с переопределением зависимостей в fastapi
tags: fastapi python
title: Fastapi testing dependencies with owerride
---
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

- [[fastapi]]
- [[тестирование]]
- [[fastapi-setting-environment-variables]]


[fastapi-setup-teardown]: fastapi-setup-teardown "Fastapi setup teardown"
[fastapi-тестирование-базы-данных]: fastapi-%D1%82%D0%B5%D1%81%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5-%D0%B1%D0%B0%D0%B7%D1%8B-%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85 "Fastapi тестирование базы данных"
[fastapi]: fastapi "Fastapi"
[тестирование]: ../lists/%D1%82%D0%B5%D1%81%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5 "Основные принципы тестровния"
[fastapi-setting-environment-variables]: fastapi-setting-environment-variables "Fastapi environment variables"
