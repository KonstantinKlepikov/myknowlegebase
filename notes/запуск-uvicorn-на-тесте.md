---
description: Fastapi v3 спецификация и тестирование
tags: fastapi python
title: Fast-api v3 спецификация
---
Тестирование на [[fastapi]] [статья из документации](https://fastapi.tiangolo.com/tutorial/testing/)

```python
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/")
async def read_main():
    return {"msg": "Hello World"}

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
```

Реализовано на [[pytest]]

Запуск в дебаггинг режиме [статья](https://fastapi.tiangolo.com/tutorial/debugging/). Подробнее про [режимы запуска](https://www.uvicorn.org/deployment/)

```python
import uvicorn
from fastapi import FastAPI

app = FastAPI()

# ...

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Запуск [[uvicorn]] в асинхронном режиме представляет проблему

[решение](https://stackoverflow.com/questions/57412825/how-to-start-a-uvicorn-fastapi-in-background-when-testing-with-pytest)


[fastapi]: fastapi "Fastapi"
[pytest]: pytest "Pytest"
[uvicorn]: uvicorn "Uvicorn"
