# fastapi-setup-teardown

[Testing Events: startup - shutdown](https://fastapi.tiangolo.com/pt/advanced/testing-events/)

Можно запускать тестовый клиент с менеджером контекста `with`

```python
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

items = {}


@app.on_event("startup")
async def startup_event():
    items["foo"] = {"name": "Fighters"}
    items["bar"] = {"name": "Tenders"}


@app.get("/items/{item_id}")
async def read_items(item_id: str):
    return items[item_id]


def test_read_items():
    with TestClient(app) as client:
        response = client.get("/items/foo")
        assert response.status_code == 200
        assert response.json() == {"name": "Fighters"}
```

Метод можно использовать для переопределения зависимостей в тестах [[fastapi-testing-dependencies-with-override]]

[[fastapi]]
[[starlette-testclient]]
[[тестирование]]