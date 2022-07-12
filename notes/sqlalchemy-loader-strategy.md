---
description: Стратегии загрузки в sqlalchemy
tags: sqlalchemy
title: Sqlalchemy loader strategy bd
---
[Ссылка на статью](https://docs.sqlalchemy.org/en/14/tutorial/orm_related_objects.html#tutorial-orm-loader-strategies)

[[sqlalchemy]] ОРИ загружает объекты лениво (laizy load), по мере их востребованности. Этот шаблон проектирования довольно противоречив - когда в памяти несколько десятков объектов, которые ссылаются на несколько других объектов, ленивая загрузка может привести к избыточным запросам к БД. Такие запросы выполняются неявно, могут провоцировать ошибки и, что важно, не работают с [[asyncio]]. При этом ленивая (отложенная) загрузка имеет много преиуществ, если совместима с параллельной обработкой.

Задача применении ОРМ сводится к запуску `SQL echoing` с целью проверки избыточности одних и тех-же селектов и дальнешем применении различных стратегий загрузки.

Стратегия загрузки может быть представлена в виде объекта, ассоциированного с методом `Select.options()`

```python
for user_obj in session.execute(
    select(User).options(selectinload(User.addresses))
).scalars():
    user_obj.addresses  # access addresses collection already loaded
```

Кроме того, стратегия может быть реализована в `relationship()` через опцию `relationship.lazy`

```python
from sqlalchemy.orm import relationship
class User(Base):
    __tablename__ = 'user_account'

    addresses = relationship("Address", back_populates="user", lazy="selectin")
```

## [Selectin load](https://docs.sqlalchemy.org/en/14/tutorial/orm_related_objects.html#selectin-load)

`selectinload()` наиболее используемая опция лоадера в [[sqlalchemy]]. Опция гарантирует, что конкретная коллекция для полной серии объектов загружается заранее с помощью одного запроса. Он делает это с помощью SELECT, который в большинстве случаев может быть отправлен только для связанной таблицы, без введения JOIN или подзапросов, и только для тех родительских объектов, для которых коллекция еще не загружена. Пример:

```python
>>> from sqlalchemy.orm import selectinload
>>> stmt = (
...   select(User).options(selectinload(User.addresses)).order_by(User.id)
... )
>>> for row in session.execute(stmt):
...     print(f"{row.User.name}  ({', '.join(a.email_address for a in row.User.addresses)})")
```

```sql
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account ORDER BY user_account.id
[...] ()
SELECT address.user_id AS address_user_id, address.id AS address_id,
address.email_address AS address_email_address
FROM address
WHERE address.user_id IN (?, ?, ?, ?, ?, ?)
[...] (1, 2, 3, 4, 5, 6)
spongebob  (spongebob@sqlalchemy.org)
sandy  (sandy@sqlalchemy.org, sandy@squirrelpower.org)
patrick  ()
squidward  ()
ehkrabs  ()
pkrabs  (pearl.krabs@gmail.com, pearl@aol.com)
```

## [Joined load](https://docs.sqlalchemy.org/en/14/tutorial/orm_related_objects.html#joined-load)

`joinload()` дополняет инструкцию SELECT, передаваемую в базу данных, с помощью JOIN (который может быть внешним или внутренним соединением в зависимости от параметров), которае затем может загружаться в связанные объекты. лучше всего подходит для загрузки связанных объектов типа "многие к одному", поскольку для этого требуется только добавить дополнительные столбцы в строку первичной сущности, которая будет извлечена в любом случае. Для большей эффективности может принимать еще и `joinedload.innerjoin`. Пример

```python
>>> from sqlalchemy.orm import joinedload
>>> stmt = (
...   select(Address).options(joinedload(Address.user, innerjoin=True)).order_by(Address.id)
... )
>>> for row in session.execute(stmt):
...     print(f"{row.Address.email_address} {row.Address.user.name}")
```

```sql
SELECT address.id, address.email_address, address.user_id, user_account_1.id AS id_1,
user_account_1.name, user_account_1.fullname
FROM address
JOIN user_account AS user_account_1 ON user_account_1.id = address.user_id
ORDER BY address.id
[...] ()
spongebob@sqlalchemy.org spongebob
sandy@sqlalchemy.org sandy
sandy@squirrelpower.org sandy
pearl.krabs@gmail.com pkrabs
pearl@aol.com pkrabs
```

Может так-же использоваться для коллекций один ко многим, но имеет эффект рекурсивного умножения первичных строк на связный элемент, что может быть затратно.

## [Explicit Join + Eager load](https://docs.sqlalchemy.org/en/14/tutorial/orm_related_objects.html#explicit-join-eager-load)

## [Augmenting Loader Strategy Paths](https://docs.sqlalchemy.org/en/14/tutorial/orm_related_objects.html#augmenting-loader-strategy-paths)

## [Raiseload](https://docs.sqlalchemy.org/en/14/tutorial/orm_related_objects.html#raiseload)

Позволяет в приципе блокировать "отложенную загрузку". Пример:

```python
class User(Base):
    __tablename__ = 'user_account'

    # ... Column mappings

    addresses = relationship("Address", back_populates="user", lazy="raise_on_sql")


class Address(Base):
    __tablename__ = 'address'

    # ... Column mappings

    user = relationship("User", back_populates="addresses", lazy="raise_on_sql")
```

[//begin]: # "Autogenerated link references for markdown compatibility"
[sqlalchemy]: ../lists/sqlalchemy "Sqlalchemy"
[asyncio]: asyncio "Asyncio"
[sqlalchemy]: ../lists/sqlalchemy "Sqlalchemy"
[//end]: # "Autogenerated link references"