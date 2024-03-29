---
description: Зависимости с yield в fastapi
tags: fastapi python
title: Fastapi зависимости с yield
---
Yield позволяет реализовать зависимости, которые делают некоторые действия после того, как завершили действие

[Сама статья](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/)

Необходимо установить

`pip install async-exit-stack async-generator`

```python
async def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()
```

Можно создавать сабзависимости:

```python
from fastapi import Depends


async def dependency_a():
    dep_a = generate_dep_a()
    try:
        yield dep_a
    finally:
        dep_a.close()


async def dependency_b(dep_a=Depends(dependency_a)):
    dep_b = generate_dep_b()
    try:
        yield dep_b
    finally:
        dep_b.close(dep_a)


async def dependency_c(dep_b=Depends(dependency_b)):
    dep_c = generate_dep_c()
    try:
        yield dep_c
    finally:
        dep_c.close(dep_b)
```

`HTTPException` после `yield` использовать нельяз - это не будет работать.

Другой путь создания зависимостей - это контекстные менеджеры. В [[fastapi]] можно использовать в качестве зависимостей любые функции, декорированные через:

- `@contextlib.contextmanager`
- `@contextlib.asynccontextmanager`

Или сосбтвенный контекстный менеджер (в данном случае синхронный)

```python
class MySuperContextManager:
    def __init__(self):
        self.db = DBSession()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()


async def get_db():
    with MySuperContextManager() as db:
        yield db
```

[Ссылкка на статью](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/)

Смотри еще:

- [[fastapi]]
- [[fatsapi-sql-orm-example]]
- [[asyncio]]
- [[dependency-injection]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[fastapi]: fastapi "Fastapi"
[fatsapi-sql-orm-example]: fatsapi-sql-orm-example "Fatsapi sql orm example"
[asyncio]: asyncio "Asyncio"
[dependency-injection]: dependency-injection "Dependency injection"
[//end]: # "Autogenerated link references"
[//begin]: # "Autogenerated link references for markdown compatibility"
[fastapi]: fastapi "Fastapi"
[fastapi]: fastapi "Fastapi"
[fatsapi-sql-orm-example]: fatsapi-sql-orm-example "Fatsapi sql orm example"
[asyncio]: asyncio "Asyncio"
[//end]: # "Autogenerated link references"