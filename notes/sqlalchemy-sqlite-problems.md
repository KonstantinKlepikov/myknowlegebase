# sqlalchemy-sqlite-problems

## При миграции с [[alembic]] выпадает ошибка "No support for ALTER of constraints in SQLite dialect"

В env.py алембика проставить:

```python
context.configure(
    connection=connection,
    target_metadata=target_metadata,
    render_as_batch=True # <===this
)
```

[Ссылка на оверфло](https://stackoverflow.com/a/32510603)

[[sqlalchemy]]
[[sqlite]]
