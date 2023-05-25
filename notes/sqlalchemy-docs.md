---
description: Документация sqlalchemy
tags: sqlalchemy python bd
title: Sqlalchemy документация bd
---
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

Используется [объект](https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session) `Session`. Сессию есть смысл использовать только с ОРМ, т.к. в других случаях она не дает особых преимуществ.

```python
>>> from sqlalchemy.orm import Session

>>> stmt = text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y").bindparams(y=6)
>>> with Session(engine) as session:
...     result = session.execute(stmt)
...     for row in result:
...        print(f"x: {row.x}  y: {row.y}")
```

```sql
BEGIN (implicit)
SELECT x, y FROM some_table WHERE y > ? ORDER BY x, y
[...] (6,)
x: 6  y: 8
x: 9  y: 10
x: 11  y: 12
x: 13  y: 14
ROLLBACK
```

## [Работа с метаданными БД](https://docs.sqlalchemy.org/en/14/tutorial/metadata.html)

Используется [объект](https://docs.sqlalchemy.org/en/14/glossary.html#term-database-metadata) `database metadata`, который в пиотоне реализует представление БД строки-колонки. Базовым элементом метаданных БД является `table`. Метвдвнные можно инициализировать так:

```python
>>> from sqlalchemy import MetaData
>>> metadata = MetaData()
```

Типичное решение для большинства приложений - один инстантс метаданных. SGLAlchemy позволяет комбинировать множетво для одного приложения. Следующий шан - создание таблиц:

```python
>>> from sqlalchemy import Table, Column, Integer, String
>>> user_table = Table(
...     "user_account",
...     metadata,
...     Column('id', Integer, primary_key=True),
...     Column('name', String(30)),
...     Column('fullname', String)
... )
```

Здесь инстанс `table` представляет отдельную таблицу в БД. Колонка представлена инстансом `column`. Типы данных, такие как `Integer` могут добавляться в колонку как с помощью, так и без помощи инствнсов.

```python
>>> user_table.c.name
Column('name', String(length=30), table=<user_account>)

>>> user_table.c.keys()
['id', 'name', 'fullname']
```

Тут-же задаются ограничение, к примеру `primary key` или [foregn key](https://docs.sqlalchemy.org/en/14/glossary.html#term-foreign-key-constraint)

```python
>>> from sqlalchemy import ForeignKey
>>> address_table = Table(
...     "address",
...     metadata,
...     Column('id', Integer, primary_key=True),
...     Column('user_id', ForeignKey('user_account.id'), nullable=False),
...     Column('email_address', String, nullable=False)
... )
```

## [Определение метаданных с помощью ОРМ](https://docs.sqlalchemy.org/en/14/tutorial/metadata.html#defining-table-metadata-with-the-orm)

Когда мыф используем ОРМ, процесс декларирования метаданных совмещен с процессом декларирования [маппированных классов](https://docs.sqlalchemy.org/en/14/glossary.html#term-mapped). Маппированный класс - это любой #python класс, который имеет аттрибуты слинкованные с колонками БД. Это делается с помощью [объекта](https://docs.sqlalchemy.org/en/14/orm/mapping_api.html#sqlalchemy.orm.registry) `registry`

```python
>>> from sqlalchemy.orm import registry
>>> mapper_registry = registry()

>>> mapper_registry.metadata
MetaData()
```

Теперь, вместо декларпирования таблиц и колонок напрямую, мы можем это сделать в маппируемом классе.

```python
>>> Base = mapper_registry.generate_base()
```

Есть и комбинированный метод, объединяющий `registry` и декларацию БД

```python
from sqlalchemy.orm import declarative_base
Base = declarative_base()
```

Теперь осталось задекларировать маппированный классы.

```python
>>> from sqlalchemy.orm import relationship
>>> class User(Base):
...     __tablename__ = 'user_account'
...
...     id = Column(Integer, primary_key=True)
...     name = Column(String(30))
...     fullname = Column(String)
...
...     addresses = relationship("Address", back_populates="user")
...
...     def __repr__(self):
...        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

>>> class Address(Base):
...     __tablename__ = 'address'
...
...     id = Column(Integer, primary_key=True)
...     email_address = Column(String, nullable=False)
...     user_id = Column(Integer, ForeignKey('user_account.id'))
...
...     user = relationship("User", back_populates="addresses")
...
...     def __repr__(self):
...         return f"Address(id={self.id!r}, email_address={self.email_address!r})"

>>> User.__table__
Table('user_account', MetaData(),
    Column('id', Integer(), table=<user_account>, primary_key=True, nullable=False),
    Column('name', String(length=30), table=<user_account>),
    Column('fullname', String(), table=<user_account>), schema=None)
```

Несколько нюансов:

- класс автоматически генерирует \__init__()
- в данном случае реализован \__repr__(). но это не обязательно
- связи между таблицами [реализованы двусторонее](https://docs.sqlalchemy.org/en/14/orm/relationship_api.html#sqlalchemy.orm.relationship) через `relationship()`

Такой метод создания метаданных [сочетаем и с прямым](https://docs.sqlalchemy.org/en/14/tutorial/metadata.html#id1) (без ОРм)

## [Работа с данными в core режиме](https://docs.sqlalchemy.org/en/14/tutorial/data.html)

Core режим сфокусирован на извлечении и отправке данных при помощи #sql эзыка

### [Core insert](https://docs.sqlalchemy.org/en/14/tutorial/data.html#core-insert)

`insert()`

```python
>>> from sqlalchemy import insert
>>> stmt = insert(user_table).values(name='spongebob', fullname="Spongebob Squarepants")

>>> print(stmt)
INSERT INTO user_account (name, fullname) VALUES (:name, :fullname)
```

Можно [скомпилировать](https://docs.sqlalchemy.org/en/14/core/internals.html#sqlalchemy.engine.Compiled)

```python
>>> compiled = stmt.compile()
>>> compiled.params
{'name': 'spongebob', 'fullname': 'Spongebob Squarepants'}
```

`execute()`

```python
>>> with engine.connect() as conn:
...     result = conn.execute(stmt)
...     conn.commit()
```

```sql
BEGIN (implicit)
INSERT INTO user_account (name, fullname) VALUES (?, ?)
[...] ('spongebob', 'Spongebob Squarepants')
COMMIT
```

Инсерт генерирует значения автоматически из параметров, переданных в `execute()`

```python
>>> with engine.connect() as conn:
...     result = conn.execute(
...         insert(user_table),
...         [
...             {"name": "sandy", "fullname": "Sandy Cheeks"},
...             {"name": "patrick", "fullname": "Patrick Star"}
...         ]
...     )
...     conn.commit()
```

```sql
BEGIN (implicit)
INSERT INTO user_account (name, fullname) VALUES (?, ?)
[...] (('sandy', 'Sandy Cheeks'), ('patrick', 'Patrick Star'))
COMMIT
```

Более реалистичный Пример

```python
>>> from sqlalchemy import select, bindparam
>>> scalar_subquery = (
...     select(user_table.c.id).
...     where(user_table.c.name==bindparam('username')).
...     scalar_subquery()
... )

>>> with engine.connect() as conn:
...     result = conn.execute(
...         insert(address_table).values(user_id=scalar_subquery),
...         [
...             {"username": 'spongebob', "email_address": "spongebob@sqlalchemy.org"},
...             {"username": 'sandy', "email_address": "sandy@sqlalchemy.org"},
...             {"username": 'sandy', "email_address": "sandy@squirrelpower.org"},
...         ]
...     )
...     conn.commit()
```

```sql
BEGIN (implicit)
INSERT INTO address (user_id, email_address) VALUES ((SELECT user_account.id
FROM user_account
WHERE user_account.name = ?), ?)
[...] (('spongebob', 'spongebob@sqlalchemy.org'), ('sandy', 'sandy@sqlalchemy.org'),
('sandy', 'sandy@squirrelpower.org'))
COMMIT
```

`Insert.from_select()` [описание метода](https://docs.sqlalchemy.org/en/14/core/dml.html#sqlalchemy.sql.expression.Insert.from_select)

```python
>>> select_stmt = select(user_table.c.id, user_table.c.name + "@aol.com")
>>> insert_stmt = insert(address_table).from_select(
...     ["user_id", "email_address"], select_stmt
... )
>>> print(insert_stmt)
```

```sql
INSERT INTO address (user_id, email_address)
SELECT user_account.id, user_account.name || :name_1 AS anon_1
FROM user_account
```

`Insert.returning()` [Описание метода](https://docs.sqlalchemy.org/en/14/core/dml.html#sqlalchemy.sql.expression.Insert.returning)

```python
>>> insert_stmt = insert(address_table).returning(address_table.c.id, address_table.c.email_address)
>>> print(insert_stmt)
```

```sql
INSERT INTO address (id, user_id, email_address)
VALUES (:id, :user_id, :email_address)
RETURNING address.id, address.email_address
```

### [Selecting Data](https://docs.sqlalchemy.org/en/14/tutorial/data.html#selecting-data)

`select()`

```python
>>> from sqlalchemy import select
>>> stmt = select(user_table).where(user_table.c.name == 'spongebob')
>>> print(stmt)
```

```sql
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.name = :name_1
```

Тоже самое через `row`

```python
>>> with engine.connect() as conn:
...     for row in conn.execute(stmt):
...         print(row)
```

```sql
BEGIN (implicit)
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.name = ?
[...] ('spongebob',)
(1, 'spongebob', 'Spongebob Squarepants')
ROLLBACK
```

Или через ОРМ

```python
>>> stmt = select(User).where(User.name == 'spongebob')
>>> with Session(engine) as session:
...     for row in session.execute(stmt):
...         print(row)
```

```sql
BEGIN (implicit)
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.name = ?
[...] ('spongebob',)
(User(id=1, name='spongebob', fullname='Spongebob Squarepants'),)
ROLLBACK
```

Примеры работы с колонками

```python
>>> print(select(user_table))
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account

>>> print(select(user_table.c.name, user_table.c.fullname))
SELECT user_account.name, user_account.fullname
FROM user_account
```

Ну и так далее - всевозможные типы запросов, делиты и т.д.: [core вариант работы с данными](https://docs.sqlalchemy.org/en/14/tutorial/data.html#selecting-data)

## [Работа с данными в ОРМ](https://docs.sqlalchemy.org/en/14/tutorial/orm_data_manipulation.html)

ОРМ режим сфокусирован на ОРМ модели и оперирует объектом `Session()`. Чтобы работать в ОРМ режиме предварительно нужно знать:

- [Executing with an ORM Session](https://docs.sqlalchemy.org/en/14/tutorial/dbapi_transactions.html#tutorial-executing-orm-session) (см. пример выше)
- [Defining Table Metadata with the ORM](https://docs.sqlalchemy.org/en/14/tutorial/metadata.html#tutorial-orm-table-metadata) (см.пример выше)
- [Selecting ORM Entities and Columns](https://docs.sqlalchemy.org/en/14/tutorial/data.html#tutorial-selecting-orm-entities) (см. пример выше)

### [Inserting Rows with the ORM](https://docs.sqlalchemy.org/en/14/tutorial/orm_data_manipulation.html#inserting-rows-with-the-orm)

Вначале мы добавляем данные к инстансу объекта `Session`, затем используя `flush()` мы отправляем весь пул в БД.

Инстанс класса представляет строки в БД.

```python
>>> squidward = User(name="squidward", fullname="Squidward Tentacles")
>>> krabs = User(name="ehkrabs", fullname="Eugene H. Krabs")

>>> squidward
User(id=None, name='squidward', fullname='Squidward Tentacles')
```

Значение `None` означает, что атрибут не был определен к текущему моменту. Маппер sqlalchemy не поднимает ошибку при неверном определении атрибута или неопределении - вместо этого он всегда подставляет представленное значение, либо `None`, либо пропускает несуществующий аттрибут.

В настоящий момент в моедли данные замаплены согласно модели `User`, но еще не ассоциированиы ни с какой базой данных. Их необходимо добавить к сессии.

```python
>>> session = Session(engine)

>>> session.add(squidward)
>>> session.add(krabs)

>>> session.new
IdentitySet([User(id=None, name='squidward', fullname='Squidward Tentacles'), User(id=None, name='ehkrabs', fullname='Eugene H. Krabs')])
```

Объект `Session` аккумулирует изменеения во времени до тех пор, пока не будет [вызван](https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session.flush) `Session.flush`.

```python
>>> session.flush()
```

```sql
BEGIN (implicit)
INSERT INTO user_account (name, fullname) VALUES (?, ?)
[...] ('squidward', 'Squidward Tentacles')
INSERT INTO user_account (name, fullname) VALUES (?, ?)
[...] ('ehkrabs', 'Eugene H. Krabs')
```

Пока `Session.flush` мы можем выполнить `Session.commit()`, `Session.rollback()`, или `Session.close()`

ОРМ создаст автоматически `primary key`для строк, добавленных во `flush`

```python
>>> squidward.id
4
>>> krabs.id
5
```

Все объекты, добавленные в память, мапятся по `identity map` и доступны через метод `get()`

```python
>>> some_squidward = session.get(User, 4)
>>> some_squidward
User(id=4, name='squidward', fullname='Squidward Tentacles')

>>> some_squidward is squidward
True
```

В завершении изменеения необходимо закомиитить, например так

```python
>>> session.commit()
COMMIT
```

### [Updating ORM Objects](https://docs.sqlalchemy.org/en/14/tutorial/orm_data_manipulation.html#updating-orm-objects)

В core реализации используется UPDATE/DELETE #sql представления. При использовании ОРМ есть два пути реализовать UPDATE:

- праймари - апдейт делается автоматически в процессе `Session`
- второй вариант - использование `Update` оператора с поддержкой ОРМ

#### Primary

```python
>>> sandy = session.execute(select(User).filter_by(name="sandy")).scalar_one()
```

```sql
BEGIN (implicit)
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.name = ?
[...] ('sandy',)
```

```python
>>> sandy
User(id=2, name='sandy', fullname='Sandy Cheeks')

# Вносим изменеения
>>> sandy.fullname = "Sandy Squirrel"

>>> sandy in session.dirty
True
```

`session.dirty` - [сет всех](https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session.dirty) "грязных" объектов, готовых к отправке изменеений.

Перед каждым следующим селектом происходит `autoflush` и изменеения отправляются в БД

```python
>>> sandy_fullname = session.execute(
...     select(User.fullname).where(User.id == 2)
... ).scalar_one()
```

```sql
UPDATE user_account SET fullname=? WHERE user_account.id = ?
[...] ('Sandy Squirrel', 2)
SELECT user_account.fullname
FROM user_account
WHERE user_account.id = ?
[...] (2,)
```

```python
>>> print(sandy_fullname)
Sandy Squirrel

>>> sandy in session.dirty
False
```

#### [ORM-enabled UPDATE statements](https://docs.sqlalchemy.org/en/14/tutorial/orm_data_manipulation.html#updating-orm-objects)

Второй вариант - это вызвать вручную update в ОРМ модели

```python
>>> session.execute(
...     update(User).
...     where(User.name == "sandy").
...     values(fullname="Sandy Squirrel Extraodinaire")
... )
```

```sql
UPDATE user_account SET fullname=? WHERE user_account.name = ?
[...] ('Sandy Squirrel Extraodinaire', 'sandy')
```

В этом случае используется специальная логика для добавления объекта в сессию.

```python
>>> sandy.fullname
'Sandy Squirrel Extraodinaire'
```

### [Deleting ORM Objects](https://docs.sqlalchemy.org/en/14/tutorial/orm_data_manipulation.html#deleting-orm-objects)

```python
>>> patrick = session.get(User, 3)
>>> session.delete(patrick)
```

До следующего селекта объект будет доступен в сессии. При селекте будет выполнен автофлаш и объект удалится

```python
>>> session.execute(select(User).where(User.name == "patrick")).first()
```

```sql
SELECT address.id AS address_id, address.email_address AS address_email_address,
address.user_id AS address_user_id
FROM address
WHERE ? = address.user_id
[...] (3,)
DELETE FROM user_account WHERE user_account.id = ?
[...] (3,)
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.name = ?
[...] ('patrick',)
```

```python
>>> patrick in session
False
```

Так-же как и с UPDATE мы можем это сделать вручную

```python
>>> # refresh the target object for demonstration purposes
>>> # only, not needed for the DELETE
SQL>>> squidward = session.get(User, 4)

>>> session.execute(delete(User).where(User.name == "squidward"))
```

```sql
DELETE FROM user_account WHERE user_account.name = ?
[...] ('squidward',)
```

### [Rolling Back](https://docs.sqlalchemy.org/en/14/tutorial/orm_data_manipulation.html#rolling-back)

```python
>>> session.rollback()
ROLLBACK

>>> sandy.fullname
'Sandy Cheeks'

>>> sandy.__dict__
{'_sa_instance_state': <sqlalchemy.orm.state.InstanceState object at 0x...>,
 'id': 2, 'name': 'sandy', 'fullname': 'Sandy Cheeks'}

>>> patrick in session
True

>>> session.execute(select(User).where(User.name == 'patrick')).scalar_one() is patrick
True
```

Роллбек отмотал все изменения в сессии, в т.ч. и в терминах БД.

### [Closing session](https://docs.sqlalchemy.org/en/14/tutorial/orm_data_manipulation.html#closing-a-session)

```python
>>> session.close()
ROLLBACK
```

Происходит закрытие всех коннекшенов и транзакций. Это означает, что если делалось только извлечение данных, совсем не обязательно вызывать `rollback()` - роллбек будет вызван автоматически. Все объекты извлекаются из сессии - это означает, что у них нет функционального состояния, связанного с БД, их, к примеру, нельзя закомитить или получить какие-то даныне из БД

```python
>>> squidward.name
Traceback (most recent call last):
  ...
sqlalchemy.orm.exc.DetachedInstanceError: Instance <User at 0x...> is not bound to a Session; attribute refresh operation cannot proceed
```

Чтобы прикрепить объекты к сессии снова, необходимо снова заюзать `add()`

```python
>>> session.add(squidward)
>>> squidward.name
```

```sql
BEGIN (implicit)
SELECT user_account.id AS user_account_id, user_account.name AS user_account_name, user_account.fullname AS user_account_fullname
FROM user_account
WHERE user_account.id = ?
[...] (4,)
'squidward'
```

## [Working with Related Objects](https://docs.sqlalchemy.org/en/14/tutorial/orm_related_objects.html)

Для установки связей между объектами [используется](https://docs.sqlalchemy.org/en/14/orm/relationship_api.html#sqlalchemy.orm.relationship) `relationship()`

```python
from sqlalchemy.orm import relationship
class User(Base):
    __tablename__ = 'user_account'

    # ... Column mappings

    addresses = relationship("Address", back_populates="user")


class Address(Base):
    __tablename__ = 'address'

    # ... Column mappings

    user = relationship("User", back_populates="addresses")
```

### Парсинг и загрузка связей

```python
>>> u1 = User(name='pkrabs', fullname='Pearl Krabs')
>>> u1.addresses
[]

>>> a1 = Address(email_address="pearl.krabs@gmail.com")
>>> u1.addresses.append(a1)

# Появились связанные данные
>>> u1.addresses
[Address(id=None, email_address='pearl.krabs@gmail.com')]

>>> a1.user
User(id=None, name='pkrabs', fullname='Pearl Krabs')
```

Синхронизацию данных обеспечивает `relationship.back_populates` параметр. Мы можем связать в отношении один ко многим и многие к одному.

```python
>>> a2 = Address(email_address="pearl@aol.com", user=u1)
>>> u1.addresses
[Address(id=None, email_address='pearl.krabs@gmail.com'), Address(id=None, email_address='pearl@aol.com')]
```

### Добавление в сессию

Каскадно добавляются все связанные объекты.

```python
>>> session.add(u1)
>>> u1 in session
True
>>> a1 in session
True
>>> a2 in session
True

>>> print(u1.id)
None
>>> print(a1.user_id)
None
```

Так как мы не делали коммит, у нас все еще не присвоены айдишники.

```python
>>> session.commit()
```

```sql
INSERT INTO user_account (name, fullname) VALUES (?, ?)
[...] ('pkrabs', 'Pearl Krabs')
INSERT INTO address (email_address, user_id) VALUES (?, ?)
[...] ('pearl.krabs@gmail.com', 6)
INSERT INTO address (email_address, user_id) VALUES (?, ?)
[...] ('pearl@aol.com', 6)
COMMIT
```

### Загрузка связей

```sql
>>> u1.id

BEGIN (implicit)
SELECT user_account.id AS user_account_id, user_account.name AS user_account_name,
user_account.fullname AS user_account_fullname
FROM user_account
WHERE user_account.id = ?
[...] (6,)
6
```

```sql
>>> u1.addresses
SELECT address.id AS address_id, address.email_address AS address_email_address,
address.user_id AS address_user_id
FROM address
WHERE ? = address.user_id
[...] (6,)
[Address(id=4, email_address='pearl.krabs@gmail.com'), Address(id=5, email_address='pearl@aol.com')]
```

Запросы со связями к БД в ОРМ высокоптимизированы, чтобы не быть затратными. Больше о стратегиях загрузки связанных данных можно [узнать тут](https://docs.sqlalchemy.org/en/14/tutorial/orm_related_objects.html#tutorial-orm-loader-strategies). [[sqlalchemy-loader-strategy]]

## [Использование связанных данных в queries](https://docs.sqlalchemy.org/en/14/tutorial/orm_related_objects.html#using-relationships-in-queries)

[[sqlalchemy-querying]]

- `Select.join()`
- `aliased()`
- `where()`
- `all()`
- `any()`

[Простейшие лоады](https://docs.sqlalchemy.org/en/14/tutorial/orm_related_objects.html#common-relationship-operators) со связанными данными:

```python
# many to one equals comparison
>>> print(select(Address).where(Address.user == u1))
SELECT address.id, address.email_address, address.user_id
FROM address
WHERE :param_1 = address.user_id

# many to one not equals comparison
>>> print(select(Address).where(Address.user != u1))
SELECT address.id, address.email_address, address.user_id
FROM address
WHERE address.user_id != :user_id_1 OR address.user_id IS NULL

# object is contained in a one-to-many collection
>>> print(select(User).where(User.addresses.contains(a1)))
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.id = :param_1

# An object has a particular parent from a one-to-many perspective
>>> from sqlalchemy.orm import with_parent
>>> print(select(Address).where(with_parent(u1, User.addresses)))
SELECT address.id, address.email_address, address.user_id
FROM address
WHERE :param_1 = address.user_id
```

[100500 дополнительных материалов по ОРМ](https://docs.sqlalchemy.org/en/14/tutorial/further_reading.html)
[колонки и типы данных](https://docs.sqlalchemy.org/en/14/core/types.html)
[коннекшен и работа с in-memory](https://docs.sqlalchemy.org/en/14/dialects/sqlite.html#connect-strings)

Утилиты для sqlalchemy: [sqlalchemy_utils](https://sqlalchemy-utils.readthedocs.io/en/latest/index.html). Не пашет с sqlalchemy-1.4. [Сурс](https://stackoverflow.com/a/66651808)

> You have installed SQLAlchemy 1.4.0. SQLAlchemy-utils is currently not compatible with SQLAlchemy > 1.4.0. The solution is to downgrade SQLAlchemy to 1.3.23.

- [[sqlalchemy-querying]]
- [[fatsapi-sql-orm-example]]
- [[sqlite]]
- [[alembic]] - тулза для миграций для sqlalchemy
- [[sqlalchemy]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[sqlite]: sqlite "Sqlite bd"
[sqlalchemy-loader-strategy]: sqlalchemy-loader-strategy "Sqlalchemy loader strategy bd"
[sqlalchemy-querying]: sqlalchemy-querying "Sqlalchgemy querying bd"
[fatsapi-sql-orm-example]: fatsapi-sql-orm-example "Fatsapi sql orm example"
[alembic]: alembic "Alembic"
[sqlalchemy]: ../lists/sqlalchemy "Sqlalchemy"
[//end]: # "Autogenerated link references"