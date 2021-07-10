# sqlalchgemy querying

[основная статья](https://docs.sqlalchemy.org/en/14/orm/tutorial.html#querying)

Создается `query`объект с помощью метода `query()` в сессии. Этот метод получает аргументы, которыми можно манипулировать над классами и дескрипторами.

А примере мы получаем инстансы юзеров, корторе можно итерировать

```Python
>>> for instance in session.query(User).order_by(User.id):
...     print(instance.name, instance.fullname)
ed Ed Jones
wendy Wendy Williams
mary Mary Contrary
fred Fred Flintstone
```

Когда мы запрашиваем несколько объектов, базирусяь на колонках, возвращается кортеж

```Python
>>> for name, fullname in session.query(User.name, User.fullname):
...     print(name, fullname)
ed Ed Jones
wendy Wendy Williams
mary Mary Contrary
fred Fred Flintstone
```

`query` возвращает `named tuples` object, ключи совпадают с именами ОРМ-бейсед объектов

```Python
>>> for row in session.query(User, User.name).all():
...    print(row.User, row.name)
<User(name='ed', fullname='Ed Jones', nickname='eddie')> ed
<User(name='wendy', fullname='Wendy Williams', nickname='windy')> wendy
<User(name='mary', fullname='Mary Contrary', nickname='mary')> mary
<User(name='fred', fullname='Fred Flintstone', nickname='freddy')> fred
```

Ключ можно изменить

```Python
>>> for row in session.query(User.name.label('name_label')).all():
...    print(row.name_label)
ed
wendy
mary
fred
```

Имена классов можно контроллировать через алияс

```Python
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
