---
description: Тестирование баз данных в fastapi
tags: fastapi data-bases python
title: Fastapi тестирование базы данных
---
```python
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..database import Base
from ..main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_user():
    response = client.post(
        "/users/",
        json={"email": "deadpool@example.com", "password": "chimichangas4life"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "deadpool@example.com"
    assert "id" in data
    user_id = data["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "deadpool@example.com"
    assert data["id"] == user_id
```

Метод описан подробнее в [[fastapi-testing-dependencies-with-override]]

- [Ссылка на этот пример с подробностями](https://fastapi.tiangolo.com/advanced/testing-database/)
- [[fatsapi-sql-orm-example]]
- [[fastapi]]
- [[тестирование]]


[fastapi-testing-dependencies-with-override]: fastapi-testing-dependencies-with-override "Fastapi testing dependencies with owerride"
[fatsapi-sql-orm-example]: fatsapi-sql-orm-example "Fatsapi sql orm example"
[fastapi]: fastapi "Fastapi"
[тестирование]: ../lists/%D1%82%D0%B5%D1%81%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5 "Основные принципы тестровния"
