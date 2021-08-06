# sqlite

[Документация python](https://docs.python.org/3/library/sqlite3.html)
[Работа с in-memory](https://sqlite.org/inmemorydb.html)

Библиотечка на C для работы с диск-бейсед ДБ. Язык SQL не стандартный.

Пайплайн работы

```python
import sqlite3

# create and/or open db
con = sqlite3.connect('example.db')

cur = con.cursor()

# Create table
cur.execute('''CREATE TABLE stocks
               (date text, trans text, symbol text, qty real, price real)''')

# Insert a row of data
cur.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# Save (commit) the changes
con.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
con.close()
```

Можно (и нужно) с контекстным менеджером.

Курсор возвращает итератор

```python
import sqlite3
con = sqlite3.connect('example.db')
cur = con.cursor()

>>> for row in cur.execute('SELECT * FROM stocks ORDER BY price'):
        print(row)

('2006-01-05', 'BUY', 'RHAT', 100, 35.14)
('2006-03-28', 'BUY', 'IBM', 1000, 45.0)
('2006-04-06', 'SELL', 'IBM', 500, 53.0)
('2006-04-05', 'BUY', 'MSFT', 1000, 72.0)
```

Для формирования запросов можно использовать питоньи строки... но **НИКОГДА так не делай**, т.к. это небезопасно с точки зрения инъекций.

```python
# Never do this -- insecure!
symbol = 'RHAT'
cur.execute("SELECT * FROM stocks WHERE symbol = '%s'" % symbol)
```

Вместо этого используй подстановку параметров DB-API. Помести плейсхолдер], где недо использовать значение, а затем укажит кортеж значений в качестве второго аргумента метода курсора execute(). Оператор SQL может использовать один из двух типов заполнителей: вопросительные знаки (стиль qmark) или именованные заполнители (именованный стиль). Для стиля qmark параметры должны быть последовательностью. Для именованного стиля это может быть как последовательность, так и экземпляр dict. Длина последовательности должна соответствовать количеству заполнителей, в противном случае возникает ошибка ProgrammingError. Если дан dict, он должен содержать ключи для всех именованных параметров. Любые лишние элементы игнорируются. Вот пример обоих стилей:

```python
import sqlite3

con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.execute("create table lang (lang_name, lang_age)")

# This is the qmark style:
cur.execute("insert into lang values (?, ?)", ("C", 49))

# The qmark style used with executemany():
lang_list = [
    ("Fortran", 64),
    ("Python", 30),
    ("Go", 11),
]
cur.executemany("insert into lang values (?, ?)", lang_list)

# And this is the named style:
cur.execute("select * from lang where lang_name=:name and lang_age=:age",
            {"name": "C", "age": 49})
print(cur.fetchall())

con.close()
```

## [Функции и константы](https://docs.python.org/3/library/sqlite3.html#module-functions-and-constants). Разберу только основные

### Connect

```python
sqlite3.connect(database[, timeout, detect_types, isolation_level, check_same_thread, factory, cached_statements, uri])
```

Возвращает [connection объект](https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection). Бд - это [path-like](https://docs.python.org/3/glossary.html#term-path-like-object) обхект. Можно запустить базу в памяти с помощью `:memory:`

SQKite может обрабатывать только один запрос, который меняет что-то в БД. На это время она лочится. Парметр `timeout` определяет сколько запрос может ждать своей очереди.

**SQLite поддерживает только TEXT, INTEGER, REAL, BLOB и NULL типы данных**. Другие типы нужно добавлять.

`check_same_thread` определяет кем используется коннекшен - текущим тредом или коннекшен может быть расшарен между несколькими.

С помощю `url` к бд можно коннектиться по урлу, а не по path-like строке

```python
db = sqlite3.connect('file:path/to/database?mode=ro', uri=True)
```

#### Конвертация типов из БД-шных в питоньи

```python
sqlite3.register_converter(typename, callable)
```

Конвертит bytestring d какой-то стандартный #python тип. Так-же конвертятся питоньи типы в SQLite

```python
sqlite3.register_adapter(type, callable)
```

### [Connection object](https://docs.python.org/3/library/sqlite3.html#connection-objects)

Класс `sqlite3.Connection` имеет множество методов, в т.ч.:

- `cursor(factory=Cursor)`
- `commit()`
- `rollback()`
- `close()`
- `execute(sql[, parameters])` - возвращает данные для cursor() и [извлечения параметров](https://docs.python.org/3/library/sqlite3.html#sqlite3.Cursor.execute). Смотри там же `eecutemany` и `executescript`
- `create_function(name, num_params, func, *, deterministic=False)` создает опреденню юзером функцию для последующего извлечения
- `create_aggregate(name, num_params, aggregate_class)` [тоже самое на основе класса](https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.create_aggregate)
- `create_collation(name, callable)`
- `interrupt()`
- `row_factory`, `text_factory`
- `total_changes` возвращает общее число измененных строк
- `iterdump()` используется для сейва дб в памяти для последующего восстановления
- `backup(target, *, pages=-1, progress=None, name="main", sleep=0.250)`. [Пример](https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.backup)
  
```python
import sqlite3

def progress(status, remaining, total):
    print(f'Copied {total-remaining} of {total} pages...')

con = sqlite3.connect('existing_db.db')
bck = sqlite3.connect('backup.db')
with bck:
    con.backup(bck, pages=1, progress=progress)
bck.close()
con.close()
```

### [Cursor objects](https://docs.python.org/3/library/sqlite3.html#cursor-objects)

Класс `sqlite3.Cursor`

- `execute(sql[, parameters])` возвращает заданное представление. Можно использовать [плейсхолдеры](https://docs.python.org/3/library/sqlite3.html#sqlite3-placeholders).

- `executemany(sql, seq_of_parameters)`. Можно с классом, можно с генератором

```python
import sqlite3
import string

def char_generator():
    for c in string.ascii_lowercase:
        yield (c,)

con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.execute("create table characters(c)")

cur.executemany("insert into characters(c) values (?)", char_generator())

cur.execute("select c from characters")
print(cur.fetchall())

con.close()
```

- `executescript(sql_script)`
- `fetchone()`, `fetchmany(size=cursor.arraysize)`, `fetchall()` добавляют строки к текущему запросу
- `close()` закрыть курсор

... и еще некоторое кол-возвращает

### [Row object](https://docs.python.org/3/library/sqlite3.html#row-objects)

Класс `sqlite3.Row`. Единственный метод `keys()` возвращает имен колонок.

Пример

```python
con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.execute('''create table stocks
(date text, trans text, symbol text,
 qty real, price real)''')
cur.execute("""insert into stocks
            values ('2006-01-05','BUY','RHAT',100,35.14)""")
con.commit()
cur.close()

>>> con.row_factory = sqlite3.Row
>>> cur = con.cursor()
>>> cur.execute('select * from stocks')
<sqlite3.Cursor object at 0x7f4e7dd8fa80>
>>> r = cur.fetchone()
>>> type(r)
<class 'sqlite3.Row'>
>>> tuple(r)
('2006-01-05', 'BUY', 'RHAT', 100.0, 35.14)
>>> len(r)
5
>>> r[2]
'RHAT'
>>> r.keys()
['date', 'trans', 'symbol', 'qty', 'price']
>>> r['qty']
100.0
>>> for member in r:
...     print(member)
...
2006-01-05
BUY
RHAT
100.0
35.14
```

### [Exceptions](https://docs.python.org/3/library/sqlite3.html#exceptions)

### [Соответствие типов python и sqlite](https://docs.python.org/3/library/sqlite3.html#sqlite-and-python-types)

## [Примеры использования](https://docs.python.org/3/library/sqlite3.html#using-sqlite3-efficiently)

[[sqlalchemy]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[sqlalchemy]: ../lists/sqlalchemy "sqlalchemy"
[//end]: # "Autogenerated link references"