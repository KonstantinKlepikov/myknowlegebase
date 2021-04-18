# alembic

Тулза для миграции ДБ в [[sqlalchemy]] на #python

[документация](https://alembic.sqlalchemy.org/en/latest/)

## [Создание окружения для миграции](https://alembic.sqlalchemy.org/en/latest/tutorial.html#the-migration-environment)

Через `alembic init folder`

Создается вот такая структура:

- yourproject/
  - alembic/
    - env.py
    - README
    - script.py.mako
    - versions/
      - 3512b954651e_add_account.py
      - 2b1ae634e5cd_add_order_id.py
      - 3adcc9a56557_rename_username_field.py

Здесь `env.py` определяет инструкции для миграций. `script.py.mako` генерирует новые скрипты миграции, а в `versions/` хранятся все версии миграций.

`alembic list_templates` выведет все шаблоны миграций

Теперь можно [сконфигурировать](https://alembic.sqlalchemy.org/en/latest/tutorial.html#editing-the-ini-file) файл `alembic.ini`

Для началанам будет достаточно указать расположение БД, например так:

```ini
sqlalchemy.url = sqlite:///./test.db
```

## [Создание миграции](https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script)

Мы можем создать новую версию миграционного скрипта так: `alembic revision -m "create account table"`

[[sqlalchemy]]
