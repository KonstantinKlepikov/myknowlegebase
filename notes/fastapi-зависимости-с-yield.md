# fastapi-зависимости-с-yield

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

[[fastapi]]
[[fatsapi-sql-orm-example]]
