---
description: Запросы в sqlalchemy
tags: sqlalchemy python bd
title: Sqlalchgemy querying bd
---
- [основная статья](https://docs.sqlalchemy.org/en/14/orm/tutorial.html#querying)
- [query API](https://docs.sqlalchemy.org/en/14/orm/query.html)

Создается `query`объект с помощью метода `query()` в сессии. Этот метод получает аргументы, которыми можно манипулировать над классами и дескрипторами.

А примере мы получаем инстансы юзеров, корторе можно итерировать

```python
>>> for instance in session.query(User).order_by(User.id):
...     print(instance.name, instance.fullname)
ed Ed Jones
wendy Wendy Williams
mary Mary Contrary
fred Fred Flintstone
```

Когда мы запрашиваем несколько объектов, базирусяь на колонках, возвращается кортеж

```python
>>> for name, fullname in session.query(User.name, User.fullname):
...     print(name, fullname)
ed Ed Jones
wendy Wendy Williams
mary Mary Contrary
fred Fred Flintstone
```

`query` возвращает `named tuples` object, ключи совпадают с именами ОРМ-бейсед объектов

```python
>>> for row in session.query(User, User.name).all():
...    print(row.User, row.name)
<User(name='ed', fullname='Ed Jones', nickname='eddie')> ed
<User(name='wendy', fullname='Wendy Williams', nickname='windy')> wendy
<User(name='mary', fullname='Mary Contrary', nickname='mary')> mary
<User(name='fred', fullname='Fred Flintstone', nickname='freddy')> fred
```

Ключ можно изменить

```python
>>> for row in session.query(User.name.label('name_label')).all():
...    print(row.name_label)
ed
wendy
mary
fred
```

Имена классов можно контроллировать через алияс

```python
>>> from sqlalchemy.orm import aliased
>>> user_alias = aliased(User, name='user_alias')

SQL>>> for row in session.query(user_alias, user_alias.name).all():
...    print(row.user_alias)
<User(name='ed', fullname='Ed Jones', nickname='eddie')>
<User(name='wendy', fullname='Wendy Williams', nickname='windy')>
<User(name='mary', fullname='Mary Contrary', nickname='mary')>
<User(name='fred', fullname='Fred Flintstone', nickname='freddy')>
```

Можно задавать порядок выдачи

```python
>>> for u in session.query(User).order_by(User.id)[1:3]:
...    print(u)
<User(name='wendy', fullname='Wendy Williams', nickname='windy')>
<User(name='mary', fullname='Mary Contrary', nickname='mary')>
```

или фильтрацию

```python
>>> for name, in session.query(User.name).\
...             filter_by(fullname='Ed Jones'):
...    print(name)
ed
```

или так

```python
>>> for name, in session.query(User.name).\
...             filter(User.fullname=='Ed Jones'):
...    print(name)
ed
```

можно выстраивать цепочки

```python
>>> for user in session.query(User).\
...          filter(User.name=='ed').\
...          filter(User.fullname=='Ed Jones'):
...    print(user)
<User(name='ed', fullname='Ed Jones', nickname='eddie')>
```

[Все базовые операции фильтрации тут](https://docs.sqlalchemy.org/en/14/orm/tutorial.html#common-filter-operators)

`query.all()` возвращает список. `Query.first()` возвращает скаляр. Есть еще  `Query.one()` Смотреть [тут](https://docs.sqlalchemy.org/en/14/orm/tutorial.html#returning-lists-and-scalars)

Кроме того, sql-запросы [можно использовать в виде текста](https://docs.sqlalchemy.org/en/14/orm/tutorial.html#using-textual-sql)

## Querying guide

[основная статья тут](https://docs.sqlalchemy.org/en/14/orm/queryguide.html)

## SELECT statements

Задаем `select()` объект, отправляем его в сессию и получаем результат

```python
>>> from sqlalchemy import select
>>> stmt = select(User).where(User.name == 'spongebob')

>>> result = session.execute(stmt)
>>> for user_obj in result.scalars():
...     print(f"{user_obj.name} {user_obj.fullname}")
spongebob Spongebob Squarepants
```

`select()` поддерживает ОРМ  модели, включая маппированные классы, такие как атрибуты уровня класса, реализующие колонки таблицы. Работа с такой аннотацией так-же осуществляется в сесссии.

```python
>>> result = session.execute(select(User).order_by(User.id))
```

При оспользовании ОРМ-мода, названия сущностей базируются на поименовании классов

```python
>>> stmt = select(User, Address).join(User.addresses).order_by(User.id, Address.id)

SQL>>> for row in session.execute(stmt):
...    print(f"{row.User.name} {row.Address.email_address}")
spongebob spongebob@sqlalchemy.org
sandy sandy@sqlalchemy.org
sandy squirrel@squirrelpower.org
patrick pat999@aol.com
squidward stentcl@sqlalchemy.org
```

Атрибуты классов можно использовать и так:

```python
>>> result = session.execute(
...     select(User.name, Address.email_address).
...     join(User.addresses).
...     order_by(User.id, Address.id)
... )

>>> for row in result:
...     print(f"{row.name}  {row.email_address}")
spongebob  spongebob@sqlalchemy.org
sandy  sandy@sqlalchemy.org
sandy  squirrel@squirrelpower.org
patrick  pat999@aol.com
squidward  stentcl@sqlalchemy.org
```

В данном случае под капотом другая реализация, итог тот же. [Подробнее](https://docs.sqlalchemy.org/en/14/orm/queryguide.html#selecting-orm-entities-and-attributes)

Тоже самое можно собрать через банедлы, но есть потенциальный риск наткнуться на тяжелый запрос. Доп.инфа по [column bundles](https://docs.sqlalchemy.org/en/14/orm/loading_columns.html#bundles)

```python
>>> from sqlalchemy.orm import Bundle
>>> stmt = select(
...     Bundle("user", User.name, User.fullname),
...     Bundle("email", Address.email_address)
... ).join_from(User, Address)
SQL>>> for row in session.execute(stmt):
...     print(f"{row.user.name} {row.email.email_address}")
spongebob spongebob@sqlalchemy.org
sandy sandy@sqlalchemy.org
sandy squirrel@squirrelpower.org
patrick pat999@aol.com
squidward stentcl@sqlalchemy.org
```

Можно использовать [алиасы](https://docs.sqlalchemy.org/en/14/orm/queryguide.html#selecting-orm-aliases)

```python
>>> from sqlalchemy.orm import aliased
>>> u1 = aliased(User, name="u1")
>>> stmt = select(u1).order_by(u1.id)
SQL>>> row = session.execute(stmt).first()
>>> print(f"{row.u1.name}")
spongebob
```

Кроме того, как и везде в [[sqlalchemy]] поддерживаются нативные запросы (текст или базовые стейтементы). [Смотреть тут](https://docs.sqlalchemy.org/en/14/orm/queryguide.html#getting-orm-results-from-textual-and-core-statements)

## [Joins](https://docs.sqlalchemy.org/en/14/orm/queryguide.html#joins)

`Select.join()` и `Select.join_from()` предпочтительнее в ОРМ 2.0, чем `Query.join()`, который является легаси. Далее простой пример джойна. В данном случае реализована связь между двумя классами User и Adress, ult User.adresses представляет коллекцию адресов, ассоциированных с юзером.

```python
>>> stmt = select(User).join(User.addresses)
>>> print(stmt)
```

```sql
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account JOIN address ON user_account.id = address.user_id
```

Множественные джойны можно выстракивать в цепь

```python
>>> stmt = (
...     select(User).
...     join(User.orders).
...     join(Order.items)
... )
>>> print(stmt)
```

```sql
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
JOIN user_order ON user_account.id = user_order.user_id
JOIN order_items AS order_items_1 ON user_order.id = order_items_1.order_id
JOIN item ON item.id = order_items_1.item_id
```

Второй вариант - джойны на основе самого класса. Такой подход потенциально опасен ошибками, которые будут подниматься, если не установлен ForeignKeyConstraint или их несколько. [Подробнее](https://docs.sqlalchemy.org/en/14/orm/queryguide.html#joins-to-a-target-entity-or-selectable)

```python
>>> stmt = select(User).join(Address)
>>> print(stmt)
```

```sql
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account JOIN address ON user_account.id = address.user_id
```

Третий вариант - [реализовать](https://docs.sqlalchemy.org/en/14/orm/queryguide.html#joins-to-a-target-with-an-on-clause) фразу `ON`

```python
>>> stmt = select(User).join(Address, User.id==Address.user_id)
>>> print(stmt)
```

```sql
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account JOIN address ON user_account.id = address.user_id
```

Можно так:

```python
>>> stmt = select(User).join(Address, User.addresses)
>>> print(stmt)
```

Такой синтаксис становится более полезным с алиасами

```python
>>> a1 = aliased(Address)
>>> a2 = aliased(Address)
>>> stmt = (
...     select(User).
...     join(a1, User.addresses).
...     join(a2, User.addresses).
...     where(a1.email_address == 'ed@foo.com').
...     where(a2.email_address == 'ed@bar.com')
... )
>>> print(stmt)
```

```sql
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
JOIN address AS address_1 ON user_account.id = address_1.user_id
JOIN address AS address_2 ON user_account.id = address_2.user_id
WHERE address_1.email_address = :email_address_1
AND address_2.email_address = :email_address_2
```

Можно тоже самое через `of_type()` метод

```python
>>> stmt = (
...     select(User).
...     join(User.addresses.of_type(a1)).
...     join(User.addresses.of_type(a2)).
...     where(a1.email_address == 'ed@foo.com').
...     where(a2.email_address == 'ed@bar.com')
... )
>>> print(stmt)
```

Цепи можно [реализовать на лету](https://docs.sqlalchemy.org/en/14/orm/queryguide.html#augmenting-built-in-on-clauses) через метод `and_()`

```python
>>> stmt = (
...     select(User).
...     join(User.addresses.and_(Address.email_address != 'foo@bar.com'))
... )
>>> print(stmt)
```

```sql
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
JOIN address ON user_account.id = address.user_id
AND address.email_address != :email_address_1
```

Можно джониться к сабзапросам. [Подробнее тут](https://docs.sqlalchemy.org/en/14/orm/queryguide.html#joining-to-subqueries)

Смотри также [ORM execution options](https://docs.sqlalchemy.org/en/14/orm/queryguide.html#orm-execution-options)

## Примеры SQL-запросов

### Get a list of values of one column from the results of a query

```python
emails = [r.email for r in db.session.query(my_table.c.email).filter_by(name=name).distinct()]
```

[источник](https://stackoverflow.com/questions/31842159/get-a-list-of-values-of-one-column-from-the-results-of-a-query)

### Raw queryng with parameters

```python
db.my_session.execute(
    "UPDATE client SET musicVol = :mv, messageVol = :ml",
    {'mv': music_volume, 'ml': message_volume}
)
```

[источник](https://stackoverflow.com/a/32333755/15966204)

Что еще почитать?

- [[sqlalchemy]]
- [[sqlalchemy-deleting]]
- [query API](https://docs.sqlalchemy.org/en/14/orm/query.html)

[//begin]: # "Autogenerated link references for markdown compatibility"
[sqlalchemy]: ..%2Flists%2Fsqlalchemy "Sqlalchemy"
[sqlalchemy-deleting]: sqlalchemy-deleting "Sqlalchemy deleting bd"
[//end]: # "Autogenerated link references"