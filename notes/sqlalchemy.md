# sqlalchemy

Схема работы

![sqlalchemy](../attachments/2021-04-15-23-51-38.png)

[туторилалы](https://docs.sqlalchemy.org/en/14/)

## [Запуск приложения](https://docs.sqlalchemy.org/en/14/tutorial/engine.html)

Используется объект [engine](https://docs.sqlalchemy.org/en/14/core/future.html#sqlalchemy.future.Engine). Engine реализует [connection pool](https://docs.sqlalchemy.org/en/14/core/pooling.html). Engine - это глобальный объект, который формируется и конфигурируется только один раз для части сервера, общающегося с ДБ.

```python
>>> from sqlalchemy import create_engine
>>> engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
```

[ДБ url](https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls) задает три вещи: диалект, параметры доступа и имя конкретной БД

`dialect+driver://username:password@host:port/database`

[Пример для](https://docs.sqlalchemy.org/en/14/core/engines.html#sqlite) [[sqlite]]

## [Работа с транзакциями и БД](https://docs.sqlalchemy.org/en/14/tutorial/dbapi_transactions.html)

`connect()`

```python
>>> from sqlalchemy import text

>>> with engine.connect() as conn:
...     result = conn.execute(text("select 'hello world'"))
...     print(result.all())
```

```sql
BEGIN (implicit)
select 'hello world'
[...] ()
[('hello world',)]
ROLLBACK
```

`commit()`

```python
# "commit as you go"
>>> with engine.connect() as conn:
...     conn.execute(text("CREATE TABLE some_table (x int, y int)"))
...     conn.execute(
...         text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
...         [{"x": 1, "y": 1}, {"x": 2, "y": 4}]
...     )
...     conn.commit()
```

```sql
BEGIN (implicit)
CREATE TABLE some_table (x int, y int)
[...] ()
<sqlalchemy.engine.cursor.CursorResult object at 0x...>
INSERT INTO some_table (x, y) VALUES (?, ?)
[...] ((1, 1), (2, 4))
<sqlalchemy.engine.cursor.CursorResult object at 0x...>
COMMIT
```

Другой метод `begin()` возвращает коннект [с уже открытым комитом](https://docs.sqlalchemy.org/en/14/core/future.html#sqlalchemy.future.Engine.begin)

```python
# "begin once"
>>> with engine.begin() as conn:
...     conn.execute(
...         text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
...         [{"x": 6, "y": 8}, {"x": 9, "y": 10}]
...     )
```

```sql
BEGIN (implicit)
INSERT INTO some_table (x, y) VALUES (?, ?)
[...] ((6, 8), (9, 10))
<sqlalchemy.engine.cursor.CursorResult object at 0x...>
COMMIT
```

## [Извлечение состояний БД напрямую](https://docs.sqlalchemy.org/en/14/tutorial/dbapi_transactions.html#basics-of-statement-execution)

[Основной метод](https://docs.sqlalchemy.org/en/14/core/future.html#sqlalchemy.future.Connection.execute) `execute()` В коньюнкции с [методом](https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.expression.text) `text()` он возвращает [объект](https://docs.sqlalchemy.org/en/14/core/connections.html#sqlalchemy.engine.Result) `result`

### [Объединение строк](https://docs.sqlalchemy.org/en/14/tutorial/dbapi_transactions.html#fetching-rows)

```python
>>> with engine.connect() as conn:
...     result = conn.execute(text("SELECT x, y FROM some_table"))
...     for row in result:
...         print(f"x: {row.x}  y: {row.y}")
```

```sql
BEGIN (implicit)
SELECT x, y FROM some_table
[...] ()
x: 1  y: 1
x: 2  y: 4
x: 6  y: 8
x: 9  y: 10
ROLLBACK
```

### [Отправка параметров](https://docs.sqlalchemy.org/en/14/tutorial/dbapi_transactions.html#sending-parameters)

### [Построение параметров из полученного ранее представления бд](https://docs.sqlalchemy.org/en/14/tutorial/dbapi_transactions.html#bundling-parameters-with-a-statement)

## [Извлечение представления при помощи ОРМ-сессии](https://docs.sqlalchemy.org/en/14/tutorial/dbapi_transactions.html#executing-with-an-orm-session)

Используется [объект](https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session) `Session`

[колонки и типы данных](https://docs.sqlalchemy.org/en/14/core/types.html)
[коннекшен и работа с in-memory](https://docs.sqlalchemy.org/en/14/dialects/sqlite.html#connect-strings)

Утилиты для sqlalchemy: [sqlalchemy_utils](https://sqlalchemy-utils.readthedocs.io/en/latest/index.html). Не пашет с sqlalchemy-1.4. [Сурс](https://stackoverflow.com/a/66651808)

> You have installed SQLAlchemy 1.4.0. SQLAlchemy-utils is currently not compatible with SQLAlchemy > 1.4.0. The solution is to downgrade SQLAlchemy to 1.3.23.

[[fatsapi-sql-orm-example]]
[[sqlite]]
[[alembic]] - тулза для миграций для sqlalchemy
